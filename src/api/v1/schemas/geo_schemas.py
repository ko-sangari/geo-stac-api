from geoalchemy2.elements import WKBElement
from geoalchemy2.shape import to_shape
from pydantic import BaseModel, ConfigDict, model_validator
from typing import List, Optional

from src.models.geo_models import GeoField


class GeometrySchema(BaseModel):
    type: str
    coordinates: List[List[List[float]]]


class FeatureSchema(BaseModel):
    type: str
    properties: dict
    geometry: GeometrySchema


class GeoJSONSchema(BaseModel):
    type: str
    features: List[FeatureSchema]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "properties": {"name": "Statue of Liberty"},
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [
                                [
                                    [-74.047285, 40.689253],
                                    [-74.047285, 40.690561],
                                    [-74.044889, 40.690561],
                                    [-74.044889, 40.689253],
                                    [-74.047285, 40.689253],
                                ]
                            ],
                        },
                    }
                ],
            }
        }
    )


class GeoFieldSchema(BaseModel):
    name: str
    geom: str
    image_url: Optional[str]
    image_date: Optional[str]

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="before")
    def serializer(cls, values):
        if isinstance(values, GeoField) and isinstance(values.geom, WKBElement):
            values.geom = str(to_shape(values.geom))
        return values


class GeoFieldResponseSchema(GeoFieldSchema):
    id: int
