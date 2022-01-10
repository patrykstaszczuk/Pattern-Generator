from tkinter import (
    Label,
    Button,
    Frame,
    IntVar,
    StringVar,
    Entry,
    PhotoImage
    )


class PatternSettings:
    def __init__(self, master):
        self.frame = Frame(master)
        self.frame.grid(row=2, column=0, padx=10, pady=5)

        self.msg = Label(self.frame)

        Label(self.frame,
              text='Pattern line width: ').grid(row=0, column=0, pady=10)
        self.width_input = IntVar()

        self.width = Entry(self.frame, textvariable=self.width_input)
        self.width.grid(row=0, column=1)
        self.width.name = 'width'
        Label(self.frame,
              text='Line color: ').grid(row=1, column=0, pady=10)
        self.color_input = StringVar()
        self.color = Entry(self.frame, textvariable=self.color_input)
        self.color.grid(row=1, column=1)
        self.color.name = 'color'
        self.set_default_values()

    def set_default_values(self) -> None:
        self.width_input.set(0)
        self.color_input.set('#000000')


class PatternImage:
    def __init__(self, master):
        self.width = int(master.winfo_screenwidth()//3)
        self.left_side = Frame(master, width=self.width//4)
        self.right_side = Frame(master, width=self.width//4)
        self.center = Frame(master, width=self.width)

        self.left_side.grid(column=0)
        self.left_side.grid_propagate(0)
        self.center.grid(column=1)
        self.right_side.grid(column=2)
        self.right_side.grid_propagate(0)

        self.drawing_area = Frame(
            self.center, width=self.width, height=self.width)
        self.drawing_area.grid(row=1, pady=10)
        self.drawing_area.grid_propagate(0)

        self.msg = Label(self.center)
        #self.msg.grid(row=5, columnspan=2)

        Label(self.center,
              text='Type your text here...', bg='white').grid(row=2)
        text_box_frame = Frame(self.center)
        text_box_frame.grid(row=3)
        self.text_var = StringVar()
        self.text_box = Entry(text_box_frame, state='normal',
                              textvariable=self.text_var)

        self.text_box.grid(row=3, column=0)
        self.clear_text_btn = Button(
            text_box_frame, text='clear', pady=2, padx=2)
        self.clear_text_btn.grid(row=3, column=1, sticky='w')

        buttons_frame = Frame(self.center)
        buttons_frame.grid(row=4, pady=5, columnspan=2)

        self.save_image_btn = Button(buttons_frame, pady=10, padx=20,
                                     text='Save', state='normal',
                                     )
        self.save_image_btn.grid(row=0, column=1)
        self.print_btn = Button(buttons_frame, pady=10,
                                padx=20, text='Print', state='disabled')
        self.print_btn.grid(row=0, column=2)

    def clear_text(self) -> None:
        self.text_var.set('')

    def is_error_on_grid(self) -> None:
        return self.msg.winfo_ismapped()

    def remove_last_char_from_text_var(self) -> None:
        current_value = self.text_var.get()
        self.text_var.set(current_value[:-1])

    def prepare_name_of_image(self) -> None:
        text = self.text_var.get()
        return text[:25]
