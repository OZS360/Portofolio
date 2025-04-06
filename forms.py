from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email

class ContactForm(FlaskForm):
    name = StringField('お名前(必須)', validators=[DataRequired()])
    email = StringField('メールアドレス(必須)', validators=[DataRequired(), Email()])
    title = StringField('件名')
    text = TextAreaField('メッセージ本文(必須)', validators=[DataRequired()])
    submit = SubmitField('送信')
