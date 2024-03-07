from geoalchemy2 import Geometry
from sqlalchemy import Column, String

from src.database.common.dependencies import BaseSQL


class GeoField(BaseSQL):
    __tablename__ = "geo_fields"

    name = Column(String, unique=True, nullable=False)
    geom = Column(Geometry("POLYGON"), nullable=False)
    image_url = Column(String, nullable=True)
    image_date = Column(String, nullable=True)
