from db.configs import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class Records(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True)
    hash = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    def __repr__(self):
        return f"id: {self.id} hash: {self.hash} date: {self.date} user_id: {self.user_id}" 