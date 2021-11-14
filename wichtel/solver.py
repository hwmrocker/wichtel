import random
from typing import Optional

from .config import settings
from .participants import Participant, ParticipantDict, ResultDict


def shuffel(participants: ParticipantDict) -> Optional[ResultDict]:
    result: ResultDict = dict()
    todo = dict(**participants)
    selected_givers: list[str] = []
    possible_givers: list[Participant] = [
        participant for participant in participants.values()
    ]

    while todo:
        receipient = todo.pop(random.choice(list(todo.keys())))

        possible_givers_for_receipient = [
            giver
            for giver in possible_givers
            if giver.name not in selected_givers
            and giver.name not in receipient.avoid
            and receipient.name != giver.name
            and result.get(receipient) != giver
        ]
        if not possible_givers_for_receipient:
            print(":( no giver found")
            return None

        giver = random.choice(possible_givers_for_receipient)
        selected_givers.append(giver.name)
        result[giver] = receipient

    return result


def solve(participant_dict: ParticipantDict) -> ResultDict:
    for i in range(10):
        if result := shuffel(participant_dict):
            break
        print("no result, trying again")
    else:
        raise Exception(f"No solution found after 10 tries.")

    return result


def verify(partipant_dict: ParticipantDict, result: ResultDict) -> bool:
    participants = {p for p in partipant_dict.keys()}
    giver = {p.name for p in result.keys()}
    receiver = {p.name for p in result.values()}

    assert participants == giver == receiver, f"{participants=} {giver=} {receiver=}"
    for g, r in result.items():
        assert r.name not in g.avoid, f"{g.name} should not gift to {r.name}"

    return True
