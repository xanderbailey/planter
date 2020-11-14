from sqlalchemy.dialects.postgresql import UUID

from api.core import Mixin
from .base import db

# Note that we use sqlite for our tests, so you can't use Postgres Arrays
class SensorData(Mixin, db.Model):
    """Sensor Data Table."""

    __tablename__ = "SensorData"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    sensor_id = db.Column(UUID(as_uuid=True), db.ForeignKey("sensors.id", ondelete="SET NULL"), nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    temperature = db.Colum(db.Float)
    humidity = db.Colum(db.Float)
    pressure = db.Colum(db.Float)



    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return f"<Email {self.email}>"
