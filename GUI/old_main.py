import tkinter as tk
import os
import sys
import subprocess

from PIL import Image, ImageTk

from pattern_generator import ImageBackground, SimplePolishSchema, Pattern


class App(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        root.bind('<Return>', self.callback)
        root.geometry("800x800")
        root.minsize(800, 800)
        root.maxsize(800, 800)
        self.grid()

        self.custom_settings_frame = self.generate_custom_settings_frame()
        self.custom_pattern_settings_frame = self.generate_pattern_settings_frame()

        self.error_msg = tk.Label(self, text=f'', bg='red')
        self.succes_msg = tk.Label(self, text='', bg='green')

        self.background = None
        self.pattern = None
        self.schema = None

    def callback(self, event) -> None:
        """ if Enter key is clicked in pattern settings,
         pass all current value to create_pattern method """
        if event.widget.master == self.custom_pattern_settings_frame:
            kwargs = {}
            for child in self.custom_pattern_settings_frame.winfo_children():
                if child.widgetName == 'entry':
                    kwargs[child.name] = child.get()
            self.create_pattern(**kwargs)

    def generate_custom_settings_frame(self) -> tk.Frame:
        custom_settings_frame = tk.Frame(self)
        custom_settings_frame['width'] = 800
        custom_settings_frame['borderwidth'] = 1
        custom_settings_frame['relief'] = 'solid'
        custom_settings_frame.grid(sticky='e')

        tk.Label(custom_settings_frame,
                 text='How width (in pixsels) you want the image be? Max(5616)? ').grid(row=0, column=0)
        width_input = tk.IntVar()
        width_input.set(4000)
        width = tk.Entry(custom_settings_frame, textvariable=width_input)
        width.grid(row=0, column=1)

        tk.Label(custom_settings_frame,
                 text='How many letters in row you want?: ').grid(row=1, column=0)
        num_of_columns_input = tk.IntVar()
        num_of_columns_input.set(7)
        num_of_columns = tk.Entry(
            custom_settings_frame, textvariable=num_of_columns_input)
        num_of_columns.grid(row=1, column=1)

        tk.Label(custom_settings_frame,
                 text='Do you want to genreate background mesh?:(yes/no) ').grid(row=2, column=0)
        with_mesh_input = tk.StringVar()
        with_mesh_input.set('no')
        with_mesh = tk.Entry(custom_settings_frame,
                             textvariable=with_mesh_input)
        with_mesh.grid(row=2, column=1)

        tk.Label(custom_settings_frame,
                 text='Input desire background color in hex format (#c8fd92). ').grid(row=3, column=0)
        color_input = tk.StringVar()
        color_input.set('#FFFFFF')
        color = tk.Entry(custom_settings_frame, textvariable=color_input)
        color.grid(row=3, column=1)
        tk.Label(custom_settings_frame,
                 text='Select schema ').grid(row=4, column=0)
        schema_input = tk.StringVar()
        schema_input.set('SimplePolishSchema')
        schema = tk.OptionMenu(
            custom_settings_frame, variable=schema_input, value='SimplePolishSchema')
        schema.grid(row=4, column=1)

        tk.Button(custom_settings_frame, text='Apply', command=lambda:
                  self.create_background(width.get(), num_of_columns.get(), with_mesh.get(), color.get(), schema_input.get())).grid(row=5, column=0)
        self.edit_button_frame = tk.Frame(custom_settings_frame)
        self.edit_button_frame.grid(row=5, column=1)
        tk.Button(self.edit_button_frame, text='Edit', state='disabled',
                  command=lambda: self.enable_children(custom_settings_frame)).grid()

        return custom_settings_frame

    def generate_pattern_settings_frame(self) -> tk.Frame:
        pattern_frame = tk.Frame(self, width=1000)
        pattern_frame['relief'] = 'solid'
        pattern_frame['borderwidth'] = 1
        tk.Label(pattern_frame,
                 text='Please input desire line width. Type 0 to use default: ').grid(row=0, column=0)
        width_input = tk.IntVar()
        width_input.set(0)
        width = tk.Entry(pattern_frame, textvariable=width_input)
        width.grid(row=0, column=1)
        width.name = 'width'
        tk.Label(pattern_frame,
                 text='Input desire line color in hex format (#c8fd92): ').grid(row=1, column=0)
        color_input = tk.StringVar()
        color_input.set('#000000')
        color = tk.Entry(pattern_frame, textvariable=color_input)
        color.grid(row=1, column=1)
        color.name = 'color'

        tk.Label(pattern_frame,
                 text='Type your text here...').grid(row=2, column=0)
        text_box = tk.Entry(pattern_frame, state='normal')
        text_box.grid(row=2, column=1)
        text_box.name = 'text'

        tk.Button(pattern_frame, text='Generate pattern', command=lambda:
                  self.create_pattern(width.get(), color.get(), text_box.get())).grid(row=3, column=0)
        return pattern_frame

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
            self.error_msg.grid_remove()
            self.disable_children(self.custom_settings_frame)
            self.enable_children(self.edit_button_frame)
            self.custom_pattern_settings_frame.grid(row=1, column=0, pady=5)
        except Exception as e:
            self.error_msg['text'] = f'{e}, try again'
            self.error_msg.grid()

    def create_pattern(self, width: str, color: str, text: str) -> None:
        try:
            self.pattern = Pattern(
                background=self.background,
                schema=self.schema,
                text=text,
                color=color,
                start_line_width=width
            )
            self.display_image(self.pattern)
            #self.save_the_image()
            self.error_msg.grid_remove()
            self.succes_msg['text'] = 'Pattern generated, you can find it in the project folder'
            self.succes_msg.grid()
        except Exception as e:
            self.succes_msg.grid_remove()
            self.error_msg['text'] = f'{e}'
            self.error_msg.grid()

    def display_image(self, pattern: Image) -> None:
        image_frame = tk.Frame(self)
        image_frame.grid()
        image = pattern.draw()
        image = image.resize((200, 200))

        img = ImageTk.PhotoImage(image=image)
        label = tk.Label(image_frame, image=img)
        label.image = img
        label.config(bg='red')
        label.grid(row=4, column=0)

    def save_the_image(self) -> None:
        image = self.pattern.draw()
        path = str(os.path.expanduser("~/Desktop/")) + 'pattern.jpg'
        image.save(path, quality=100)

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


if __name__ == '__main__':
    root = tk.Tk()
    myapp = App(root)
    myapp.mainloop()
