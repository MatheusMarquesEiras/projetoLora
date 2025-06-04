from db.configs import DBConnectionHandler
from db.entities import Users, Records

def create_user(username, password):
    with DBConnectionHandler() as db:
        try:
            data_isert = Users(username=username, password=password)
            db.session.add(data_isert)
            db.session.commit()
        except Exception as exception:
            db.session.rollback()
            raise exception
