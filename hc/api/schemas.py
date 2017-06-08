check = {
    "properties": {
        "name": {"type": "string"},
        "tags": {"type": "string"},
        "timeout": {"type": "number", "minimum": 1, "maximum": 186624000},
        "grace": {"type": "number", "minimum": 1, "maximum": 186624000},
        "channels": {"type": "string"}
    }
}
