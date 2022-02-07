import subprocess
import os
import platform
from abc import ABC, abstractmethod


class Printer(ABC):

    @abstractmethod
    def print(self) -> None:
        pass

    @abstractmethod
    def get_default_printer(self) -> str:
        pass


class MacPrinter(Printer):
    def __init__(self, path_to_file: str):
        self.path = path_to_file
        self.default_printer = self.get_default_printer()

    def print(self) -> None:
        os.system(f"lpr -P {self.default_printer} {self.path}")

    def get_default_printer(self) -> str:
        try:
            return subprocess.getoutput("lpstat -d").split(": ")[1]
        except KeyError:
            raise KeyError(
                'No default printer founded. Add printer and try again')


class WinPrinter(Printer):
    def __init__(self, path_to_file: str):
        self.path = path_to_file
        self.default_printer = self.get_default_printer()

    def print(self) -> None:
        pass

    def get_default_printer(self) -> str:
        pass


class PrinterManager:
    def __init__(self, path_to_file: str):
        self.printer = self._get_os_specific_print_instance(path_to_file)

    def _get_os_specific_print_instance(self, path_to_file: str) -> Printer:
        if platform.system() == 'Darwin':
            return MacPrinter(path_to_file)
        elif platform.system() == 'Windows':
            return WinPrinter(path_to_file)
        else:
            raise NotImplementedError(
                'Printing is not yet supported on Linux systems')
