from flask import Flask,render_template,redirect,url_for,session,flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail,Message
from wtforms import StringField , SubmitField
from wtforms.validators import DataRequired
from threading import Thread
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SECRET_KEY"] = "HARD TO GUEESS STRING"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir,"data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#Mail configuration
app.config["FLASKY_ADMIN"] = "diego269707@gmail.com"
app.config["FLASKY_MAIL_SUBJECT_PREFIX"] = "[Flasky]"
app.config["FLASKY_MAIL_SENDER"] = "Flasky Admin <diego269707@gmail.com>"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "your email"
app.config["MAIL_PASSWORD"] = "yor password"

mail = Mail(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app,db)


def send_asyn_email(app,msg):
	with app.app_context():
		mail.send(msg)


def send_email(to,subject,template,**kwargs):
	msg = Message(app.config["FLASKY_MAIL_SUBJECT_PREFIX"]+subject,sender=app.config["FLASKY_MAIL_SENDER"],recipients=[to])
	msg.body = render_template(template+".txt",**kwargs)
	msg.html = render_template(template+".html",**kwargs)
	thread = Thread(target=send_asyn_email, args=[app,msg])
	thread.start()
	return thread


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

		#query in database filter by username
		user = User.query.filter_by(username=form.name.data).first()

		#if the username doesn't exist
		#then add to the database
		if user is None:
			user = User(username=form.name.data)
			db.session.add(user)
			#db.session.commit()
			session["known"] = False
			if app.config["FLASKY_ADMIN"]:
				send_email(app.config["FLASKY_ADMIN"],"New User","mail/new_user",user=user)
		#else session["known"] is True
		else:
			session["known"] = True
		session["name"] = form.name.data
		form.name.data = ""
		return redirect(url_for("index"))
	return render_template('index.html',form=form,name=session.get("name"),known=session.get("known",False))


@app.route('/user/<name>')
def user(name):
	return render_template('user.html',name=name)


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'),404


@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'),500

@app.shell_context_processor
def make_shell_context():
	return dict(db=db,User=User,Role=Role)


if __name__ == "__main__":
	app.run(debug=True)