import os
import re
import math
import string
import textwrap

from PIL import Image as PIL_Image
from PIL import ImageFont, ImageDraw

from pattern_generator.background import ImageBackground
from pattern_generator.schemas import Schema


def get_font_instance(font_size: int) -> ImageFont:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    font_name = "DejaVuSans.ttf"
    font_path = dir_path + '/fonts/' + font_name
    try:
        return ImageFont.truetype(
            f"{font_path}", font_size)
    except OSError:
        raise ImportError(f'Cannot import font {font_name}".')


class Pattern:
    def __init__(
        self,
        background: ImageBackground,
        image: PIL_Image,
        schema: Schema,
        text: str = '',
        color: str = '#000000',
        start_line_width: int = 0
    ) -> None:
        self.background = background
        self.image = image
        self.original_background = image.copy()
        self.schema = schema
        self.text = text
        self.prev_text = self.text
        self.color = color
        self.start_line_width = start_line_width

        self.width = image.size[0]
        self.height = image.size[1]

        self.existing_letter_pairs = {}

    def _calculate_line_width(self) -> int:
        """ calculate line width based on image width """
        return self.image.width//1000

    def draw(self, text: str) -> PIL_Image:
        """ generate lines on given image based on provided parameters """
        setattr(self, 'text', text)
        if len(self.prev_text) == 0 or self.prev_text != text[:-1]:
            self.redraw()
        else:
            self.draw_new_line()
        self.prev_text = self.text
        return self.image

    def draw_new_line(self) -> PIL_Image:
        draw = ImageDraw.Draw(self.image)
        mapping = self.background.mapping
        self.draw_line(self.prev_text[-1], self.text[-1], draw, mapping)

    def redraw(self) -> PIL_Image:
        self.image = self.original_background.copy()
        draw = ImageDraw.Draw(self.image)
        mapping = self.background.mapping
        self.existing_letter_pairs = {}
        for i, value in enumerate(self.text):
            if i == len(self.text) - 1:
                break
            self.draw_line(self.text[i], self.text[i+1], draw, mapping)

    def draw_line(self, a: str, b: str, draw: ImageDraw, mapping: dict) -> None:
        if any([a == ' ', b == ' ']):
            return
        line_start_point = mapping[a.lower()]
        line_end_point = mapping[b.lower()]
        pair = a + b
        width_of_line = self._get_line_width(pair)
        draw.line((line_start_point[0], line_start_point[1], line_end_point[0],
                   line_end_point[1]), fill=self.color, width=width_of_line)

    def _get_line_width(self, pair: str) -> None:
        if pair in list(self.existing_letter_pairs.keys()):
            self.existing_letter_pairs.update(
                {pair: self.existing_letter_pairs[pair] + self.start_line_width*2})
            width = self.existing_letter_pairs[pair]
        elif pair[::-1] in list(self.existing_letter_pairs.keys()):
            self.existing_letter_pairs.update(
                {pair[::-1]: self.existing_letter_pairs[pair[::-1]] + self.start_line_width*2})
            width = self.existing_letter_pairs[pair[::-1]]
        else:
            self.existing_letter_pairs.update({pair: 1})
            width = self.start_line_width
        return width

    def get_printable_version(self) -> PIL_Image:
        # need to redraw becouse there is new Pattern obj created
        self.redraw()
        font_size = self._calculate_printable_font_size()
        rows_to_be_added = self._calculate_nums_of_rows_for_text(font_size)
        extra_space = self._calculate_extra_space(font_size, rows_to_be_added)

        new_image_size = (self.width, self.height + extra_space)
        img_with_space = PIL_Image.new('RGB', new_image_size, color='white')
        img_with_space.paste(self.image)

        img_with_text = self._add_text_to_printable_image(
            img_with_space, font_size, rows_to_be_added)
        return img_with_text

    def _calculate_extra_space(self, font_size: int, rows_to_be_added: int) -> int:
        bottom_padding = font_size
        return (rows_to_be_added*font_size) + bottom_padding

    def _calculate_nums_of_rows_for_text(self, font_size: int) -> int:
        return math.ceil((len(self.text) * font_size)/self.width)

    def _calculate_printable_font_size(self) -> int:
        return self.height//60

    def _add_text_to_printable_image(self, img: PIL_Image, font_size: int, rows_to_be_added: int) -> PIL_Image:
        draw = ImageDraw.Draw(img)
        font_size = self._calculate_printable_font_size()
        font = get_font_instance(font_size)

        size_of_one_letter = font.getlength('a')
        max_chars_in_row = math.floor(
            self.width / size_of_one_letter)
        text_lines = textwrap.wrap(self.text, width=max_chars_in_row)
        text_hight = self.height

        left_padding = font_size * 2
        for line in text_lines:
            width, height = font.getsize(line)
            draw.text((0 + left_padding, text_hight),
                      text=line, font=font, fill='black')
            text_hight += height

        return img

    @property
    def start_line_width(self) -> int:
        return self._start_line_width

    @property
    def text(self) -> str:
        return self._text

    @property
    def color(self) -> str:
        return self._color

    @text.setter
    def text(self, value) -> None:
        if not isinstance(value, str):
            raise ValueError('Text must be a string')
        translator = str.maketrans(
            string.punctuation, ' '*len(string.punctuation))
        value = value.translate(translator)
        value = value.lower()
        for char in value:
            if char not in self.schema.get_letters() and char != ' ':
                raise ValueError(
                    f'Given schema does not support char "{char}"')
        self._text = value

    @color.setter
    def color(self, value) -> None:
        if len(value) == 0:
            self._color = '#000000'
            return
        match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', value)
        if not match:
            raise ValueError('Please provide color in correct hex format')
        self._color = value

    @start_line_width.setter
    def start_line_width(self, value: int) -> None:
        try:
            value = int(value)
        except ValueError:
            raise ValueError('Line width must must be a number')
        if value is None or value == 0:
            self._start_line_width = self._calculate_line_width()
            return
        if value < 0:
            raise ValueError('Line width cannot be negative')

        self._start_line_width = value
