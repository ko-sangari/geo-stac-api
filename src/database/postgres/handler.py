import logging

from geoalchemy2 import WKTElement
from sqlalchemy import and_
from sqlalchemy.engine.url import URL
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from typing import List

from src.api.v1.schemas.geo_schemas import GeoJSONSchema
from src.database.postgres.core import PostgreSQLCore
from src.models.geo_models import GeoField
from src.services.stac_service import STAC
from src.utils.geo_utils import extract_info_geojson

logger = logging.getLogger(__name__)


class PostgreSQLHandler(PostgreSQLCore):
    """
    A subclass of PostgreSQLHandler to handle database queries.
    """

    def __init__(self, db_url: URL = None, database: str = None) -> None:
        """
        Initializes the PostgreSQLCore with a database URL and connects to it.

        Args:
            db_url (str, optional): The database URL. Defaults to None.
            database (str, optional): The name of the database to connect to. Defaults to None.
        """
        super().__init__(db_url, database)

    async def retrieve_satellite_image(self, geojson: GeoJSONSchema) -> List[GeoField]:
        """
        Retrieves satellite images for the given GeoJSON.

        Processes each feature in the GeoJSON, checks for existing satellite
        images in the database, and fetches new images if necessary.

        Args:
            geojson (GeoJSONSchema): The GeoJSON containing features to process.

        Returns:
            List[GeoField]: A list of GeoField objects, either retrieved from the database or
                newly fetched.
        """
        result: List[GeoField] = []
        async with self.session_factory() as session:
            for feature in geojson.features:
                name, geom, ewkt_polygon = extract_info_geojson(feature)

                # Check for existing GeoField with the same geometry
                query = await session.execute(
                    select(GeoField).where(
                        GeoField.geom.ST_Equals(WKTElement(ewkt_polygon))
                    )
                )
                geofield_item = query.scalar_one_or_none()

                if geofield_item:
                    if geofield_item.image_url:  # Skip if image_url already exists
                        continue

                    # Update existing GeoField's image URL and date
                    new_image_url, datetime = await STAC.newest_satellite_image(geom)  # type: ignore[arg-type]
                    geofield_item.image_url = new_image_url  # type: ignore[assignment]
                    geofield_item.image_date = datetime  # type: ignore[assignment]

                elif not geofield_item:
                    # Create a GeoField and update the associated satellite image.
                    new_image_url, datetime = await STAC.newest_satellite_image(geom)  # type: ignore[arg-type]
                    geofield_item = GeoField(
                        name=name,
                        geom=ewkt_polygon,
                        image_url=new_image_url,
                        image_date=datetime,
                    )
                    session.add(geofield_item)

                result.append(geofield_item)
                try:
                    await session.commit()
                except IntegrityError:
                    await session.rollback()

        return result

    async def insert_geo_fields(self, geojson: GeoJSONSchema) -> List[GeoField]:
        """
        Inserts new geo fields based on the provided GeoJSON data.

        Each feature in the GeoJSON data is extracted and stored as a new GeoField in the database.
        If a database integrity error occurs (e.g., a duplicate entry), the transaction is rolled back.

        Args:
            geojson (GeoJSONSchema): The GeoJSON data containing geo field information.

        Returns:
            List[GeoField]: A list of successfully inserted GeoField instances.

        Raises:
            IntegrityError: If a database integrity issue occurs during the insert operation.
        """
        result: List[GeoField] = []
        async with self.session_factory() as session:
            for feature in geojson.features:
                name, geom, ewkt_polygon = extract_info_geojson(feature)

                new_item = GeoField(
                    name=name,
                    geom=ewkt_polygon,
                )
                session.add(new_item)
                try:
                    await session.commit()
                    result.append(new_item)
                except IntegrityError:
                    await session.rollback()
        return result

    async def retrieve_geo_fields(self) -> List[GeoField]:
        """
        Retrieves a list of all GeoField objects from the database.

        Returns:
            List[GeoField]: A list of GeoField objects from the database.
        """
        async with self.session_factory() as session:
            query = select(GeoField)
            result = await session.execute(query)
            return result.scalars().all()  # type: ignore[return-value]

    async def get_intersecting_fields(self, geojson: GeoJSONSchema) -> List[GeoField]:
        """
        Retrieves a list of GeoField objects that intersect with the specified GeoJSON polygon.

        This method queries the database for all GeoField entries whose geometry intersects
        with the given GeoJSON polygon. It only works with the first or single polygon coordinates
        specified in the GeoJSON object.

        Args:
            geojson: A GeoJSONSchema object containing the polygon data for intersection check.

        Returns:
            A list of GeoField objects that intersect with the specified GeoJSON polygon.
        """
        _, _, ewkt_polygon = extract_info_geojson(geojson.features[0])
        async with self.session_factory() as session:
            result = await session.execute(
                select(GeoField).where(GeoField.geom.ST_Intersects(ewkt_polygon))
            )
            return result.scalars().all()  # type: ignore[return-value]
