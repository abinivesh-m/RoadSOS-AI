import json

FILE_PATH = "data/analytics.json"


def load_analytics():

    with open(FILE_PATH, "r") as file:
        return json.load(file)


def save_analytics(data):

    with open(FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)


def increment(event_name):

    data = load_analytics()

    data[event_name] += 1

    save_analytics(data)