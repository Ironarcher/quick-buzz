import os
import time
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, render_template, flash, abort, jsonify
from contextlib import closing
import forms
from functools import wraps

#Create the application
app = Flask(__name__)
app.config.update(dict(
	DATABASE=os.path.join(app.root_path, 'pprwork.db'),
	DEBUG=True,
	SECRET_KEY="development key",
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def init_db():
	with closing(connect_db()) as db:
		with app.open_resource("schema.sql", mode="r") as f:
			db.cursor().executescript(f.read())
		db.commit()

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()

def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def createFriendship(friendid):
	userid = getCurrentUserId()
	g.db.execute('insert into friends (frienderId, friendedId) values (?, ?)', [userid, friendid])
	g.db.commit()

def getFriends(userid):
	stack = []
	query1 = query_db('select friendedId from friends where frienderId = ?', userid)
	query2 = query_db('select frienderId from friends where friendedId = ?', userid)

	if query1 is not None:
		for row in query1:
			stack.append(row[0])

	if query2 is not None:
		for row in query2:
			stack.append(row[0])

	return stack

def getUserId(username):
	return query_db('select id from users where username = ?', [username], one=True)[0]

def getCurrentUserId():
	return getUserId(session['username'])

def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if session['logged_in'] is None:
			return redirect(url_for('login'))
		return f(*args, **kwargs)
	return decorated_function

@app.route('/')
def show_entries():
	cur = g.db.execute('select title, text from entries order by id desc')
	entries = [dict(title = row[0], text = row[1]) for row in cur.fetchall()]
	return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)
	g.db.execute('if insert into entries (title, text) values (?, ?)',
		[request.form['title'], request.form['text']])
	g.db.commit()
	flash('New entry was successfully posted')
	return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	form = forms.LoginForm(request.form)
	print(query_db('select password from users where username = ?', [form.username.data], one=True))
	print(form.password.data)
	if request.method == 'POST' and form.validate():
		if query_db('select * from users where username = ?', [form.username.data], one=True) is None:
			error = 'Invalid username'
		elif query_db('select password from users where username = ?', [form.username.data], one=True)[0] != form.password.data:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			session['username'] = form.username.data
			flash('You were logged in')
			return redirect(url_for('show_entries'))
	return render_template('login.html', form=form, error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	session.pop('username', None)
	flash('You were logged out')
	return redirect(url_for('show_entries'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	error = None
	form = forms.RegistrationForm(request.form)
	if request.method == 'POST' and form.validate():
		cur = g.db.execute('select * from users where username = ?', (form.username.data,)).fetchone()
		if cur is not None:
			error = "Username already taken"
		elif form.username.data == "searchbox":
			error = "Invalid username"
		else:
			g.db.execute('insert into users (username, firstname, lastname, password, email) values (?, ?, ?, ?, ?)',
				[form.username.data, form.firstname.data, form.lastname.data, form.password.data, form.email.data])
			g.db.commit()
			flash('Your account has been registered')
			return redirect(url_for('login'))
	return render_template('register.html', form=form, error=error)

@app.route('/search', methods=['GET', 'POST'])
def search():
	userentries = None
	f = request.form
	for key in f.keys():
		for value in f.getlist(key):
			print key,":",value
	if request.method == 'POST':
		print('hi')
		if request.form['submit'] == "Search":
			print('going through')
			query1 = g.db.execute("select username, firstname, lastname from users where username like ?", ('%'+request.form['searchbox']+'%',))
			userentries = [dict(username = row[0], firstname = row[1], lastname = row[2]) for row in query1.fetchall()]
		#elif request.form['submit'] == "Add Friend":
		##	print('hello')
		#	return redirect(url_for('show_entries.html'))
		#else:
		#	print('erroar')
	print('end')
	return render_template('search.html', userentries=userentries)

@login_required
@app.route('/invite', methods=['GET', 'POST'])
def invite():
	form = forms.InviteFriendForm(request.form)
	if request.method == 'POST' and form.validate():
		#Send the email via flask-mail
		flash('Invitation sent!')
	return render_template('invitefriends.html', form=form)

@login_required
@app.route('/sets/add', methods=['GET', 'POST'])
def addsets():
	error = None
	form = forms.SetForm(request.form, public=True)
	if request.method == 'POST' and form.validate():
		if query_db('select * from sets where name = ?', [form.name.data], one=True) is None:
			g.db.execute('insert into sets (creatorId, isPublic, categorytype, name) values (?, ?, ?, ?)',
				[getCurrentUserId(), form.public.data, form.category.data, form.name.data])
			g.db.commit()
			#flash('Your new set has been created')
			newsetid = query_db('select id from sets where name = ?', [form.name.data], one=True)[0]
			redirect(url_for('addquestions', set_id=str(newsetid)))
		else:
			error = "This set's name is already being used. Choose a different name."
	return render_template('addset.html', form=form, error=error)

@login_required
@app.route('/questions/add', methods=['GET', 'POST'])
def addquestions_no_set():
	error = None
	defaulted = False
	userId = getCurrentUserId()
	getallsets = query_db('select * from sets where creatorId = ?', [getCurrentUserId()])
	form = forms.QuestionForm(request.form)
	form.setbox.choices = [(q[0], q[4]) for q in getallsets]
	if request.method == 'POST' and form.validate():
		if request.form['submit'] == "Create new set":
			return redirect(url_for('addsets'))
		elif request.form['submit'] == "Create new question":
			g.db.execute("""insert into questions (creatorId, question, answer, timeallowed, datecreated, ownerset) 
				values (?, ?, ?, ?, ?, ?)""", [userId, form.question.data, form.answer.data, form.time.data, 
				int(time.time()), form.setbox.data])
			g.db.commit()
			flash('Question created')
			return redirect(url_for('addquestions', set_id=str(form.setbox.data)))
		else:
			print('Critical Error')
	return render_template('addquestion.html', form=form, error=error, defaulted=defaulted)

@login_required
@app.route('/questions/add/<int:set_id>', methods=['GET', 'POST'])
def addquestions(set_id):
	error = None
	defaulted = True
	userId = getCurrentUserId()
	getset = query_db('select * from sets where id = ?', [set_id], one=True)
	getallsets = query_db('select * from sets where creatorId = ?', [userId])
	if getset is None:
		print('here')
		return redirect(url_for('addquestions_no_set'))
	else:
		form = forms.QuestionForm(request.form, setbox=getset[0])
	form.setbox.choices = [(q[0], q[4]) for q in getallsets]
	if getset is None:
		#Will never reach this because it will automaticaly redirect
		error = "Set not found"
	elif getset[1] != userId and getset[2] is False:
		error = "Permission not granted"
	else:
		if request.method == "POST" and form.validate():
			if request.form['submit'] == 'Create new set':
				return redirect(url_for('addsets'))
			elif request.form['submit'] == 'Create new question':
				g.db.execute("""insert into questions (creatorId, question, answer, timeallowed, datecreated, ownerset) 
					values (?, ?, ?, ?, ?, ?)""", [userId, form.question.data, form.answer.data, form.time.data, 
					int(time.time()), form.setbox.data])
				g.db.commit()
				print('here')
				return redirect(url_for('addquestions', set_id=str(form.setbox.data)))
			else:
				print('Critical error')
	return render_template('addquestion.html', form=form, error=error, defaulted=defaulted, currentset=getset[0])

if __name__ == "__main__":
	app.run()