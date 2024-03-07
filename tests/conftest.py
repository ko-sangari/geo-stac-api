import pytest_asyncio

from datetime import datetime, timezone
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from typing import AsyncGenerator, Callable

from src.api.v1.schemas.geo_schemas import GeoJSONSchema
from src.database.postgres.handler import PostgreSQLHandler
from src.models.geo_models import GeoField
from src.utils.geo_utils import extract_info_geojson


@pytest_asyncio.fixture
async def override_get_database_dependency() -> Callable:
    """
    A pytest fixture to override the database handler dependency for testing.
    """

    async def _override_get_database_dependency():
        db_handler = PostgreSQLHandler(database="test_geo_stac_db")
        await db_handler.initialize()
        return db_handler

    return _override_get_database_dependency


@pytest_asyncio.fixture
async def app(
    override_get_database_dependency: Callable,
) -> AsyncGenerator[FastAPI, None]:
    """
    Creates a FastAPI test app with overridden database dependencies.

    Args:
        override_get_database_dependency: A callable that returns an instance
            of the test database handler.

    Yields:
        The FastAPI test application instance.
    """
    from src.api.common.dependencies import get_database_dependency
    from src.main import app

    app.dependency_overrides[get_database_dependency] = override_get_database_dependency
    yield app

    db_handler = PostgreSQLHandler(database="test_geo_stac_db")
    await db_handler.drop_tables()
    await db_handler.engine.dispose()


@pytest_asyncio.fixture
async def async_client_v1(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """
    Creates an asynchronous test client for FastAPI app.

    Args:
        app (FastAPI): The FastAPI application to which the client will send requests.

    Yields:
        AsyncClient: An instance of httpx.AsyncClient for making API requests.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app),  # type: ignore[arg-type]
        base_url="http://testserver/api/v1/geo",
    ) as async_client:
        yield async_client


@pytest_asyncio.fixture
async def postgres() -> AsyncGenerator:
    """
    Asynchronous fixture to set up and tear down a PostgreSQL database
        for testing.

    Yields:
        PostgreSQLHandler: An instance of the database handler for testing.
    """
    db_handler = PostgreSQLHandler(database="test_geo_stac_db")
    await db_handler.initialize()
    yield db_handler

    # Perform cleanup after all tests are done
    await db_handler.drop_tables()
    await db_handler.engine.dispose()


@pytest_asyncio.fixture
def geojson_request() -> dict:
    """
    Fixture to provide GeoJSON data for testing.

    Returns:
        dict: A dictionary representing the GeoJSON data.
    """
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "Rotterdam"},
                "geometry": {
                    "coordinates": [
                        [
                            [4.369498592495802, 51.958455125061136],
                            [4.373182175674373, 51.88121056902091],
                            [4.581304625280353, 51.883484364969945],
                            [4.581304625280353, 51.956185123200754],
                            [4.369498592495802, 51.958455125061136],
                        ]
                    ],
                    "type": "Polygon",
                },
                "id": 0,
            },
        ],
    }


@pytest_asyncio.fixture
def geojson_data(geojson_request: dict) -> GeoJSONSchema:
    """
    Fixture to create a GeoJSONSchema object from a provided dictionary.

    Returns:
        GeoJSONSchema: An instance of the GeoJSONSchema model created from the provided GeoJSON data.
    """
    return GeoJSONSchema(**geojson_request)


@pytest_asyncio.fixture
def satellite_image_instance(geojson_data: GeoJSONSchema) -> GeoField:
    """
    Fixture to provide a GeoField instance for testing.

    Returns:
        GeoField: An instance of GeoField.
    """
    feature = geojson_data.features[0]
    name, geom, ewkt_polygon = extract_info_geojson(feature)
    return GeoField(
        name=name,
        geom=ewkt_polygon,
        image_url="https://planetarycomputer.microsoft.com/api/data/v1/item/preview.png",
        image_date=datetime.now(timezone.utc).isoformat(timespec="microseconds") + "Z",
    )
