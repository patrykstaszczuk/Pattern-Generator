from tkinter import (
    Label,
    Button,
    Frame,
    IntVar,
    StringVar,
    OptionMenu,
    Entry,
    Radiobutton,
    )


class ImageSettings:
    def __init__(self, master):
        self.frame = Frame(master, bg='white')
        self.frame.grid(row=1, column=0, pady=5, padx=10)
        self.error_msg = Label(self.frame)

        Label(self.frame, bg='white', text='Background settings: ').grid(
            row=0, columnspan=2, pady=10)
        Label(self.frame,
              text='Image width: ', bg='white').grid(row=1, column=0, sticky='w', pady=10)
        self.background_width_input = IntVar()
        self.background_width = Entry(
            self.frame, textvariable=self.background_width_input, width=15, bg='white')
        self.background_width.grid(row=1, column=1, sticky='e')

        Label(self.frame,
              text='Letters in row: ', bg='white').grid(row=2, column=0, sticky='w', pady=10)
        self.num_of_columns_input = IntVar()
        self.num_of_columns = Entry(
            self.frame, textvariable=self.num_of_columns_input, width=15, bg='white')
        self.num_of_columns.grid(row=2, column=1, sticky='e')

        Label(self.frame,
              text='With mesh: ', bg='white').grid(row=3, column=0, sticky='w', pady=10)
        self.with_mesh_input = StringVar()
        radio_buttons = Frame(self.frame, bg='white')
        radio_buttons.grid(row=3, column=1)
        r1 = Radiobutton(radio_buttons, text="Yes",
                         variable=self.with_mesh_input, value='yes', bg='white')
        r1.grid(row=0, column=0)
        r2 = Radiobutton(radio_buttons, text="No",
                         variable=self.with_mesh_input, value='no', bg='white')
        r2.grid(row=0, column=1)

        Label(self.frame,
              text='Background color: ', bg='white').grid(row=4, column=0, pady=10)
        self.background_color_input = StringVar()
        self.background_color = Entry(
            self.frame, textvariable=self.background_color_input, width=15, bg='white')
        self.background_color.grid(row=4, column=1, sticky='e')

        Label(self.frame, text='Mesh color: ', bg='white').grid(
            row=5, column=0, sticky='w', pady=10)
        self.mesh_color_input = StringVar()
        self.mesh_color = Entry(
            self.frame, textvariable=self.mesh_color_input, width=15, bg='white')
        self.mesh_color.grid(row=5, column=1, sticky='e')

        Label(self.frame,
              text='Select schema ', bg='white').grid(row=6, column=0, sticky='w', pady=10)
        self.schema_input = StringVar()
        self.schema = OptionMenu(
            self.frame, variable=self.schema_input, value='SimplePolishSchema')
        self.schema.grid(row=6, column=1, sticky='e')

        Label(self.frame, bg='white', text='Pattern settings: ').grid(
            row=7, columnspan=2, pady=10)
        Label(self.frame,
              text='Pattern line width: ', bg='white').grid(row=8, column=0, pady=10)
        self.pattern_line_width_input = IntVar()
        self.pattern_line_width = Entry(
            self.frame, textvariable=self.pattern_line_width_input, bg='white')
        self.pattern_line_width.grid(row=8, column=1)
        self.pattern_line_width.name = 'width'

        Label(self.frame,
              text='Line color: ', bg='white').grid(row=9, column=0, pady=10)
        self.pattern_line_color_input = StringVar()
        self.pattern_line_color = Entry(
            self.frame, textvariable=self.pattern_line_color_input, bg='white')
        self.pattern_line_color.grid(row=9, column=1)
        self.pattern_line_color.name = 'color'

        self.save_settings_btn = Button(
            self.frame, pady=10, padx=30, text='Save')
        self.save_settings_btn.grid(row=10, column=1, sticky='e')

        self.restore_default_settings_btn = Button(self.frame, pady=10,
                                                   padx=20, text='Restore default')
        self.restore_default_settings_btn.grid(row=10, column=0, sticky='w')

        self.set_default_values()

    def set_default_values(self) -> None:
        self.background_width_input.set(1920)
        self.num_of_columns_input.set(7)
        self.with_mesh_input.set('no')
        self.background_color_input.set('#FFFFFF')
        self.mesh_color_input.set('#000000')
        self.schema_input.set('SimplePolishSchema')

        self.pattern_line_width_input.set(0)
        self.pattern_line_color_input.set('#000000')

    def has_active_errors(self) -> None:
        return self.error_msg.grid_info()
