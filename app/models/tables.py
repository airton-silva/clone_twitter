from app import db
# from sqlalchemy import Column, Integer, String


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    name = db.Column(db.String)
    password = db.Column(db.String)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, password, name, email):
        self.username = username
        self.password = password
        self.name = name
        self.email = email

    def __repr__(self):
        return f'<User {self.name!r}>'
    

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', foreign_keys=user_id)

    def __init__ (self, content, user_id):
        self.content = content
        self.user_id =user_id

    def __repr__(self) -> str:
        return f'<Post %r >' % self.id
    
class Follow(db.Model):
    __tablename__ = "follow"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    user = db.relationship('User', foreign_keys=user_id)
    user = db.relationship('Post', foreign_keys=post_id)

    def __init__ (self, user_id, post_id):
        self.user_id = user_id
        self.post_id =post_id

    def __repr__(self) -> str:
        return f'<Post %r >' % self.id