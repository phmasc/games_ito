import flet as ft
from ito.home import ito_page
from ito.game import ito_game_page


def main(page: ft.Page):
    page.title = "Games PHMasc"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.fonts = {
        "RobotoSlab": "https://github.com/google/fonts/raw/main/apache/robotoslab/RobotoSlab%5Bwght%5D.ttf"
    }
    page.theme_mode = ft.ThemeMode.LIGHT

    def route_change(route):
        page.views.clear()  # Remove views anteriores para evitar sobreposição

        match page.route:
            case "/ito":
                ito_page(page)

            case route if route.startswith("/"):
                parts = page.route.strip('/').split('/')
                if len(parts) == 3 and parts[-1] == 'game':
                    if parts[0] == 'ito':
                        room = parts[1]
                        ito_game_page(page, room)
                else:
                    show_home(page)

            case _:
                show_home(page)

        page.update()



    def show_home(page):
        page.views.append(
            ft.View(
                "/",
                controls=[
                    ft.ResponsiveRow(
                        controls=[
                            ft.Text(
                                "Selecione seu jogo!",
                                size=30,
                                weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Container(
                                content=ft.ElevatedButton(
                                    text="ITO",
                                    on_click=lambda _: page.go("/ito"),
                                ),
                                alignment=ft.alignment.center,
                                padding=10,
                            ),
                        ],
                    ),
                ]
            )
        )
    # Configure os eventos de navegação
    page.on_route_change = route_change
    page.go(page.route)


# Iniciar o aplicativo
if __name__ == "__main__":
    ft.app(target=main)
