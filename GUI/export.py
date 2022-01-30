import re

from tkinter import (
    StringVar,
    )
from tkinter.ttk import (
    Button,
    Frame,
    Label,
    OptionMenu,
    Style,
)


class ImageExportFrame:
    def __init__(self, master, style: Style):
        style.configure('ImageExportLocal.TButton', width=19)

        self.pattern_export_frame = Frame(master)
        self.pattern_export_frame.grid(pady=400)
        Label(self.pattern_export_frame,
              text='Chose appropriate resolution and save/print the image').grid(row=0)
        self.resolution_input = StringVar()
        self.resolution = OptionMenu(
            self.pattern_export_frame, self.resolution_input, 'None')
        self.resolution.grid(row=1, column=0, padx=1, pady=1)
        self.save_image_btn = Button(
            self.pattern_export_frame, text='Save', state='normal', style='ImageExportLocal.TButton')
        self.save_image_btn.grid(row=2, column=0)

        self.print_btn = Button(
            self.pattern_export_frame, text='Print', state='disabled', style='ImageExportLocal.TButton')
        self.print_btn.grid(row=3, column=0)
        self.back_to_typing_btn = Button(
            self.pattern_export_frame, text='Back to typing', style='ImageExportLocal.TButton')
        self.back_to_typing_btn.grid(row=4, column=0)

        self.msg = Label(self.pattern_export_frame,
                         wraplength=300, justify='center')
        self.msg.grid(row=5, column=0)
        self.msg.grid_remove()

    def refresh_resolutions(self, resolution: list[str]) -> None:
        self.resolution.grid_forget()

        self.resolution = OptionMenu(
            self.pattern_export_frame, self.resolution_input, resolution[0], *resolution)
        self.resolution.grid(row=1, column=0)

    def get_current_resolution(self) -> tuple:
        res = self.resolution_input.get()
        res_tuple = re.search(r'\((.*?)\)', res).groups(0)[0]
        res_tuple = res_tuple.split(',')
        res_tuple[0] = int(res_tuple[0])
        res_tuple[1] = int(res_tuple[1])
        return tuple(res_tuple)

    def remove_message(self) -> None:
        self.msg.grid_remove()
