# import http request library
import requests
import json
import time
import wfdb
import numpy as np


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


url = "https://no1rz2.deta.dev/signals/append/"


def send_signal():
    # read signal from file named file_name
    file_name = "100"
    record = wfdb.rdrecord(file_name, channels=[0])

    buff_size = 100
    full_signal = record.p_signal.tolist()

    for signal in range(0, buff_size, len(record.p_signal)):
        time.sleep(record.fs * buff_size)

        signal_data = signal_data[signal:signal+buff_size]
        # send signal to server
        response = requests.patch(url, data=signal_data)
        print(response.text)


def send_csv_signal():
    '''Send signal from csv file'''
    import pandas as pd
    import os

    # reinitialize signals
    # request deletion of signal id 1
    requests.delete("https://no1rz2.deta.dev/signals/1")

    # request deletion of signal id 2
    requests.delete("https://no1rz2.deta.dev/signals/2")

    # request creation of signal id 1
    fsample1 = 1
    window_sec1 = 20

    signal1data = {
        "signal_id": 1,
        "signal_name": "Heart Rate",
        "signal_values": [], #np.zeros(fsample1 * window_sec1).tolist(),
        "fsample": fsample1,
        "window_sec": window_sec1,
        "decimal_point": 1,
        "alarms": [preset_alarms_dict["hr_brady"], preset_alarms_dict["hr_tachy"]]
    }

    # url encoded data
    signal1data = json.dumps(signal1data)
    print(signal1data)

    response = requests.post(
        "https://no1rz2.deta.dev/signals/new/1", data=signal1data)
    print(response.text)
    # request creation of signal id 2

    fsample2 = 1
    window_sec2 = 20

    signal2data = {
        "signal_id": 2,
        "signal_name": "Resp. Rate",
        "signal_values": [], #np.zeros(fsample2 * window_sec2).tolist(),
        "fsample": fsample2,
        "window_sec": window_sec2,
        "decimal_point": 1,
        "alarms": []
    }

    signal2data = json.dumps(signal2data)
    response = requests.post(
        "https://no1rz2.deta.dev/signals/new/2", data=signal2data)

    print(response.text)

    # get absolute path to csv file using os
    file_path = os.path.join(os.path.dirname(__file__), "test_measure.csv")
    df = pd.read_csv(file_path)
    print(df)
    # get RR column and convert it to list
    RespRate = df["RR"].tolist()
    # get HR column and convert it to list
    HR = df["HR"].tolist()
    # print(RespRate)
    # print(HR)

    sec_delay = 2
    fs = 0.5
    buff_size = round(fs * sec_delay)
    for i in range(0, len(RespRate), buff_size):
        time.sleep(sec_delay/2)
        payload = RespRate[i:i + buff_size]
        payload = json.dumps(payload)
        print(payload)
        response = requests.patch(url+"2", data=payload)
        print(response.text)

        time.sleep(sec_delay/2)
        payload2 = HR[i:i + buff_size]
        payload2 = json.dumps(payload2)
        print(payload2)
        response = requests.patch(url+"1", data=payload2)

        print(response.text)


def send_sine_wave():
    '''Generate random sine wave and send it to server'''
    import numpy as np

    # generate sine wave
    fs = 20
    t = np.arange(0, 10000, 1/fs)
    signal = np.sin(2*np.pi*t)
    sec_delay = 1
    buff_size = fs * sec_delay
    for i in range(0, len(t), buff_size):
        time.sleep(sec_delay)
        signal_data = signal[i:i + buff_size] * 20 * np.random.rand() + 5
        signal_data = json.dumps(signal_data.tolist())
        print(signal_data)
        response = requests.patch(url+"3", data=signal_data)

        print(response.text)


# send_sine_wave()
send_csv_signal()
