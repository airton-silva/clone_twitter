import os
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from werkzeug.utils import secure_filename

from flask_login import login_user, logout_user, current_user, login_required

from app.models.tables import User, Post
from app.models.form import LoginForm, UserForm, UserFormUpdate, PostForm

@app.route("/index")
@app.route("/")
def index():
    read_users = User.query.all()
    read_posts = Post.query.all()
    form = PostForm()
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        return render_template('index.html', users=read_users, posts=read_posts, form=form)

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
        usuario = User(form.username.data, form.name.data, form.password.data, form.email.data,'')
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
    # form = UploadForm()
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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

@app.route('/upload/<int:id>', methods=['GET', 'POST'])
def upload_file(id):
    user = db.get_or_404(User, id)
    if request.method == 'POST' and user:
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # Obtém o caminho relativo
            relative_path = os.path.relpath(path, app.config['BASE_FOLDER_STATIC'])
            
            # Debugging prints
            print(f"UPLOAD_FOLDER: {app.config['UPLOAD_FOLDER']}")
            print(f"Filename: {filename}")
            print(f"Path: {relative_path}")
            
            file.save(path)
            user.image_url = relative_path
            db.session.add(user)
            db.session.commit()

            print("File saved.")
            return redirect(url_for('user_detail', id=id))
    else:
        return redirect(url_for('user_detail', id=id))
    return


@app.route("/posts", methods=["GET"])
def show_post():
    read_posts = Post.query.all()
    return render_template("index.html", users=read_posts)

@app.route("/post/create", methods=["GET", "POST"])
def create_post():

    form = PostForm()
    if form.validate_on_submit():
        post = Post(form.content.data, current_user.id)
        db.session.add(post)
        db.session.commit()

        flash("Tweeter criado com sucesso.", "success")
        return redirect(url_for('index.html'))

    else:
        print(form.errors)
    return render_template('user/form.html', form=form) 

@app.route("/post/<int:id>/delete", methods=["GET", "POST"])
@login_required
def user_post(id):
    post = db.get_or_404(Post, id)

    # request.method == "POST"
    if  current_user.id == post.user_id:
        db.session.delete(post)
        db.session.commit()
        flash("Post deletado com sucesso.", "success")
        return redirect(url_for('/'))
    else:
        return "<h1>Post não Autorizado</h1>"