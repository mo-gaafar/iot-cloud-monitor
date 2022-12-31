from pydantic import BaseModel
import numpy as np

#! hardcoded for now
preset_alarms_dict = {
    "hr_tachy": {
        "description": "The patient is tachycardic!",
        "type": "hrm",
        "triggered": True,
        "threshold": 120,
        "debouncing": 5,
        "threshold_direction": "above",
        "threshold_unit": "BPM",
    },
    "spo2_hypo": {
        "description": "The patient is hypoxic!",
        "type": "spo2",
        "triggered": False,
        "threshold": 90,
        "debouncing": 5,
        "threshold_direction": "below",
        "threshold_unit": "%",
    },
    "hr_brady": {
        "description": "The patient is bradycardic!",
        "type": "hrm",
        "triggered": False,
        "threshold": 50,
        "debouncing": 5,
        "threshold_direction": "below",
        "threshold_unit": "BPM",
    },
    "temp_hypo": {
        "description": "The patient is hypothermic!",
        "type": "temp",
        "triggered": False,
        "threshold": 35,
        "debouncing": 5,
        "threshold_direction": "below",
        "threshold_unit": "°C",
    },
    "temp_hyper": {
        "description": "The patient is hyperthermic!",
        "type": "temp",
        "triggered": False,
        "threshold": 38,
        "debouncing": 5,
        "threshold_direction": "above",
        "threshold_unit": "°C",
    },
}



def alarm_updater(alarm: dict, signal_values: list, fsample: float):

    seconds = alarm["debounce"]
    # get last n values of signal
    n = int(fsample * seconds)

    # clip to maximum just in case
    if n > len(signal_values):
        n = len(signal_values)

    #! NOTE: This is not the best way to adaptively average a signal,
    #! might not work with ecg for example due to negative values

    signal_part_avg = np.average(signal_values[-n:])

    if alarm is not None:
        # check threshold direction
        if alarm["threshold_direction"] == "above":
            # check if last value is above threshold
            if signal_part_avg > alarm["threshold"]:
                # set alarm triggered
                alarm["triggered"] = True
            else:
                alarm["triggered"] = False
        elif alarm["threshold_direction"] == "below":
            # check if last value is below threshold
            if signal_part_avg < alarm["threshold"]:
                # set alarm triggered
                alarm["triggered"] = True
            else:
                alarm["triggered"] = False

    return alarm

def format_alarm_msg(alarm: dict):
    return {
        "notification_id": np.random.randint(0, 1000000),
        "title": "Monitor Alarm",
        "body": "Warning: " + alarm["Description"],
    }


def triggered_alarms(alarms: list, formatted: bool = False):
    output_alarms = []
    for alarm in alarms:
        if alarm["triggered"]:
            if formatted:
                output_alarms.append(format_alarm_msg(alarm))
            else:
                output_alarms.append(alarm)
    return output_alarms


# alarm notification request
# alarm checking function
#


# all alarms request
# return formatted alarm message
# {

#     [
#         {"alarm_key": "1",
#          "alarm_name": "1",
#          "alarm_message": ??,
#          "threshold": 1,
#          "criticality_level": ??,
#          "direction": "above",
#          "last_checked": "2021-05-19T15:12:12.000000"},

#         {"alarm_key": "2",
#          "alarm_name": "2",
#          "alarm_message":,
#          "threshold": 2,
#          "criticality_level": ??,
#          "direction": "below",
#          "last_checked": "2021-05-19T15:12:12.000000"
#          }
#     ]
# }

# TODO: add alarm notification message

# {
#     [
#     {"notification_id": 1,
#     "title": "Alarm triggered",
#     "body": "Alarm triggered"}
#     ,
#     {"notification_id": 2,
#     "title": "Alarm triggered",
#     "body": "Alarm triggered"}

#     ]
# }
