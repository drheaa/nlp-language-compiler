INTENT_TEMPLATES = [
    {
        "name": "threshold_action",
        "examples": [
            "If temperature exceeds 30, turn on the AC.",
            "Turn on the AC when temperature is above 30.",
            "Close the windows when the air quality index exceeds 150.",
            "If humidity is greater than 70, dehumidify the room.",
            "Notify me when CPU usage goes above 90 percent."
        ],
        "canonical_form": "IF <metric> <operator> <threshold> THEN <action>",
        "slots": ["metric", "operator", "threshold", "action"],
        "slot_hints": {
            "threshold": "numeric threshold is missing",
            "operator": "comparison operator is missing",
            "metric": "metric/variable is unclear",
            "action": "action is unclear"
        },
    },
    {
        "name": "event_action",
        "examples": [
            "When the door opens, turn on the hallway light.",
            "If motion is detected, start recording.",
            "When the kettle finishes, send a notification."
        ],
        "canonical_form": "WHEN <event> THEN <action>",
        "slots": ["event", "action"],
        "slot_hints": {
            "event": "event trigger is unclear",
            "action": "action is unclear"
        },
    },
    {
        "name": "unless_negation",
        "examples": [
            "Turn on the heater unless a window is open.",
            "Water the garden unless it is raining.",
            "Lock the door unless someone is inside."
        ],
        "canonical_form": "<action> UNLESS <condition>",
        "slots": ["action", "condition"],
        "slot_hints": {
            "condition": "exception/negation condition is unclear",
            "action": "action is unclear"
        },
    },
]
