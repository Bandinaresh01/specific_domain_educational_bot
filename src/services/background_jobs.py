from fastapi import BackgroundTasks
from typing import List
import time
from .preprocessing import preprocess_all_subjects

def long_running_task(subject: str):
    # Simulate a long-running task, such as indexing or processing
    time.sleep(10)  # Simulate a delay
    print(f"Completed background task for subject: {subject}")

def enqueue_background_task(subject: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(long_running_task, subject)

def process_batch_tasks(subjects: List[str], background_tasks: BackgroundTasks):
    for subject in subjects:
        enqueue_background_task(subject, background_tasks)

def preprocess_task():
    """Background task for preprocessing all subjects."""
    preprocess_all_subjects()
