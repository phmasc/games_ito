import flet as ft


def ito_game_page(page, room):
    page.views.append(
        ft.View(
            f"/ito/{room}/game",
            controls=[
                ft.Text(
                    f"Bem-vindo à sala {room}!",
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.ElevatedButton(
                    text="Sair",
                    on_click=lambda _: page.go("/"),
                ),
            ],
        )
    )