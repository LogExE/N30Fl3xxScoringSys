import flet as ft
import flet_material as fm
import json
import os
import asyncio
import aiohttp
import requests


DEFAULT_FLET_PATH = ''
DEFAULT_FLET_PORT = 50422

FORM_WIDTH = 800
MAIN_COLOR = ft.colors.DEEP_PURPLE_500


class InputFields(ft.UserControl):
    def __init__(self, title: str):
        self.input: ft.Control = ft.TextField(
            label=title
        )
        self.input_box: ft.Container = ft.Container(
            expand=True,
            content=self.input,
            animate=ft.Animation(300, "ease")

        )
        self.status: ft.Control = fm.CheckBox(
            shape="circle",
            value=False,
            disabled=True,
            offset=ft.Offset(1, 0),
            right=0,
            bottom=0,
            top=1,
            animate_opacity=ft.Animation(200, "linear"),
            animate_offset=ft.Animation(300, "ease"),
            opacity=0
        )
        self.object = self.create_input(title)
        super().__init__()

    # async def set_ok(self):
    #     self.status.offset = ft.Offset(-0.5, 0)
    #     self.status.opacity = 1
    #     self.update()
    #
    #     await asyncio.sleep(1)
    #
    #     self.status.content.value = True
    #     self.status.animate_checkbox(e=None)
    #     self.status.update()


    def create_input(self, title):
        return ft.Column(
            spacing=5,
            controls=[
                ft.Stack(
                    controls=[
                        self.input_box,
                        self.status
                    ]
                )
            ]
        )

    def build(self):
        return self.object

class MainFormUI(ft.UserControl):
    def __init__(self):
        self.email = InputFields("Email")
        self.education = InputFields("Education")
        self.submit = ft.FilledButton(
            width=FORM_WIDTH,
            height=45,
            text="Submit",
            # on_click=lambda e: asyncio.run(self.validation(e))
            on_click=lambda e: asyncio.run(self.submit_clicked(e))
        )
        super().__init__()

    # async def validation(self, e):
    #     email_val = self.email.input.value
    #     education_val = self.education.input.value
    #     # data = {
    #     #     'email': self.email.input.value,
    #     #     'education': self.education.input.value
    #     # }
    #     # await return json.dumps(data)
    #     # print(json.dumps(data))
    #
    #     if len(email_val) > 3:
    #         await asyncio.sleep(0.5)
    #         await self.email.set_ok()
    #     if len(education_val) > 3:
    #         await asyncio.sleep(0.5)
    #         await self.education.set_ok()
    #     self.update()

    async def submit_clicked(self, e):
        url = 'http://127.0.0.1:8000'
        data_json = {
            'email': self.email.input.value,
            'education': self.education.input.value
        }
        # backend
        # print(json.dumps(data_json))
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data_json) as response:
                data = await response.text()
                print(data)
        # res = await requests.post(, data=data)

    def build(self):
        return ft.Container(
            width=FORM_WIDTH, height=600,
            bgcolor=ft.colors.with_opacity(0.01, ft.colors.WHITE),
            border_radius=10,
            padding=40,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        "Оценка кредитоспособности",
                        size=25,
                        weight=ft.FontWeight.W_700,
                        color=MAIN_COLOR
                    ),
                    ft.Text(
                        "Заполните форму, чтобу узнать свой кредитный рейтинг.",
                        size=18,
                        opacity=0.4
                    ),
                    ft.Divider(height=25, color="transparent"),
                    self.email,
                    self.education,
                    self.submit
                ]
            )
        )


def main(page: ft.Page):
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=MAIN_COLOR,
            primary_container=ft.colors.PINK_200
        )
    )
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def swap_dark_mode_clicked(e):
        """ Переключение между светлой и темной темой """
        if e.control.selected:
            page.theme_mode = ft.ThemeMode.LIGHT
        else:
            page.theme_mode = ft.ThemeMode.DARK
        e.control.selected = not e.control.selected
        e.control.update()
        page.update()

    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.CREDIT_SCORE),
        title=ft.Text("Neo-Scoring System"),
        bgcolor=ft.colors.SURFACE_VARIANT,
        color=MAIN_COLOR,
        actions=[
            ft.IconButton(
                icon=ft.icons.DARK_MODE_OUTLINED,
                selected_icon=ft.icons.DARK_MODE,
                on_click=swap_dark_mode_clicked,
                selected=False,
            ),
        ],
    )

    form = MainFormUI()
    page.add(form)
    page.update()


if __name__ == '__main__':
    flet_path = os.getenv("FLET_PATH", DEFAULT_FLET_PATH)
    flet_port = int(os.getenv("FLET_PORT", DEFAULT_FLET_PORT))
    ft.app(name=flet_path, target=main, view=ft.WEB_BROWSER, port=flet_port)
