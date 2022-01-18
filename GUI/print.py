import subprocess
import os


class Printer:
    def __init__(self, path_to_file: str):
        self.path = path_to_file
        self.default_printer = self.get_default_printer()

    def print(self) -> None:
        print(self.path)
        print(self.default_printer)
        os.system(f"lpr -P {self.default_printer} {self.path}")

    def get_default_printer(self) -> str:
        return subprocess.getoutput("lpstat -d").split(": ")[1]
