from . import db
from flask_login import UserMixin

class Ord(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(100), unique=False)
    cost = db.Column(db.String(100))