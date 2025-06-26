from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON


db = SQLAlchemy()

class Attendee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    ward = db.Column(db.String(100))
    stake = db.Column(db.String(100))
    registration_id = db.Column(db.String(100), unique=True, nullable=False)
    time_in = db.Column(db.DateTime)
    time_out = db.Column(db.DateTime)
    attendance = db.Column(JSON)



