from flask import Blueprint

bp = Blueprint('news', __name__, url_prefix='/news')

from app.news import routes
