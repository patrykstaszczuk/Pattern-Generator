from tkinter import (
    # Label,
    # Button,
    # Frame,
    IntVar,
    StringVar,
    # OptionMenu,
    # Entry,
    # Radiobutton,
    )
from tkinter.ttk import (
    Label,
    Button,
    Frame,
    Entry,
    Radiobutton,
    OptionMenu,
    Style,
    )


class ImageSettings:
    def __init__(self, master):
        self.frame = Frame(master, )
        self.frame.grid(row=1, column=0, pady=5)

        Label(self.frame, text='Background settings: ').grid(
            row=0, columnspan=2, pady=10)
        Label(self.frame,
              text='Image width: ', ).grid(row=1, column=0, sticky='w', pady=10)
        self.background_width_input = IntVar()
        self.background_width = Entry(
            self.frame, textvariable=self.background_width_input, width=15, )
        self.background_width.grid(row=1, column=1, sticky='e')

        Label(self.frame,
              text='Letters in row: ', ).grid(row=2, column=0, sticky='w', pady=10)
        self.num_of_columns_input = IntVar()
        self.num_of_columns = Entry(
            self.frame, textvariable=self.num_of_columns_input, width=15, )
        self.num_of_columns.grid(row=2, column=1, sticky='e')

        Label(self.frame,
              text='With mesh: ', ).grid(row=3, column=0, sticky='w', pady=10)
        self.with_mesh_input = StringVar()
        radio_buttons = Frame(self.frame, )
        radio_buttons.grid(row=3, column=1)
        r1 = Radiobutton(radio_buttons, text="Yes",
                         variable=self.with_mesh_input, value='yes', )
        r1.grid(row=0, column=0)
        r2 = Radiobutton(radio_buttons, text="No",
                         variable=self.with_mesh_input, value='no', )
        r2.grid(row=0, column=1)

        Label(self.frame,
              text='Background color: ', ).grid(row=4, column=0, pady=10)
        self.background_color_input = StringVar()
        self.background_color = Entry(
            self.frame, textvariable=self.background_color_input, width=15, )
        self.background_color.grid(row=4, column=1, sticky='e')

        Label(self.frame, text='Mesh color: ', ).grid(
            row=5, column=0, sticky='w', pady=10)
        self.mesh_color_input = StringVar()
        self.mesh_color = Entry(
            self.frame, textvariable=self.mesh_color_input, width=15, )
        self.mesh_color.grid(row=5, column=1, sticky='e')

        Label(self.frame,
              text='Select schema ', ).grid(row=6, column=0, sticky='w', pady=10)
        self.schema_input = StringVar()
        self.schema_input.set('SimplePolishSchema')
        self.schema = OptionMenu(
            self.frame, variable=self.schema_input)
        self.schema.grid(row=6, column=1, sticky='e')

        Label(self.frame, text='Pattern settings: ').grid(
            row=7, columnspan=2, pady=10)
        Label(self.frame,
              text='Pattern line width: ', ).grid(row=8, column=0, pady=10)
        self.pattern_line_width_input = IntVar()
        self.pattern_line_width = Entry(
            self.frame, textvariable=self.pattern_line_width_input, )
        self.pattern_line_width.grid(row=8, column=1)
        self.pattern_line_width.name = 'width'

        Label(self.frame,
              text='Line color: ', ).grid(row=9, column=0, pady=10)
        self.pattern_line_color_input = StringVar()
        self.pattern_line_color = Entry(
            self.frame, textvariable=self.pattern_line_color_input, )
        self.pattern_line_color.grid(row=9, column=1)
        self.pattern_line_color.name = 'color'

        self.save_settings_btn = Button(
            self.frame, text='Save')
        self.save_settings_btn.grid(row=10, column=1, sticky='e')

        self.restore_default_settings_btn = Button(
            self.frame, text='Restore default')
        self.restore_default_settings_btn.grid(row=10, column=0, sticky='w')

        self.error_msg = Label(self.frame)
        self.error_msg.grid(row=11, columnspan=3)

        self.set_default_values()

    def set_default_values(self) -> None:
        if self.has_active_message():
            self.error_msg.grid_remove()

        self.background_width_input.set(1920)
        self.num_of_columns_input.set(7)
        self.with_mesh_input.set('no')
        self.background_color_input.set('#FFFFFF')
        self.mesh_color_input.set('#000000')
        self.schema_input.set('SimplePolishSchema')

        self.pattern_line_width_input.set(0)
        self.pattern_line_color_input.set('#000000')

    def has_active_message(self) -> None:
        return self.error_msg.grid_info()
