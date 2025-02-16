from classes import InequalityMeasurement
from mgmt_functions import rename, search, show
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
from utils import attempt_ingest_from_name


def high_level_loop():
    # Defines mapping of commands to their respective functions.
    function_mapping: dict[str, callable] = {
        "write": write,
        "read": read,
        "graph": graph,
        "manage": manage,
        "exit": exit,
    }

    while True:
        # Parse new user input.
        requested_function = prompt_user("main")

        # Split function from arguments.
        if len(func_arg_pair := requested_function.split(" ")) > 1:
            requested_function = func_arg_pair[0]
            arguments = func_arg_pair[1:]
        else:
            arguments = []

        # Attempt to run requested function.
        if requested_function in function_mapping.keys():
            function_mapping[requested_function](arguments)
        else:
            logger.add("warning", f"'{requested_function}' is not recognised.")

        # Catch exit call, assuming exit() handled everything.
        if requested_function == "exit":
            return


def write(_: list):
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
    handler: InputHandler = handler_callable(metric_file_path=FILE_DIR_NAME)

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


def read(arguments: list):
    """
    Loop to handle reading a metric file to HealthMetric object. WIP.

    Accepted arguments:
        Position 1: Name of file to read.

    """
    health_metric = attempt_ingest_from_name(arguments, "read")

    # Check nonzero entries:
    if len(health_metric.entries) > 0:
        print(f"(Found {len(health_metric.entries)} entries)")
        for measurement in health_metric.entries:
            print(
                " - ",
                f"{str(measurement)}{(" "+measurement.unit) if measurement.unit else ""}",
                " -> ",
                measurement.date,
            )

    else:
        print("File is empty.")

    print("\n")


def manage(_: list):
    # Defines mapping of commands to their respective functions.
    function_mapping: dict[str, callable] = {
        "rename": rename,
        "show": show,
        "search": search,
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


def exit(_: list):
    """End high level loop."""
    logger.add("action", "Exiting high level loop now.")
    logger.dump_to_file()


def graph(arguments: list):
    # Initial testing, get single metric to graph.
    # Read requested file.
    health_metric = attempt_ingest_from_name(arguments, "graph")

    if health_metric:
        plot = health_metric.generate_plot()
        plot.show()


if __name__ == "__main__":
    welcome()
    # If no directory exists, generate one.
    create_metric_dir()

    # Start high level loop.
    high_level_loop()
