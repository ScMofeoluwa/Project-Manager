from ... import db, bcrypt
from typing import List


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(120))
    lists = db.relationship("ListModel", lazy="dynamic", backref="owner")

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_all(cls) -> List["UserModel"]:
        return cls.query.all()

    @staticmethod
    def generate_hash(password):
        return bcrypt.generate_password_hash(password).decode("utf-8")

    @staticmethod
    def verify_hash(hash_pwd, password):
        bcrypt.check_password_hash(hash_pwd, password)
