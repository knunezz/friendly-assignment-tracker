from . import db
from flask_login import UserMixin

# Stores information about each assignment a user creates.
class Assignment(db.Model):
    # Unique column ID for each assignment and primary_key makes it their identifyer
    id = db.Column(db.Integer, primary_key=True)
            #the db.column creates a new column on each category(aka a new column in courses or title.) 
                        #the number here shows the max length of the string
    course = db.Column(db.String(100))
    title = db.Column(db.String(200))
    due_date = db.Column(db.Date)
    # Tracks whether the assignment has been completed.
    completed = db.Column(
        db.Boolean,
        default=False
    )

    user_id = db.Column(
        db.Integer, 
        # Foreign key connects an assignment to a user.
        db.ForeignKey('user.id')
    )

# Stores account information for each user.
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    # Creates a connection between users and assignments.
    assignments = db.relationship('Assignment')