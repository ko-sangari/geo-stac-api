import pytest

from fastapi import status

from src.models.geo_models import GeoField
from src.api.v1.schemas.geo_schemas import GeoFieldResponseSchema


@pytest.mark.asyncio
async def test_retrieve_satellite_image(async_client_v1, geojson_request):
    response = await async_client_v1.post("/satellite-image", json=geojson_request)
    assert response.status_code == status.HTTP_200_OK

    satellite_images = [GeoField(**item) for item in response.json()]
    assert all(isinstance(item, GeoField) for item in satellite_images)


@pytest.mark.asyncio
async def test_insert_geo_fields(async_client_v1, geojson_request):
    response = await async_client_v1.post("/fields", json=geojson_request)
    assert response.status_code == status.HTTP_200_OK

    assert len(response.json()) == 1
    satellite_images = [GeoFieldResponseSchema(**item) for item in response.json()]
    assert all(isinstance(item, GeoFieldResponseSchema) for item in satellite_images)

    response = await async_client_v1.post("/fields", json=geojson_request)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.asyncio
async def test_retrieve_geo_fields(async_client_v1, geojson_request):
    response = await async_client_v1.post("/fields", json=geojson_request)
    assert response.status_code == status.HTTP_200_OK

    response = await async_client_v1.get("/fields")
    assert response.status_code == status.HTTP_200_OK

    assert len(response.json()) == 1
    satellite_images = [GeoFieldResponseSchema(**item) for item in response.json()]
    assert all(isinstance(item, GeoFieldResponseSchema) for item in satellite_images)


@pytest.mark.asyncio
async def test_find_intersecting_fields(async_client_v1, geojson_request):
    response = await async_client_v1.post("/fields-intersect", json=geojson_request)
    assert response.status_code == status.HTTP_200_OK

    satellite_images = [GeoFieldResponseSchema(**item) for item in response.json()]
    assert all(isinstance(item, GeoFieldResponseSchema) for item in satellite_images)
