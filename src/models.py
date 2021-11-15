from src import db


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gender = db.Column(db.String(200))
    first_name = db.Column(db.String(length=200, convert_unicode=True))
    last_name = db.Column(db.String(length=200, convert_unicode=True))
    e_mail = db.Column(db.String(200))
    born_date = db.Column(db.DateTime)

    def __repr__(self):
        return f"{self.id} - {self.e_mail}"
