import hashlib

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from server import app
from flask_login import UserMixin

from .extensions import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Profile
    nickname = db.Column(db.String(16))
    bio = db.Column(db.String(80))
    email = db.Column(db.String(254), unique=True, nullable=False)
    github = db.Column(db.String(125))
    website = db.Column(db.String(254))
    company = db.Column(db.String(254))

    # Security
    session_token = db.Column(db.String(128))
    pw_hash = db.Column(db.String(128))
    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

db.init_app(app)