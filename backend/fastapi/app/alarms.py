from pydantic import BaseModel

#! hardcoded for now
preset_alarms_dict = {
    "hr_tachy": {
        "description": "The patient is tachycardic!",
        "type": "hrm",
        "tiggered": True,
        "threshold": 120,
        "debouncing": 5,
        "threshold_direction": "above",
        "threshold_unit": "BPM",
    },
    "spo2_hypo": {
        "description": "The patient is hypoxic!",
        "type": "spo2",
        "tiggered": True,
        "threshold": 90,
        "debouncing": 5,
        "threshold_direction": "below",
        "threshold_unit": "%",
    },
    "hr_brady": {
        "description": "The patient is bradycardic!",
        "type": "hrm",
        "tiggered": True,
        "threshold": 50,
        "debouncing": 5,
        "threshold_direction": "below",
        "threshold_unit": "BPM",
    },
    "temp_hypo": {
        "description": "The patient is hypothermic!",
        "type": "temp",
        "tiggered": True,
        "threshold": 35,
        "debouncing": 5,
        "threshold_direction": "below",
        "threshold_unit": "°C",
    },
    "temp_hyper": {
        "description": "The patient is hyperthermic!",
        "type": "temp",
        "tiggered": True,
        "threshold": 38,
        "debouncing": 5,
        "threshold_direction": "above",
        "threshold_unit": "°C",
    },
}

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


    
