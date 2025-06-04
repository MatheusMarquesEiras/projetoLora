from db.configs import Base
from sqlalchemy import Column, String, Integer, ForeignKey

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)

    def __repr__(self):
        return f"id: {self.id} username: {self.username} password: {self.password}"