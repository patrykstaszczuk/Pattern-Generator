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
        style.configure('Clear.TButton', background='white',
                        padding=0, width=5)

        self.master = master
        self.width = int(master.winfo_screenwidth()//2.6)
        self.height = self.width
        self.left_side = Frame(master, width=80)
        self.right_side = Frame(master, width=80)
        self.center = Frame(master, width=self.width, )

        self.left_side.grid(column=0)
        self.left_side.grid_propagate(0)
        self.center.grid(column=1, sticky='e')
        self.right_side.grid(column=2)
        self.right_side.grid_propagate(0)

        self.drawing_area = Frame(
            self.center, width=self.width, height=self.height, )
        self.drawing_area.grid(row=1)
        self.drawing_area.grid_propagate(0)

        self.msg = Label(self.center)

        Label(self.center,
              text='Type your text here...', style='Header.TLabel').grid(row=2)
        text_box_frame = Frame(self.center)
        text_box_frame.grid(row=3)
        self.text_var = StringVar()
        self.text_box = Entry(text_box_frame, state='normal',
                              textvariable=self.text_var)

        self.text_box.grid(row=3, column=0)
        self.clear_text_btn = Button(
            text_box_frame, text='clear', style='Clear.TButton')
        self.clear_text_btn.grid(row=3, column=1, sticky='w')

        self.buttons_frame = Frame(self.center, padding=20)
        self.buttons_frame.grid(row=4, columnspan=2)
        Label(self.buttons_frame, text='Save the image: ', style='Header.TLabel').grid(
            row=0, columnspan=3,)
        self.save_image_btn = Button(
            self.buttons_frame, text='Save', state='normal')
        self.save_image_btn.grid(row=1, column=0)

        self.resolution_input = StringVar()
        self.resolution = OptionMenu(
            self.buttons_frame, self.resolution_input, 'None')
        # Label(self.buttons_frame, text='..or print direclty: ').grid(
        #     row=2, columnspan=3, pady=10)
        self.print_btn = Button(
            self.buttons_frame, text='Print', state='disabled')
        #self.print_btn.grid(row=3, columnspan=3)

    def clear_text(self) -> None:
        self.text_var.set('')

    def has_active_errors(self) -> None:
        return self.msg.grid_info()

    def remove_last_char_from_text_var(self) -> None:
        current_value = self.text_var.get()
        self.text_var.set(current_value[:-1])

    def prepare_name_of_image(self) -> None:
        text = self.text_var.get()
        return text[:25]

    def refresh_resolutions(self, resolution: list[str]) -> None:
        self.resolution.grid_forget()
        
        self.resolution = OptionMenu(
            self.buttons_frame, self.resolution_input, resolution[0], *resolution)
        self.resolution.grid(row=1, column=2)

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
