import flet as ft


def main(page: ft.Page):
    page.title = "Hello, Flet!"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Adicionando conteúdo à página
    page.add(
        ft.Text("Welcome to Flet!", size=30, weight=ft.FontWeight.BOLD),
        ft.ElevatedButton(
            text="Click me!",
            on_click=lambda _: page.add(ft.Text("Button clicked!"))
        ),
    )


# Iniciar o aplicativo
if __name__ == "__main__":
    ft.app(target=main)
