from app import db, UserMixin
from sqlalchemy.sql import func

__all__ = ["User"]
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    fullname = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)

    create_date = db.Column(db.DateTime(timezone=True), default=func.now())
    is_verified = db.Column(db.Boolean, default=0)
    is_active = db.Column(db.Boolean, default=1)

    def __init__(self, username, password, fullname, email, birthday = None, highest_degree = None, university = None, major = None):
        self.username = username
        self.password = password
        self.fullname = fullname
        self.email = email

