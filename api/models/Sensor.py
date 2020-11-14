from sqlalchemy.dialects.postgresql import UUID

from api.core import Mixin
from .base import db


class Sensor(Mixin, db.Model):
    """Sensor Table."""

    __tablename__ = "sensor"

    id = db.Column(UUID(as_uuid=True), unique=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)


    def __init__(self, name: str, location: str):
        self.name = name
        self.location = location
