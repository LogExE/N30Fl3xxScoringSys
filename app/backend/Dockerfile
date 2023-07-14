FROM python:3.11.4-alpine

WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD uvicorn main:app