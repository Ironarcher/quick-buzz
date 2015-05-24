from wtforms import Form, TextField, PasswordField, validators
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


