from random import choice, sample
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils.timezone import now

from .models import Room, Player, RoomPlayer
from .serializers import RoomPlayerSerializer
from theme.models import Theme


class RoomSetupView(APIView):
    def get(self, request, room_name):
        # Busca a sala pelo nome
        room = get_object_or_404(Room, room_config__name=room_name)

        # Obtém os jogadores na sala
        room_players = RoomPlayer.objects.filter(room=room)
        serializer = RoomPlayerSerializer(room_players, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, room_name):
        # Dados do jogador recebido no corpo da requisição
        player_name = request.data.get('player_name')

        if not player_name:
            return Response({"detail": "Player name is required."}, 
                            status=status.HTTP_400_BAD_REQUEST)

        # Busca a sala pelo nome
        room = get_object_or_404(Room, room_config__name=room_name)

        # Verifica se há espaço na sala
        if room.room_players.count() >= room.room_config.max_players:
            return Response({"detail": "A sala está cheia."}, 
                            status=status.HTTP_400_BAD_REQUEST)

        # Verifica se o jogador já existe, senão cria
        player, created = Player.objects.get_or_create(name=player_name)

        # Adiciona o jogador na sala
        RoomPlayer.objects.create(room=room, player=player, card=card_number)
        
        if not room.theme:
            available_themes = Theme.objects.all()
            if available_themes.exists():
                room.theme = choice(available_themes)
                room.save()

        # Obtém os jogadores atualizados na sala
        room_players = RoomPlayer.objects.filter(room=room)
        serializer = RoomPlayerSerializer(room_players, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RoomStartView(APIView):
    def post(self, request, room_name):
        # Busca a sala
        room = get_object_or_404(Room, room_config__name=room_name)

        # Obtém os jogadores na sala
        room_players = RoomPlayer.objects.filter(room=room)

        # Atualiza o status de "ready" do jogador que fez o POST
        player_name = request.data.get('player_name')
        if not player_name:
            return Response({"detail": "Player name is required."}, 
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            room_player = room_players.get(player__name=player_name)
            room_player.ready = True
            room_player.save()
        except RoomPlayer.DoesNotExist:
            return Response({"detail": "Player not found in the room."}, 
                            status=status.HTTP_404_NOT_FOUND)

        # Verifica se todos os jogadores estão prontos
        all_ready = all([rp.ready for rp in room_players])

        if not all_ready:
            # Retorna a lista de jogadores e seus estados "ready"
            response_data = {
                rp.player.name: rp.ready for rp in room_players
            }
            return Response(response_data, status=100)
        
        room.game_start_time = now()
        room.save()

        # Gera cartas para todos os jogadores
        cards = sample(range(101), len(room_players))  # Baralho de 0 a 100, sem repetição
        for room_player, card in zip(room_players, cards):
            room_player.card = card
            room_player.save()

        # Retorna os jogadores e suas cartas
        response_data = {
            rp.player.name: rp.card for rp in room_players
        }
        return Response(response_data, status=status.HTTP_200_OK)


class GameOverView(APIView):
    def post(self, request, room_name, player_name):
        # Busca a sala e o jogador
        room = get_object_or_404(Room, room_config__name=room_name)
        room_player = get_object_or_404(RoomPlayer, room=room, player__name=player_name)

        # Atualiza o estado para "final"
        room_player.final = True

        # Verifica se o jogador desistiu (POST vazio)
        player_order = request.data.get('player_order', [])
        if not player_order:
            room_player.score = 0
        else:
            # Ordena os jogadores na sala por suas cartas (decrescente)
            sorted_players = sorted(
                RoomPlayer.objects.filter(room=room), 
                key=lambda rp: rp.card
            )
            correct_order = [rp.player.name for rp in sorted_players]

            # Compara a ordem enviada com a correta
            room_player.score = sum(1 for a, b in zip(player_order, correct_order) if a == b)

        room_player.save()
        return Response({"score": room_player.score}, status=status.HTTP_200_OK)


class ResultView(APIView):
    def post(self, request, room_name):
        from datetime import timedelta

        # Busca a sala
        room = get_object_or_404(Room, room_config__name=room_name)
        room_players = RoomPlayer.objects.filter(room=room)

        # Condições de finalização com base no tempo e no estado "final"
        player_count = room_players.count()
        half_players_done = sum(1 for rp in room_players if rp.final) >= player_count / 2

        time_elapsed = now() - room.game_start_time
        time_condition = (
            (player_count > 7 and time_elapsed >= timedelta(minutes=10)) or
            (player_count <= 7 and time_elapsed >= timedelta(minutes=5))
        )
        all_done = all(rp.final for rp in room_players)

        if not (all_done or (time_condition and half_players_done)):
            return Response({"detail": "O jogo ainda não pode ser finalizado."}, 
                            status=status.HTTP_400_BAD_REQUEST)

        # Determina o(s) vencedor(es) com base no maior score
        max_score = max(rp.score for rp in room_players)
        winners = [rp for rp in room_players if rp.score == max_score]

        # Atualiza o número de vitórias/derrotas
        for rp in room_players:
            if rp in winners:
                rp.player.victory += 1
            else:
                rp.player.defeaut += 1
            rp.player.save()

        # Retorna os resultados finais
        results = {
            rp.player.name: {
                "score": rp.score,
                "victory": rp.player.victory,
                "defeat": rp.player.defeaut
            } for rp in room_players
        }
        return Response(results, status=status.HTTP_200_OK)

