from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def home():
    """The home route of our API."""
    return {"message": "Hello from drivr's API."}
