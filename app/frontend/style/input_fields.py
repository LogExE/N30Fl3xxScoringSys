""" Текстовое поле для ввода """

import flet as ft
from style.custom_containers import ONE_FIELD_WIDTH


class InputFields(ft.TextField):
    """ Текстовое поле для ввода """
    def __init__(self, title, width, max_length=None, hint_text=None, suffix_text=None):
        super().__init__()
        self.label = title
        self.height = 60
        self.width = width * ONE_FIELD_WIDTH
        self.capitalization = "WORDS"

        self.max_length = max_length
        self.counter_text = " "

        self.hint_text = hint_text
        self.hint_style = ft.TextStyle(size=14, weight=ft.FontWeight.NORMAL)

        self.suffix_text = suffix_text

        self.border_color = ft.colors.BLACK
        self.border_width = 1
        self.focused_border_color = ft.colors.DEEP_PURPLE_500
        self.focused_border_width = 2

    def set_error(self, is_error):
        """ Установка поля в состояние 'заполнено корректно'/'заполнено с ошибками' """
        if is_error:
            # заполнено с ошибками
            self.border_color = ft.colors.RED_500
            self.focused_border_color = ft.colors.RED_500
            self.border_width = 2
        else:
            # заполнено корректно
            self.border_color = ft.colors.BLACK
            self.focused_border_color = ft.colors.DEEP_PURPLE_500
            self.border_width = 1

        self.update()
