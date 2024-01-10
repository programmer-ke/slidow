"""The slide-ow app"""
from dataclasses import dataclass

class Event:
    def __init__(self, name: str):
        self.name = name


@dataclass
class Quiz:
    title: str


@dataclass
class Question:
    text: str


@dataclass
class Option:
    text: str
    correct: bool = False
