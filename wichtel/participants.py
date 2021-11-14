from pathlib import Path
from typing import Optional, TypedDict, cast

import yaml
from pydantic import BaseModel

from .config import settings


class Participant(BaseModel):
    name: str
    avoid: list[str] = []
    email: Optional[str] = None

    def __hash__(self):
        my_hash = hash(self.name)
        for name in self.avoid:
            my_hash ^= hash(name)
        return my_hash


class RawParticipant(TypedDict):
    name: str
    avoid: list[str]
    email: Optional[str]


ParticipantDict = dict[str, Participant]
ResultDict = dict[Participant, Participant]


def load_participants(filename: Path) -> ParticipantDict:
    with open(filename, "r") as stream:
        participants = cast(list[RawParticipant], yaml.safe_load(stream))
        if participants is None:
            raise ValueError("empty input file")

    participants_dict = {}
    for participant in participants:
        participants_dict[participant["name"]] = Participant(**participant)
    if len(participants_dict) != len(participants):
        from collections import Counter

        c = Counter([p["name"] for p in participants])
        duplicates = [duplicate for duplicate, count in c.most_common() if count > 1]
        raise ValueError(
            f"Duplicate names in input. The following names are duplicated {duplicates}"
        )
    return participants_dict
