from Telekod import db


class Mockdata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firs_name = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.Integer, primary_key=True)
    data_of_birth = db.Column(db.Integer, primary_key=True)
    payment = db.Column(db.Integer, primary_key=True)
