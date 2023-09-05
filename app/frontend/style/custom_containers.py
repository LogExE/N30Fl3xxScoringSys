""" Оформление контейнеров для полей """

import flet as ft
ONE_FIELD_WIDTH = 170


def custom_column(controls):
    """ Стилизованная колонка """
    return ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=0,
        controls=controls
    )


def custom_container(controls):
    """ Стилизованные контейнер """
    return ft.Container(
        bgcolor=ft.colors.with_opacity(0.2, ft.colors.OUTLINE_VARIANT),
        padding=25,
        border_radius=30,
        content=custom_column(controls)
    )
