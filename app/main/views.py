from flask import render_template,session,redirect,url_for,current_app
from .. import db
from ..models import User
from . import main
from .forms import NameForm
from ..email import send_email


@main.route("/",methods=["GET", "POST"])
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
			db.session.commit()
			session["known"] = False
			if current_app.config["FLASKY_ADMIN"]:
				send_email(current_app.config['FLASKY_ADMIN'], 'New User',
                           'mail/new_user', user=user)
		#else session["known"] is True
		else:
			session["known"] = True
		session["name"] = form.name.data
		form.name.data = ""
		return redirect(url_for(".index"))
	return render_template('index.html',
							form=form,name=session.get("name"),
							known=session.get("known",False))