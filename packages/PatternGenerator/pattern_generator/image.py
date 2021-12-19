from .schemas import Schema
from PIL import Image as PIL_Image
from PIL import ImageDraw, ImageFont
import math
import re
import os


class ImageBackground:
    def __init__(
        self,
        width: int,
        schema: Schema,
        num_of_colums: int,
        color: str = '#FFFFFF',
        mesh_color: str = '#000000',
        with_mesh: bool = False,
    ) -> None:
        self.width = width
        self.schema = schema
        self.num_of_colums = num_of_colums
        self.with_mesh = with_mesh
        self.mesh_color = mesh_color
        self.color = color
        self._height = self._calculate_image_height()

        self._tile_width = 0
        self._tile_height = 0
        self.mapping = {item: 0 for item in self.schema.get_letters()}
        dir_path = os.path.dirname(os.path.realpath(__file__))
        font_name = "DejaVuSans.ttf"
        font_path = dir_path + '/fonts/' + font_name
        try:

            self.font = ImageFont.truetype(
                f"{font_path}", round(self.width/100))
        except OSError:
            raise ImportError(f'Cannot import font {font_name}".')

    def _calculate_image_height(self) -> None:
        """ calculate image height based on number of
        columns and number of schema letters"""
        num_of_letters = self.schema.get_length()
        num_of_rows = math.ceil(num_of_letters/self.num_of_colums)
        height_in_px = num_of_rows * self.get_tile_size()[1]
        if height_in_px >= 65500:
            raise ValueError('Cannot create background. '
                             + 'Height cannot be greater then 65500px. '
                             + 'Please decrease width or increase number of letters in one row')
        return height_in_px

    def generate_image_background(self) -> PIL_Image:
        """ generate PIL image """
        image = PIL_Image.new(
            'RGB',
            (self.width, self._height),
            color=self.color)
        self._map_letters_to_image()
        if self.with_mesh:
            image = self._draw_mesh(image)
        return image

    def _map_letters_to_image(self) -> None:
        """ map letters to image pixels"""
        self._tile_width, self._tile_height = self.get_tile_size()
        tile_center = self._get_first_tile_center()
        x_start = tile_center[0]

        for item, value in self.mapping.items():
            self.mapping.update({item: [tile_center[0], tile_center[1]]})
            if self.width - self._tile_width < tile_center[0] + self._tile_width/2:
                tile_center[0] = x_start
                tile_center[1] += self._tile_height
            else:
                tile_center[0] += self._tile_width

    def _draw_mesh(self, background: PIL_Image) -> PIL_Image:
        """ draw mesh on existing image based on mapping """
        draw = ImageDraw.Draw(background)
        for item, value in self.mapping.items():
            draw.text(value, item, self.mesh_color, font=self.font)
            half_tile = self._tile_width/2
            draw.rectangle(
                (value[0]-half_tile,  value[1]-half_tile,
                 value[0]+half_tile, value[1]+half_tile),
                outline=self.mesh_color, width=1)
        return background

    def _get_first_tile_center(self) -> tuple[int, int]:
        """ return center of the first tile """
        return [item/2 for item in self.get_tile_size()]

    def get_tile_size(self) -> tuple[int, int]:
        """ return one tile size. Tile is a 1x1 square field inside image
        defing one letter of schema letters """
        tile_width = math.floor(self.width/self.num_of_colums)
        tile_height = tile_width
        return (tile_width, tile_height)

    def get_height(self) -> int:
        return self._height

    @property
    def width(self) -> int:
        return self._width

    @property
    def num_of_colums(self) -> int:
        return self._num_of_colums

    @property
    def with_mesh(self) -> bool:
        return self._with_mesh

    @property
    def color(self) -> bool:
        return self._color

    @property
    def mesh_color(self) -> str:
        return self._mesh_color

    def _validate_hex(self, value: str) -> bool:
        if not isinstance(value, str) or not re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', value):
            raise ValueError('Please provide color in correct hex format')

    @color.setter
    def color(self, value) -> bool:
        self._validate_hex(value)
        self._color = value

    @mesh_color.setter
    def mesh_color(self, value) -> bool:
        self._validate_hex(value)
        self._mesh_color = value

    @width.setter
    def width(self, value) -> None:
        max_width = 5616
        try:
            value = int(value)
        except ValueError:
            raise ValueError('Width of the image must be a number')
        if value > max_width:
            raise ValueError(f'Width cannot be greater then {max_width}')
        self._width = value

    @num_of_colums.setter
    def num_of_colums(self, value) -> int:
        try:
            value = int(value)
        except ValueError:
            raise ValueError('Num of columns must must be a number')
        if not 0 < value < self.schema.get_length():
            raise ValueError(
                f'Number of columns must be a value between 0 and {self.schema.get_length()}')
        self._num_of_colums = value

    @with_mesh.setter
    def with_mesh(self, value) -> None:
        try:
            value = bool(int(value))
        except ValueError:
            raise ValueError('Must be True or False')
        self._with_mesh = value


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
        self.color = color
        self.start_line_width = start_line_width

    def _calculate_line_width(self) -> int:
        """ calculate line width based on image width """
        return self.image.width//1000

    def draw(self) -> None:
        """ generate lines on given image based on provided parameters """
        draw = ImageDraw.Draw(self.image)
        mapping = self.background.mapping
        existing_letter_pairs = {}
        for i, value in enumerate(self.text):
            if i == len(self.text) - 1:
                break
            if any([self.text[i] == ' ', self.text[i+1] == ' ']):
                continue
            line_start_point = mapping[value.lower()]
            line_end_point = mapping[self.text[i+1].lower()]
            pair = self.text[i] + self.text[i+1]
            if pair in list(existing_letter_pairs.keys()):
                existing_letter_pairs.update(
                    {pair: existing_letter_pairs[pair] + self.start_line_width*2})
                width = existing_letter_pairs[pair]
            elif pair[::-1] in list(existing_letter_pairs.keys()):
                existing_letter_pairs.update(
                    {pair[::-1]: existing_letter_pairs[pair[::-1]] + self.start_line_width*2})
                width = existing_letter_pairs[pair[::-1]]
            else:
                existing_letter_pairs.update({pair: 1})
                width = self.start_line_width
            draw.line((line_start_point[0], line_start_point[1], line_end_point[0],
                       line_end_point[1]), fill=self.color, width=width)
        return self.image

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
        for char in value.replace(' ', ''):
            if char.lower() not in self.schema.get_letters():
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
