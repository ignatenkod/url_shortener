# URL Shortener API Documentation

## Base URL
`https://your-service.com/api/v1`

## Authentication
No authentication required for basic functionality.

## Endpoints

### Create Short URL
`POST /urls/`

Request body:
```json
{
  "original_url": "string (required)"
}
Response:

json
{
  "id": "string",
  "original_url": "string",
  "short_key": "string",
  "created_at": "string",
  "is_active": boolean,
  "clicks_count": number
}
Get URL Info
GET /urls/{short_key}

Response: Same as create endpoint

Redirect
GET /urls/{short_key}/redirect

Response: 307 redirect to original URL

Get Analytics
GET /analytics/url/{url_id}/stats

Parameters:

time_range: number (days, default 7)

Response:

json
{
  "total_clicks": number,
  "countries": {
    "country_code": count
  },
  "time_range": "string"
}
Get Clicks Plot
GET /analytics/url/{url_id}/clicks-plot

Returns: PNG image with clicks by country

Get Timeline Plot
GET /analytics/url/{url_id}/timeline-plot

Returns: PNG image with clicks timeline

text

## 7.5. Примеры использования

Добавим файл `examples/example_usage.py`:

```python
import httpx
import asyncio

BASE_URL = "http://localhost:8000"

async def main():
    async with httpx.AsyncClient() as client:
        # Создаем короткий URL
        response = await client.post(
            f"{BASE_URL}/urls/",
            json={"original_url": "https://example.com"}
        )
        url_data = response.json()
        print(f"Created short URL: {url_data['short_key']}")
        
        # Получаем информацию о URL
        info_response = await client.get(
            f"{BASE_URL}/urls/{url_data['short_key']}"
        )
        print("URL info:", info_response.json())
        
        # Делаем несколько редиректов
        for _ in range(3):
            await client.get(
                f"{BASE_URL}/urls/{url_data['short_key']}/redirect",
                follow_redirects=False
            )
        
        # Получаем аналитику
        stats = await client.get(
            f"{BASE_URL}/analytics/url/{url_data['id']}/stats"
        )
        print("Stats:", stats.json())
        
        # Получаем график
        plot = await client.get(
            f"{BASE_URL}/analytics/url/{url_data['id']}/clicks-plot"
        )
        with open("clicks_plot.png", "wb") as f:
            f.write(plot.content)
        print("Plot saved to clicks_plot.png")

if __name__ == "__main__":
    asyncio.run(main())
7.6. Запуск тестов
Для запуска тестов выполните:

bash
pytest -v
