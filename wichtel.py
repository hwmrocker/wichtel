import random
import sys
from typing import Dict, List, NamedTuple, Optional, Sequence


class Participant(NamedTuple):
    name: str
    avoid: List[str]

    def __hash__(self):
        my_hash = hash(self.name)
        for name in self.avoid:
            my_hash ^= hash(name)
        return my_hash


ResultDict = Dict[Participant, Participant]
ParticipantDict = Dict[str, Participant]

participants = [
    Participant("Rachel", ["Natalie"]),
    Participant("Natalie", ["Rachel"]),
    Participant("Sarah", ["Jenny"]),
    Participant("Jenny", ["Sarah"]),
    Participant("Isabelle", ["Max"]),
    Participant("Max", ["Isabelle"]),
    Participant("Anika", []),
]
participant_dict = dict((e.name, e) for e in participants)
assert len(participants) == len(
    participant_dict
), f"ERR: duplicated key found in participants"


def shuffel(participants: ParticipantDict) -> Optional[ResultDict]:
    result: ResultDict = dict()
    todo = dict(**participants)
    selected_givers: List[str] = []
    possible_givers: List[Participant] = [
        participant for participant in participants.values()
    ]

    while todo:
        # 1. chose random receipient
        receipient = todo.pop(random.choice(list(todo.keys())))

        possible_givers_for_receipient = [
            giver
            for giver in possible_givers
            if giver.name not in selected_givers
            and giver.name not in receipient.avoid
            and receipient.name != giver.name
        ]
        if not possible_givers_for_receipient:
            print(":( no giver found")
            return None

        giver = random.choice(possible_givers_for_receipient)
        selected_givers.append(giver.name)
        result[giver] = receipient

    return result


def main():
    for i in range(10):
        if result := shuffel(participant_dict):
            break
        print("no result, trying again")
    else:
        print(":(")
        return -1
    print(len(result))
    for k, v in result.items():
        print(f"{k.name} -> {v.name}")
    return


if __name__ == "__main__":
    sys.exit(main())
