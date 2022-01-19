import os
import sys
import re
from tkinter import (
    Tk,
    Label,
    Button,
    Frame,
    )
from PIL import Image, ImageTk

from pattern_generator import ImageBackground, SimplePolishSchema, Pattern, Schema
from pattern import ImageFrame
from settings import ImageSettings
from image_exporter import ImageExporter


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
        master.configure(bg='white')

        self.settings_frame = Frame(
            self.master, width=(self.width//4) - 10, height=self.height, bg='white')
        self.drawing_frame = Frame(
            self.master, width=(self.width//2) - 10, height=self.height, bg='white')
        self.right_frame = Frame(
            self.master, width=(self.width//4) - 10, height=self.height, bg='white')

        self.settings_frame.grid(row=0, column=1, padx=5)
        self.settings_frame.grid_propagate(0)
        self.drawing_frame.grid(row=0, column=2, padx=5)
        self.drawing_frame.grid_propagate(0)
        self.right_frame.grid(row=0, column=3, padx=5)
        self.right_frame.grid_propagate(0)

        self.settings = ImageSettings(self.settings_frame)
        self.image_frame = ImageFrame(self.drawing_frame)

        self.background = self.invoke_create_background()
        self.show_config_btn = self.set_config_button()

        self.bind_save_settings_btn()
        self.bind_restore_default_settings_btn()
        self.bind_pattern_image_text_input()
        self.bind_pattern_image_buttons()
        self.show_drawing_frame()

    def bind_save_settings_btn(self) -> Button:
        self.settings.save_settings_btn['command'] = lambda: [
            self.save_settings()
            ]

    def save_settings(self) -> None:
        self.invoke_create_background()
        if self.settings.has_active_errors():
            return
        self.draw_pattern()
        self.show_drawing_frame()

    def bind_restore_default_settings_btn(self) -> Button:
        self.settings.restore_default_settings_btn['command'] = lambda: [
            self.settings.set_default_values(),
        ]

    def set_config_button(self) -> Button:
        icon_path = self.get_icon_path()
        setting_icon = ImageTk.PhotoImage(file=icon_path)

        btn = Button(self.settings_frame, state='normal',
                     image=setting_icon,
                     width=12,
                     height=12,
                     )
        btn.image = setting_icon
        btn.grid(row=0, sticky='w')

        btn['command'] = lambda: self.show_config()
        return btn

    def get_icon_path(self) -> None:
        relative_path = 'GUI/setting-icon.png'
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def bind_pattern_image_text_input(self) -> None:
        self.image_frame.clear_text_btn['command'] = \
            lambda: [self.image_frame.clear_text(),
                     self.draw_pattern()]
        self.image_frame.text_var.trace_add(
            'write', self.text_callback)

    def text_callback(self, *args):
        self.draw_pattern()

    def bind_pattern_image_buttons(self) -> None:
        self.image_frame.save_image_btn['command'] = lambda: self.save_the_image(
        )
        self.image_frame.print_btn['command'] = lambda: self.print_the_pattern(
        )

    def invoke_create_background(self) -> None:
        """ Inputs are validated by package """
        return self.create_background(
            self.settings.background_width.get(),
            self.settings.num_of_columns.get(),
            self.settings.with_mesh_input.get(),
            self.settings.background_color.get(),
            self.settings.mesh_color.get(),
            self.settings.schema_input.get())

    def show_drawing_frame(self) -> None:
        self.settings.frame.grid_remove()
        self.drawing_frame.grid()
        self.right_frame.grid()

        resolutions = self.background.get_available_resolutions()
        self.image_frame.refresh_resolutions(resolutions)

    def show_config(self) -> None:
        self.drawing_frame.grid_remove()
        self.right_frame.grid_remove()
        self.settings.frame.grid()

    def print_the_pattern(self) -> None:
        pass

    def create_background(self, width: str, num_of_columns: str,
                          with_mesh: str, color: str, mesh_color: str,
                          schema: str) -> None:

        schema = SimplePolishSchema()

        if with_mesh.upper() == 'YES':
            with_mesh = True
        else:
            with_mesh = False

        try:
            self.background = ImageBackground(
                width=width,
                schema=schema,
                with_mesh=with_mesh,
                mesh_color=mesh_color,
                num_of_columns=num_of_columns,
                color=color,
                )
            self.clear_info(self.settings.error_msg)
            self.init_pattern(self.background, schema)
            return self.background
        except ValueError as e:
            self.show_info(self.settings.error_msg, e)

    def init_pattern(self, background: ImageBackground, schema: Schema) -> None:
        try:
            background_img = background.generate_image_background()
            self.pattern = Pattern(
                background=background,
                schema=schema,
                image=background_img,
                start_line_width=self.settings.pattern_line_width.get(),
                color=self.settings.pattern_line_color.get(),
            )
            # we need to keep prev text after settings change
            self.pattern.prev_text = self.image_frame.text_box.get()

            self.image_frame.calculate_preview_image_dimensions(
                background_img.width, background_img.height)
            self.clear_info(self.settings.error_msg)
        except ValueError as e:
            self.show_info(self.settings.error_msg, e, 'red')

    def draw_pattern(self) -> None:
        if not hasattr(self, 'pattern'):
            self.init_pattern()

        text = self.image_frame.text_box.get()

        try:
            image = self.pattern.draw(text)
            self.display_image(
                self.image_frame.drawing_area,
                image
                )
            self.clear_info(self.image_frame.msg)
            self.enable_widget(self.image_frame.save_image_btn)
        except ValueError as e:
            if self.image_frame.has_active_errors():
                """ do not append new letters if error is active """
                self.image_frame.remove_last_char_from_text_var()
            self.show_info(self.image_frame.msg, e, 'red')
            self.disable_widget(self.image_frame.save_image_btn)

    def display_image(self, frame: Frame, image: Image,) -> None:
        frame_size = frame.winfo_width()
        width = self.image_frame.preview_image_width
        height = self.image_frame.preview_image_height
        self.remove_children(frame)
        image = image.resize((round(width), round(height)))

        if image.size[0] < frame_size:
            image = self.get_resized_image_in_width(image, frame_size)
        if image.size[1] < frame_size:
            image = self.get_reisized_image_in_height(image, frame_size)

        img = ImageTk.PhotoImage(image=image)
        label = Label(frame, image=img, bg='white')
        label.image = img
        label.grid()

    @staticmethod
    def get_resized_image_in_width(image: Image, frame_size: int) -> Image:
        """ fit image in width inside drawing frame """
        diff = frame_size - image.size[0]
        new_size = (image.size[0]+diff, image.size[1])
        wider_image = Image.new('RGB', new_size, color='white')
        wider_image.paste(image, (diff//2, 0))
        return wider_image

    @staticmethod
    def get_reisized_image_in_height(image: Image, frame_size: int) -> Image:
        """ fit image in height inside drawing frame """
        diff = frame_size - image.size[1]
        new_size = (image.size[0], image.size[1] + diff)
        higher_image = Image.new('RGB', new_size, color='white')
        higher_image.paste(image, (0, diff//2))
        return higher_image

    def clear_info(self, label: Label) -> None:
        label.grid_remove()

    def show_info(self, label: Label, info: str, bg_color: str = 'red') -> None:
        label['text'] = f'{info}'
        label['fg'] = bg_color
        label.grid(columnspan=3)

    def save_the_image(self) -> None:
        resolution = self.get_resolution()
        name = self.image_frame.prepare_name_of_image()

        if len(name) == 0:
            info = 'You cannot save pattern without any letters'
            self.show_info(self.image_frame.msg, info, 'red')
            return

        image_exporter = ImageExporter(
            resolution, name, self.background, self.settings, self.pattern)
        try:
            path = image_exporter.prepare_path()
        except(RuntimeError, OSError) as e:
            self.show_info(self.image_frame.msg, e, 'red')

        image_exporter.save(path)
        info = f'Done, pattern available in {path}'
        self.show_info(self.image_frame.msg, info, 'green')

    def get_resolution(self) -> tuple:
        res = self.image_frame.resolution_input.get()
        res_tuple = re.search(r'\((.*?)\)', res).groups(0)[0]
        res_tuple = res_tuple.split(',')
        res_tuple[0] = int(res_tuple[0])
        res_tuple[1] = int(res_tuple[1])
        return tuple(res_tuple)

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


if __name__ == '__main__':
    root = Tk()
    my_gui = PatternGenerator(root)
    root.mainloop()
