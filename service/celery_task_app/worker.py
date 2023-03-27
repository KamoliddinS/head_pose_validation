import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

BROKER_URI = os.environ['BROKER_URI']
BACKEND_URI = os.environ['BACKEND_URI']

app = Celery(
    'celery_app',
    broker=BROKER_URI,
    backend=BACKEND_URI,
    include=['celery_task_app.tasks'],
    worker_max_tasks_per_child = 2,
    worker_prefetch_multiplier = 1, 
    task_time_limit = 100, 
    task_soft_time_limit = 90,
    # worker_concurrency = 1
)
