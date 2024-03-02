

from datetime import datetime

from api import db


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, index=True)
    recipient_id = db.Column(db.Integer, index=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Message {}>'.format(self.body)

    def to_dict(self):
        return {
            'body': self.body
        }
