import os
import math
import re

from PIL import Image as PIL_Image
from PIL import ImageFont, ImageDraw

from pattern_generator.schemas import Schema


class ImageBackground:
    def __init__(
        self,
        width: int,
        schema: Schema,
        num_of_columns: int,
        color: str = '#FFFFFF',
        mesh_color: str = '#000000',
        with_mesh: bool = False,
    ) -> None:
        self.width = width
        self.schema = schema
        self.num_of_colums = num_of_columns
        self.with_mesh = with_mesh
        self.mesh_color = mesh_color
        self.color = color
        self.height = self._calculate_image_height()

        self._tile_width = 0
        self._tile_height = 0
        self.mapping = {item: 0 for item in self.schema.get_letters()}
        dir_path = os.path.dirname(os.path.realpath(__file__))
        font_name = "DejaVuSans.ttf"
        font_path = dir_path + '/fonts/' + font_name
        try:
            font_size = round(self.width/80)
            self.font = ImageFont.truetype(
                f"{font_path}", font_size)
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
                             + 'Height cannot be greater then 65500px. \n'
                             + 'Please decrease width or increase number of letters in one row \n')
        return height_in_px

    def generate_image_background(self) -> PIL_Image:
        """ generate PIL image """
        image = PIL_Image.new(
            'RGB',
            (self.width, self.height),
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
            if self.width - self._tile_width + 1 <= tile_center[0] + self._tile_width/2:
                tile_center[0] = x_start
                tile_center[1] += self._tile_height
            else:
                tile_center[0] += self._tile_width

    def _draw_mesh(self, background: PIL_Image) -> PIL_Image:
        """ draw mesh on existing image based on mapping """
        draw = ImageDraw.Draw(background)
        for item, value in self.mapping.items():
            draw.text(value, item, self.mesh_color, font=self.font)
        return background

    def _get_first_tile_center(self) -> tuple[int, int]:
        """ return center of the first tile """
        return [round(item/2) for item in self.get_tile_size()]

    def get_tile_size(self) -> tuple[int, int]:
        """ return one tile size. Tile is a 1x1 square field inside image
        defing one letter of schema letters """
        tile_width = math.floor(self.width/self.num_of_colums)
        tile_height = tile_width
        return (tile_width, tile_height)

    def get_available_resolutions(self) -> list[str]:
        horizontal = self.width >= self.height
        resolutions = []

        original = f'Current size ({self.width},{self.height})'
        if horizontal:
            a4_300_dpi = f'A4 - 300 DPI ({3508},{self._get_predicted_height(3508)})'
            a3_300_dpi = f'A3 - 300 DPI ({4960},{self._get_predicted_height(4960)})'
            a2_300_dpi = f'A2 - 300 DPI ({7016},{self._get_predicted_height(7016)})'
            a1_300_dpi = f'A1 - 300 DPI ({9933},{self._get_predicted_height(9933)})'
        else:
            a4_300_dpi = f'A4 - 300 DPI ({self._get_predicted_width(3508)},{3508})'
            a3_300_dpi = f'A3 - 300 DPI ({self._get_predicted_width(4960)},{4960})'
            a2_300_dpi = f'A2 - 300 DPI ({self._get_predicted_width(7016)},{7016})'
            a1_300_dpi = f'A1 - 300 DPI ({self._get_predicted_width(9933)},{9933})'

        resolutions.append(original)
        resolutions.append(a4_300_dpi)
        resolutions.append(a3_300_dpi)
        resolutions.append(a2_300_dpi)
        resolutions.append(a1_300_dpi)

        return resolutions

    def _get_predicted_height(self, width: int) -> int:
        num_of_letters = self.schema.get_length()
        num_of_rows = math.ceil(num_of_letters/self.num_of_colums)
        tile_width = math.floor(width/self.num_of_colums)
        height_in_px = num_of_rows * tile_width
        return height_in_px

    def _get_predicted_width(self, height) -> int:
        height_ratio = height/self.height
        return math.floor(self.width * height_ratio)

    def get_height(self) -> int:
        return self.height

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
        max_width = 10000
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
        if not 0 < value <= self.schema.get_length():
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
