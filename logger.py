from datetime import datetime

LOG_FILE = "data/logs.txt"


def log_event(message):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    log_line = (
        f"[{timestamp}] {message}\n"
    )

    with open(
        LOG_FILE,
        "a"
    ) as file:

        file.write(log_line)