"""The slide-ow app domain"""
from dataclasses import dataclass


class Event:
    def __init__(self, name: str):
        self.name = name


@dataclass
class Quiz:
    title: str
    questions: list = None


@dataclass
class Question:
    text: str
    options: list = None


@dataclass
class Option:
    text: str
    correct: bool = False
