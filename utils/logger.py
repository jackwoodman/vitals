from enum import Enum
from datetime import datetime


class LogType(Enum):
    Info = "INFO"
    Status = "STATUS"
    Action = "ACTION"
    Warning = "WARNING"
    Error = "ERROR"
    Unknown = "UNKNOWN"


class LogEntry:
    """
    An object representing a log event.
    """

    def __init__(self, log_type_str: str, log_string: str):
        self.type: LogType = LogType(log_type_str.upper())
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
    accepted_log_types: list[str] = [log.value for log in LogType]

    def __init__(self, display_logs: bool = False):
        self.init_time = datetime.now()
        self.collection_id = abs(hash(self.init_time))
        self.collection_name = (
            f"log_{str(self.init_time).split('.')[0].replace(' ', '_')}"
        )
        self.should_display_logs = display_logs

    def add(self, log_level: str, log: str, cli_out: bool = False):
        """
        Add new log entry from text.

        Arguments:
            log_level: The log level identifier.
            log: The string to be logged.
            cli_out: If true, will print to output.
        """

        if log_level.upper() in self.accepted_log_types:
            log_event = LogEntry(log_type_str=log_level.upper(), log_string=log)

            if cli_out:
                print(f"{log_level.upper()} - {log}")
        else:
            log_event = LogEntry(log_type_str="unknown", log_string=log)

            if cli_out:
                print(f"UNKNOWN - {log}")

        self.collection.append(log_event)

        if self.should_display_logs:
            print(log_event.to_string())

        return log_event

    def add_entry(self, new_log: LogEntry):
        """
        Add new log entry from LogEntry object.

         Arguments:
            new_log: The LogEntry to be logged.
        """
        self.collection.append(new_log)

        if self.should_display_logs:
            print(new_log.to_string())

    def count(self) -> int:
        """
        Return the number of Logs present in the collector.
        """
        return len(self.collection)

    def dump_to_file(self) -> str:
        """
        Assuming end of logging operations, create a new file and write
        the collected logs to the file.

        Returns:
            Filepath to the generated file.
        """
        filepath = f"logs/{self.collection_name}.txt"
        with open(filepath, "w") as log_file:
            log_file.write(f"Health Log - {self.collection_id}\n")
            log_file.write(f"File init at {self.init_time}\n\n")

            for log in self.collection:
                log_file.write(log.to_string())
                log_file.write("\n")

            log_file.write(f"\nFile dumped at {datetime.now()}")

        return filepath


# Initialise logger.
logger = LogCollector()
