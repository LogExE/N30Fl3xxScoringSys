""" Главный файл Frontend-модуля """

import asyncio
import os

import aiohttp
import flet as ft
from datetime import datetime

from data import *
from style.custom_containers import custom_container
from style.input_dropdown import InputDropdown
from style.input_fields import InputFields
from style.input_radio import InputRadio

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
        self.gender = InputRadio({"M": "Мужской", "F": "Женский"})

        self.birth_date = InputFields("", 1, 10, "ДД.ММ.ГГГГ")
        self.passport_series = InputFields("Серия", 1, 4)
        self.passport_number = InputFields("Номер", 2, 6)

        self.family = InputDropdown(NAME_FAMILY_STATUS_rus, 2)
        self.children = InputFields("Количество детей", 1, 2)
        self.house = InputDropdown(NAME_HOUSING_TYPE_rus, 2)
        self.car = ft.Checkbox(label="Есть машина", offset=(0, -0.1))
        self.education = InputDropdown(NAME_EDUCATION_TYPE_rus, 3)

        self.occupation = InputDropdown(sorted(OCCUPATION_TYPE_rus), 3)
        self.organization = InputDropdown(sorted(ORGANIZATION_TYPE_rus), 3)
        self.days_employed = InputFields("", 3, 3, suffix_text="лет")
        self.income_type = InputDropdown(NAME_INCOME_TYPE_rus, 1.5)
        self.income_total = InputFields("Годовой доход", 1.42, suffix_text="\u20BD")

        self.credit = InputFields("Сумма кредита", 1.92, suffix_text="\u20BD")
        self.months = InputFields("Кредитный период", 1.92, suffix_text="месяцев")

        self.submit = ft.FloatingActionButton(
            width=MAIN_WIDTH,
            height=45,
            content=ft.Text("Узнать кредитный рейтинг", color=ft.colors.WHITE),
            bgcolor=MAIN_COLOR,
            on_click=lambda e: asyncio.run(self.submit_clicked(e))
        )
        self.progress = ft.ProgressRing(visible=False)
        self.score = ft.Text(
            size=21,
            weight=ft.FontWeight.W_700,
            color=MAIN_COLOR
        )

        self.fields = {
            'SURNAME': self.surname,
            'NAME': self.name,
            'PATRONYMIC': self.patronymic,
            'CODE_GENDER': self.gender,
            'DAYS_BIRTH': self.birth_date,
            'PASSPORT': [self.passport_series, self.passport_number],

            'NAME_FAMILY_STATUS': self.family,
            'CNT_CHILDREN': self.children,
            'NAME_HOUSING_TYPE': self.house,
            'NAME_EDUCATION_TYPE': self.education,

            'OCCUPATION_TYPE': self.occupation,
            'ORGANIZATION_TYPE': self.organization,
            'DAYS_EMPLOYED': self.days_employed,
            'NAME_INCOME_TYPE': self.income_type,
            'AMT_INCOME_TOTAL': self.income_total,

            'AMT_CREDIT': self.credit,
            'AMT_ANNUITY': self.months
        }
        super().__init__()

    def check_date(self, date):
        """ Преобразование даты в количество дней до текущего момента """
        try:
            return (datetime.now() - datetime.strptime(date, "%d.%m.%Y")).days
        except:
            return None

    def mapping(self, val, dct):
        """ Преобразование значений выпадающий полей в формат, с которым работает ML-модель """
        return dct[val] if val else None

    async def submit_clicked(self, e):
        """ Обработчик нажатия на кнопку - отправка запроса на Backend """
        self.submit.visible = False
        self.progress.visible = True
        self.score.value = None
        self.update()

        # Отправка данных из формы на сервер (в формате JSON)
        host = os.getenv("BACKEND_HOST", DEFAULT_BACKEND_HOST)
        port = os.getenv("BACKEND_PORT", DEFAULT_BACKEND_PORT)
        url = f'http://{host}:{port}'

        data_json = {
            'SURNAME': self.surname.value,
            'NAME': self.name.value,
            'PATRONYMIC': self.patronymic.value,
            'CODE_GENDER': self.gender.content.value,
            'DAYS_BIRTH': self.check_date(self.birth_date.value),
            'PASSPORT': self.passport_series.value + self.passport_number.value,

            'NAME_FAMILY_STATUS': self.mapping(self.family.value, NAME_FAMILY_STATUS_dict),
            'CNT_CHILDREN': self.children.value,
            'NAME_HOUSING_TYPE': self.mapping(self.house.value, NAME_HOUSING_TYPE_dict),
            'FLAG_OWN_CAR': str(int(self.car.value)),
            'NAME_EDUCATION_TYPE': self.mapping(self.education.value, NAME_EDUCATION_TYPE_dict),

            'OCCUPATION_TYPE': self.mapping(self.occupation.value, OCCUPATION_TYPE_dict),
            'ORGANIZATION_TYPE': self.mapping(self.organization.value, ORGANIZATION_TYPE_dict),
            'DAYS_EMPLOYED': self.days_employed.value,
            'NAME_INCOME_TYPE': self.mapping(self.income_type.value, NAME_INCOME_TYPE_dict),
            # TODO: вычисления на бэке: AMT_INCOME_TOTAL = AMT_INCOME_TOTAL / 2? уточнить у Алены
            'AMT_INCOME_TOTAL': self.income_total.value,

            'AMT_CREDIT': self.credit.value,
            # TODO: вычисления на бэке: AMT_ANNUITY = AMT_CREDIT / AMT_ANNUITY
            'AMT_ANNUITY': self.months.value
        }

        print("Req_body: ", data_json)

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data_json) as response:
                resp = await response.json()

                print("\nResp_body: ", resp)

                # Подсвечивание полей, заполненных неправильно
                if resp == 'SUCCESS':
                    err_fields = {}
                    # TODO: извечение скорингового балла
                else:
                    err_fields = {err_dict['loc'][1]: err_dict['msg'] for err_dict in resp['detail']}

                for field in self.fields.keys():
                    if field != 'PASSPORT':
                        self.fields[field].set_error(err_fields[field] if field in err_fields.keys() else None)
                    else:
                        for f in self.fields[field]:
                            f.set_error(err_fields[field] if field in err_fields.keys() else None)

                # Вывод результата
                score = 100  # позже заменим на скоринговый балл
                self.submit.visible = True
                self.progress.visible = False

                if not err_fields:
                    self.score.value = f"Ваш крединый рейтинг: {score}"
                else:
                    self.score.value = f"Пожалуйста, заполните форму правильно :("

                self.update()

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
                    custom_container([
                        ft.Row([
                            ft.Text("ФИО:"),
                            ft.VerticalDivider(width=104),
                            self.surname,
                            self.name,
                            self.patronymic,
                        ]),
                        ft.Row([
                            ft.Text("Дата рождения:"),
                            ft.VerticalDivider(width=31),
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
                    custom_container([
                        ft.Row([
                            ft.Text("Семейное положение: "),
                            self.family, self.children
                        ]),
                        ft.Divider(height=10, color="transparent"),
                        ft.Row([
                            ft.Text("Тип жилья:"),
                            ft.VerticalDivider(width=68), self.house, self.car
                        ]),
                        ft.Divider(height=20, color="transparent"),
                        ft.Row([
                            ft.Text("Тип образования:"),
                            ft.VerticalDivider(width=23), self.education,
                        ]),
                    ]),

                    # Информация о работе
                    custom_container([
                        ft.Row([
                            ft.Text("Тип занятости:"),
                            ft.VerticalDivider(width=42), self.occupation,
                        ]),
                        ft.Divider(height=20, color="transparent"),
                        ft.Row([
                            ft.Text("Тип организации: "),
                            ft.VerticalDivider(width=22), self.organization,
                        ]),
                        ft.Divider(height=10, color="transparent"),
                        ft.Row([
                            ft.Text("Стаж по текущей\nработе:"),
                            ft.VerticalDivider(width=28), self.days_employed,
                        ]),
                        ft.Row([
                            ft.Text("Тип дохода: "),
                            ft.VerticalDivider(width=60), self.income_type, self.income_total
                        ]),
                    ]),

                    # Информация о кредите
                    custom_container([
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
    """ Основная страница """
    page.theme = ft.Theme(color_scheme=ft.ColorScheme(primary=MAIN_COLOR))
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
