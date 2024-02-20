import typing

from .. import models
from ..adapters.repos import AbstractRepo
from . import unit_of_work


class InvalidEventNameError(ValueError):
    def __init__(self, arg: object) -> None:
        self.msg = f"Invalid Event Name: {arg}"


def add_event(event_name: str, uow: unit_of_work.AbstractUOW) -> str:
    """Adds a new event

    Given an event name, generate a unique id as its identifier
    and save it to the repository"""
    if len(event_name) == 0:
        raise InvalidEventNameError(event_name)
    with uow:
        event = models.Event.with_random_identifier(event_name)
        uow.events.add(event)
        uow.commit()
    return event.identifier


def get_events(repo: AbstractRepo) -> list[tuple]:
    return [(event.identifier, event.name) for event in repo.list()]
