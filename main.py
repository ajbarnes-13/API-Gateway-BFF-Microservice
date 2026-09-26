# Title: API-Gateway-BFF-Microservice
# Date: 9/26/2026
# Created by: Alice Barnes using a tutorial made by Gemini AI.
# Description: An API gateway and BFF that runs as a microservice. Receives an HTTP request
# from a client program and routes it to the appropriate API service, gets the requested
# information, and routes it back to the client. Uses FastAPI as an asynchronous framework to
# handle multiple requests from multiple clients at once.

import httpx
import os
import uvicorn
from fastapi import FastAPI, Request

# API dictionary. Allows the microservice to access APIs that do not require a key and APIs that
# do require a key.
ROUTE_CONFIG = {
    "catfacts": {
        "base_url": "https://catfact.ninja/fact",
        "needs_key": False
    }
}

API_SECRET_KEYS = {
    # Insert API keys here
}

# sets the FastAPI class as the app variable.
app = FastAPI()

# @ in FastAPI attaches the function to the app so it is ready and waiting when the
# client calls it.
@app.get("/")
def start_service():
    """
    Confirms the service is running.
    :return: Confirmation message that the service is running.
    """
    return {"API Service is Running..."}

# BFF (Backend-for-Frontend) Aggregator
@app.post("/aggregate")
# The "async" in front of the function here allows the function to run asynchronously,
# instead of having to wait in line for its turn.
async def request_handler(targets: dict):
    """
    Asynchronously aggregates the requests made.
    """
    results = {}

    for api_name, query_params in targets.items():
        if api_name not in ROUTE_CONFIG:
            results[api_name] = {"Error": f"'{api_name}' not found in API Dictionary."}
            continue

        try:
            config = ROUTE_CONFIG[api_name]
            request_headers = {}

            if config["needs_key"]:
                request_headers["Authorization"] = f"Bearer {API_SECRET_KEYS[api_name]}"

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url = config["base_url"],
                    headers = request_headers,
                    params = query_params
                )
                results[api_name] = response.json()
        except httpx.RequestError:
            results[api_name] = {"Error": f"failed to fetch data from {api_name}."}

    return results

# API Gateway
@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def route_handler(request: Request, path: str):
    """
    Asynchronously routes the requests made.
    """
    if path not in ROUTE_CONFIG:
        return {"Error": f"'{path}' not found in API Dictionary."}

    config = ROUTE_CONFIG[path]
    target_url = config["base_url"]

    request_headers = {}
    if config["needs_key"]:
        request_headers["Authorization"] = f"Bearer {API_SECRET_KEYS.get(path)}"

    body_data = await request.body()

    try:
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method = request.method,
                url = target_url,
                content = body_data,
                headers = request_headers,
                params = request.query_params
            )
            return response.json()
    except httpx.RequestError:
        return {"Error": f"failed to fetch data from {path}."}

if __name__ == "__main__":
    # Gets the port from the host, or locally uses 8000
    port = int(os.environ.get("PORT", 8000))

    # 0.0.0.0 is required for cloud services to receive outside traffic.
    uvicorn.run(app, host="0.0.0.0", port=port)
