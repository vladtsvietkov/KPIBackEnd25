from backend.extensions import db
from sqlalchemy.sql import func


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    records = db.relationship("Record", back_populates="user", cascade="all, delete")
    own_categories = db.relationship("Category", back_populates="user", cascade="all, delete")


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    user = db.relationship("User", back_populates="own_categories")
    records = db.relationship("Record", back_populates="category", cascade="all, delete")


class Record(db.Model):
    __tablename__ = "records"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    timestamp = db.Column(db.DateTime, server_default=func.now())
    amount = db.Column(db.Float, nullable=False)

    user = db.relationship("User", back_populates="records")
    category = db.relationship("Category", back_populates="records")