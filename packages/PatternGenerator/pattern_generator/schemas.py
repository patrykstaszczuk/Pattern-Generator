from dataclasses import dataclass, field
from abc import ABC, abstractmethod


class Schema(ABC):

    @abstractmethod
    def get_letters(self) -> dict:
        pass

    @abstractmethod
    def get_length(self) -> int:
        pass


@dataclass
class SimplePolishSchema(Schema):

    def __init__(
        self,
    ) -> None:
        self.name = 'Polish Schema'
        self.letters = [
            'a', 'ą', 'b', 'c', 'ć', 'd', 'e', 'ę',
            'f', 'g', 'h', 'i', 'j', 'k', 'l', 'ł',
            'm', 'n', 'ń', 'o', 'ó', 'p', 'q', 'r',
            's', 'ś', 't', 'u', 'v', 'w', 'x', 'y',
            'z', 'ź', 'ż']
        self.mapping = None

    def get_letters(self) -> list:
        """ return all letters of schema in default order """
        return self.letters

    # def get_mapping(self) -> dict:
    #     """ return current mapping or create default one """
    #     if self.mapping is None:
    #         return {item: (0, 0) for item in self.letters}
    #     return self.mapping

    # def set_mapping(self, new_mapping: dict) -> None:
    #     """ set new mapping """
    #     if not isinstance(new_mapping, dict):
    #         raise TypeError('New mapping has to be dict type')
    #     if len(new_mapping) != len(self.letters):
    #         raise ValueError(
    #             'New mapping must map all the letters of schema. Must be same lentgth')
    #     self.mapping = new_mapping

    def get_length(self):
        """ retrun length of schema """
        return len(self.get_letters())
