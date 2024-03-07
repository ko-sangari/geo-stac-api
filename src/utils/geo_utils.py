from typing import Any, Dict, List, Tuple

from src.api.v1.schemas.geo_schemas import FeatureSchema


def coordinates_to_wkt(coordinates: List[List[Tuple[float, float]]]) -> str:
    """
    Convert a list of GeoJSON-style coordinates to a WKT string.

    Args:
        coordinates (List[List[Tuple[float, float]]]): A list of lists of
            tuples, where each tuple represents a coordinate (longitude, latitude).

    Returns:
        str: The WKT (Well-Known Text) representation of the polygon.

    Example:
        >>> coordinates_to_wkt([[(1.0, 2.0), (3.0, 4.0), (5.0, 6.0), (1.0, 2.0)]])
        'POLYGON ((1.0 2.0, 3.0 4.0, 5.0 6.0, 1.0 2.0))'
    """
    wkt_coordinates = ", ".join(f"{lon} {lat}" for lon, lat in coordinates[0])
    return f"POLYGON (({wkt_coordinates}))"


def extract_info_geojson(data: FeatureSchema) -> Tuple[str, Dict[str, Any], str]:
    """
    Extracts information from a GeoJSON feature.

    This function extracts the name, geometry, and EWKT (Extended Well-Known Text)
        polygon from a GeoJSON feature.

    Args:
        data (Feature): The GeoJSON feature from which to extract information.

    Returns:
        Tuple[str, Dict[str, Any], str]: A tuple containing the name, geometry as
            a dictionary, and EWKT (Extended Well-Known Text) polygon.
    """
    name = data.properties.get("name", "Unknown")
    geom = dict(data.geometry)
    ewkt_polygon = coordinates_to_wkt(geom["coordinates"])

    return name, geom, ewkt_polygon
