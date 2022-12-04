from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from deta import Deta
from deta.base import Util
import datetime
import json
from starlette.requests import Request

print("Starting up...")
deta = Deta("a0gu0e0f_F8wAnskRDHQ6PPubHyPui11CSy8KAv8S")
signals = deta.Base("signal-store")
timezone = datetime.timezone(datetime.timedelta(hours=2))

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Started up. at " + str(datetime.datetime.now(timezone).isoformat()))

MAX_SIGNAL_SAMPLES = 100000

#! hardcoded for now
preset_alarms_dict = {
    "hr_tachy": {
        "description": "The patient is tachycardic.",
        "type": "hrm",
        "tiggered": True,
        "acknowledged": False,
        "threshold": 120,
        "debouncing": 5,
        "threshold_direction": "above",
        "threshold_unit": "BPM",
        "criticality_increment": 10,
        "alarm_state": "Normal",
    },
    "spo2_hypo": {
        "description": "The patient is hypoxic.",
        "type": "spo2",
        "tiggered": True,
        "acknowledged": False,
        "threshold": 90,
        "debouncing": 5,
        "threshold_direction": "below",
        "threshold_unit": "%",
        "criticality_increment": -5,
        "alarm_state": "Normal",
    },
    "hr_brady": {
        "description": "The patient is bradycardic.",
        "type": "hrm",
        "tiggered": True,
        "acknowledged": False,
        "threshold": 50,
        "debouncing": 5,
        "threshold_direction": "below",
        "threshold_unit": "BPM",
        "criticality_increment": -10,
        "alarm_state": "Normal",
    },
    "temp_hypo": {
        "description": "The patient is hypothermic.",
        "type": "temp",
        "tiggered": True,
        "acknowledged": False,
        "threshold": 35,
        "debouncing": 5,
        "threshold_direction": "below",
        "threshold_unit": "°C",
        "criticality_increment": -0.8,
        "alarm_state": "Normal",
    },
    "temp_hyper": {
        "description": "The patient is hyperthermic.",
        "type": "temp",
        "tiggered": True,
        "acknowledged": False,
        "threshold": 38,
        "debouncing": 5,
        "threshold_direction": "above",
        "threshold_unit": "°C",
        "criticality_increment": 0.8,
        "alarm_state": "Normal",
    },
}

signal_dict = [{
    "signal_id":
    1,
    "signal_name":
    "Heart Rate",
    "signal_values":
    np.random.rand(1000).tolist(),
    "fsample": 1000,
    "window_sec": 30,
    "decimal_point": 1,
    "time_created":
    datetime.datetime.now(timezone).isoformat(),
    "time_updated":
    datetime.datetime.now(timezone).isoformat(),
    "alarms": [preset_alarms_dict["hr_brady"], preset_alarms_dict["hr_tachy"]],
},
    {
    "signal_id": 2,
    "signal_name": "SpO2",
    "signal_values": np.random.rand(1000).tolist(),
    "fsample": 1000,
    "window_sec": 20,
    "decimal_point": 1,
    "time_created": datetime.datetime.now(timezone).isoformat(),
    "time_updated": datetime.datetime.now(timezone).isoformat(),
    "alarms": [preset_alarms_dict["spo2_hypo"]],
},
    {
    "signal_id": 3,
    "signal_name": "Body Temperature",
    "signal_values": np.random.rand(1000).tolist(),
    "fsample": 1000,
    "window_sec": 30,
    "decimal_point": 1,
    "time_created": datetime.datetime.now(timezone).isoformat(),
    "time_updated": datetime.datetime.now(timezone).isoformat(),
    "alarms": [preset_alarms_dict["temp_hypo"], preset_alarms_dict["temp_hyper"]],
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
    # iterate on dict keys
    for item in signal_dict:
        if len(signals.fetch({"signal_id": item["signal_id"]}).items) == 0:
            signals.put(item)
        else:
            return {"message": "some signals are already initialized"}
    return {"status": "ok", "message": "signals initialized"}


# Get -> get signals info
@app.get("/signals/all", tags=["Frontend", "Testing"])
async def get_signals() -> dict:
    # get important info from signals (not the whole signal)
    try:
        signals_info = []
        response = signals.fetch().items
        # print(len(response))
        for item in response:
            signals_info.append({
                "signal_id": item['signal_id'],
                "signal_name": item['signal_name'],
                "fsample": item["fsample"],
                "window_sec": item["window_sec"],
                "decimal_point": item["decimal_point"],
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
async def create_signal(signal_id: int, request: dict) -> dict:
    """ Create new signal 
    Swagger request example:
    {
        "signal_name": "Heart Rate",
        "signal_values": [0.1, 0.2, 0.3, 0.4, 0.5],
        "fsample": 1000,
        "window_sec": 30,
        "decimal_point": 1,
        "alarms": [
            {
                "description": "The patient is bradycardic.",
                "type": "hr",
                "tiggered": 1,
                "acknowledged": 0,
                "threshold": 60,
                "debouncing": 5,
                "threshold_direction": "below",
                "threshold_unit": "bpm",
                "criticality_increment": -0.8,
                "alarm_state": "Normal"
            }]
    }

    """

    try:
        # request_body = await request.json()
        request_body = request

        if len(signals.fetch({"signal_id": signal_id}).items) == 0:
            signals.insert({
                "signal_id": signal_id,
                "signal_name": request_body["signal_name"],
                "signal_values": request_body["signal_values"],
                "fsample": request_body["fsample"],
                "window_sec": request_body["window_sec"],
                "decimal_point": request_body["decimal_point"],
                "time_created": datetime.datetime.now().isoformat(),
                "time_updated": datetime.datetime.now().isoformat(),
                "alarms": request_body["alarms"]
            })
            return {"message": f"signal {signal_id} created",
                    "body": request_body}
        else:
            return {"message": f"signal {signal_id} already exists"}
    except:
        return {"message": "an error occured",
                "body": request_body}

# ! Inefficient way to update signal values, stop reading the full signal!
# Patch -> append signal with buffer


@app.patch("/signals/append/{signal_id}", tags=["Embedded"])
async def push_signal(signal_id: int, signal_values: list) -> dict:
    try:
        # search for signal in db
        res = signals.fetch({"signal_id": signal_id}).items[0]
        key = res["key"]

        # clear array if it exceeds max size then append
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
                    "median": round(np.median(signal_values), 4),
                    "max": max(signal_values),
                    "min": min(signal_values),
                    "std": np.std(signal_values),
                    "var": np.var(signal_values),
                    "sampling_rate": item["fsample"]
                }
            }
    except:
        return {"signal_id": signal_id, "message": "signal not found"}


# ? start time and end time instead?
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

        output_alarms = []

        # for each alarm in signal
        for alarm in alarms:
            # check threshold direction
            alarm = alarm_updater(alarm, signal["signal_values"][:-1])
            output_alarm = format_alarm_msg(alarm)

        return {"signal_id": signal_id,
                "alarms": output_alarms}
    except:
        return {"signal_id": signal_id, "message": "signal not found"}


def format_alarm_msg(alarm: dict):
    return {
        "alarm_key": alarm["key"],
        "alarm_name": alarm.key(),
        "alarm_message": alarm["description"],
        "triggered": alarm["triggered"],
        "threshold": alarm["threshold"],
        "direction": alarm["direction"],
        "last_checked": datetime.datetime.now().isoformat(),

    }


def alarm_updater(alarm: dict, signal: dict):

    fsample = signal["fsample"]
    seconds = alarm["debounce"]
    # get last n values of signal
    n = int(fsample * seconds)
    #! NOTE: This is not the best way to adaptively average a signal,
    #! might not work with ecg for example due to negative values
    signal_part_avg = np.average(signal["signal_values"][-n:])

    if alarm is not None:
        # check if alarm is active
        if alarm["active"] == True:
            # check threshold direction
            if alarm["threshold_direction"] == "above":
                # check if last value is above threshold
                if signal_part_avg > alarm["threshold"]:
                    # set alarm triggered
                    alarm["triggered"] = True
                    # set alarm criticality level
                    alarm["criticality_level"] = get_critical_level(
                        signal_part_avg,
                        alarm["threshold"],
                        alarm["threshold_direction"],
                        alarm["criticality_increment"],
                    )
                else:
                    alarm["triggered"] = False
            elif alarm["threshold_direction"] == "below":
                # check if last value is below threshold
                if signal_part_avg < alarm["threshold"]:
                    # set alarm triggered
                    alarm["triggered"] = True
                    # set alarm criticality level
                    alarm["criticality_level"] = get_critical_level(
                        signal_part_avg,
                        alarm["threshold"],
                        alarm["threshold_direction"],
                        alarm["criticality_increment"],
                    )
                else:
                    alarm["triggered"] = False

            # TODO: implement acknowledgment using timing
            if alarm["triggered"] == True:
                alarm["acknowledged"] = False

            if alarm["acknowledged"] == True:
                alarm["triggered"] = False

    return alarm

# TODO: this can be done better :(


def get_critical_level(signal_val, threshold, threshold_direction, criticality_increment):

    if threshold_direction == "above":
        if signal_val > threshold + criticality_increment*3:
            return "Fatal"
        elif signal_val > threshold + criticality_increment*2:
            return "Critical"
        elif signal_val > threshold + criticality_increment:
            return "Warning"
        else:
            return "Normal"
    elif threshold_direction == "below":
        if signal_val < threshold - criticality_increment*3:
            return "Fatal"
        elif signal_val < threshold - criticality_increment*2:
            return "Critical"
        elif signal_val < threshold - criticality_increment:
            return "Warning"
        else:
            return "Normal"


# websockets
# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         data = await websocket.receive_text()
#         await websocket.send_text(f"Message text was: {data}")
