from django.db import models

from theme.models import Theme


class RoomConfig(models.Model):
    name = models.TextField(max_length=25, unique=True)
    max_players = models.PositiveIntegerField()

    class Meta:
        db_table = 'room_config'

    def __str__(self):
        return f'{self.name}:{self.max_players}'


class Player(models.Model):
    name = models.TextField(max_length=30, unique=True)
    victory = models.PositiveIntegerField(default=0)
    defeaut = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'players'

    def __str__(self):
        return f'{self.name} := {self.victory}:{self.defeaut}'


class Room(models.Model):
    room_config = models.ForeignKey(RoomConfig, on_delete=models.CASCADE, related_name='rooms')
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name='rooms', null=True, blank=True)
    players = models.ManyToManyField(Player, through='RoomPlayer', related_name='rooms')
    is_active = models.BooleanField(default=False)
    game_start_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'rooms'

    def clean(self):
        if Room.objects.filter(room_config=self.room_config, is_active=True).exclude(id=self.id).exists():
            raise ValidationError(f"Já existe uma sala ativa para a configuração {self.room_config.name}.")

    def __str__(self):
        return f"Sala de {self.room_config.name} - {'Ativa' if self.is_active else 'Inativa'}"


class RoomPlayer(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_players')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='room_players')
    card = models.IntegerField(null=True, blank=True)
    score = models.IntegerField(default=0)
    ready = models.BooleanField(default=False)
    final = models.BooleanField(default=False)

    class Meta:
        db_table = 'room_players'

        constraints = [
            models.UniqueConstraint(fields=['room', 'player'], name='unique_room_player')
        ]

    def clean(self):
        """
        Valida o limite de jogadores com base na configuração da sala.
        """
        if self.room.room_config.max_players and \
           self.room.room_players.count() >= self.room.room_config.max_players:
            raise ValidationError("O limite de jogadores para esta sala já foi atingido.")

    def __str__(self):
        return f"Player {self.player.name} na Sala {self.room.room_config.name} com Card {self.card}"
