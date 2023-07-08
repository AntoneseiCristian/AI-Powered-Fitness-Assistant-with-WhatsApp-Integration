from datetime import datetime
from database import db  # Import db from database.py

class BMIRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bmi = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)  # New date field

    def __repr__(self):
        return f'<BMIRecord {self.bmi} on {self.date}>'
