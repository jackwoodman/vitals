import sys
from data.analysis_tools import find_oor
from functions.mgmt_functions import rename, search, show, instantiate, update_units
from file_tools.metric_file_tools import FILE_DIR_NAME, create_metric_dir
from utils.cli_displays import prompt_user, welcome
from data.data_entry import (
    AssistedEntryHandler,
    InputHandler,
    ManualEntryHandler,
    SpeedyEntryHandler,
)
from utils.logger import logger
from utils.plotting import plot_metrics
from high_level_functions.read import read_by_name
from utils.utils import attempt_ingest_from_name, function_mapping_t, generic_hll_function


def high_level_loop():
    # Defines mapping of commands to their respective functions.
    function_mapping: function_mapping_t = {
        "write": write,
        "read": read,
        "graph": graph,
        "manage": manage,
        "analyse": analyse,
        "exit": exit,
    }

    generic_hll_function(sub_func_map=function_mapping, hll_name="main")
    exit(None)


def write(_: list):
    """
    Loop to ingest input for writing new measurements and metrics.
    """
    c_level = "write"
    set_handler = True
    handler_mapping: dict[int, InputHandler] = {
        1: ManualEntryHandler,
        2: AssistedEntryHandler,
        3: SpeedyEntryHandler,
    }
    handler_descriptions: dict[int, str] = {1: "MANUAL", 2: "ASSIST", 3: "SPEEDY"}

    # Run writing loop using this handler.
    logger.add("info", "Entering input loop.")

    while True:
        if set_handler:
            # Get required entry handler, default to manual mode,
            print("\nSelect handler mode (1, 2, or 3): ")
            req_handler = prompt_user(["main", c_level, "handler_select"])
            if req_handler == "exit":
                return
            req_handler = int(req_handler)
            handler_callable: InputHandler = handler_mapping.get(
                req_handler, ManualEntryHandler
            )
            handler_description = handler_descriptions.get(req_handler, "MANUAL")
            logger.add("info", f"Handler set to mode `{req_handler}`")

            # Instantiate the required handler.
            handler: InputHandler = handler_callable(metric_file_path=FILE_DIR_NAME)
            set_handler = False

            print("\nStarting input loop, format is 'metric measurement DDMMYYYY'")
            print("    (type 'exit' to quit, 'handler' to change handler mode)\n")

        # Loop requests.
        new_input = prompt_user(["main", c_level, handler_description])

        # Catch exit request.
        if new_input == "exit":
            logger.add("info", "Exiting input loop.")
            break
        # Backing out to handler select.
        elif new_input == "handler":
            set_handler = True
            continue

        # Pass raw input to handler object.
        handler.handle_input(new_input)


def read(_: list):
    function_mapping: function_mapping_t = {"read_metric": read_by_name}

    generic_hll_function(
        sub_func_map=function_mapping, hll_name="read", proper_name="reading"
    )


def analyse(_: list):
    function_mapping: dict[str, callable] = {
        "find_oor": find_oor,
    }

    generic_hll_function(
        sub_func_map=function_mapping, hll_name="analyse", proper_name="analysis"
    )


def manage(_: list):
    function_mapping: dict[str, callable] = {
        "rename": rename,
        "show": show,
        "search": search,
        "instantiate": instantiate,
        "update_units": update_units,
    }

    generic_hll_function(
        sub_func_map=function_mapping, hll_name="manage", proper_name="management"
    )


def exit(_: list):
    """End high level loop."""
    logger.add("action", "Exiting high level loop now.")
    logger.dump_to_file()


def graph(arguments: list):
    # Read requested file.
    health_metrics = attempt_ingest_from_name(arguments, "graph")

    if health_metrics:
        if not isinstance(health_metrics, list):
            current_plot = health_metrics.graph_metric()
        else:
            current_plot = plot_metrics(health_metrics, show_bounds=True)

        current_plot.show()


if __name__ == "__main__":
    welcome()
    # If no directory exists, generate one.
    create_metric_dir()

    # Start high level loop
    try:
        high_level_loop()
    except KeyboardInterrupt:
        # Do some cleanup before allowing program to close.
        print()
        logger.add("WARNING", "HLL terminated due to interrupt signal.", cli_out=True)
        logger.dump_to_file()
        sys.exit()
