from tkinter import (
    Tk,
    Label,
    Button,
    Frame,
    IntVar,
    StringVar,
    OptionMenu,
    Entry
    )
from PIL import Image, ImageTk

from pattern_generator import ImageBackground, SimplePolishSchema, Pattern


class BackgroundSettings:
    def __init__(self, master):
        self.frame = Frame(master, width=550, height=350)
        self.frame.grid(row=0, column=0, padx=25, pady=5)
        self.frame.grid_propagate(0)
        self.frame['relief'] = 'raised'
        self.frame['borderwidth'] = 1

        self.error_msg = Label(self.frame)

        Label(self.frame,
              text='How width (in pixsels) you want the image be? Max(5616)? ').grid(row=0, column=0, sticky='w', pady=10)
        self.width_input = IntVar()
        self.width_input.set(4000)
        self.width = Entry(self.frame, textvariable=self.width_input, width=15)
        self.width.grid(row=0, column=1, sticky='e')

        Label(self.frame,
              text='How many letters in row you want?: ').grid(row=1, column=0, sticky='w', pady=10)
        self.num_of_columns_input = IntVar()
        self.num_of_columns_input.set(7)
        self.num_of_columns = Entry(
            self.frame, textvariable=self.num_of_columns_input, width=15)
        self.num_of_columns.grid(row=1, column=1, sticky='e')

        Label(self.frame,
              text='Do you want to genreate background mesh?:(yes/no) ').grid(row=2, column=0, sticky='w', pady=10)
        self.with_mesh_input = StringVar()
        self.with_mesh_input.set('yes')
        self.with_mesh = Entry(self.frame,
                               textvariable=self.with_mesh_input, width=15)
        self.with_mesh.grid(row=2, column=1, sticky='e')

        Label(self.frame,
              text='Input desire background color in hex format (#c8fd92). ').grid(row=3, column=0, sticky='w', pady=10)
        self.color_input = StringVar()
        self.color_input.set('#FFFFFF')
        self.color = Entry(self.frame, textvariable=self.color_input, width=15)
        self.color.grid(row=3, column=1, sticky='e')
        Label(self.frame,
              text='Select schema ').grid(row=4, column=0, sticky='w', pady=10)
        self.schema_input = StringVar()
        self.schema_input.set('SimplePolishSchema')
        self.schema = OptionMenu(
            self.frame, variable=self.schema_input, value='SimplePolishSchema')
        self.schema.grid(row=4, column=1, sticky='e')
        Label(self.frame, pady=20).grid(row=5)
        self.apply_button = Button(
            self.frame,
            pady=10,
            padx=10,
            text='Apply',
        )
        self.apply_button.grid(row=6, column=0)


class BackgroundImage:
    def __init__(self, master):
        self.frame = Frame(master, width=390, height=370)
        self.frame.grid(row=0, column=1, pady=5)


class PatternSettings:
    def __init__(self, master):
        self.frame = Frame(master, width=550, height=350)
        self.frame.grid(row=1, column=0, padx=25, pady=5)
        self.frame.grid_propagate(0)
        self.frame['relief'] = 'raised'
        self.frame['borderwidth'] = 1

        self.msg = Label(self.frame)

        Label(self.frame,
              text='Please input desire line width. Type 0 to use default: ').grid(row=0, column=0, pady=10)
        width_input = IntVar()
        width_input.set(0)
        self.width = Entry(self.frame, textvariable=width_input)
        self.width.grid(row=0, column=1)
        self.width.name = 'width'
        Label(self.frame,
              text='Input desire line color in hex format (#c8fd92): ').grid(row=1, column=0, pady=10)
        color_input = StringVar()
        color_input.set('#000000')
        self.color = Entry(self.frame, textvariable=color_input)
        self.color.grid(row=1, column=1)
        self.color.name = 'color'

        Label(self.frame,
              text='Type your text here...').grid(row=2, column=0, pady=10)
        self.text_box = Entry(self.frame, state='normal')
        self.text_box.grid(row=2, column=1)
        self.text_box.name = 'text'
        Label(self.frame, pady=20).grid(row=3)
        self.generate_button = Button(self.frame, text='Generate pattern',
                                      padx=10, pady=10)
        self.generate_button.grid(row=4, column=0)
        self.edit_button = Button(self.frame, text='Edit background settings',
                                  pady=10, padx=10)
        self.edit_button.grid(row=4, column=1)


class PatternImage:
    def __init__(self, master):
        self.frame = Frame(master, width=390, height=370)
        self.frame.grid(row=1, column=1, pady=5)


class PatternGenerator:
    def __init__(self, master):
        self.master = master
        master.title("Pattern Generator")
        master.geometry('1000x800')
        master.maxsize(1000, 800)

        self.bg_settings = BackgroundSettings(master)
        self.bg_image = BackgroundImage(master)

        self.pattern_settings = PatternSettings(master)
        self.disable_children(self.pattern_settings.frame)
        self.pattern_image = PatternImage(master)

        self.bg_settings.apply_button['command'] = \
            lambda: self.create_background(
                self.bg_settings.width.get(),
                self.bg_settings.num_of_columns.get(),
                self.bg_settings.with_mesh.get(),
                self.bg_settings.color.get(),
                self.bg_settings.schema_input.get())
        self.pattern_settings.edit_button['command'] = \
            lambda: [
                self.enable_children(self.bg_settings.frame),
                self.disable_children(self.pattern_settings.frame),
                ]
        self.pattern_settings.generate_button['command'] = \
            lambda: [
               self.create_pattern(
                self.pattern_settings.width.get(),
                self.pattern_settings.color.get(),
                self.pattern_settings.text_box.get())
               ]

    def display_background(self, background: Image) -> None:
        image = background.resize((390, 370))
        img = ImageTk.PhotoImage(image=image)
        label = Label(self.bg_image.frame, image=img)
        label.image = img
        label.config(bg='black', borderwidth=1)
        label.grid()

    def create_background(self, width: str, num_of_columns: str, with_mesh: str, color: str, schema: str) -> None:

        self.schema = SimplePolishSchema()
        if with_mesh.upper() == 'YES':
            with_mesh = True
        else:
            with_mesh = False

        try:
            self.background = ImageBackground(
                width=width,
                schema=self.schema,
                with_mesh=with_mesh,
                num_of_colums=num_of_columns,
                color=color,
                )
            self.display_background(
                self.background.generate_image_background())
            self.bg_settings.error_msg.grid_remove()
            self.disable_children(self.bg_settings.frame)
            self.enable_children(self.pattern_settings.frame)
        except Exception as e:
            self.bg_settings.error_msg['text'] = f'{e}, try again'
            self.bg_settings.error_msg.grid(columnspan=2)

    def create_pattern(self, width: str, color: str, text: str) -> None:
        try:
            self.pattern = Pattern(
                background=self.background,
                schema=self.schema,
                text=text,
                color=color,
                start_line_width=width
            )
            self.display_image(self.pattern.draw())
            #self.save_the_image()
            self.pattern_settings.msg.grid_remove()
            self.pattern_settings.msg['text'] = 'Pattern generated, you can find it in the project folder'
            self.pattern_settings.msg.grid()
        except Exception as e:
            self.pattern_settings.msg.grid_remove()
            self.pattern_settings.msg['text'] = f'{e}'
            self.pattern_settings.msg.grid()

    def display_image(self, background: Image) -> None:
        image = background.resize((390, 370))
        img = ImageTk.PhotoImage(image=image)
        label = Label(self.pattern_image.frame, image=img)
        label.image = img
        label.config(bg='black', borderwidth=1)
        label.grid()

    def disable_children(self, parent):
        for child in parent.winfo_children():
            wtype = child.winfo_class()
            if wtype not in ('Frame', 'Labelframe'):
                child.configure(state='disable')
            else:
                self.disable_children(child)

    def enable_children(self, parent):
        for child in parent.winfo_children():
            wtype = child.winfo_class()
            if wtype not in ('Frame', 'Labelframe'):
                child.configure(state='normal')
            else:
                self.enable_children(child)


root = Tk()
my_gui = PatternGenerator(root)
root.mainloop()
