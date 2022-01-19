import math
import textwrap
import os

from PIL import Image as PIL_Image
from PIL import ImageDraw, ImageFont


def get_font_instance(font_size: int) -> ImageFont:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    font_name = "DejaVuSans.ttf"
    font_path = dir_path + '/fonts/' + font_name
    try:
        return ImageFont.truetype(
            f"{font_path}", font_size)
    except OSError:
        raise ImportError(f'Cannot import font {font_name}".')


class PatternExporter:
    def __init__(
            self,
            pattern: PIL_Image,
            ) -> None:
        self.image = pattern.redraw()
        self.width = pattern.width
        self.height = pattern.height
        self.text = pattern.text

    def get_printable_version(self, text: str = None) -> PIL_Image:
        # need to redraw becouse there is new Pattern obj created
        if text is None:
            text = self.text
        font_size = self._calculate_printable_font_size()
        rows_to_be_added = self._calculate_nums_of_rows_for_text(
            font_size, text)
        extra_space = self._calculate_extra_space(font_size, rows_to_be_added)

        new_image_size = (self.width, self.height + extra_space)
        img_with_space = PIL_Image.new('RGB', new_image_size, color='white')
        img_with_space.paste(self.image)

        img_with_text = self._add_text_to_printable_image(
            img_with_space, font_size, rows_to_be_added, text)
        return img_with_text

    def _calculate_extra_space(self, font_size: int, rows_to_be_added: int) -> int:
        bottom_padding = font_size
        return (rows_to_be_added*font_size) + bottom_padding

    def _calculate_nums_of_rows_for_text(self, font_size: int, text: str) -> int:
        return math.ceil((len(self.text) * font_size)/self.width)

    def _calculate_printable_font_size(self) -> int:
        return self.height//60

    def _add_text_to_printable_image(
            self,
            img: PIL_Image,
            font_size: int,
            rows_to_be_added: int,
            text: str
            ) -> PIL_Image:
        draw = ImageDraw.Draw(img)
        font_size = self._calculate_printable_font_size()
        font = get_font_instance(font_size)

        size_of_one_letter = font.getlength('a')
        max_chars_in_row = math.floor(
            self.width / size_of_one_letter)
        text_lines = textwrap.wrap(text, width=max_chars_in_row)
        text_hight = self.height

        left_padding = font_size * 2
        for line in text_lines:
            width, height = font.getsize(line)
            draw.text((0 + left_padding, text_hight),
                      text=line, font=font, fill='black')
            text_hight += height

        return img
