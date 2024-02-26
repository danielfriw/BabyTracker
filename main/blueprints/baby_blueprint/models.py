
from main import db

class Baby(db.Model):
    __tablename__ = 'baby'

    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.TEXT, nullable=False)
    gender = db.Column(db.TEXT, nullable=False)
    dob = db.Column(db.DATE, nullable=False)
    user_id = db.Column(db.INTEGER, db.ForeignKey('users.id'), nullable=False)
    percentile_results = db.Column(db.JSON, nullable=True)

    def __init__(self, name, gender, dob, user_id):
        self.name = name
        self.gender = gender
        self.dob = dob
        self.user_id = user_id
        self.percentile_results = None

    def __repr__(self):
        return f'Name: {self.name}, Gender: {self.gender}, DOB: {self.dob}'

    def json(self):
        return {'name': self.name,
                'gender': self.gender,
                'dob': str(self.dob)}