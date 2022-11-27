from fastapi import FastAPI
import numpy as np
from typing import List

app = FastAPI()

@app.get("/", tags = ["Root"])
async def read_root() -> dict:
    return {"message": "bing chilling"}

# Health check
@app.get("/health", tags = ["Health"])
async def health_check() -> dict:
    return {"status": "ok"}


signal_dict = {
    1:[1,2,3,4,56,6,7,7,5],
    2:[2,3,4,5,2,3,456,3,2,1],
    3:[1,22,34,5,3,2,5],
}

# Get --> read signal
@app.get("/signals/{signal_id}", tags = ["Signals"])
async def read_signal(signal_id: int) -> dict:
    return {"signal_id": signal_id, "signal_values": signal_dict[signal_id]}



# Post --> create new signal
@app.post("/signals/new/{signal_id}", tags = ["Signals"])
async def create_signal(signal_id: int) -> dict:
    signal_dict.append({signal_id:[]})

# Post -> append signal with buffer
@app.post("/signals/append/{signal_id}", tags = ["Signals"])
async def push_signal(signal_id: int, signal_values: list) -> dict:
    for value in signal_values:
        signal_dict[signal_id].append(value)
    return {"signal_id": signal_id, "signal_values": signal_dict[signal_id]}

# Delete --> delete signal
@app.delete("/signals/{signal_id}", tags = ["Signals"])
async def delete_signal(signal_id: int) -> dict:
    signal_dict[signal_id].pop()
    return {"signal_id": signal_id, "signal_values": signal_dict[signal_id]}

# Get --> calculate signal statistics
@app.get("/signals/stats/{signal_id}", tags = ["Signals"])
async def calculate_signal_stats(signal_id: int) -> dict:
    signal_values = signal_dict[signal_id]
    return {
        "signal_id": signal_id, 
        "signal_values": signal_values,
        "signal_stats": {
            "mean": sum(signal_values)/len(signal_values),
            "median": np.median(signal_values),
            "max": max(signal_values),
            "min": min(signal_values),
            "std": np.std(signal_values),
            "var": np.var(signal_values),
        }
    }

# Get --> gets a subset of the signal
@app.get("/signals/subset/{signal_id}", tags = ["Signals"])
async def get_signal_subset(signal_id: int, start: int, end: int) -> dict:
    signal_values = signal_dict[signal_id]
    return {
        "signal_id": signal_id, 
        "signal_values": signal_values[start:end]
    }

