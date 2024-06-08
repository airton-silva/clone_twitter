from flask import render_template, flash, redirect, url_for, request
from app import app, db

from flask_login import login_user, logout_user, current_user, login_required

from app.models.tables import User, Post
from app.models.form import LoginForm, UserForm, UserFormUpdate, PostForm

@app.route("/index")
@app.route("/")
def index():
    read_users = User.query.all()
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        return render_template('index.html', users=read_users)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # print(user.password)

        if user and user.password == form.password.data:
            login_user(user)
            flash("Logged in.", "success")
            return redirect(url_for('index'))


        else:
            flash("Usuário ou Senha Inválidos", "error")

    else:
        print(form.errors)
    return render_template('login.html', form=form) 

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

# @app.route("/user")
@app.route("/user/create", methods=["GET", "POST"])
def create_user():

    form = UserForm()
    if form.validate_on_submit():
        usuario = User(form.name.data, form.username.data, form.password.data, form.email.data)
        db.session.add(usuario)
        db.session.commit()

        flash("Usuário criado com sucesso.", "success")
        return redirect(url_for('login'))

    else:
        print(form.errors)
    return render_template('user/form.html', form=form) 

@app.route("/user/<int:id>")
@login_required
def user_detail(id):
    user = db.get_or_404(User, id)
    if current_user.id != user.id:
        return "<h1>Usuário não Autorizado</h1>"
    else:
        return render_template("user/detail.html", user=user)

@app.route("/user/<int:id>/update", methods=["GET", "POST"])
def update_user(id):
    user = db.get_or_404(User, id)

    form = UserFormUpdate()
    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        user.username = form.username.data
     
        db.session.add(user)
        db.session.commit()

        flash("Usuário atualizado com sucesso.", "success")
        return redirect(url_for('user_detail',id=user.id))

    else:
        print(form.errors)
    return render_template('user/form.html', form=form, user=user) 

@app.route("/user/<int:id>/delete", methods=["GET", "POST"])
@login_required
def user_delete(id):
    user = db.get_or_404(User, id)

    if request.method == "POST" and current_user.id == user.id:
        db.session.delete(user)
        db.session.commit()
        flash("Usuário deletado com sucesso.", "success")
        return redirect(url_for('login'))
    else:
        return "<h1>Usuário não Autorizado</h1>"

    return render_template("user/detail.html", user=user)

@app.route("/users", methods=["GET"])
def getUsers():
    read_user = User.query.all()
    return read_user

@app.route("/new", methods=["GET"])
def newT():
    read_users = User.query.all()
    read_posts = Post.query.all()
    return render_template("new_template/index.html", users=read_users)

@app.route("/posts", methods=["GET"])
def show_post():
    read_posts = Post.query.all()
    return render_template("new_template/index.html", users=read_posts)

@app.route("/post/create", methods=["GET", "POST"])
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        usuario = User(form.content.data)
        db.session.add(usuario)
        db.session.commit()

        flash("Tweeter criado com sucesso.", "success")
        return redirect(url_for('new_template/index.html'))

    else:
        print(form.errors)
    return render_template('user/form.html', form=form) 