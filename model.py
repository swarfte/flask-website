import basic
import datetime as dt


db = basic.get_db()


class User(db.Model):
    username = db.Column(db.String(255), nullable=False,primary_key=True, unique=True)
    password = db.Column(db.String(255), nullable=False)
    create_date = db.Column(db.DateTime, default=dt.datetime.now())
    last_online_date = db.Column(db.DateTime, default=dt.datetime.now())
    online = db.Column(db.Boolean, default=False)
    level = db.Column(db.Integer, default=0)

    def __repr__(self) -> str:
        return f"< {self.username} : {self.password} : {self.level} >"
