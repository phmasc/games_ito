import flet as ft

def card_number(number: int = -1, tip_start: str = '', tip_end: str = ''):
    if number < 0:
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "PH\nito",
                            size=100,
                            text_align=ft.TextAlign.CENTER,
                            color=ft.Colors.WHITE70,
                        ),
                    ],
                ),
                alignment=ft.alignment.center,
                width=200,
                height=300,
                padding=10,
            ),
            color=ft.Colors.BLACK38,
        )

    # Controle do estado do card
    card_ref = ft.Ref[ft.Card]()  # Referência para o Card
    text_number_ref = ft.Ref[ft.Text]()  # Referência para o texto do número
    text_number = str("0" + str(number))[-2:]

    def toggle_card(e):
        if text_number_ref.current.value == str(text_number):
            text_number_ref.current.value = "PH"
            card_ref.current.color = ft.Colors.BLACK
        else:
            text_number_ref.current.value = str(text_number)
            card_ref.current.color = ft.Colors.AMBER
        # Atualiza o card para refletir as mudanças
        card_ref.current.update()

    card = ft.Card(
        ref=card_ref,
        content=ft.Container(
            on_click=toggle_card,
            content=ft.Column(
                [
                    ft.Text(
                        tip_start,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.WHITE70
                    ),
                    ft.Text(
                        text_number,
                        ref=text_number_ref,
                        size=140,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.WHITE70,
                    ),
                    ft.Text(
                        tip_end,
                        text_align=ft.TextAlign.END,
                        color=ft.Colors.WHITE70
                    ),
                ],
            ),
            alignment=ft.alignment.center,
            width=200,
            height=300,
            padding=10,
        ),
        color=ft.Colors.AMBER,
    )

    return card
