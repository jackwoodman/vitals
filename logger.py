from pathlib import Path
from enum import Enum
from datetime import datetime


class LogType(Enum):
    Info = "INFO"
    Status = "STAT"
    Action = "ACTN"
    Warning = "WARN"
    Error = "ERRO"


class LogEntry:
    """
    An object representing a log event.
    """

    def __init__(self, log_type_str: str, log_string: str):
        self.type: LogType = LogType(log_type_str)
        self.value: str = log_string
        self.time: datetime = datetime.now()

    def to_string(self) -> str:
        return f"{str(self.time)} ({str(self.type.value)}) - " f"{self.value}"


class LogCollector:
    """
    Singleton object to collect LogEntry objects as they
    are generated. Has functionality to dump to a log file for
    recording.
    """

    collection: list[LogEntry] = []

    def __init__(self, display_logs: bool = False):
        self.init_time = datetime.now()
        self.collection_id = hash(self.init_time)
        self.collection_name = (
            f"log_{str(self.init_time).split('.')[0].replace(' ', '_')}"
        )
        self.should_display_logs = display_logs

    def add(self, new_log: LogEntry):
        self.collection.append(new_log)

        if self.should_display_logs:
            print(new_log.to_string())

        if self.count() >= 5:
            self.dump_to_file()

    def count(self) -> int:
        return len(self.collection)

    def dump_to_file(self):
        filepath = f"logs/{self.collection_name}.txt"
        with open(filepath, "w") as log_file:
            log_file.write(f"Health Log - {self.collection_id}\n")
            log_file.write(f"File init at {self.init_time}\n\n")

            for log in self.collection:
                log_file.write(log.to_string())
                log_file.write("\n")

            log_file.write(f"\n\File dumped at {datetime.now()}")
