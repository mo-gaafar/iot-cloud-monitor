from fastapi import FastAPI
import numpy as np
from deta import Deta
from deta.base import Util
import datetime
import json

print("Starting up...")
deta = Deta("a0gu0e0f_F8wAnskRDHQ6PPubHyPui11CSy8KAv8S")
signals = deta.Base("signal-store")
timezone = datetime.timezone(datetime.timedelta(hours=2))

app = FastAPI()

print("Started up. at " + str(datetime.datetime.now(timezone).isoformat()))

MAX_SIGNAL_SAMPLES = 100000

#! hardcoded for now
alarms_dict = {
    "ecg_tachy": {
        "description": "The patient is tachycardic.",
        "type": "ecg",
        "active": True,
        "threshold": 150,
        "debouncing": 5,
        "threshold_direction": "above",
        "threshold_unit": "mV",
    },
    "spo2_hypo": {
        "description": "The patient is hypoxic.",
        "type": "spo2",
        "active": True,
        "threshold": 90,
        "debouncing": 5,
        "threshold_direction": "below",
        "threshold_unit": "%",
    },
    "ecg_brady": {
        "description": "The patient is bradycardic.",
        "type": "ecg",
        "active": True,
        "threshold": 50,
        "debouncing": 5,
        "threshold_direction": "below",
        "threshold_unit": "mV",
    },
    "temp_hypo": {
        "description": "The patient is hypothermic.",
        "type": "temp",
        "active": True,
        "threshold": 35,
        "debouncing": 5,
        "threshold_direction": "below",
        "threshold_unit": "°C",
    },
}

signal_dict = [{
    "signal_id": 1,
    "signal_name": "signal1",
    "signal_values": np.random.rand(1000).tolist(),
    "fsample": 1000,
    "time_created": datetime.datetime.now(timezone).isoformat(),
    "time_updated": datetime.datetime.now(timezone).isoformat()
}, {
    "signal_id": 2,
    "signal_name": "signal2",
    "signal_values": np.random.rand(1000).tolist(),
    "fsample": 1000,
    "time_created": datetime.datetime.now(timezone).isoformat(),
    "time_updated": datetime.datetime.now(timezone).isoformat()
}, {
    "signal_id": 3,
    "signal_name": "signal3",
    "signal_values": np.random.rand(1000).tolist(),
    "fsample": 1000,
    "time_created": datetime.datetime.now(timezone).isoformat(),
    "time_updated": datetime.datetime.now(timezone).isoformat()
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
        if len(signals.fetch({"signal_id": item["signal_id"]}).items) == 0:
            signals.put(item)
        else:
            return {"message": "some signals are already initialized"}
    return {"status": "ok", "message": "signals initialized"}


# Get -> get signals info
@app.get("/signals/all", tags=["Frontend", "Testing"])
async def get_signals() -> dict:
    #get important info from signals (not the whole signal)
    try:
        signals_info = []
        response = signals.fetch().items
        # print(len(response))
        for item in response:
            signals_info.append({
                "signal_id": item['signal_id'],
                "signal_name": item['signal_name'],
                "fsample": item["fsample"],
                "time_created": item['time_created'],
                "time_updated": item['time_updated'],
                "signal_length": len(item['signal_values'])
            })
        if len(signals_info) == 0:
            return {"message": "no signals found"}
        return {"status": "ok", "signals": signals_info}
    except:
        return {"message": "an error occured"}


# Get -> read signal
@app.get("/signals/{signal_id}", tags=["Frontend"])
async def read_signal(signal_id: int) -> dict:
    try:
        signal = signals.fetch({"signal_id": signal_id}).items[0]
        return {
            "signal_values": signal["signal_values"],
            "fsample": signal["fsample"],
            "time_created": signal["time_created"],
            "time_updated": signal["time_updated"]
        }
    except:
        return {"message": "signal not found or an error occured"}


# Post -> create new signal
@app.post("/signals/new/{signal_id}", tags=["Embedded"])
async def create_signal(signal_id: int, signal_name: str,
                        f_sample: int) -> dict:
    # check if signal_id already exists
    if len(signals.fetch({"signal_id": signal_id}).items) == 0:
        signals.insert({
            "signal_id": signal_id,
            "signal_name": signal_name,
            "signal_values": [],
            "fsample": f_sample,
            "time_created": datetime.datetime.now().isoformat(),
            "time_updated": datetime.datetime.now().isoformat()
        })
        return {"message": f"signal {signal_id} created"}
    else:
        return {"message": f"signal {signal_id} already exists"}


# ! Inefficient way to update signal values, stop reading the full signal!
# Patch -> append signal with buffer
@app.patch("/signals/append/{signal_id}", tags=["Embedded"])
async def push_signal(signal_id: int, signal_values: list) -> dict:
    try:
        #search for signal in db
        res = signals.fetch({"signal_id": signal_id}).items[0]
        key = res["key"]

        #clear array if it exceeds max size then append
        if len(res["signal_values"]) > MAX_SIGNAL_SAMPLES:
            if len(res["signal_values"]) + len(
                    signal_values) > MAX_SIGNAL_SAMPLES:
                #clear and append
                signal_values = signal_values
                signals.update({"signal_values": signal_values}, key)
            else:
                if len(signal_values) > MAX_SIGNAL_SAMPLES:
                    return {
                        "message": "input signal values exceed max size",
                        "status": "error"
                    }
        else:
            new_signal_values = Util.Append(signal_values)
            # print("new signal values: ", new_signal_values)
            signals.update(
                {
                    "signal_values": new_signal_values,
                    "time_updated":
                    datetime.datetime.now(timezone).isoformat()
                }, key)

        return {"message": f"signal {signal_id} appended"}

    except:
        return {
            "message":
            f"signal {signal_id} does not exist or an error occured",
            "status": "error"
        }


# Delete -> delete signal
@app.delete("/signals/{signal_id}", tags=["Embedded"])
async def delete_signal(signal_id: int) -> dict:
    try:
        result = signals.fetch({"signal_id": signal_id}).items
        for item in result:
            signals.delete(item["key"])
        return {"message": f"signal {signal_id} deleted"}
    except:
        return {"signal_id": signal_id, "message": "signal not found"}


# Delete -> delete all signals
@app.delete("/signals/all/", tags=["Backend", "Embedded"])
async def delete_all_signals(confirm: str) -> dict:
    """ Write 'y' to confirm deletion of all signals """
    if confirm == "y":
        signals_dict = signals.fetch().items

        for item in signals_dict:
            # print("deleted item: ", item["signal_id"])
            signals.delete(item["key"])

        return {"message": "all signals deleted"}
    else:
        return {"message": "confirmation failed"}


# Get -> calculate signal statistics
@app.get("/signals/stats/{signal_id}", tags=["Frontend"])
async def calculate_signal_stats(signal_id: int) -> dict:
    try:
        item = signals.fetch({"signal_id": signal_id}).items[0]
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
    except:
        return {"signal_id": signal_id, "message": "signal not found"}


#? start time and end time instead?
# Get -> gets a subset of the signal
@app.get("/signals/subset/{signal_id}", tags=["Frontend"])
async def get_signal_subset(signal_id: int, start: int, end: int) -> dict:
    try:
        resp = signals.fetch(query={"signal_id": signal_id}).items[0]

        if len(resp) == 0:
            return {"signal_id": signal_id, "message": "signal not found"}
        else:
            return {
                "signal_id": int(resp['signal_id']),
                "signal_values": resp['signal_values'][start:end],
                "fsample": resp['fsample']
            }
    except:
        return {
            "signal_id": signal_id,
            "message": "signal not found or out of range"
        }


# Get -> gets the last n values of the signal
@app.get("/signals/last/{signal_id}", tags=["Frontend"])
async def get_last_n_values(signal_id: int, n: int) -> dict:
    try:
        signal_values = signals.fetch(query={
            "signal_id": signal_id
        }).items[0]["signal_values"]

        if len(signal_values) != 0:
            return {
                "signal_id": signal_id,
                "signal_values": signal_values[-n:]
            }
    except:
        return {"signal_id": signal_id, "message": "signal not found"}


# Get -> gets last values by seconds using fsample
@app.get("/signals/last/seconds/{signal_id}", tags=["Frontend"])
async def get_last_values_by_seconds(signal_id: int, seconds: float) -> dict:
    try:
        response = signals.fetch(query={"signal_id": signal_id}).items[0]
        signal_values = response["signal_values"]
        fsample = response["fsample"]
        time_updated = response["time_updated"]

        if len(signal_values) != 0:
            n = int(fsample * seconds)
            return {
                "signal_id": signal_id,
                "signal_values": signal_values[-n:],
                "fsample": fsample,
                "time_updated": time_updated
            }
    except:
        return {
            "signal_id": signal_id,
            "message": "signal not found or an error occured"
        }


@app.get("/signals/{signal_id}/alarms/", tags=["Frontend"])
async def check_alarms(signal_id: int) -> dict:
    try:
        # fetch db signal_id
        signal = signals.fetch(query={"signal_id": signal_id}).items[0]
        # get alarms from alarm field of signal_id
        alarms = signal["alarms"]

        # for each alarm in alarms
        for alarm in alarms:
            # get alarm_id
            alarm_id = alarm["alarm_id"]
            # get alarm_type
            alarm_type = alarm["alarm_type"]
            # get alarm_value
            alarm_value = alarm["alarm_value"]
            # get alarm_status
            alarm_status = alarm["alarm_status"]
            # get signal_values
            signal_values = signal["signal_values"]
            # get signal_id
            signal_id = signal["signal_id"]
            # get signal_fsample
            signal_fsample = signal["fsample"]

            # check if alarm is active
            if alarm_status == "active":
                #TODO: finish this function
                pass
                # check if alarm is of type "max"
                # if alarm_type == "max":
                #     # check if signal_value is greater than alarm_value
                #     if max(signal_values) > alarm_value:
                #         # send email
                #         email = EmailMessage()
                #         email["Subject"] = f"Alarm {alarm_id} triggered"
                #         email["From"] = "

    except:
        return {"signal_id": signal_id, "message": "signal not found"}
