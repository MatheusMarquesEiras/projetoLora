from db.configs import DBConnectionHandler
from db.entities import Users, Records
from app import bcrypt

def create_user(username, password):

    hash_password = bcrypt.generate_password_hash(password=password).decode('utf-8')

    with DBConnectionHandler() as db:
        try:
            data_isert = Users(username=username, password=hash_password)
            db.session.add(data_isert)
            db.session.commit()
        except Exception as exception:
            db.session.rollback()
            raise exception
