#from flask_login import UserMixin

from db import get_db

#class Friend(UserMixin):
class Friend():
    def __init__(self, id_, user_id, friend_user_id, friend_name, friend_email, friend_phone):
        self.friend_id = id_
        self.user_id = user_id
        self.friend_user_id = friend_user_id
        self.friend_name = friend_name
        self.friend_email = friend_email
        self.friend_phone = friend_phone

    @staticmethod
    def get(friend_id):
        db = get_db()
        friend = db.execute(
            "SELECT * FROM friend WHERE friend_id = ?", (friend_id,)
        ).fetchone()
        if not friend:
            return None

        friend = Friend(
            id_=friend[0], user_id=friend[1], friend_user_id=friend[2], friend_name=friend[3], friend_email=friend[4], friend_phone = friend[5]
        )
        return friend

    @staticmethod
    def create(id_, user_id, friend_user_id, friend_name, friend_email, friend_phone):
        db = get_db()
        db.execute(
            "INSERT INTO friend (friend_id, user_id, friend_user_id, friend_name, friend_email, friend_phone) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (id_, user_id, friend_user_id, friend_name, friend_email, friend_phone),
        )
        db.commit()
