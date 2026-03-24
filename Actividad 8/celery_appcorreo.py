from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

celery = Celery(
    "tasks",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_BROKER_URL")
)