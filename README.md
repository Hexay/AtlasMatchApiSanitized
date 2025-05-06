# Steam ID to BattleMetrics ID Converter API

A FastAPI application that converts between Steam IDs and BattleMetrics IDs using the BattleMetrics API.

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `config.json` file with the following structure:
```json
{
    "port": 8001,
    "bm_token": "your-battlemetrics-token-here",
    "api_token": "your-secret-api-token-here"
}
```

3. Run the application:
```bash
python main.py
```
The server will start on `http://localhost:8001`

## Production Deployment

See [DEPLOY.md](DEPLOY.md) for Docker deployment instructions.

## API Endpoints

### Convert ID (`POST /convert/{identifier}`)
Converts between Steam and BattleMetrics IDs.

**Authentication Required**
Include your API token in the request header:
```
Authorization: your-secret-api-token-here
```

**Example Request:**
```bash
curl -X POST "http://localhost:8001/convert/76561198123456789" \
     -H "Authorization: your-secret-api-token-here"
```

**Response:**
```json
{
    "steam_id": "765xxxxxxxxxx",
    "battlemetrics_id": "xxxxxxxx",
    "message": null
}
```

If no match is found:
```json
{
    "steam_id": null,
    "battlemetrics_id": null,
    "message": "No matching steamId/battlemetricsId found"
}
```

## Error Handling
- Returns 401 error if API token is missing or invalid
- Returns 500 error if BattleMetrics token is not configured
- Handles API errors gracefully with appropriate error messages

## Project Structure
```
.
├── main.py              # FastAPI application
├── config.json          # Configuration file
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose services
├── nginx.conf          # Nginx reverse proxy config
└── certbot/            # SSL certificate files
```

## Security Notes
- API requires token authentication
- In production, all traffic is SSL encrypted
- Configuration file is mounted read-only in Docker
- Sensitive tokens are never exposed in logs

## Notes
- The ngrok URL changes each time you restart the server (with free account)
- The server must be running for the URL to be active
- Monitor requests and debug using the ngrok web interface at http://localhost:4040
- For a fixed URL, consider upgrading to a paid ngrok account 