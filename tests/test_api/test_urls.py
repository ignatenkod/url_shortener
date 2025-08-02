import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_short_url(client: AsyncClient):
    """Тест создания короткого URL"""
    response = await client.post(
        "/urls/",
        json={"original_url": "https://example.com"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "short_key" in data
    assert data["original_url"] == "https://example.com"

@pytest.mark.asyncio
async def test_redirect_url(client: AsyncClient):
    """Тест перенаправления по короткому URL"""
    # Сначала создаем URL
    create_resp = await client.post(
        "/urls/",
        json={"original_url": "https://example.com"}
    )
    short_key = create_resp.json()["short_key"]
    
    # Тестируем перенаправление
    redirect_resp = await client.get(
        f"/urls/{short_key}/redirect",
        follow_redirects=False
    )
    assert redirect_resp.status_code == 307
    assert redirect_resp.headers["location"] == "https://example.com"

@pytest.mark.asyncio
async def test_get_url_info(client: AsyncClient):
    """Тест получения информации о URL"""
    create_resp = await client.post(
        "/urls/",
        json={"original_url": "https://example.com"}
    )
    short_key = create_resp.json()["short_key"]
    
    info_resp = await client.get(f"/urls/{short_key}")
    assert info_resp.status_code == 200
    data = info_resp.json()
    assert data["short_key"] == short_key
    assert data["clicks_count"] == 0
