from flask import Flask,render_template,redirect,url_for,session,flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField , SubmitField
from wtforms.validators import DataRequired
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SECRET_KEY"] = "HARD TO GUEESS STRING"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir,"data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


class NameForm(FlaskForm):
	name = StringField("What is your name?" , validators=[DataRequired()])
	submit = SubmitField("Submit")


class Role(db.Model):
	__tablename__ = "roles"
	id = db.Column(db.Integer , primary_key=True)
	name = db.Column(db.String(64) , unique=True)

	users = db.relationship("User" , backref="role" , lazy="dynamic")

	def __repr__(self):
		return f"<Role {self.name}>"


class User(db.Model):
	__tablename__ = "users"
	id = db.Column(db.Integer , primary_key=True)
	username = db.Column(db.String(64),unique=True,index=True)

	role_id = db.Column(db.Integer,db.ForeignKey("roles.id"))

	def __repr__(self):
		return f"<User {self.username}>"



@app.route('/' , methods=["GET","POST"])
def index():
	form = NameForm()

	#if form is submitted
	if form.validate_on_submit():
		old_name = session.get("name")
		if old_name is not None and old_name != form.name.data:
			flash("Looks like you have changed your name!")
		session["name"] = form.name.data
		return redirect(url_for("index"))
	return render_template('index.html',form=form,name=session.get("name"))


@app.route('/user/<name>')
def user(name):
	return render_template('user.html',name=name)


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'),404


@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'),500


app.run(debug=True)