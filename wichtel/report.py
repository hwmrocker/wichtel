from typing import cast

import httpx

from .config import settings
from .participants import Participant, ResultDict


def printer(result: ResultDict) -> None:
    print("results: ")
    for k, v in result.items():
        print(f"{k.name} -> {v.name}")


def send_mails(result: ResultDict) -> None:
    print("mails: ")

    for k, v in result.items():
        send_mail(k, v)


def send_mail(a: Participant, b: Participant) -> None:
    mail_text = f"""\
    Hallo {a.name.split()[0]},
    
    für dich wurde {b.name} als Wichtelpartner gezogen.
    Bitte kaufe ein Wichtelgeschenk für 10-15€
    """
    if settings.DEBUG:
        print(mail_text)

    # we tested already that the api was provided, we know it is not None at this point
    api_key = cast(str, settings.MAILGUN_API_KEY)
    httpx.post(
        url="https://api.mailgun.net/v3/gladis.org/messages",
        data={
            "from": "Der Weihnachtswichtel <wichtel@gladis.org>",
            "to": a.email,
            "subject": "Weihnachtswichteln 2022",
            "text": mail_text,
        },
        headers={"Authorization": httpx.BasicAuth("api", api_key)._auth_header},
    )
