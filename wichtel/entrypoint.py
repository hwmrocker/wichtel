import argparse
import sys
from argparse import Namespace
from pathlib import Path

from .config import settings
from .participants import Participant, ParticipantDict, load_participants
from .report import printer, send_mail, send_mails
from .solver import solve, verify


def get_args(argv: list) -> Namespace:
    """
    Parse the command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="A simple example of a wichtel application."
    )
    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")
    parser.add_argument("--test-mail", action="store")
    parser.add_argument("input", nargs="?")
    return parser.parse_args(argv)


def main(argv: list = None) -> int:
    """
    Main entry point for the application.
    """
    if argv is None:
        argv = sys.argv[1:]
    args = get_args(argv)
    if args.test_mail:
        print(f"sending test email to {args.test_mail}")
        send_mail(
            Participant(
                name="TestUser geb. Foo",
                email=args.test_mail,
            ),
            Participant(
                name="WichtelEmpfänger geb. Foo",
                email="should-not-be-used@gladis.org",
            ),
        )
        return 0

    if args.input is None:
        print("no input file specified")
        return 1

    inputfile = Path(args.input)
    if not inputfile.exists():
        print("Input file does not exist.")
        return 1
    participants: ParticipantDict = load_participants(inputfile)

    if settings.EMAIL:
        participants_without_email = []
        for participant in participants.values():
            if not participant.email:
                participants_without_email.append(participant.name)
        if participants_without_email:
            print(
                f"EMAIL specified, but {', '.join(participants_without_email)} don't have an email address configured"
            )
            return 2

        if not settings.MAILGUN_API_KEY:
            print("EMAIL specified but no MAILGUN_API_KEY not set")
            return 3

    participant_connections = solve(participants)
    if verify(participants, participant_connections):
        if settings.EMAIL:
            send_mails(participant_connections)
        else:
            printer(participant_connections)
        # save(participant_connections)

    return 0
