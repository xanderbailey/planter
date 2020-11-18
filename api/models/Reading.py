from sqlalchemy.dialects.postgresql import UUID

from api.core import Mixin
from .base import db

# Note that we use sqlite for our tests, so you can't use Postgres Arrays
class Reading(Mixin, db.Model):
    """Sensor Data Table."""

    __tablename__ = "reading"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    sensor_id = db.Column(UUID(as_uuid=True), db.ForeignKey("sensor.id", ondelete="SET NULL"), nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    pressure = db.Column(db.Float)



    def __init__(self, sensor_id, temperature, humidity, pressure):
        self.sensor_id = sensor_id
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure

