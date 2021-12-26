from tkinter import (
    Label,
    Button,
    Frame,
    IntVar,
    StringVar,
    Entry,
    PhotoImage
    )
from PIL import ImageTk


class PatternSettings:
    def __init__(self, master):
        self.frame = Frame(master)
        self.frame.grid(row=1, column=0, padx=25, pady=5)

        self.msg = Label(self.frame)

        Label(self.frame,
              text='Pattern line width: ').grid(row=0, column=0, pady=10)
        width_input = IntVar()
        width_input.set(0)
        self.width = Entry(self.frame, textvariable=width_input)
        self.width.grid(row=0, column=1)
        self.width.name = 'width'
        Label(self.frame,
              text='Line color: ').grid(row=1, column=0, pady=10)
        color_input = StringVar()
        color_input.set('#000000')
        self.color = Entry(self.frame, textvariable=color_input)
        self.color.grid(row=1, column=1)
        self.color.name = 'color'

        # Label(self.frame,
        #       text='Type your text here...').grid(row=2, column=0, pady=10)
        # self.text_var = StringVar()
        # self.text_box = Entry(self.frame, state='normal',
        #                       textvariable=self.text_var)
        # self.text_box.grid(row=2, column=1)
        # self.text_box.name = 'text'

        # self.continous_reading_btn = Button(
        #     self.frame, pady=10, padx=30, text='Live', highlightbackground='red')
        # self.continous_reading_btn.grid(row=3, column=0)
        #
        # self.pattern_preview_btn = Button(self.frame, text='Preview',
        #                                   padx=10, pady=10)
        # self.pattern_preview_btn.grid(row=3, column=1)
        # self.edit_background_btn = Button(self.frame, text='Edit background settings',
        #                                   pady=10, padx=10, name='edit_bg_settings', state='disable')
        # Label(self.frame).grid(row=4, columnspan=2)
        # self.edit_background_btn.grid(row=5, column=0)


class PatternImage:
    def __init__(self, master):
        setting_icon = ImageTk.PhotoImage(file='GUI/setting-icon.png')
        self.config_btn = Button(master, state='normal',
                                 image=setting_icon,
                                 width=12,
                                 height=12,
                                 )
        self.config_btn.image = setting_icon
        self.config_btn.grid(row=0, column=3)
        self.width = master.winfo_screenwidth()
        self.height = master.winfo_screenheight()
        self.drawing_area = Frame(master, width=600, height=600,
                                  # relief='solid',
                                  # borderwidth='1'
                                  )
        self.drawing_area.grid(row=1, pady=10, columnspan=2)

        self.msg = Label(master)
        self.msg.grid(row=5)

        Label(master,
              text='Type your text here...').grid(row=2, columnspan=2)
        self.text_var = StringVar()
        self.text_box = Entry(master, state='normal',
                              textvariable=self.text_var)
        self.text_box.grid(row=3, columnspan=2)

        buttons_frame = Frame(master)
        buttons_frame.grid(row=4, columnspan=2, pady=5)

        self.save_image_btn = Button(buttons_frame, pady=10, padx=20,
                                     text='Save', state='normal',
                                     )
        self.save_image_btn.grid(row=0, column=1)
        self.print_btn = Button(buttons_frame, pady=10,
                                padx=20, text='Print', state='normal')
        self.print_btn.grid(row=0, column=2)
