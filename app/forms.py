from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length#,ValidationError
from app.models import Item, Category 
from app.factory import category_query


class EditItemForm(FlaskForm): 


	title = StringField('Title', validators=[DataRequired()])
	description = TextAreaField('Description', validators=[Length(min=0, max=140)])
	opts = QuerySelectField('Category', query_factory=category_query, allow_blank=False, get_label='title')
	submit = SubmitField('Submit')


class DeleteItemForm(FlaskForm):


	submit = SubmitField('Delete')


class AddItemForm(FlaskForm): 


	title = StringField('Title', validators=[DataRequired()])
	description = TextAreaField('Description', validators=[Length(min=0, max=140)])
	opts = QuerySelectField('Category', query_factory=category_query, allow_blank=True, get_label='title')
	submit = SubmitField('Submit') 


class AddCategoryForm(FlaskForm):

	
	title = StringField('Title', validators=[DataRequired()])
	submit = SubmitField('Submit')