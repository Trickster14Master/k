from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class StartParserForm(FlaskForm):
    start_link = StringField("Старая ссылка", validators=[DataRequired()])
    count = IntegerField("Количество ссылок (не более 100 за раз)", default=1)
    submit = SubmitField("Запуск")