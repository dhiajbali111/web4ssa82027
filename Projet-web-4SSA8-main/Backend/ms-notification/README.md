# ms-notification (advanced technology)

Python **FastAPI** service that will consume domain events from **RabbitMQ**
and send notifications (e-mail). Optional LLM-assisted message drafting is planned.

## Run locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --port 8085 --reload
```

Health: http://localhost:8085/actuator/health
