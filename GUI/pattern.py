from tkinter import (
    StringVar,
    )
from tkinter.ttk import (
    Label,
    Button,
    Frame,
    Entry,
    OptionMenu,
    Style,
)


class ImageFrame:
    def __init__(self, master, style: Style):
        style.configure('Local.TButton', background='white',
                        padding=0, width=10)

        self.master = master
        self.width = int(master.winfo_screenwidth()//2.8)
        self.height = int(master.winfo_screenheight())
        self.left_side = Frame(master, width=80)
        self.right_side = Frame(master, width=80)
        self.center = Frame(master, width=self.width, height=self.height)

        self.left_side.grid(column=0)
        self.left_side.grid_propagate(0)
        self.center.grid(column=1, sticky='e')
        self.center.grid_propagate(0)
        self.right_side.grid(column=2)
        self.right_side.grid_propagate(0)

        self.drawing_area = Frame(
            self.center, width=self.width, height=self.width)
        self.drawing_area.grid(row=1)
        self.drawing_area.grid_propagate(0)

        self.pattern_text_box_frame = Frame(self.center, padding=50)
        self.pattern_text_box_frame.place(anchor='w', relx=0.2, rely=0.8)
        Label(self.pattern_text_box_frame, text='Type your text here:').grid(
            row=0, column=0)
        self.text_var = StringVar()
        self.text_box = Entry(self.pattern_text_box_frame, state='normal',
                              textvariable=self.text_var)
        self.text_box.grid(row=1, column=0, columnspan=2)
        self.clear_text_btn = Button(
            self.pattern_text_box_frame, text='clear', style='Local.TButton')
        self.clear_text_btn.grid(row=1, column=2, sticky='w')
        self.export_image_btn = Button(
            self.pattern_text_box_frame, text='export', style='Local.TButton')
        self.export_image_btn.grid(row=1, column=3, sticky='w')

        self.msg = Label(self.pattern_text_box_frame)
        self.msg.grid(row=2, columnspan=4)
        self.msg.grid_remove()

    def clear_text(self) -> None:
        self.text_var.set('')

    def has_active_message(self) -> None:
        return self.msg.grid_info()

    def remove_last_char_from_text_var(self) -> None:
        current_value = self.text_var.get()
        self.text_var.set(current_value[:-1])

    def prepare_name_of_image(self) -> None:
        text = self.text_var.get()
        return text[:25]

    def calculate_preview_image_dimensions(self, width: int, height: int) -> None:
        self.preview_image_width = width
        self.preview_image_height = height
        frame_size = self.width

        if width >= height:
            width_ratio = width/frame_size
            self.preview_image_width = frame_size
            self.preview_image_height = height/width_ratio
        else:
            height_ratio = height/frame_size
            self.preview_image_height = frame_size
            self.preview_image_width = width/height_ratio

    def disable_typing(self) -> None:
        self._disable_children(self.pattern_text_box_frame)

    def enable_typing(self) -> None:
        self._enable_children(self.pattern_text_box_frame)

    def _disable_children(self, parent: Frame) -> None:
        for child in parent.winfo_children():
            wtype = child.winfo_class()
            if wtype not in ('Frame', 'Labelframe'):
                child.configure(state='disable')
            else:
                self.disable_children(child)

    def _enable_children(self, parent: Frame) -> None:
        for child in parent.winfo_children():
            wtype = child.winfo_class()
            if wtype not in ('Frame', 'Labelframe'):
                child.configure(state='normal')
            else:
                self.enable_children(child)
