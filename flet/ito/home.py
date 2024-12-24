import flet as ft
import asyncio
from services.api import ItoAPI


def ito_page(page: ft.Page):
    page.views.clear()  # Limpa a visualização anterior
    api = ItoAPI()

    # Botão para voltar à página inicial
    btn_home = ft.ElevatedButton(text="Home", on_click=lambda _: page.go("/"))

    # Campos de entrada para nome e sala
    name_input = ft.TextField(label='Informe seu nome:')
    room_input = ft.TextField(label='Insira uma sala para começar:')

    # Componente para mostrar mensagens de erro ou sucesso
    error_message = ft.Text("", size=20, weight=ft.FontWeight.BOLD)
    pb = ft.ProgressBar(width=400, color="amber", bgcolor="#eeeeee", visible=False)

    async def start_game(name, room):
        try:
            # Exibe o ProgressBar
            pb.visible = True
            error_message.value = "Iniciando o jogo..."
            page.update()

            # Simula a chamada à API (troque pelo código real)
            response = await api.start_game(room, name)  # Substitua pela chamada real

            # Navega para a nova rota se a resposta for válida
            if response.get("success", False):
                pb.visible = False
                error_message.value = "Jogo iniciado com sucesso!"
                page.update()
                await asyncio.sleep(1)  # Pequeno delay antes da navegação
                page.go(f"/ito/{room}/game")
            else:
                pb.visible = False
                message = response.get('message, "Erro ao iniciar o jogo')
                room_input.error_text = message
                page.update()
        except Exception as e:
            pb.visible = False
            print(e)
            error_message.value = f"Erro: {str(e)}"
            error_message.bgcolor = "#FF0000"
            error_message.color = "#FFFFFF"
            page.update()

    # Função chamada ao clicar no botão "Iniciar"
    def on_start_game_click(e):
        if not name_input.value:
            name_input.error_text = "Insira um nome"
        if not room_input.value:
            room_input.error_text = "Insira uma sala"

        name = name_input.value
        room = room_input.value
        if name and room:
            asyncio.run(start_game(name, room))
        page.update()

    page.views.append(
        ft.View(
            "/ito",  # Identificador da view
            controls=[
                btn_home,  # Botão Home
                ft.ResponsiveRow(
                    controls=[
                        ft.Text("Bem-vindo ao ITO!", size=25, weight=ft.FontWeight.W_600),
                        name_input,   # Campo para o nome
                        room_input,   # Campo para a sala
                    ]
                ),
                ft.ElevatedButton(text="Iniciar", on_click=on_start_game_click),  # Botão para iniciar o jogo
                error_message,  # Exibe a mensagem de erro ou sucesso
                pb
            ],
        )
    )
