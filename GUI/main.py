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
        self.pattern_image = PatternImage(master)

        self.set_initial_state_for_frames()

        self.bind_background_setting_apply_button()
        self.bind_pattern_settings_edit_button()
        self.bind_pattern_settings_generate_button()
        self.bind_live_writing_button()

        self.save_image_button = Button(
            self.pattern_settings.frame, pady=10, padx=30, text='Save', state='disable')
        self.save_image_button.grid(row=5, column=1)
        self.bind_save_image_button()

    def set_initial_state_for_frames(self) -> None:
        self.disable_children(self.pattern_settings.frame)

    def bind_background_setting_apply_button(self) -> None:
        self.bg_settings.apply_button['command'] = \
            lambda: self.create_background(
                self.bg_settings.width.get(),
                self.bg_settings.num_of_columns.get(),
                self.bg_settings.with_mesh.get(),
                self.bg_settings.color.get(),
                self.bg_settings.mesh_color.get(),
                self.bg_settings.schema_input.get())

    def bind_pattern_settings_edit_button(self) -> None:
        self.pattern_settings.edit_button['command'] = \
            lambda: [
                self.enable_children(self.bg_settings.frame),
                self.disable_children(self.pattern_settings.frame),
                ]

    def bind_pattern_settings_generate_button(self) -> None:
        self.pattern_settings.generate_button['command'] = \
            lambda: [
               self.create_pattern()
               ]

    def bind_live_writing_button(self) -> None:
        self.pattern_settings.continous_reading_button['command'] = \
            lambda: self.live_pattern_creation()

    def bind_save_image_button(self) -> None:
        self.save_image_button['command'] = lambda: self.save_the_image()

    def create_background(
            self, width: str, num_of_columns: str, with_mesh: str,
            color: str, mesh_color: str, schema: str
            ) -> None:

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
            self.clear_errors(self.bg_settings.error_msg)
        except Exception as e:
            self.show_errors(self.bg_settings.error_msg, e)
            return

        self.display_image(self.bg_image.frame,
                           self.background.generate_image_background())
        self.disable_children(self.bg_settings.frame)
        self.enable_children(self.pattern_settings.frame)
        self.disable_save_button()
        self.deactivate_live_button()
        self.init_pattern()

    def init_pattern(self) -> None:
        self.pattern = Pattern(
            background=self.background,
            schema=self.schema,
            image=self.background.generate_image_background(),
        )

    def create_pattern(self) -> None:
        if not self.pattern:
            self.init_pattern()
        start_line_width = self.pattern_settings.width.get()
        color = self.pattern_settings.color.get()
        text = self.pattern_settings.text_box.get()
        try:
            setattr(self.pattern, 'start_line_width', start_line_width)
            setattr(self.pattern, 'color', color)
            setattr(self.pattern, 'text', text)
            self.enable_save_button()
            self.clear_errors(self.pattern_settings.msg)
        except Exception as e:
            self.show_errors(self.pattern_settings.msg, e)
            self.disable_save_button()

        self.pattern.image = self.pattern.original_background.copy()
        self.display_image(self.pattern_image.frame, self.pattern.draw())

    def display_image(self, frame: Frame, image: Image) -> None:
        self.remove_children(frame)
        image = image.resize((390, 370))
        img = ImageTk.PhotoImage(image=image)
        label = Label(frame, image=img)
        label.image = img
        label.grid()

    def enable_save_button(self) -> None:
        self.save_image_button['state'] = 'normal'

    def disable_save_button(self) -> None:
        self.save_image_button['state'] = 'disable'

    def clear_errors(self, label: Label) -> None:
        label.grid_remove()

    def show_errors(self, label: Label, e: Exception) -> None:
        label['text'] = f'{e}, try again'
        label.grid(columnspan=3)

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

    def live_pattern_creation(self) -> None:
        if self.pattern_settings.generate_button['state'] == 'disabled':
            self.activate_generate_button()
            self.deactivate_live_button()
        else:
            self.activate_live_button()
            self.deactivate_generate_button()

    def deactivate_live_button(self) -> None:
        traces = self.pattern_settings.text_var.trace_info()
        if not traces:
            return
        self.pattern_settings.text_var.trace_remove(*traces[0])
        self.pattern_settings.continous_reading_button['highlightbackground'] = 'red'

    def deactivate_generate_button(self) -> None:
        self.pattern_settings.generate_button['state'] = 'disable'

    def activate_live_button(self) -> None:
        self.pattern_settings.continous_reading_button['highlightbackground'] = 'green'
        self.pattern_settings.text_var.trace_add(
            'write', self.text_callback)

    def text_callback(self, *args):
        self.create_pattern()

    def activate_generate_button(self) -> None:
        self.pattern_settings.generate_button['state'] = 'normal'


root = Tk()
my_gui = PatternGenerator(root)
root.mainloop()
