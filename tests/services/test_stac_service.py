import pytest

from unittest.mock import patch, MagicMock

from src.services.stac_service import STAC


@pytest.mark.asyncio
@patch("pystac_client.Client.search")
async def test_newest_satellite_image_success(mock_search):
    # Setup the mock search method
    mock_item = MagicMock()
    mock_item.assets["rendered_preview"].href = "http://example.com/image.jpg"
    mock_item.properties.__getitem__.side_effect = (
        lambda key: "2024-01-10T10:54:21.024000Z" if key == "datetime" else None
    )
    mock_search.return_value.items.return_value = [mock_item]

    bbox = (
        4.369498592495802,
        51.958455125061136,
        4.581304625280353,
        51.956185123200754,
    )
    image_url, image_datetime = await STAC.newest_satellite_image(bbox)

    assert image_url == "http://example.com/image.jpg"
    assert image_datetime == "2024-01-10T10:54:21.024000Z"


@pytest.mark.asyncio
@patch("pystac_client.Client.search")
async def test_newest_satellite_image_no_image_found(mock_search):
    mock_search.return_value.items.return_value = []

    bbox = (0, 0, 0, 0)  # An unlikely bounding box to return results
    result = await STAC.newest_satellite_image(bbox)

    assert result is None
