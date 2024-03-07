import pytest

from src.api.v1.schemas.geo_schemas import FeatureSchema
from src.utils.geo_utils import coordinates_to_wkt, extract_info_geojson


def test_coordinates_to_wkt_single_polygon():
    coords = [[(1.0, 2.0), (3.0, 4.0), (5.0, 6.0), (1.0, 2.0)]]
    result = coordinates_to_wkt(coords)
    expected = "POLYGON ((1.0 2.0, 3.0 4.0, 5.0 6.0, 1.0 2.0))"
    assert result == expected


def test_coordinates_to_wkt_empty_coordinates():
    with pytest.raises(IndexError):
        coordinates_to_wkt([])


def test_extract_info_geojson_with_name():
    feature = FeatureSchema(
        type="Feature",
        properties={"name": "Test Feature"},
        geometry={
            "type": "Polygon",
            "coordinates": [[(1.0, 2.0), (3.0, 4.0), (1.0, 2.0)]],
        },
    )
    name, geom, ewkt_polygon = extract_info_geojson(feature)
    assert name == "Test Feature"
    assert geom == {
        "type": "Polygon",
        "coordinates": [[[1.0, 2.0], [3.0, 4.0], [1.0, 2.0]]],
    }
    assert ewkt_polygon == "POLYGON ((1.0 2.0, 3.0 4.0, 1.0 2.0))"


def test_extract_info_geojson_without_name():
    feature = FeatureSchema(
        type="Feature",
        properties={},
        geometry={
            "type": "Polygon",
            "coordinates": [[(1.0, 2.0), (3.0, 4.0), (1.0, 2.0)]],
        },
    )
    name, geom, ewkt_polygon = extract_info_geojson(feature)
    assert name == "Unknown"
