from enum import unique
from flask_uuid import FlaskUUID
from sqlalchemy.sql.sqltypes import String
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db
from app import login
from flask_login import UserMixin
import uuid
import sqlalchemy.dialects.postgresql as postgresql

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship("Note", backref="author", lazy = "dynamic")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User {}>".format(self.username)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

#Puedes modificar este modelo para las Notas
class Note(db.Model):
    __tablename__="notes"
    id = db.Column(db.Integer,primary_key=True)
    name= db.Column(db.String(120))
    body = db.Column(db.String(280))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    users_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    
    def __repr__(self):
        return "<Post {}>".format(self.body)