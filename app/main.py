from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
import app as frontend


app = FastAPI()

origins = [
    "http://127.0.0.1:50422/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    await frontend.run()


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
