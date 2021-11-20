from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

from pattern_generator import (
    SimplePolishSchema,
    Schema,
    ImageBackground,
    Pattern
    )
from pydantic import BaseModel

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Background(BaseModel):
    width: int
    use_schema: str
    num_of_colums: int
    color: str
    with_mesh: bool


class PatternModel(BaseModel):
    text: str
    color: str
    start_line_width: int


@app.get("/")
async def index():
    routes = [{"path": route.path, "name": route.name} for route in app.routes]
    return routes


@app.get("/schemas")
async def schemas():
    available_schemas = {
        'schemas': ['SimplePolishSchema', ]}
    return available_schemas


@app.post("/create-pattern", response_class=FileResponse, status_code=201)
async def background(background: Background, pattern: PatternModel):

    schema = SimplePolishSchema()

    image_background = ImageBackground(
        width=background.width,
        schema=schema,
        num_of_colums=background.num_of_colums,
        color=background.color,
        with_mesh=background.with_mesh
    )

    image_background_path = os.path.dirname(os.path.realpath(
        __file__)) + "/media/background.jpg"
    pil_image = image_background.generate_image_background()
    pil_image.save(image_background_path, quality=100)

    pattern = Pattern(
        image=pil_image,
        schema=image_background.schema,
        text=pattern.text,
        color=pattern.color,
        start_line_width=pattern.start_line_width,
    )
    pattern_image = pattern.draw()
    pattern_image_path = os.path.dirname(os.path.realpath(
        __file__)) + "/media/pattern.jpg"
    pattern_image.save(pattern_image_path, quality=100)
    return pattern_image_path
