from db.configs import Base
from app import db

class Records(Base):
    __tablename__ = "records"

    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date.strftime("%d/%m/%Y %H:%M:%S"), 
            "value": self.hash,
        }

    def __repr__(self):
        return f"id: {self.id} hash: {self.hash} date: {self.date}" 