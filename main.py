# Title: API_Gateway_Microservice
# Date: 9/26/2026
# Created by: Alice Barnes using a tutorial made by Gemini AI.
# Description: An API gateway that runs as a microservice. Receives an HTTP request
# from a client program and routes it to the appropriate API service. Uses FastAPI
# as an asynchronous framework to handle multiple requests at once.

import httpx
from fastapi import FastAPI

# sets the FastAPI class as the app variable.
app = FastAPI()

# @ in FastAPI attaches the function to the app so it is ready and waiting when the
# client calls it.
@app.get("/")
# The "async" in front of the function here allows the function to run asynchronously,
# instead of having to wait in line for its turn.
async def read_request():
    """
    Asynchronously reads the request.
    :return: Confirmation message that the request was received.
    """
    return {"Request Received."}

# Gets the inventory
@app.get("/inventory")
async def get_inventory():
    """
    Asynchronously gets inventory data. Gateway waits for the Java service,
    allowing it to handle other incoming requests while it waits.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://java-inventory-backend/api/items")
            return response.json()
    except:
        return {"Error": "Inventory service is currently unavailable."}

# Gets specific user data
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    """
    Asynchronously gets user data. Gateway waits for the node.js service, allowing it to handle other incoming requests while it waits.
    :param user_id:
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://nodejs-user-backend/api/users/{user_id}")
            return response.json()
    except:
        return {"Error": "User service is unavailable."}
