import uvicorn
import os
from fastapi import FastAPI

PORT = 8888

app = FastAPI()

@app.post("/")
async def root():
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    uvicorn.run(app, port=PORT)