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
