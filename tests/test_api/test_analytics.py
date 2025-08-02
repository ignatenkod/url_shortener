import pytest
from httpx import AsyncClient
import uuid

@pytest.mark.asyncio
async def test_get_url_stats(client: AsyncClient):
    """Тест получения статистики"""
    # Создаем URL
    create_resp = await client.post(
        "/urls/",
        json={"original_url": "https://example.com"}
    )
    url_id = create_resp.json()["id"]
    
    # Делаем несколько кликов
    for _ in range(3):
        await client.get(
            f"/urls/{create_resp.json()['short_key']}/redirect",
            follow_redirects=False
        )
    
    # Получаем статистику
    stats_resp = await client.get(
        f"/analytics/url/{url_id}/stats",
        params={"time_range": 1}
    )
    assert stats_resp.status_code == 200
    data = stats_resp.json()
    assert data["total_clicks"] == 3

@pytest.mark.asyncio
async def test_get_clicks_plot(client: AsyncClient):
    """Тест получения графика кликов"""
    create_resp = await client.post(
        "/urls/",
        json={"original_url": "https://example.com"}
    )
    url_id = create_resp.json()["id"]
    
    plot_resp = await client.get(
        f"/analytics/url/{url_id}/clicks-plot"
    )
    assert plot_resp.status_code == 200
    assert plot_resp.headers["content-type"] == "image/png"

@pytest.mark.asyncio
async def test_rate_limiting(client: AsyncClient):
    """Тест ограничения запросов"""
    # Делаем больше запросов чем разрешено
    for i in range(1002):
        response = await client.get("/urls/")
        if i >= 1000:
            assert response.status_code == 429
            break
