import uvicorn
import os
from fastapi import FastAPI

PORT = 8888

app = FastAPI()

@app.post("/")
async def root():
    print('1')
    return {"Данные пришли"}

if __name__ == "__main__":
    uvicorn.run(app, port=PORT)