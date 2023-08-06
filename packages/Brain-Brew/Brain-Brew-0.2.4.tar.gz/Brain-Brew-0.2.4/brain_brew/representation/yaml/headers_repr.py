from dataclasses import dataclass

from brain_brew.representation.json.wrappers_for_crowd_anki import CA_NAME
from brain_brew.representation.yaml.my_yaml import YamlRepr


@dataclass
class Headers(YamlRepr):
    data: dict

    @classmethod
    def from_file(cls, filename: str):
        return cls(data=cls.read_to_dict(filename))

    def encode(self) -> dict:
        return self.data

    @property
    def name(self) -> str:
        return self.data[CA_NAME]

    @property
    def data_without_name(self) -> dict:
        return {k: v for k, v in self.data.items() if k != CA_NAME}
