from app import db, login
from flask_login import UserMixin
from hashlib import md5
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    news = db.relationship('News', backref='author', lazy='dynamic')
    links = db.relationship('Link', backref='author', lazy='dynamic')

    def __repr__(self):
        return 'User: {}'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return '//gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    path = db.Column(db.Text, nullable=False)
    md5h = db.Column(db.String(32), nullable=False)
    is_parsed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    parsed_at = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    page = db.relationship('Page', backref='page', lazy=True, uselist=False)

    def mark_parsed(self, val=True):
        if val:
            self.parsed_at = datetime.utcnow()
        self.is_parsed = bool(val)


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text)
    link_id = db.Column(db.Integer, db.ForeignKey('link.id'))



@login.user_loader
def load_user(id):  # noqa
    return User.query.get(id)
