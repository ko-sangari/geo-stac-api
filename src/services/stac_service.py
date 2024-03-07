from planetary_computer import sign_inplace
from pystac_client import Client
from typing import ClassVar, Tuple, Optional


class STAC:
    _client: ClassVar[Client] = Client.open(
        "https://planetarycomputer.microsoft.com/api/stac/v1",
        modifier=sign_inplace,
    )

    @classmethod
    async def newest_satellite_image(
        cls, geom: Tuple[float, float, float, float]
    ) -> Optional[Tuple[str, str]]:
        """
        Retrieve the newest satellite image within a given bounding box.

        Searches for the most recent satellite image of the specified area
        with cloud cover less than 10%.

        Args:
            bbox (Tuple[float, float, float, float]): The bounding box for
                the area of interest, specified as (min_lon, min_lat, max_lon, max_lat).

        Returns:
            Optional[Tuple[str, str]]: A tuple containing the URL of the rendered
                preview of the satellite image and its capture datetime, or None
                if no image is found.
        """
        search = cls._client.search(
            collections=["sentinel-2-l2a"],
            intersects=geom,  # type: ignore[arg-type]
            sortby=[{"field": "properties.datetime", "direction": "desc"}],
            query={
                "eo:cloud_cover": {"lt": 10},
            },
            max_items=1,
        )

        if items := list(search.items()):
            item = items[0]
            return item.assets["rendered_preview"].href, item.properties["datetime"]

        return None
