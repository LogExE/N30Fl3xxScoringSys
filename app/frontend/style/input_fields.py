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

        self.tooltip = None

    def set_error(self, error_msg):
        """ Установка поля в состояние 'заполнено корректно'/'заполнено с ошибками' """
        if error_msg:
            # заполнено с ошибками
            self.border_color = ft.colors.RED_500
            self.focused_border_color = ft.colors.RED_500
            self.border_width = 2

            if "integer" in error_msg:
                if self.hint_text == "ДД.ММ.ГГГГ":
                    self.tooltip = "Введите корректную дату в формате ДД.ММ.ГГГГ"
                else:
                    self.tooltip = "Введите целочисленное значение"
            elif "number" in error_msg:
                self.tooltip = "Введите числовое значение"
            elif "10" in error_msg:
                if self.label == "Серия":
                    self.tooltip = "Поле должно содержать ровно 4 цифры"
                elif self.label == "Номер":
                    self.tooltip = "Поле должно содержать ровно 6 цифр"
            elif "3" in error_msg:
                self.tooltip = "Поле должно содержать хотя бы 3 символа"
            elif "1" in error_msg:
                self.tooltip = "Поле должно содержать хотя бы 1 символ"
            elif "less" in error_msg:
                self.tooltip = "Превышение допустимого возраста"
            elif "greater" in error_msg:
                self.tooltip = "Недостижение допустимого возраста"
            else:
                self.tooltip = error_msg

        else:
            # заполнено корректно
            self.border_color = ft.colors.BLACK
            self.focused_border_color = ft.colors.DEEP_PURPLE_500
            self.border_width = 1
            self.tooltip = None

        self.update()
