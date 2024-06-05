from flask import render_template, flash, redirect, url_for
from app import app, db

from flask_login import login_user, logout_user

from app.models.tables import User
from app.models.form import LoginForm

@app.route("/index")
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print(user.password)

        if user and user.password == form.password.data:
            login_user(user)
            flash("Logged in.")
            return redirect(url_for('index'))


        else:
            flash("Invalida login")

    else:
        print(form.errors)
    return render_template('login.html', form=form) 

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/teste/<info>")
@app.route("/teste", defaults={"info": None})
def teste(info):
    usuario = User("airton_silva", "62868642", "Antonio Airton", "aa@mail.com")

    db.session.add(usuario)
    db.session.commit()
    return "OK"

@app.route("/users", methods=["GET"])
def getUsers():
    read_user = User.query.all()
    return read_user
