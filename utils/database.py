import json

DB_PATH = "database/patient_history.json"

def save_record(record):
    with open(DB_PATH, "r") as file:
        data = json.load(file)

    data.append(record)

    with open(DB_PATH, "w") as file:
        json.dump(data, file, indent=4)
