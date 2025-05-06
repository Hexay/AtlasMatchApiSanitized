# Steam ID to BattleMetrics ID Converter API

A FastAPI application that converts between Steam IDs and BattleMetrics IDs using the BattleMetrics API.

## Setup

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

3. Ngrok Configuration:
The application uses ngrok to create a public URL. With a free ngrok account, you'll get a random URL each time you start the server. It will look something like:
```
https://xxxx-xxx-xx-xxx-xx.ngrok-free.app
```

For a fixed URL, you would need a paid ngrok account. The configuration is in `ngrok.yml`.

## Running the Application

Simply run:
```bash
python main.py
```

The application will:
1. Start the FastAPI server
2. Generate a new public URL using ngrok
3. Start the ngrok web interface at http://localhost:4040 (for monitoring requests)

Example console output:
```
Public URL: https://4156-130-43-180-70.ngrok-free.app
Ngrok web interface: http://localhost:4040
```

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
# Replace with your actual ngrok URL shown in the console
curl -X POST "https://4156-130-43-180-70.ngrok-free.app/convert/76561198123456789" \
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

## Notes
- The ngrok URL changes each time you restart the server (with free account)
- The server must be running for the URL to be active
- Monitor requests and debug using the ngrok web interface at http://localhost:4040
- For a fixed URL, consider upgrading to a paid ngrok account 