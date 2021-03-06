import os
import re
import math
import string
import textwrap

from PIL import Image as PIL_Image
from PIL import ImageFont, ImageDraw

from pattern_generator.background import ImageBackground
from pattern_generator.schemas import Schema


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
        self.original_text_with_punctuation = text
        self.prev_text = self.text
        self.color = color
        self.start_line_width = start_line_width

        self.width = image.size[0]
        self.height = image.size[1]

        self.existing_letter_pairs = {}
        self.draw_instance = ImageDraw.Draw(self.image)
        self.mapping = self.background.mapping

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
        setattr(self, 'prev_text', self.text)
        return self.image

    def draw_new_line(self) -> None:
        self.draw_line(self.prev_text[-1], self.text[-1])

    def redraw(self) -> PIL_Image:
        self.image = self.original_background.copy()
        self.draw_instance = ImageDraw.Draw(self.image)

        self.existing_letter_pairs = {}
        for i, value in enumerate(self.text[:-1]):
            self.draw_line(self.text[i], self.text[i+1])
        return self.image

    def draw_line(self, a: str, b: str) -> None:
        if any([a == ' ', b == ' ']) or any([a in string.punctuation, b in string.punctuation]):
            return
        line_start_point = self.mapping[a]
        line_end_point = self.mapping[b]
        pair = a + b
        width_of_line = self._get_line_width(pair)
        self.draw_instance.line((line_start_point[0], line_start_point[1], line_end_point[0],
                                 line_end_point[1]), fill=self.color, width=width_of_line)

    def _get_line_width(self, pair: str) -> None:
        if pair in self.existing_letter_pairs.keys():
            self.existing_letter_pairs.update(
                {pair: self.existing_letter_pairs[pair] + self.start_line_width*2})
            width = self.existing_letter_pairs[pair]
        elif pair[::-1] in self.existing_letter_pairs.keys():
            self.existing_letter_pairs.update(
                {pair[::-1]: self.existing_letter_pairs[pair[::-1]] + self.start_line_width*2})
            width = self.existing_letter_pairs[pair[::-1]]
        else:
            self.existing_letter_pairs.update({pair: 1})
            width = self.start_line_width
        return width

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
        self.original_text_with_punctuation = value
        value = value.translate(translator)
        value = value.lower()
        for char in value:
            if char in string.punctuation:
                continue
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
