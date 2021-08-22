from flask import Flask,render_template,redirect,url_for,session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField , SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config["SECRET_KEY"] = "HARD TO GUEESS STRING"

bootstrap = Bootstrap(app)


class NameForm(FlaskForm):
	name = StringField("What is your name?" , validators=[DataRequired()])
	submit = SubmitField("Submit")





@app.route('/' , methods=["GET","POST"])
def index():
	name = None
	form = NameForm()

	#if form is submitted
	if form.validate_on_submit():
		name = form.name.data
		form.name.data = ""
	return render_template('index.html',form=form,name=name)


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