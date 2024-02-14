import os

import click
from flask import Blueprint, Flask, current_app, g
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from slidow.adapters import orm, repos

slidow_bp = Blueprint("slidow", __name__)


@slidow_bp.route("/", methods=("GET",))
def root():
    return "<p> Welcome to slidow!</p>"


@slidow_bp.route("/events", methods=("GET",))
def events_list():
    session = get_db_session()
    events_repo = repos.EventSQLAlchemyRepo(session)
    events = events_repo.list()
    return " ".join([event.name for event in events])


def get_db_session():
    if "db_session" not in g:
        Session = current_app.config["DB_SESSION_FACTORY"]
        g.db_session = Session()
    return g.db_session


def close_db(e=None):
    g.pop("db_session", None)
    Session = current_app.config["DB_SESSION_FACTORY"]
    Session.remove()


def init_db():
    Session = get_db_session()
    engine = Session.get_bind()
    orm.mapper_registry.metadata.create_all(engine)


@click.command("init-db")
def init_db_command():
    init_db()
    click.echo("Initialized the DB")


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev", DATABASE=os.path.join(app.instance_path, "slidow-dev.sqlite")
    )
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)
        if db_name := test_config.get("db_name"):
            app.config.from_mapping(DATABASE=os.path.join(app.instance_path, db_name))

    # Create a scoped session factory for use in views
    db_engine = create_engine("sqlite:///" + app.config["DATABASE"])
    Session = scoped_session(sessionmaker(bind=db_engine))
    app.config.from_mapping(DB_SESSION_FACTORY=Session)

    # create instance folder in dev
    try:
        os.makedirs(app.instance_path)
    except OSError:
        ...

    # register callbacks etc..
    app.register_blueprint(slidow_bp)
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    return app