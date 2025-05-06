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
    "is_development": true,
    "port": 8001,
    "bm_token": "your_battlemetrics_token_here"
}
```

## Running the Application

### Development Mode
Set `"is_development": true` in `config.json` and run:
```bash
python main.py
```
The server will start at `http://127.0.0.1:8001` with auto-reload enabled.

### Production Mode
Set `"is_development": false` in `config.json` and run:
```bash
python main.py
```
The server will start on `0.0.0.0:8001`.

## API Endpoints

### Convert ID (`POST /convert/{identifier}`)
Converts between Steam and BattleMetrics IDs.

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
- Returns 500 error if BattleMetrics token is not configured
- Handles API errors gracefully with appropriate error messages 