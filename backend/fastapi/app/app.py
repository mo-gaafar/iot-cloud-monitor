from fastapi import FastAPI
import numpy as np
from deta import Deta
import json

deta = Deta("a0gu0e0f_F8wAnskRDHQ6PPubHyPui11CSy8KAv8S")
signals = deta.Base("signal-store")

app = FastAPI()

signal_dict = [{
    "signal_id": "1",
    "signal_name": "signal1",
    "signal_values": np.random.rand(1000).tolist(),
    "fsample": 1000,
}, {
    "signal_id": "2",
    "signal_name": "signal2",
    "signal_values": np.random.rand(1000).tolist(),
    "fsample": 1000,
}, {
    "signal_id": "3",
    "signal_name": "signal3",
    "signal_values": np.random.rand(1000).tolist(),
    "fsample": 1000,
}]


@app.get("/", tags=["Root"])
async def read_root() -> dict:
    return {"message": "nassoura fel mansoura"}


# Health check
@app.get("/health", tags=["Health", "Embedded", "Frontend"])
async def health_check() -> dict:
    return {"status": "ok"}


# Post -> initialize test signals
@app.post("/init", tags=["Testing"])
async def init_signals() -> dict:
    #iterate on dict keys
    for item in signal_dict:
        signals.put(item)
    return {"status": "ok", "message": "signals initialized"}


# Get --> read signal
@app.get("/signals/{signal_id}", tags=["Frontend"])
async def read_signal(signal_id: int) -> dict:
    signal_dict = json.loads(signals.fetch())
    return {"signal_id": signal_id, "signal_values": signal_dict[signal_id]}


# Post --> create new signal
@app.post("/signals/new/{signal_id}", tags=["Embedded"])
async def create_signal(signal_id: int) -> dict:
    signal_dict = json.loads(signals.fetch())
    # signal_dict.append({signal_id: []})
    if signal_id not in signal_dict:
        signals.insert({"signal_id": signal_id, "signal_values": []})
        return {"message": f"signal {signal_id} created"}
    else:
        return {"message": f"signal {signal_id} already exists"}


# Put -> append signal with buffer
@app.put("/signals/append/{signal_id}", tags=["Embedded"])
async def push_signal(signal_id: int, signal_values: list) -> dict:
    signal_dict = json.loads(signals.fetch())
    if signal_id in signal_dict:
        for value in signal_values:
            signal_dict[signal_id].append(value)

        signals.update({
            "signal_id": signal_id,
            "signal_values": signal_dict[signal_id]
        })
        return {"message": f"signal {signal_id} appended"}
    else:
        return {"message": f"signal {signal_id} does not exist"}


# Delete --> delete signal
@app.delete("/signals/{signal_id}", tags=["Embedded"])
async def delete_signal(signal_id: int) -> dict:
    if signal_id in signal_dict.keys():
        signal_dict[signal_id].pop()
        signals.delete("signal_id", signal_id)
        return {"signal_id": signal_id, "message": "signal deleted"}
    else:
        return {"signal_id": signal_id, "message": "signal not found"}


# Delete -> delete all signals
@app.delete("/signals/all/", tags=["Backend", "Embedded"])
async def delete_all_signals(confirm: str) -> dict:
    if confirm == "y":
        signals_dict = signals.fetch().items

        for item in signals_dict:
            # print("deleted item: ", item["signal_id"])
            signals.delete(item["key"])

        return {"message": "all signals deleted"}
    else:
        return {"message": "confirmation failed"}


# Get --> calculate signal statistics
@app.get("/signals/stats/{signal_id}", tags=["Frontend"])
async def calculate_signal_stats(signal_id: int) -> dict:
    signals_dict = signals.fetch().items
    # print (signals_dict)
    for item in signals_dict:
        item["signal_id"] = int(item["signal_id"])
        if item["signal_id"] == signal_id:
            signal_values = item["signal_values"]
            return {
                "signal_id": signal_id,
                # "signal_values": signal_values,
                "signal_stats": {
                    "mean": sum(signal_values) / len(signal_values),
                    "median": np.median(signal_values),
                    "max": max(signal_values),
                    "min": min(signal_values),
                    "std": np.std(signal_values),
                    "var": np.var(signal_values),
                    "sampling_rate": signal_dict[signal_id]["fsample"],
                }
            }

    return {"signal_id": signal_id, "message": "signal not found"}


# Get --> gets a subset of the signal
@app.get("/signals/subset/{signal_id}", tags=["Frontend"])
async def get_signal_subset(signal_id: int, start: int, end: int) -> dict:
    signal_values = signal_dict[signal_id]
    return {
        "signal_id": signal_id,
        "signal_values": signal_values[start:end],
        "fsample": 1000
    }


# Get -> gets the last n values of the signal
@app.get("/signals/last/{signal_id}", tags=["Frontend"])
async def get_last_n_values(signal_id: int, n: int) -> dict:
    signal_dict = json.loads(signals.fetch())
    signal_values = signal_dict[signal_id]
    if signal_id in signal_dict.keys():
        return {"signal_id": signal_id, "signal_values": signal_values[-n:]}
    else:
        return {"signal_id": signal_id, "message": "signal not found"}