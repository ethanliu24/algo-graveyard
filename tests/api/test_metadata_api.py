import pytest

API = "/api/metadata"

@pytest.mark.asyncio
async def test_get_all_metadata(endpoint):
    """ Test getting all metadata. """
    response = endpoint.get(f"{API}?sources=true&difficulties=true&statuses=true&tags=true&languages=true")
    metadata = response.json()
    assert "sources" in metadata
    assert "difficulties" in metadata
    assert "statuses" in metadata
    assert "tags" in metadata
    assert "languages" in metadata


@pytest.mark.asyncio
async def test_get_all_metadata_no_queries(endpoint):
    """ Test getting metadata with no queries. Should return nothing. """
    response = endpoint.get(f"{API}")
    metadata = response.json()
    assert metadata == {}


@pytest.mark.asyncio
async def test_get_partial_metadata(endpoint):
    """ Test getting parital metadata. """
    response = endpoint.get(f"{API}?languages=true")
    metadata = response.json()
    assert "sources" not in metadata
    assert "difficulties" not in metadata
    assert "statuses" not in metadata
    assert "tags" not in metadata
    assert "languages" in metadata
