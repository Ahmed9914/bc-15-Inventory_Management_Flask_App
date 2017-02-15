from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

class BaseUser(UserMixin):

    @property
    def password(self):
        raise AttributeError('password: write-only field')


    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def __repr__(self):
        return self.username

    