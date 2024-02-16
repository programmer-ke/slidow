import typing

from slidow import models
from slidow.adapters.repos import AbstractRepo


def add_event(event_name: str, session: typing.Any, repo: AbstractRepo) -> models.Event:
    """Adds a new event

    Given an event name, generate a unique id as its identifier
    and save it to the repository"""

    event = models.Event.with_random_identifier(event_name)
    repo.add(event)
    session.commit()
    return event
