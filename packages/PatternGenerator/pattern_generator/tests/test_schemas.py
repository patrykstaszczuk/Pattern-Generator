from pattern_generator.schemas import SimplePolishSchema
import pytest


def test_name_of_SimplePolishSchema() -> None:
    schema = SimplePolishSchema()
    assert schema.name == 'Polish Schema'


def test_get_letters_method() -> None:
    schema = SimplePolishSchema()
    assert isinstance(schema.get_letters(), list)


def test_get_length_methods() -> None:
    schema = SimplePolishSchema()
    assert schema.get_length() == len(schema.get_letters())
