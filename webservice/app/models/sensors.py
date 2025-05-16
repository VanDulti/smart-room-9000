# app/models/sensors.py
from app import db
from datetime import datetime


class SensorData(db.Model):
    __tablename__ = 'sensor_data'

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"SensorData('{self.topic}', '{self.value}', '{self.timestamp}')"

    def to_dict(self):
        return {
            'id': self.id,
            'topic': self.topic,
            'value': self.value,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }