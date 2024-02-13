from flask import Blueprint, Flask

slidow_bp = Blueprint("slidow", __name__)


@slidow_bp.route("/", methods=("GET",))
def landing_page():
    return "<p> Welcome to slidow!</p>"


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(SECRET_KEY="dev")
    if test_config:
        app.config.from_mapping(test_config)

    app.register_blueprint(slidow_bp)
    return app
