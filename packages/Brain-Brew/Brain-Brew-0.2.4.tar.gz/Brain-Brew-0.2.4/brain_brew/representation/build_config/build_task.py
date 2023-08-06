import logging
from typing import Dict, List, Type

from brain_brew.utils import str_to_lowercase_no_separators


class BuildTask(object):
    task_regex: str

    def execute(self):
        raise NotImplemented()

    @classmethod
    def from_repr(cls, data: dict):
        raise NotImplemented()

    @classmethod
    def get_all_task_regex(cls) -> Dict[str, Type['BuildTask']]:
        subclasses: List[Type[BuildTask]] = cls.__subclasses__()
        task_regex_matches: Dict[str, Type[BuildTask]] = {}

        for sc in subclasses:
            if sc.task_regex in task_regex_matches:
                raise KeyError(f"Multiple instances of task regex '{sc.task_regex}'")
            elif sc.task_regex == "" or sc.task_regex is None:
                raise KeyError(f"Unknown task regex {sc.task_regex}")

            task_regex_matches.setdefault(sc.task_regex, sc)

        # logging.debug(f"Known build tasks: {known_build_tasks}")
        return task_regex_matches


class TopLevelBuildTask(BuildTask):
    @classmethod
    def get_all_task_regex(cls) -> Dict[str, Type['BuildTask']]:
        return super(TopLevelBuildTask, cls).get_all_task_regex()


class DeckPartBuildTask(BuildTask):
    @classmethod
    def get_all_task_regex(cls) -> Dict[str, Type['BuildTask']]:
        return super(DeckPartBuildTask, cls).get_all_task_regex()
