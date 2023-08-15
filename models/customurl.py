from datetime import datetime
from resources.db import db


class CustomUrlModel(db.Model):
    
    __tablename__ = "customurls"
    
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String, nullable=False)
    custom_url = db.Column(db.String(120), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    clicks = db.Column(db.Integer, default=0)