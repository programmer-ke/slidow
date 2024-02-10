from sqlalchemy import Boolean, Column, ForeignKey, Integer, Table, Text
from sqlalchemy.orm import registry, relationship

import slidow

mapper_registry = registry()

events_table = Table(
    "event",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("identifier", Text),
    Column("name", Text),
)

quizzes_table = Table(
    "quiz",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("identifier", Text),
    Column("title", Text),
)

event_quiz_table = Table(
    "event_quiz",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("event_id", ForeignKey("event.id")),
    Column("quiz_id", ForeignKey("quiz.id")),
)

questions_table = Table(
    "question",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("quiz_id", Integer, ForeignKey("quiz.id")),
    Column("text", Text),
)

options_table = Table(
    "option",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("question_id", Integer, ForeignKey("question.id")),
    Column("text", Text),
    Column("correct", Boolean),
)

mapper_registry.map_imperatively(
    slidow.Event,
    events_table,
    properties={"quizzes": relationship(slidow.Quiz, secondary=event_quiz_table)},
)

mapper_registry.map_imperatively(
    slidow.Quiz,
    quizzes_table,
    properties={"questions": relationship(slidow.Question, backref="quiz")},
)

mapper_registry.map_imperatively(
    slidow.Question,
    questions_table,
    properties={"options": relationship(slidow.Option, backref="question")},
)

mapper_registry.map_imperatively(
    slidow.Option,
    options_table,
)
