from functions.mgmt_functions import instantiate, rename, search, show, update_units
from high_level_functions.graph import from_names
from high_level_functions.read import read_by_name
from utils.utils import generic_hll_function


from data.data_entry import (
    AssistedEntryHandler,
    InputHandler,
    ManualEntryHandler,
    SpeedyEntryHandler,
)
from file_tools.metric_file_tools import FILE_DIR_NAME
from utils import logger
from utils.cli_displays import prompt_user
from utils.utils import function_mapping_t
from data.analysis_tools import find_oor


def analyse(_: list):
    function_mapping: dict[str, callable] = {
        "find_oor": find_oor,
    }

    generic_hll_function(
        sub_func_map=function_mapping, hll_name="analyse", proper_name="analysis"
    )


def graph(_: list):
    function_mapping: dict[str, callable] = {
        "from_names": from_names,
    }

    generic_hll_function(
        sub_func_map=function_mapping, hll_name="graph", proper_name="graphing"
    )


def read(_: list):
    function_mapping: function_mapping_t = {"read_metric": read_by_name}

    generic_hll_function(
        sub_func_map=function_mapping, hll_name="read", proper_name="reading"
    )


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
