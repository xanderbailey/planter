from sqlalchemy.dialects.postgresql import UUID

from api.core import Mixin
from .base import db
import uuid


class Sensor(Mixin, db.Model):
    """Sensor Table."""

    __tablename__ = "sensor"
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4, nullable=False)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)


    def __init__(self, name: str, location: str):
        self.name = name
        self.location = location
