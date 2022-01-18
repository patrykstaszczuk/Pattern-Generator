import os
import datetime
import sys

from PIL import Image

from pattern_generator import Pattern
from pattern_generator import ImageBackground
from settings import ImageSettings


class ImageExporter:
    def __init__(
            self,
            resolution: tuple,
            name: str,
            background: ImageBackground,
            settings: ImageSettings,
            pattern: Pattern,
            ) -> None:
        self.resolution = resolution
        self.name = name
        self.background = background
        self.settings = settings
        self.pattern = pattern

    def save(self, path: str) -> None:
        pattern_obj = self.get_resized_pattern_object()
        image = pattern_obj.get_printable_version()
        image.save(path, quality=100)

    def get_resized_pattern_object(self) -> Image:
        new_background = ImageBackground(
            width=self.resolution[0],
            schema=self.background.schema,
            with_mesh=self.background.with_mesh,
            mesh_color=self.background.mesh_color,
            num_of_columns=self.background.num_of_colums,
            color=self.background.color,
            )

        return Pattern(
            background=new_background,
            image=new_background.generate_image_background(),
            schema=new_background.schema,
            start_line_width=self.settings.pattern_line_width.get(),
            color=self.settings.pattern_line_color.get(),
            text=self.pattern.text,
        )

    def prepare_path(self) -> str:
        root_path = os.path.dirname(sys.argv[0])
        folder_name = f'Patterns-{datetime.date.today()}'
        path = f'{root_path}/{folder_name}/'
        if not os.path.exists(path):
            os.mkdir(path)

        path = path + self.name
        ext = '.jpg'
        full_path = path + ext

        if os.path.exists(full_path):
            counter = 1
            while os.path.exists(path + str(counter) + ext) and counter < 30:
                counter += 1
            if counter == 31:
                raise RuntimeError(
                    f'Max number of files with name {self.name} reached')
            self.name = self.name+str(counter)
            full_path = path + str(counter) + ext
        return full_path
