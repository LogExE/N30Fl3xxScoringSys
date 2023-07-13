from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
import datetime

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
    print('Server started :', datetime.datetime.now())


@app.on_event("shutdown")
async def shutdown_event():
    print('Server shutdown :', datetime.datetime.now())


@app.post("/")
async def get_form_data(info: Request):
    req_info = await info.json()
    print(req_info)
    return {
        "status": "SUCCESS",
        "data": req_info
    }


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
