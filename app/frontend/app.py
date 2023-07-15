import flet as ft
import json
import os
import asyncio
import aiohttp
import time
from datetime import datetime

from data import *
from style.input_fields import InputFields
from style.custom_input import CustomContainer, CustomDropdown

DEFAULT_FLET_PATH = ''
DEFAULT_FLET_PORT = 50422

DEFAULT_BACKEND_HOST = '127.0.0.1'
DEFAULT_BACKEND_PORT = '8000'

MAIN_WIDTH = 800
MAIN_COLOR = ft.colors.DEEP_PURPLE_500


class MainFormUI(ft.UserControl):
    """ Главная форма """

    def __init__(self):
        self.surname = InputFields("Фамилия", 1)
        self.name = InputFields("Имя", 1)
        self.patronymic = InputFields("Отчество", 1)

        # TODO: добавить преобразование
        self.gender = ft.RadioGroup(ft.Row([
            ft.Radio(value="0", label="Мужской"),
            ft.Radio(value="1", label="Женский")],
        ))

        self.birth_date = InputFields("", 1, 10, "ДД.ММ.ГГГГ")
        self.passport_series = InputFields("Серия", 1, 4)
        self.passport_number = InputFields("Номер", 2, 6)

        self.family = CustomDropdown(NAME_FAMILY_STATUS_rus, 2)
        self.children = InputFields("Количество детей", 1)
        self.house = CustomDropdown(NAME_HOUSING_TYPE_rus, 2)
        self.car = ft.Checkbox(label="Есть машина", offset=(0, -0.1))
        self.education = CustomDropdown(NAME_EDUCATION_TYPE_rus, 3)

        self.occupation = CustomDropdown(OCCUPATION_TYPE_rus, 3)
        self.organization = CustomDropdown(ORGANIZATION_TYPE_rus, 3)
        self.days_employed = InputFields("", 3, 10, "ДД.ММ.ГГГГ")
        self.income_type = CustomDropdown(NAME_INCOME_TYPE_rus, 1.5)
        self.income_total = InputFields("Среднегодовой доход", 1.42, suffix_text="\u20BD")

        self.credit = InputFields("Сумма кредита", 1.92, suffix_text="\u20BD")
        self.months = InputFields("Кредитный период", 1.92, suffix_text="месяцев")

        self.submit = ft.FilledButton(
            width=MAIN_WIDTH,
            height=45,
            text="Узнать кредитный рейтинг",
            # on_click=lambda e: asyncio.run(self.validation(e))
            on_click=lambda e: asyncio.run(self.submit_clicked(e))
        )
        self.progress = ft.ProgressRing(visible=False)
        self.score = ft.Text(
            size=21,
            weight=ft.FontWeight.W_700,
            color=MAIN_COLOR
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

    def mapping(self, val, dct):
        return None if val is None else dct[val]

    async def submit_clicked(self, e):
        self.submit.visible = False
        self.progress.visible = True
        self.score.value = None
        self.update()

        """ Отправка данных из формы на сервер (в формате JSON) """
        host = os.getenv("BACKEND_HOST", DEFAULT_BACKEND_HOST)
        port = os.getenv("BACKEND_PORT", DEFAULT_BACKEND_PORT)
        url = f'http://{host}:{port}'

        # TODO: пока все параметры имеют строковый тип данных - исправить после создания модели данных на Pydentic
        data_json = {
            'SURNAME': self.surname.input.value,
            'NAME': self.name.input.value,
            'PATRONYMIC': self.patronymic.input.value,
            'CODE_GENDER': self.gender.value,
            # TODO: перенести вычисления на бэк, чтобы они происходили после валидации
            # 'DAYS_BIRTH': self.birth_date.input.value,
            'DAYS_BIRTH': str((datetime.now() - datetime.strptime(self.birth_date.input.value, "%d.%m.%Y")).days),
            'PASSPORT': self.passport_series.input.value + self.passport_number.input.value,

            'NAME_FAMILY_STATUS': self.mapping(self.family.value, NAME_FAMILY_STATUS_dict),
            'CNT_CHILDREN': self.children.input.value,
            'NAME_HOUSING_TYPE': self.mapping(self.house.value, NAME_HOUSING_TYPE_dict),
            'FLAG_OWN_CAR': str(int(self.car.value)),
            'NAME_EDUCATION_TYPE': self.mapping(self.education.value, NAME_EDUCATION_TYPE_dict),

            'OCCUPATION_TYPE': self.mapping(self.occupation.value, OCCUPATION_TYPE_dict),
            'ORGANIZATION_TYPE': self.mapping(self.organization.value, ORGANIZATION_TYPE_dict),
            # TODO: перенести вычисления на бэк, чтобы они происходили после валидации
            # 'DAYS_EMPLOYED': self.days_employed.input.value,
            'DAYS_EMPLOYED': str((datetime.now() - datetime.strptime(self.days_employed.input.value, "%d.%m.%Y")).days),
            'NAME_INCOME_TYPE': self.mapping(self.income_type.value, NAME_INCOME_TYPE_dict),
            # TODO: перенести вычисления на бэк, чтобы они происходили после валидации
            # 'AMT_INCOME_TOTAL': self.income_total.input.value,
            'AMT_INCOME_TOTAL': str(float(self.income_total.input.value) / 2),

            'AMT_CREDIT': self.credit.input.value,
            # TODO: перенести вычисления на бэк, чтобы они происходили после валидации
            # 'AMT_ANNUITY': self.months.input.value
            'AMT_ANNUITY': str(float(self.credit.input.value) / int(self.months.input.value))
        }


        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data_json) as response:
                data = await response.text()

                time.sleep(3)  # для демонстрации!!

                score = 100  # позже заменим на data

                self.submit.visible = True
                self.progress.visible = False
                self.score.value = f"Ваш крединый рейтинг: {score}"

                self.update()
                print(data)

    def build(self):
        """ Содержимое формы """
        return ft.Container(
            width=MAIN_WIDTH,
            bgcolor=ft.colors.with_opacity(0.01, ft.colors.WHITE),
            border_radius=10,
            padding=40,
            alignment=ft.alignment.center,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
                controls=[
                    # Заголовок
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

                    # Информация для идентификации клиента
                    CustomContainer([
                        ft.Row([
                            ft.Text("ФИО:  "),
                            ft.VerticalDivider(width=90),
                            self.surname,
                            self.name,
                            self.patronymic,
                        ]),
                        ft.Row([
                            ft.Text("Дата рождения:  "),
                            ft.VerticalDivider(width=21),
                            self.birth_date,

                            ft.VerticalDivider(width=1),
                            ft.Text("Пол: "),
                            self.gender,
                        ]),
                        ft.Row([
                            ft.Text("Паспортные данные:  "),
                            self.passport_series,
                            self.passport_number
                        ]),
                    ]),

                    # Информация о семье
                    CustomContainer([
                        ft.Row([
                            ft.Text("Семейное положение:"),
                            self.family,
                            self.children
                        ]),
                        ft.Divider(height=10, color="transparent"),
                        ft.Row([
                            ft.Text("Тип жилья:"),
                            ft.VerticalDivider(width=68), self.house,
                            ft.VerticalDivider(width=15), self.car
                        ]),
                        ft.Divider(height=20, color="transparent"),
                        ft.Row([
                            ft.Text("Тип образования:"),
                            ft.VerticalDivider(width=23), self.education,
                        ]),
                    ]),

                    # Информация о работе
                    CustomContainer([
                        ft.Row([
                            ft.Text("Тип занятости:"),
                            ft.VerticalDivider(width=42), self.occupation,
                        ]),
                        ft.Divider(height=20, color="transparent"),
                        ft.Row([
                            ft.Text("Тип организации:"),
                            ft.VerticalDivider(width=22), self.organization,
                        ]),
                        ft.Divider(height=10, color="transparent"),
                        ft.Row([
                            ft.Text("Стаж по текущей\nработе:"),
                            ft.VerticalDivider(width=22), self.days_employed,
                        ]),
                        ft.Row([
                            ft.Text("Тип дохода:"),
                            ft.VerticalDivider(width=60), self.income_type, self.income_total
                        ]),
                    ]),

                    # Информация о кредите
                    CustomContainer([
                        ft.Row([self.credit, self.months])
                    ]),

                    # Кнопка для отправки данных
                    self.submit,

                    # Ожидание ответа на запрос
                    self.progress,

                    # Результат запроса
                    self.score
                ]
            )
        )


def main(page: ft.Page):
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(primary=MAIN_COLOR)
    )
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 30
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.HIDDEN

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
        bgcolor=ft.colors.SECONDARY_CONTAINER,
        color=ft.colors.ON_SECONDARY_CONTAINER,
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
    # ft.app(name=flet_path, target=main, port=flet_port) #  удобнее для отладки
