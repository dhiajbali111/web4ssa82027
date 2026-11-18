"""Notification microservice (advanced): Python FastAPI + RabbitMQ consumer.
Validation 1 skeleton — no real e-mail / LLM business logic yet.
"""
from fastapi import FastAPI

app = FastAPI(title="ms-notification", version="0.0.1")


@app.get("/actuator/health")
def health():
    return {"status": "UP", "service": "ms-notification"}


@app.get("/api/notifications/ping")
def ping():
    return {"status": "ok", "service": "notification"}


# Placeholder: RabbitMQ consumer will be wired in a later iteration.
# Expected queues: application.created, interview.scheduled, application.status.changed
