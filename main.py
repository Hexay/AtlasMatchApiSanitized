from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import uvicorn
import json
from pathlib import Path
import httpx
from typing import Optional, Dict, Any, Tuple

# Load config
with open('config.json', 'r') as f:
    config = json.load(f)

port = config['port']
is_development = config['is_development']
BM_TOKEN = config['bm_token']
API_TOKEN = config['api_token']
BM_API_URL = "https://api.battlemetrics.com"

# fastapi app
app = FastAPI(
    title="Match Api",
    description="Match Api",
    version="1.0.0"
)

# classes
class IDResponse(BaseModel):
    steam_id: Optional[str] = None
    battlemetrics_id: Optional[str] = None
    message: Optional[str] = None

# helper functions
def get_headers() -> Dict[str, str]:
    return {"Authorization": f"Bearer {BM_TOKEN}"}

def verify_token(authorization: str = Header(..., description="Api token")) -> None:
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    try:
        token = authorization.split()
        if token != API_TOKEN:
            raise HTTPException(status_code=401, detail="Invalid token")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header format")

def create_match_payload(identifier: str, id_type: str) -> Dict[str, Any]:
    return {
        "data": {
            "type": "identifier",
            "attributes": {
                "type": id_type,
                "identifier": identifier
            }
        }
    }

def extract_identifier_from_response(response_data: Dict[str, Any]) -> Tuple[Optional[str], Optional[str]]:
    try:
        #Here is where the identifier is extracted, returns both steamID and battlemetricsId
        bm_id = response_data["data"]["id"]
        
        identifiers = response_data["data"]["relationships"]["identifiers"]["data"]
        for identifier in identifiers:
            if identifier["type"] == "identifier" and identifier["attributes"]["type"] == "steamID":
                return identifier["attributes"]["identifier"], bm_id
            
    except (KeyError, TypeError):
        print(f"Error extracting identifier from response: {response_data}")

    return None, None

def is_steam_id(identifier: str) -> bool:
    return identifier.isdigit() and identifier.startswith('7656')

# api functions
async def quick_match_conversion(client: httpx.AsyncClient, identifier: str, id_type: str) -> Tuple[Optional[str], Optional[str]]:
    response = await client.post(
        f"{BM_API_URL}/players/quick-match",
        headers=get_headers(),
        json=create_match_payload(identifier, id_type)
    )
    
    if response.status_code == 200:
        data = response.json()
        return extract_identifier_from_response(data)
    return None, None

async def handle_id_conversion(client: httpx.AsyncClient, identifier: str) -> IDResponse:
    #this is where id_type is initialized
    id_type = "steamID" if is_steam_id(identifier) else "battlemetricsId"
    steam_id, bm_id = await quick_match_conversion(client, identifier, id_type)
    
    if steam_id and bm_id:
        return IDResponse(steam_id=steam_id, battlemetrics_id=bm_id)
    return IDResponse(
        message=f"No matching {id_type} found"
    )

# routes
@app.get("/")
async def root():
    return {"message": "Match Api for Hexaytron"}

@app.post("/convert/{identifier}", response_model=IDResponse)
async def convert_id(identifier: str, authorization: str = Header(..., description="Api token")):
    # Verify the api token
    verify_token(authorization)
    
    if not BM_TOKEN:
        raise HTTPException(status_code=500, detail="BattleMetrics API token not configured")

    async with httpx.AsyncClient() as client:
        try:
            return await handle_id_conversion(client, identifier)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

# main
if __name__ == "__main__":
    print(f"Development mode: {is_development}")
    # local host for development
    if is_development:
        print(f"Starting development server at http://127.0.0.1:{port}")
        uvicorn.run("main:app", host="127.0.0.1", port=port, reload=True)
    # production server
    else:
        print(f"Starting production server on port {port}")
        uvicorn.run("main:app", host="0.0.0.0", port=port) 