import pytest

from unittest.mock import patch

from src.models.geo_models import GeoField


@pytest.mark.asyncio
@patch("src.services.stac_service.STAC.newest_satellite_image")
async def test_retrieve_satellite_image(
    mock_newest_satellite_image, postgres, geojson_data
):
    mock_newest_satellite_image.return_value = ("mock_url", "mock_datetime")

    result = await postgres.retrieve_satellite_image(geojson_data)
    assert all(isinstance(item, GeoField) for item in result)

    result = await postgres.retrieve_satellite_image(geojson_data)
    mock_newest_satellite_image.assert_called()


@pytest.mark.asyncio
async def test_insert_geo_fields(postgres, geojson_data):
    result = await postgres.insert_geo_fields(geojson_data)
    assert len(result) == 1
    assert all(isinstance(item, GeoField) for item in result)
    assert result[0].name == geojson_data.features[0].properties["name"]


@pytest.mark.asyncio
async def test_retrieve_geo_fields(postgres, geojson_data):
    await postgres.insert_geo_fields(geojson_data)

    result = await postgres.retrieve_geo_fields()

    assert len(result) == 1
    assert all(isinstance(item, GeoField) for item in result)
    assert result[0].name == geojson_data.features[0].properties["name"]


@pytest.mark.asyncio
async def test_get_intersecting_fields(postgres, geojson_data):
    await postgres.insert_geo_fields(geojson_data)

    result = await postgres.get_intersecting_fields(geojson_data)

    assert len(result) == 1
    assert all(isinstance(item, GeoField) for item in result)
    assert result[0].name == geojson_data.features[0].properties["name"]
