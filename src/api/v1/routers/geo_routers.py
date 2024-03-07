from fastapi import APIRouter, Depends, HTTPException
from typing import List

from src.api.common.dependencies import get_database_dependency
from src.api.v1.schemas.geo_schemas import (
    GeoFieldResponseSchema,
    GeoJSONSchema,
)
from src.database.common.exceptions import DatabaseIntegrityError
from src.database.postgres.handler import PostgreSQLHandler

router = APIRouter(
    prefix="/geo",
    tags=["geo APIs"],
)


@router.post("/satellite-image", response_model=List[GeoFieldResponseSchema])
async def retrieve_satellite_image(
    request: GeoJSONSchema,
    database: PostgreSQLHandler = Depends(get_database_dependency),
) -> List[GeoFieldResponseSchema]:
    """
    Handle POST requests to retrieve satellite images based on GeoJSON data.

    Args:
        request (GeoJSONSchema): A GeoJSON object containing the geographic area of interest.

    Returns:
        List[GeoFieldResponseSchema]: A list of satellite image data conforming to the GeoFieldResponseSchema.

    Raises:
        HTTPException: If a database integrity error occurs.
    """
    try:
        return await database.retrieve_satellite_image(request)  # type: ignore[return-value]
    except DatabaseIntegrityError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.post("/fields", response_model=List[GeoFieldResponseSchema])
async def insert_geo_fields(
    request: GeoJSONSchema,
    database: PostgreSQLHandler = Depends(get_database_dependency),
) -> List[GeoFieldResponseSchema]:
    """
    Inserts a new geo field into the database from a GeoJSON request.

    Args:
        request (GeoJSONSchema): A GeoJSON object containing the geographic area of interest.

    Returns:
        List[GeoFieldResponseSchema]: A list of GeoFieldResponseSchema instances reflecting the inserted geo fields.

    Raises:
        HTTPException: If a database integrity error occurs.
    """
    try:
        return await database.insert_geo_fields(request)  # type: ignore[return-value]
    except DatabaseIntegrityError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("/fields", response_model=List[GeoFieldResponseSchema])
async def retrieve_geo_fields(
    database: PostgreSQLHandler = Depends(get_database_dependency),
) -> List[GeoFieldResponseSchema]:
    """
    Retrieve all GeoField entries from the database.

    Returns:
        List[GeoFieldResponseSchema]: A list of GeoFieldResponseSchema objects
            representing the GeoFields.
    """
    return await database.retrieve_geo_fields()  # type: ignore[return-value]


@router.post("/fields-intersect", response_model=List[GeoFieldResponseSchema])
async def find_intersecting_fields(
    request: GeoJSONSchema,
    database: PostgreSQLHandler = Depends(get_database_dependency),
) -> List[GeoFieldResponseSchema]:
    """
    Retrieve a list of fields that intersect with the given GeoJSON polygon.

    Args:
        request: The GeoJSON request containing the polygon data.

    Returns:
        List[GeoFieldResponseSchema]: A list of GeoFieldResponseSchema instances intersecting with the GeoJSON polygon.

    Raises:
        HTTPException: If any errors occur during the database operation.
    """
    try:
        return await database.get_intersecting_fields(request)  # type: ignore[return-value]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
