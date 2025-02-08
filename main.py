from classes import InequalityMeasurement
from mgmt_functions import rename
from metric_file_tools import (
    FILE_DIR_NAME,
    create_metric_dir,
    load_metric_from_json,
    read_metric_file_to_json,
)
from cli_displays import prompt_user, welcome
from data_entry import (
    AssistedEntryHandler,
    InputHandler,
    ManualEntryHandler,
    SpeedyEntryHandler,
)
from logger import logger


def high_level_loop():
    # Defines mapping of commands to their respective functions.
    function_mapping: dict[str, callable] = {
        "write": write,
        "read": read,
        "manage": manage,
        "exit": exit,
    }

    while True:
        # Parse new user input.
        requested_function = prompt_user("main")

        # Attempt to run requested function.
        if requested_function in function_mapping.keys():
            function_mapping[requested_function]()
        else:
            logger.add("warning", f"'{requested_function}' is not recognised.")

        # Catch exit call, assuming exit() handled everything.
        if requested_function == "exit":
            return


def write():
    """
    Loop to ingest input for writing new measurements and metrics.
    """
    c_level = "write"
    handler_mapping: dict[int, InputHandler] = {
        1: ManualEntryHandler,
        2: AssistedEntryHandler,
        3: SpeedyEntryHandler,
    }
    handler_descriptions: dict[int, str] = {1: "MANUAL", 2: "ASSIST", 3: "SPEEDY"}

    # Get required entry handler, default to manual mode,
    print("\nSelect handler mode (1, 2, or 3): ")
    req_handler = int(prompt_user(["main", c_level]))
    handler_callable: InputHandler = handler_mapping.get(
        req_handler, ManualEntryHandler
    )
    handler_description = handler_descriptions.get(req_handler, "MANUAL")

    # Instantiate the required handler.
    handler: InputHandler = handler_callable(
        metric_file_path=FILE_DIR_NAME
    )

    # Run writing loop using this handler.
    logger.add("info", "Entering input loop.")
    print("\nStarting input loop, format is 'metric measurement DDMMYYYY'")
    print("    (type 'exit' to quit)\n")
    while True:
        new_input = prompt_user(["main", c_level, handler_description])

        # Catch exit request.
        if new_input == "exit":
            logger.add("info", "Exiting input loop.")
            break

        # Pass raw input to handler object.
        handler.handle_input(new_input)


def read():
    """
    Loop to handle reading a metric file to HealthMetric object. WIP.
    """
    print("read which metric file?")
    target_metric = prompt_user("read")
    health_file = read_metric_file_to_json(target_metric)
    health_metric = load_metric_from_json(health_file)

    print(f"Ingested '{health_metric.metric_name}':")
    for measurement in health_metric.entries:

        print(" - ", f"{str(measurement)}{(" "+measurement.unit) if measurement.unit else ""}", " -> ", measurement.date)

    print()

def manage():
    # Defines mapping of commands to their respective functions.
    function_mapping: dict[str, callable] = {
        "rename": rename,
    }

    print("Entering management terminal.")
    logger.add("info", "Entered management terminal.")

    while True:
        # Parse new user input.
        requested_function = input("(manage) -> ").lower()

        # Catch exit call, assuming exit() handled everything.
        if requested_function == "exit":
            logger.add("info", "Exiting management terminal.")
            break

        # Attempt to run requested function.
        if requested_function in function_mapping.keys():
            function_mapping[requested_function]()
        else:
            logger.add("warning", f"'{requested_function}' is not recognised.")


def exit():
    """End high level loop."""
    logger.add("action", "Exiting high level loop now.")
    logger.dump_to_file()


if __name__ == "__main__":
    welcome()
    # If no directory exists, generate one.
    create_metric_dir()

    # Start high level loop.
    high_level_loop()
