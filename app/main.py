from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from confluent_kafka import Producer
import os
from uuid import UUID


def read_secret(path):
    with open(path, "r") as f:
        return f.read().strip()


KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
KAFKA_SECRET_PATH = "/etc/kafka/secrets"
KAFKA_CA_PATH = "/etc/kafka/ca"

KAFKA_KEY_PASSWORD = read_secret(
    os.path.join(KAFKA_SECRET_PATH, "user.password")
)
KAFKA_KEY = os.path.join(KAFKA_SECRET_PATH, "user.key")
KAFKA_CERT = os.path.join(KAFKA_SECRET_PATH, "user.crt")
KAFKA_CA = os.path.join(KAFKA_CA_PATH, "ca.crt")

producer_conf = {
    "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
    "security.protocol": "SSL",
    "ssl.key.location": KAFKA_KEY,
    "ssl.certificate.location": KAFKA_CERT,
    "ssl.ca.location": KAFKA_CA,
    "ssl.key.password": KAFKA_KEY_PASSWORD,
}

producer = Producer(producer_conf)


class ApplicationForm(BaseModel):
    id: UUID
    age: int
    income: int
    employed: bool
    credit_score: int
    loan_amount: int


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/apply")
async def apply(form: ApplicationForm):
    print("Received payload from TS:", form.dict())
    try:
        producer.produce(
            KAFKA_TOPIC,
            key=str(form.id),
            value=form.json().encode("utf-8")
        )
        producer.flush()
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kafka error: {str(e)}")
