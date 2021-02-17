from fastapi import FastAPI

from drivr.api.v1 import router

app = FastAPI()
app.include_router(router)


@app.get("/")
async def home():
    """The home route of our API."""
    return {"message": "Hello from drivr's API."}
