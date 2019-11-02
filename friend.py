#from flask_login import UserMixin

from db import get_db

#class Friend(UserMixin):
class Friend():
    def __init__(self, id_, user_id, friend_user_id):
        self.friend_id = id_
        self.user_id = user_id
        self.friend_user_id = friend_user_id

    @staticmethod
    def get(friend_id):
        db = get_db()
        friend = db.execute(
            "SELECT * FROM friend WHERE friend_id = ?", (friend_id,)
        ).fetchone()
        if not friend:
            return None

        friend = Friend(
            id_=friend[0], user_id=friend[1], friend_user_id=friend[2]
        )
        return friend

    @staticmethod
    def create(id_, user_id, friend_user_id):
        db = get_db()
        db.execute(
            "INSERT INTO friend (friend_id, user_id, friend_user_id) "
            "VALUES (?, ?, ?)",
            (id_, user_id, friend_user_id),
        )
        db.commit()
