from fastapi import FastAPI
from app.store.memory_store import event_store
import threading
from app.consumer import start_consumer

app = FastAPI(title="User Activity Event Service")

@app.on_event("startup")
def startup_event():
    thread = threading.Thread(target=start_consumer)
    thread.daemon = True
    thread.start()

@app.get("/events/processed")
def get_processed_events():
    return event_store.get_all()