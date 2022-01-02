import os
import sys

from tkinter import (
    Tk,
    Label,
    Button,
    Frame,
    )
from PIL import Image, ImageTk

from pattern_generator import ImageBackground, SimplePolishSchema, Pattern
from background import BackgroundImage, BackgroundSettings
from pattern import PatternImage, PatternSettings


class PatternGenerator:
    def __init__(
            self,
            master: Tk,
            ):
        self.master = master
        self.width = master.winfo_screenwidth()
        self.height = master.winfo_screenheight()
        master.title("Pattern Generator")
        master.geometry(f'{self.width}x{self.height}')

        self.settings_frame = Frame(
            self.master, width=(self.width//4) - 10, height=self.height)
        self.drawing_frame = Frame(
            self.master, width=(self.width//2) - 10, height=self.height)
        self.right_frame = Frame(
            self.master, width=(self.width//4) - 10, height=self.height)

        self.img_background_settings = BackgroundSettings(self.settings_frame)
        self.pattern_settings = PatternSettings(self.settings_frame)
        self.pattern_image = PatternImage(self.drawing_frame)

        self.settings_frame.grid(row=0, column=1, padx=5)
        self.settings_frame.grid_propagate(0)
        self.drawing_frame.grid(row=0, column=2, padx=5)
        self.drawing_frame.grid_propagate(0)
        self.right_frame.grid(row=0, column=3, padx=5)
        self.right_frame.grid_propagate(0)

        self.set_save_settings_button()
        self.set_config_button()
        self.configure_pattern_image_buttons()
        self.show_drawing_frame()
        self.invoke_create_background()
        self.enable_widget(self.save_settings_btn)
        self.bind_bg_setting_apply_btn()
        self.bind_edit_background_btn()
        self.bind_save_settings_btn()

    def set_save_settings_button(self) -> None:
        self.save_settings_btn = Button(
            self.settings_frame, pady=10, padx=30, text='Save', state='disable')
        self.save_settings_btn.grid(row=3)

    def set_config_button(self) -> None:
        icon_path = self.get_icon_path()
        setting_icon = ImageTk.PhotoImage(file=icon_path)
        self.config_btn = Button(self.settings_frame, state='normal',
                                 image=setting_icon,
                                 width=12,
                                 height=12,
                                 )
        self.config_btn.image = setting_icon
        self.config_btn.grid(row=0, sticky='w')
        self.config_btn['command'] = lambda: self.show_config()

    def configure_pattern_image_buttons(self) -> None:
        self.pattern_image.text_var.trace_add(
            'write', self.text_callback)

        self.pattern_image.save_image_btn['command'] = lambda: self.save_the_image(
        )
        self.pattern_image.print_btn['command'] = lambda: self.print_the_pattern(
        )

    def show_drawing_frame(self) -> None:
        self.img_background_settings.frame.grid_remove()
        self.pattern_settings.frame.grid_remove()
        self.save_settings_btn.grid_remove()
        self.drawing_frame.grid()

    def invoke_create_background(self) -> None:
        self.create_background(
            self.img_background_settings.width.get(),
            self.img_background_settings.num_of_columns.get(),
            self.img_background_settings.with_mesh.get(),
            self.img_background_settings.color.get(),
            self.img_background_settings.mesh_color.get(),
            self.img_background_settings.schema_input.get())

    def show_config(self) -> None:
        self.drawing_frame.pack_forget()
        self.img_background_settings.frame.grid()
        self.save_settings_btn.grid()
        self.pattern_settings.frame.grid()

    def print_the_pattern(self) -> None:
        pass

    def bind_bg_setting_apply_btn(self) -> None:
        self.img_background_settings.apply_button['command'] = \
            lambda: self.invoke_create_background()

    def bind_edit_background_btn(self) -> None:
        self.img_background_settings.edit_background_btn['command'] = \
            lambda: [
                self.enable_children(self.img_background_settings.frame),
                self.disable_widget(
                    self.img_background_settings.edit_background_btn),
                self.disable_children(self.pattern_settings.frame),

                ]

    def bind_pattern_settings_generate_btn(self) -> None:
        self.pattern_settings.pattern_preview_btn['command'] = \
            lambda: [
               self.create_pattern()
               ]

    def bind_save_settings_btn(self) -> None:
        self.save_settings_btn['command'] = lambda: [
            self.create_pattern(),
            self.show_drawing_frame()]

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
            self.clear_info(self.img_background_settings.error_msg)
        except ValueError as e:
            self.show_info(self.img_background_settings.error_msg, e)
            return
        self.disable_children(self.img_background_settings.frame)
        self.enable_children(self.pattern_settings.frame)

        self.enable_widget(self.img_background_settings.edit_background_btn)
        self.init_pattern()

    def init_pattern(self) -> None:
        self.pattern = Pattern(
            background=self.background,
            schema=self.schema,
            image=self.background.generate_image_background(),
        )

    def create_pattern(self) -> None:
        if not hasattr(self, 'pattern'):
            self.init_pattern()
        start_line_width = self.pattern_settings.width.get()
        color = self.pattern_settings.color.get()
        text = self.pattern_image.text_box.get()
        try:
            setattr(self.pattern, 'start_line_width', start_line_width)
            setattr(self.pattern, 'color', color)
            setattr(self.pattern, 'text', text)
            self.clear_info(self.pattern_image.msg)
        except ValueError as e:
            self.show_info(self.pattern_image.msg, e, 'red')
        self.pattern.image = self.pattern.original_background.copy()
        self.display_image(
            self.pattern_image.drawing_area,
            self.pattern.draw(),
            self.pattern_image.width,
            self.pattern_image.width
            )

    def display_image(self,
                      frame: Frame,
                      image: Image,
                      width: int = 360,
                      height: int = 360) -> None:
        self.remove_children(frame)
        image = image.resize((width, height))
        img = ImageTk.PhotoImage(image=image)
        label = Label(frame, image=img)
        label.image = img
        label.grid()

    def clear_info(self, label: Label) -> None:
        label.grid_remove()

    def show_info(self, label: Label, info: str, bg_color: str = 'red') -> None:
        label['text'] = f'{info}'
        label['fg'] = bg_color
        label.grid(columnspan=3)

    def save_the_image(self) -> None:
        image = self.pattern.draw()
        path = str(os.path.expanduser("~/Desktop/")) + 'pattern.jpg'
        image.save(path, quality=100)
        info = 'Pattern generated on the Desktop, under the pattern.jpg name'
        self.show_info(self.pattern_image.msg, info, 'green')

    def disable_children(self, parent: Frame) -> None:
        for child in parent.winfo_children():
            wtype = child.winfo_class()
            if wtype not in ('Frame', 'Labelframe'):
                child.configure(state='disable')
            else:
                self.disable_children(child)

    def enable_children(self, parent: Frame) -> None:
        for child in parent.winfo_children():
            wtype = child.winfo_class()
            if wtype not in ('Frame', 'Labelframe'):
                child.configure(state='normal')
            else:
                self.enable_children(child)

    def enable_widget(self, widget) -> None:
        widget['state'] = 'normal'

    def disable_widget(self, widget) -> None:
        widget['state'] = 'disable'

    def remove_children(self, parent) -> None:
        for child in parent.winfo_children():
            child.destroy()

    def text_callback(self, *args):
        self.create_pattern()

    def get_icon_path(self) -> None:
        relative_path = 'GUI/setting-icon.png'
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    root = Tk()
    my_gui = PatternGenerator(root)
    root.mainloop()
