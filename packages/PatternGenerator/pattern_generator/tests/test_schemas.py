from pattern_generator.schemas import SimplePolishSchema
import pytest


def test_name_of_SimplePolishSchema() -> None:
    schema = SimplePolishSchema()
    assert schema.name == 'Polish Schema'


def test_get_letters_method() -> None:
    schema = SimplePolishSchema()
    assert isinstance(schema.get_letters(), list)


def test_get_mapping_method() -> None:
    schema = SimplePolishSchema()
    assert isinstance(schema.get_mapping(), dict)
    assert all(True for value in schema.get_mapping().values()
               if value == (0, 0))


def test_setting_new_mapping_success() -> None:
    schema = SimplePolishSchema()
    new_mapping = schema.get_mapping()
    new_mapping['a'] == 'test'
    schema.set_mapping(new_mapping)
    assert schema.get_mapping() == new_mapping


def test_settings_new_mapping_incorrect_type_raise_error() -> None:
    schema = SimplePolishSchema()
    with pytest.raises(TypeError):
        schema.set_mapping([])


def test_setting_new_mapping_different_length_raise_error() -> None:
    schema = SimplePolishSchema()
    with pytest.raises(ValueError):
        schema.set_mapping({'a': 0})


def test_get_length_methods() -> None:
    schema = SimplePolishSchema()
    assert schema.get_length() == len(schema.get_letters())
