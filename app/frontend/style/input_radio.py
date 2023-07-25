""" Поле с вариантами ответа в виде переключателя"""

import flet as ft
from style.custom_containers import ONE_FIELD_WIDTH


class InputRadio(ft.Container):
    """ Текстовое поле для ввода в виде переключателя """
    def __init__(self, options):
        super().__init__()
        self.content = ft.RadioGroup(ft.Row(
            [ft.Radio(value=key, label=options[key]) for key in options.keys()]
        ))
        self.width = 1.70 * ONE_FIELD_WIDTH
        self.offset = (0, -0.3)

        self.border = None
        self.border_radius = 5

        self.tooltip = None

    def set_error(self, error_msg):
        """ Установка поля в состояние 'заполнено корректно'/'заполнено с ошибками' """
        if error_msg:
            # заполнено с ошибками
            self.border = ft.border.all(width=2, color=ft.colors.RED_500)
            self.tooltip = "Выберите значение"
        else:
            # заполнено корректно
            self.border = None
            self.tooltip = None

        self.update()
