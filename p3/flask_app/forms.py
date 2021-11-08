from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, NumberRange, Length

class SearchForm(FlaskForm):
    search_query = StringField('Query', validators=[InputRequired(), Length(min=1, max=30)])
    submit = SubmitField('Search')

class MovieReviewForm(FlaskForm):
    name = TextAreaField('name', validators=[InputRequired(), Length(min=1, max=50)])
    text = TextAreaField('text', validators=[InputRequired(), Length(min=1, max=500)])
    submit = SubmitField('Enter Comment')