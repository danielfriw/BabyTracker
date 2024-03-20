from extensions import db


class LengthMeasurementsResults(db.Model):
    __tablename__ = 'length_measurements_results'

    id = db.Column(db.INTEGER, primary_key=True)
    user_id = db.Column(db.INTEGER, db.ForeignKey('users.id'), nullable=False)
    baby_id = db.Column(db.INTEGER, db.ForeignKey('baby.id'), nullable=False)
    age_in_months = db.Column(db.INTEGER, nullable=False)
    length = db.Column(db.FLOAT, nullable=True)
    percentile_result = db.Column(db.FLOAT, nullable=True)

    def __init__(self, user_id, baby_id, age_in_months, length=None, percentile_result=None):
        self.user_id = user_id
        self.baby_id = baby_id
        self.age_in_months = age_in_months
        self.length = length
        self.percentile_result = percentile_result

    def __repr__(self):
        return f'Age: {self.age_in_months} months ; Length: {self.length} ; Percentile: {self.percentile_result}'
