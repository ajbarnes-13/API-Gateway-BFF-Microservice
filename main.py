# Title: API_Gateway_Microservice
# Date: 9/26/2026
# Created by: Alice Barnes using a tutorial made by Gemini AI.
# Description: An API gateway that runs as a microservice. Receives an HTTP request
# from a client program and routes it to the appropriate API service. Uses FastAPI
# as an asynchronous framework to handle multiple requests at once.

# Imports the FastAPI class from the fastapi library.
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
