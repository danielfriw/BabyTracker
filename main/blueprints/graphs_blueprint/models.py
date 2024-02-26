
from main import db


class TestResults(db.Model):
    __tablename__ = 'test_results'

    id = db.Column(db.INTEGER, primary_key=True)
    user_id = db.Column(db.INTEGER, db.ForeignKey('users.id'), nullable=False)
    baby_id = db.Column(db.INTEGER, db.ForeignKey('baby.id'), nullable=False)
    test_name = db.Column(db.TEXT, nullable=False)
    age_in_months = db.Column(db.INTEGER, nullable=False)
    length = db.Column(db.FLOAT, nullable=True)
    weight = db.Column(db.FLOAT, nullable=True)
    percentile_result = db.Column(db.FLOAT, nullable=True)

    def __init__(self, user_id, baby_id, test_name, age_in_months, length=None, weight=None, percentile_result=None):
        self.user_id = user_id
        self.baby_id = baby_id
        self.test_name = test_name
        self.age_in_months = age_in_months
        self.length = length
        self.weight = weight
        self.percentile_result = percentile_result

    def __repr__(self):
        return f'Test: {self.test_name} ; Age: {self.age_in_months} months ; Length: {self.length} ; Percentile: {self.percentile_result}'