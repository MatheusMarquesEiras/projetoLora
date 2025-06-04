from db.configs import Base
from app import db

class Users(Base):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"id: {self.id} username: {self.username} password: {self.password}"