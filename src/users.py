from flask_login import UserMixin

users = {"username": {"password": "temppassword"}}

class User(UserMixin):
    def __init__(self, username):
        self.id = username

    @classmethod
    def get(cls, username):
        if username in users:
            return cls(username)
        return None

    @classmethod
    def check_password(cls, username, password):
        return users.get(username, {}).get("password") == password

