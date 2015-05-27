from wtforms import Form, TextField, PasswordField, SelectField, IntegerField, BooleanField, validators
from wtforms.widgets import TextArea

class RegistrationForm(Form):
	username = TextField('Username', [
		validators.Length(min=4, max=20),
		validators.Required()])
	firstname = TextField('First Name', [
		validators.Length(max=50)])
	lastname = TextField('Last Name', [
		validators.Length(max=50)])
	password = PasswordField('New Password', [
		validators.Required(),
		validators.EqualTo('confirm', message='Passwords must match'),
		validators.Length(min=8, max=50)])
	confirm = PasswordField('Repeat Password')
	email = TextField('Email Address', [
		validators.Length(min=6, max=35),
		validators.Required(),
		validators.Email()])

class LoginForm(Form):
	username = TextField('Username', [validators.Required()])
	password = PasswordField('New Password', [validators.Required()])

class FindFriendForm(Form):
	username = TextField("Friend's Username", [validators.Required()])

class InviteFriendForm(Form):
	email = TextField('E-mail Address', [validators.Required(),
		validators.Email()])	
	message = TextField('Message', widget=TextArea())

class SearchForm(Form):
	searchbox = TextField('Search', validators.Required())

class QuestionForm(Form):
	setbox = SelectField('Set Used', coerce=int)
	question = TextField('Question', widget=TextArea())
	answer = TextField('Answer')
	time = IntegerField('Answering time',
		[validators.NumberRange(min=5, max=60, message='The answering time must be between %(min)d and %(max)d seconds')],
		default=15)

class SetForm(Form):
	name = TextField('Name', [validators.Required(),
		validators.Length(min=6, max=50)])
	public = BooleanField('Public?')
	category = SelectField('Category', choices=[('history', 'History'), ('science', 'Science')])
