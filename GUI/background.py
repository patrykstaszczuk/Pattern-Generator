from tkinter import (
    Label,
    Button,
    Frame,
    IntVar,
    StringVar,
    OptionMenu,
    Entry
    )


class BackgroundSettings:
    def __init__(self, master):
        self.frame = Frame(master)
        self.frame.grid(row=0, column=0, padx=25, pady=5)

        self.error_msg = Label(self.frame)

        Label(self.frame,
              text='Image width: ').grid(row=0, column=0, sticky='w', pady=10)
        self.width_input = IntVar()
        self.width_input.set(4000)
        self.width = Entry(self.frame, textvariable=self.width_input, width=15)
        self.width.grid(row=0, column=1, sticky='e')

        Label(self.frame,
              text='Letters in row: ').grid(row=1, column=0, sticky='w', pady=10)
        self.num_of_columns_input = IntVar()
        self.num_of_columns_input.set(7)
        self.num_of_columns = Entry(
            self.frame, textvariable=self.num_of_columns_input, width=15)
        self.num_of_columns.grid(row=1, column=1, sticky='e')

        Label(self.frame,
              text='With mesh: ').grid(row=2, column=0, sticky='w', pady=10)
        self.with_mesh_input = StringVar()
        self.with_mesh_input.set('no')
        self.with_mesh = Entry(self.frame,
                               textvariable=self.with_mesh_input, width=15)
        self.with_mesh.grid(row=2, column=1, sticky='e')

        Label(self.frame,
              text='Background color: ').grid(row=3, column=0, pady=10)
        self.color_input = StringVar()
        self.color_input.set('#FFFFFF')
        self.color = Entry(self.frame, textvariable=self.color_input, width=15)
        self.color.grid(row=3, column=1, sticky='e')

        Label(self.frame, text='Mesh color: ').grid(
            row=4, column=0, sticky='w', pady=10)
        self.mesh_color_input = StringVar()
        self.mesh_color_input.set('#000000')
        self.mesh_color = Entry(
            self.frame, textvariable=self.mesh_color_input, width=15)
        self.mesh_color.grid(row=4, column=1, sticky='e')
        Label(self.frame,
              text='Select schema ').grid(row=5, column=0, sticky='w', pady=10)
        self.schema_input = StringVar()
        self.schema_input.set('SimplePolishSchema')
        self.schema = OptionMenu(
            self.frame, variable=self.schema_input, value='SimplePolishSchema')
        self.schema.grid(row=5, column=1, sticky='e')
        self.apply_button = Button(
            self.frame,
            pady=10,
            padx=10,
            text='Apply',
        )
        self.apply_button.grid(row=7, column=0)
        self.edit_background_btn = Button(self.frame, text='Edit background settings',
                                          pady=10, padx=10, name='edit_bg_settings', state='disable')
        #Label(self.frame).grid(row=7, column=1)
        self.edit_background_btn.grid(row=7, column=1)


class BackgroundImage:
    def __init__(self, master):
        self.frame = Frame(master, width=390, height=370)
        self.frame.grid(row=0, column=1, pady=5)
