from datetime import datetime
from database import db  # Import db from database.py
from flask_login import UserMixin
class BMIRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bmi = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)  # New field
    height = db.Column(db.Float, nullable=False)  # New field
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<BMIRecord {self.bmi} on {self.date}>'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
