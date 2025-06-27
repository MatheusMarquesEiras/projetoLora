from sqlalchemy import select
from db.configs import DBConnectionHandler
from db.entities import Records

def get_records():
    with DBConnectionHandler() as db:
        try:
            stmt = select(Records).order_by(Records.date.desc())
            records = db.session.scalars(stmt).all()
            return records
        except Exception as exception:
            db.session.rollback()
            raise exception
