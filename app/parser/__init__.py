from flask import Blueprint

bp = Blueprint('parser', __name__, url_prefix='/parser')

from app.parser import routes  # noqa
