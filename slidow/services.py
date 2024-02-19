import typing

from slidow import models
from slidow.adapters.repos import AbstractRepo


class InvalidEventNameError(ValueError):
    def __init__(self, arg: object) -> None:
        self.msg = f"Invalid Event Name: {arg}"


def add_event(event_name: str, session: typing.Any, repo: AbstractRepo) -> str:
    """Adds a new event

    Given an event name, generate a unique id as its identifier
    and save it to the repository"""
    if len(event_name) == 0:
        raise InvalidEventNameError(event_name)
    event = models.Event.with_random_identifier(event_name)
    repo.add(event)
    session.commit()
    return event.identifier
