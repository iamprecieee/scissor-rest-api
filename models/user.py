from resources.db import db


class UserModel(db.Model):
    
    __tablename__ = "users"
    
    id = db.Column(db.Integer, unique=True, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    shorturls = db.relationship("ShortUrlModel", backref="user", lazy="dynamic", cascade="all, delete")
    customurls = db.relationship("CustomUrlModel", backref="user", lazy="dynamic", cascade="all, delete")