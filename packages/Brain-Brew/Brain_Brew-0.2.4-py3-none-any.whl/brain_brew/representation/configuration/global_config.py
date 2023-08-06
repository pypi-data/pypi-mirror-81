from dataclasses import dataclass, field
from typing import Union, Optional

from brain_brew.representation.build_config.representation_base import RepresentationBase
from brain_brew.representation.yaml.my_yaml import YamlRepr


@dataclass
class GlobalConfig(YamlRepr):
    __instance = None

    @dataclass
    class Representation(RepresentationBase):
        media_files_location: str
        sort_case_insensitive: Optional[bool] = field(default=False)
        join_values_with: Optional[str] = field(default=" ")

    sort_case_insensitive: bool
    join_values_with: str
    media_files_location: str

    @classmethod
    def from_repr(cls, data: Union[Representation, dict]):
        rep: cls.Representation = data if isinstance(data, cls.Representation) else cls.Representation.from_dict(data)
        return cls(
            media_files_location=rep.media_files_location,
            sort_case_insensitive=rep.sort_case_insensitive,
            join_values_with=rep.join_values_with
        )

    def __post_init__(self):
        if GlobalConfig.__instance is None:
            GlobalConfig.__instance = self
        else:
            raise Exception("Multiple GlobalConfigs created")

    @classmethod
    def from_file(cls, filename: str = "brain_brew_config.yaml"):
        return cls.from_repr(cls.read_to_dict(filename))

    @classmethod
    def get_instance(cls) -> 'GlobalConfig':
        return cls.__instance

    @classmethod
    def clear_instance(cls):
        if cls.__instance:
            cls.__instance = None
