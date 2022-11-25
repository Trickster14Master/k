from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment

from config import Config

bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
moment = Moment()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initials
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    moment.init_app(app)

    # Blueprint
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.user import bp as user_bp
    app.register_blueprint(user_bp)

    from app.news import bp as news_bp
    app.register_blueprint(news_bp)

    from app.parser import bp as parser_bp
    app.register_blueprint(parser_bp)

    return app


from app import models  # noqa
