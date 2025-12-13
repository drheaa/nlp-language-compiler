import random

METRICS = [
    "temperature",
    "humidity",
    "air quality index",
    "CPU usage",
    "queue length",
    "battery level"
]

ACTIONS = [
    "turn on the AC",
    "send a notification",
    "close the windows",
    "activate the alarm",
    "start recording",
    "decrease the fan speed"
]

THRESHOLDS = ["20", "25", "30", "70", "80", "90", "150"]

TIME_PHRASES = [
    "after 5 minutes",
    "during the night",
    "when it is evening",
    "after a while",
    "as soon as possible"
]

def simple_condition():
    return f"If {random.choice(METRICS)} exceeds {random.choice(THRESHOLDS)}, {random.choice(ACTIONS)}."

def negation():
    return f"{random.choice(ACTIONS).capitalize()} unless {random.choice(METRICS)} is low."

def multi_condition():
    return (
        f"If {random.choice(METRICS)} exceeds {random.choice(THRESHOLDS)} "
        f"and {random.choice(METRICS)} is high, {random.choice(ACTIONS)}."
    )

def temporal():
    return f"{random.choice(ACTIONS).capitalize()} {random.choice(TIME_PHRASES)}."

def ambiguous():
    return f"{random.choice(ACTIONS).capitalize()} when {random.choice(METRICS)} is high."
