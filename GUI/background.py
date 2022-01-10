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


class BackgroundSettings:
    def __init__(self, master):
        self.frame = Frame(master)
        self.frame.grid(row=1, column=0, pady=5, padx=10)

        self.error_msg = Label(self.frame)

        Label(self.frame,
              text='Image width: ', bg='white').grid(row=0, column=0, sticky='w', pady=10)
        self.width_input = IntVar()
        self.width = Entry(
            self.frame, textvariable=self.width_input, width=15, bg='white')
        self.width.grid(row=0, column=1, sticky='e')

        Label(self.frame,
              text='Letters in row: ', bg='white').grid(row=1, column=0, sticky='w', pady=10)
        self.num_of_columns_input = IntVar()
        self.num_of_columns = Entry(
            self.frame, textvariable=self.num_of_columns_input, width=15, bg='white')
        self.num_of_columns.grid(row=1, column=1, sticky='e')

        Label(self.frame,
              text='With mesh: ', bg='white').grid(row=2, column=0, sticky='w', pady=10)
        self.with_mesh_input = StringVar()
        radio_buttons = Frame(self.frame)
        radio_buttons.grid(row=2, column=1)
        r1 = Radiobutton(radio_buttons, text="Yes",
                         variable=self.with_mesh_input, value='yes')
        r1.grid(row=0, column=0)
        r2 = Radiobutton(radio_buttons, text="No",
                         variable=self.with_mesh_input, value='no')
        r2.grid(row=0, column=1)

        Label(self.frame,
              text='Background color: ', bg='white').grid(row=3, column=0, pady=10)
        self.color_input = StringVar()
        self.color = Entry(
            self.frame, textvariable=self.color_input, width=15, bg='white')
        self.color.grid(row=3, column=1, sticky='e')

        Label(self.frame, text='Mesh color: ', bg='white').grid(
            row=4, column=0, sticky='w', pady=10)
        self.mesh_color_input = StringVar()
        self.mesh_color = Entry(
            self.frame, textvariable=self.mesh_color_input, width=15, bg='white')
        self.mesh_color.grid(row=4, column=1, sticky='e')
        Label(self.frame,
              text='Select schema ', bg='white').grid(row=5, column=0, sticky='w', pady=10)
        self.schema_input = StringVar()
        self.schema = OptionMenu(
            self.frame, variable=self.schema_input, value='SimplePolishSchema')
        self.schema.grid(row=5, column=1, sticky='e')
        self.apply_button = Button(
            self.frame,
            pady=10,
            padx=10,
            text='Apply',
            bg='white'
        )
        self.apply_button.grid(row=7, column=0)
        self.edit_background_btn = Button(self.frame, text='Edit background settings',
                                          pady=10, padx=10, name='edit_bg_settings',
                                          bg='white', state='disable')
        self.edit_background_btn.grid(row=7, column=1)
        self.set_default_values()

    def set_default_values(self) -> None:
        self.width_input.set(1920)
        self.num_of_columns_input.set(7)
        self.with_mesh_input.set('no')
        self.color_input.set('#FFFFFF')
        self.mesh_color_input.set('#000000')
        self.schema_input.set('SimplePolishSchema')


class BackgroundImage:
    def __init__(self, master):
        self.frame = Frame(master)
        self.frame.grid(row=3)
