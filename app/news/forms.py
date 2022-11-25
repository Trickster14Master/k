from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class NewsCreateForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    body = TextAreaField('Содержимое', validators=[DataRequired()])
    submit = SubmitField('Создать запись')
