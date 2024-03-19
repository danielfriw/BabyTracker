from datetime import datetime

from extensions import db


class Event(db.Model):
    __tablename__ = 'event'

    id = db.Column(db.INTEGER, primary_key=True)
    user_id = db.Column(db.INTEGER, db.ForeignKey('users.id'), nullable=False)
    baby_name = db.Column(db.TEXT, nullable=True)
    activity = db.Column(db.TEXT, nullable=False)
    created_at = db.Column(db.TEXT, nullable=False, default=datetime.utcnow)
    comment = db.Column(db.TEXT, nullable=True)

    def __init__(self, activity, user_id, baby_name, comment=None):
        self.activity = activity
        self.user_id = user_id
        self.baby_name = baby_name
        self.comment = comment

    def __repr__(self):
        return f'Event: {self.activity} ; Created at: {self.created_at} ; Comment: {self.comment}'
