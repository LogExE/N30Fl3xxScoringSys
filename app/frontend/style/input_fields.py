import flet as ft
from style.custom_input import ONE_FIELD_WIDTH


class InputFields(ft.UserControl):
    def __init__(self, title, width, max_length=None, hint_text=None, suffix_text=None):
        self.input: ft.Control = ft.TextField(
            label=title,
            height=60,
            width=width*ONE_FIELD_WIDTH,
            capitalization="WORDS",

            max_length=max_length,
            counter_text=" ",
            expand=True,

            hint_text=hint_text,
            hint_style=ft.TextStyle(size=14, weight=ft.FontWeight.NORMAL),

            suffix_text=suffix_text
        )
        self.input_box: ft.Container = ft.Container(
            expand=True,
            content=self.input,
            animate=ft.Animation(300, "ease")
        )
        # self.status: ft.Control = fm.CheckBox(
        #     shape="circle",
        #     value=False,
        #     disabled=True,
        #     offset=ft.Offset(1, 0),
        #     right=0,
        #     bottom=0,
        #     top=1,
        #     animate_opacity=ft.Animation(200, "linear"),
        #     animate_offset=ft.Animation(300, "ease"),
        #     opacity=0
        # )
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
                        # self.status
                    ]
                )
            ]
        )

    def build(self):
        return self.object
