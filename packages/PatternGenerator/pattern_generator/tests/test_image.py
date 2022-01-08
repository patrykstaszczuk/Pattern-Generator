import pytest
from unittest.mock import patch, Mock
from pattern_generator.image import ImageBackground, Pattern
from pattern_generator.schemas import SimplePolishSchema, Schema
from PIL.Image import Image as PIL_Image
from PIL import ImageFont
import math


@pytest.fixture()
def schema() -> Schema:
    class TestSchema(SimplePolishSchema):
        name = 'Test Schema'
    return TestSchema()


@pytest.fixture()
def image_params(schema) -> dict:
    return {
        'width': 4000,
        'schema': schema,
        'num_of_colums': 7,
    }


@pytest.fixture()
def background(image_params) -> ImageBackground:
    with patch('PIL.ImageFont.truetype') as mock:
        return ImageBackground(**image_params)


@pytest.fixture()
def pattern_params(background, schema) -> dict:
    return {
        'background': background,
        'image': background.generate_image_background(),
        'schema': schema,
        'text': 'test',
        'start_line_width': 3,
    }


@pytest.fixture()
def pattern(pattern_params) -> Pattern:
    return Pattern(**pattern_params)


@patch('PIL.ImageFont.truetype')
def test_creating_image_instance_success(mock_font, schema) -> None:
    width = 4000
    schema = schema
    num_of_colums = 7
    with_mesh = True

    image = ImageBackground(
        width=width,
        schema=schema,
        num_of_colums=num_of_colums,
        with_mesh=with_mesh,
        )
    assert image.width == width
    assert image.schema == schema
    assert image.num_of_colums == num_of_colums


def test_creating_image_with_invalid_width_raise_exception(image_params) -> None:
    image_params['width'] = 'string'
    with pytest.raises(ValueError):
        ImageBackground(**image_params)


def test_creating_image_with_width_greater_then_max_raise_exception(image_params) -> None:
    image_params['width'] = 5617
    with pytest.raises(ValueError):
        ImageBackground(**image_params)


def test_creating_image_with_invalid_number_of_columns(image_params) -> None:
    image_params['num_of_colums'] = -1
    with pytest.raises(ValueError):
        ImageBackground(**image_params)
    image_params['num_of_colums'] = image_params['schema'].get_length() + 1
    with pytest.raises(ValueError):
        ImageBackground(**image_params)


def test_creating_image_with_non_defaults_background_color(image_params) -> None:
    image_params.update({'color': '#5a5795'})
    image = ImageBackground(**image_params)
    assert image.color == image_params['color']


def test_creating_image_with_invalid_background_color_failed(image_params) -> None:
    image_params.update({'color': 'dsadsadas'})
    with pytest.raises(ValueError):
        ImageBackground(**image_params)
    image_params.update({'color': 1233})
    with pytest.raises(ValueError):
        ImageBackground(**image_params)


def test_creating_image_with_non_default_mesh_color(image_params) -> None:
    image_params.update({'mesh_color': '#5a5795'})
    image = ImageBackground(**image_params)
    assert image.mesh_color == image_params['mesh_color']


def test_creating_image_with_invalid_mesh_color_failed(image_params) -> None:
    image_params.update({'mesh_color': 'dsadsadas'})
    with pytest.raises(ValueError):
        ImageBackground(**image_params)
    image_params.update({'mesh_color': 1233})
    with pytest.raises(ValueError):
        ImageBackground(**image_params)


def test_background_height_should_be_calculated_dynamically(image_params) -> None:
    image_params['num_of_colums'] = 9
    image = ImageBackground(**image_params)

    num_of_columns = image_params['num_of_colums']
    num_of_schema_letters = image.schema.get_length()
    excpected_num_of_rows = math.ceil(num_of_schema_letters/num_of_columns)
    expected_height = excpected_num_of_rows * image.get_tile_size()[1]
    assert image.get_height() == expected_height


def test_getting_proper_width_of_one_tile(background) -> None:
    """ tile is a 1x1 square field inside image defining one letter
    from schema """
    tile_width = round(background.width/background.num_of_colums)
    tile_height = tile_width
    assert background.get_tile_size() == (tile_width, tile_height)


def test_get_PIL_image_object_with_proper_dimensions(background) -> None:
    pil_image = background.generate_image_background()
    assert isinstance(pil_image, PIL_Image)
    assert pil_image.height == background.get_height()
    assert pil_image.width == background.width
    assert pil_image.width == background.width


def test_create_Pattern_instance_success(background, schema) -> None:
    text = 'test'
    start_line_width = 3
    pattern = Pattern(
        background=background,
        image=background.generate_image_background(),
        schema=schema,
        text=text,
        start_line_width=start_line_width,
    )
    assert pattern.image == background.generate_image_background()
    assert pattern.text == text
    assert pattern.start_line_width == start_line_width


def test_create_Pattern_with_invalid_start_line_width_raise_exception(pattern_params) -> None:
    pattern_params['start_line_width'] = -1
    with pytest.raises(ValueError):
        Pattern(**pattern_params)


def test_create_Pattern_with_invalid_chars_in_text_raise_exception(pattern_params) -> None:
    pattern_params['text'] = '123456'
    with pytest.raises(ValueError):
        Pattern(**pattern_params)


def test_create_Patter_with_int_text_raise_exception(pattern_params) -> None:
    pattern_params['text'] = 1234
    with pytest.raises(ValueError):
        Pattern(**pattern_params)


def test_pattern_draw_method(pattern) -> None:
    assert isinstance(pattern.draw(), PIL_Image)


def test_creating_lines_with_non_default_color(pattern_params) -> None:
    pattern_params.update({'color': '#fa1a92'})
    pattern = Pattern(**pattern_params)
    assert pattern.color == pattern_params['color']


def test_GetPrintableVersion_method(pattern_params) -> None:
    pattern = Pattern(**pattern_params)
    default_image = pattern.draw()
    font_size = pattern._calculate_printable_font_size()
    rows_to_be_added = pattern._calculate_nums_of_rows_for_text(font_size)
    new_height = default_image.size[1] + \
        pattern._calculate_extra_space(font_size, rows_to_be_added)
    image = pattern.get_printable_version()
    assert image.size[1] == new_height
    assert image.size[1] == new_height
