import sched
import time
import threading
from typing import Callable

scheduler: sched.scheduler | None = None
scheduled_events: list[sched.Event] = []
scheduler_thread: threading.Thread | None = None

def initialize():
    global scheduler
    
    scheduler = sched.scheduler(time.time, time.sleep)


def scheduled_job(job: Callable, interval: float):
    global scheduler

    job()

    event = scheduler.enter(interval, 1, scheduled_job, (job, interval))
    scheduled_events.append(event)


def register_job(job: Callable, interval: float):
    global scheduler_thread

    event = scheduler.enter(0, 1, scheduled_job, (job, interval))
    scheduled_events.append(event)

    # Run the scheduler in a separate thread if it's not already running
    if scheduler_thread is None or not scheduler_thread.is_alive():
        scheduler_thread = threading.Thread(target=scheduler.run, daemon=True)
        scheduler_thread.start()


def cancel_all_jobs():
    global scheduled_events

    for event in scheduled_events:
        try:
            scheduler.cancel(event)
        except ValueError:
            pass
    scheduled_events = []
    print("All scheduled jobs cancelled.")