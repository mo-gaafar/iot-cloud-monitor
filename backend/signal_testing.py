# import http request library
import requests
import json
import time
import wfdb

url = "https://no1rz2.deta.dev/signals/append/1"


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
        response = requests.patch(url, data=signal_data)

        print(response.text)


send_sine_wave()
