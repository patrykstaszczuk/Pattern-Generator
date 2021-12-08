import os

from tkinter import (
    Tk,
    Label,
    Button,
    Frame,
    Toplevel,
    IntVar,
    StringVar,
    OptionMenu,
    Entry
    )
from PIL import Image, ImageTk

from pattern_generator import ImageBackground, SimplePolishSchema, Pattern
from background import BackgroundImage, BackgroundSettings
from pattern import PatternImage, PatternSettings


class PatternGenerator:
    def __init__(self, master):
        self.master = master
        master.title("Pattern Generator")
        master.geometry('800x800')

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
                self.bg_settings.mesh_color.get(),
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
        self.save_image_button = Button(
            self.pattern_settings.frame, pady=10, padx=30, text='Save')
        self.save_image_button['command'] = lambda: self.save_the_image()

        self.pattern_settings.continous_reading_button['command'] = lambda: self.live_patter_creation(
        )

    def create_background(
            self,
            width: str,
            num_of_columns: str,
            with_mesh: str,
            color: str,
            mesh_color: str,
            schema: str) -> None:

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
                mesh_color=mesh_color,
                num_of_colums=num_of_columns,
                color=color,
                )
            self.display_image(self.bg_image.frame,
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
            self.display_image(self.pattern_image.frame, self.pattern.draw())
            self.save_image_button.grid(row=5, column=1)
            self.pattern_settings.msg.grid_remove()
        except Exception as e:
            self.pattern_settings.msg.grid_remove()
            self.pattern_settings.msg['text'] = f'{e}'
            self.pattern_settings.msg.grid(row=6, columnspan=2)

    def display_image(self, frame: Frame, image: Image) -> None:
        self.remove_children(frame)
        image = image.resize((390, 370))
        img = ImageTk.PhotoImage(image=image)
        label = Label(frame, image=img)
        label.image = img
        # label.config(bg='black', borderwidth=1)
        label.grid()

    def save_the_image(self) -> None:
        image = self.pattern.draw()
        path = str(os.path.expanduser("~/Desktop/")) + 'pattern.jpg'
        image.save(path, quality=100)
        self.pattern_settings.msg['text'] = 'Pattern generated on the Desktop, under the pattern.jpg name'
        self.pattern_settings.msg.grid(columnspan=2)

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

    def remove_children(self, parent) -> None:
        for child in parent.winfo_children():
            child.destroy()

    def live_patter_creation(self) -> None:
        if self.pattern_settings.generate_button['state'] == 'disabled':
            self.pattern_settings.generate_button['state'] = 'normal'
            self.pattern_settings.text_var.trace_remove(
                *self.pattern_settings.text_var.trace_info()[0])
            self.pattern_settings.continous_reading_button['highlightbackground'] = 'red'
        else:
            self.pattern_settings.continous_reading_button['highlightbackground'] = 'green'
            self.pattern_settings.generate_button['state'] = 'disable'
            self.pattern_settings.text_var.trace_add(
                'write', self.text_callback)

    def text_callback(self, *args):
        self.create_pattern(
            self.pattern_settings.width.get(),
            self.pattern_settings.color.get(),
            self.pattern_settings.text_box.get()
            )


# class ImageWindow(Toplevel):
#     def __init__(self, master: Tk = None) -> None:
#         super().__init__(master=master)
#         self.geometry('400x400')
#         # self.xE = StringVar()
#         # entry = Entry(self, textvariable=self.xE)
#         # entry.grid(pady=5, padx=10)
#         # self.xE.trace("w", self.callback)  # "w"  is a write argument
#
#         self.xl = StringVar()
#         lab = Label(self, textvariable=self.xl)
#         self.xl.set(" the input display ")
#         lab.grid(pady=5, padx=10)


root = Tk()
my_gui = PatternGenerator(root)
root.mainloop()
