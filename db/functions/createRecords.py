from db.configs import DBConnectionHandler
from db.entities import Users, Records

def create_record(hash, date):

    with DBConnectionHandler() as db:
        try:
            data_isert = Records(hash=hash, date=date)
            db.session.add(data_isert)
            db.session.commit()
        except Exception as exception:
            db.session.rollback()
            raise exception
