from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    course = db.Column(db.String(100))
    title = db.Column(db.String(200))
    due_date = db.Column(db.Date)

    completed = db.Column(
        db.Boolean,
        default=False
    )

    user_id = db.Column(
        db.Integer, 
        db.ForeignKey('user.id')
    )

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    assignments = db.relationship('Assignment')