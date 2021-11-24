from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from .main import app


client = TestClient(app)


def test_getting_available_schemas() -> None:
    response = client.get("/schemas")
    assert response.status_code == 200
    assert response.json() == {'schemas': ['SimplePolishSchema', ]}


def test_creating_background_success() -> None:
    params = {
        'background': {
            'width': 4000,
            'use_schema': 'SimplePolishSchema',
            'num_of_colums': 7,
            'color': '#FFFFFF',
            'with_mesh': True,
            },
        'pattern': {
            'text': 'Test Test',
            'color': '#000000',
            'start_line_width': 0,
        }}
    with patch('pattern_generator.image', 'ImageBackground') as mock:
        response = client.post(
            "/create-pattern",
            json=params,
            )
        assert response.status_code == 201
        assert type(response.content) == bytes
        assert False
