from typing import Optional, Union
from file_tools.metric_file_parsing import load_metric_from_json
from utils.logger import LogEntry, logger
from classes import HealthMetric
from utils.cli_displays import prompt_user
from file_tools.metric_file_tools import (
    FILE_DIR_NAME,
    get_filenames_without_extension,
    read_metric_file_to_json,
)
from utils.sequence_matcher import get_closest_match

function_mapping_t = dict[str, callable]


def generic_hll_function(
    sub_func_map: function_mapping_t, hll_name: str, proper_name: str = None
):
    """
    Provides a generic HLL function interface. Some HLL functions have complex requirements,
    such as write() or read(). Others, such as manage() and analyse() are simple functions, identical
    except for their subfunctions, and their name. This function is an attempt to template out that
    identical functionality to reduce code reuse. It should suit most generic HLL functions, until their
    complexity grows, at which point this can be replaced with a bespoke handler function.

    Args:
        sub_fun_map: A mapping of subfunction names to function callables.
        hll_name: The name of the function implementing this function.
        proper_name: The name of the terminal.

    """
    terminal_name = proper_name or hll_name
    available_functions = sub_func_map.keys()
    logger.add("info", f"Entered {terminal_name} terminal.", cli_out=True)

    while True:
        # Parse new user input.
        requested_function = prompt_user(hll_name).lower()

        # Split function from arguments.
        if len(func_arg_pair := requested_function.split(" ")) > 1:
            requested_function = func_arg_pair[0]
            arguments = func_arg_pair[1:]
        else:
            arguments = []

        # Catch exit call, assuming exit() handled everything.
        if requested_function == "exit":
            logger.add("info", f"Exiting {terminal_name} terminal.", cli_out=True)
            break
        # Catch request for help.
        elif requested_function == "help":
            print(f"Functions supported by '{hll_name}':")
            for function_name in available_functions:
                print(f" - {function_name}")
            print()
            continue

        # Attempt to find function name if not correct.
        if requested_function not in available_functions:
            closest_match = get_closest_match(requested_function, available_functions)
            logger.add(
                "warning",
                f"'{requested_function}' was not recognised. '{closest_match}' was closest match.",
            )
            requested_function = closest_match

        sub_func_map[requested_function](arguments)


def is_verbatim(input_text: str) -> Optional[str]:
    """
    Check if a user input is a "verbatim request", meaning it should
    be parsed without checking for correctness or close matches.

    If verbatim, return the string without the verbatim signifier.
    Otherwise, returns None.

    Arguments:
        input_text: String to check for verbatimness.

    Returns:
        None if not verbatim request, otherwise verbatim text.
    """

    # First check - wrapped in quotes.
    if input_text[0] == '"' and input_text[-1] == '"':
        return input_text[1:-1]

    # Second check - ends with an asterix.
    elif input_text[-1] == "*" and len(input_text) > 1:
        return input_text[:-1]

    # Any other checks go here.

    # Not verbatim
    return None


def source_metric(metric_input: str):
    """
    Helper function, that will attempt to ingest a health metric from file and return as a HealthMetric object.
    If no name is provided, it will prompt the user, using the prompt_verb if provided.
    If unable to load, will return None.
    """
    metric_objects = []

    # Build health metric object from requested file.
    health_file = read_metric_file_to_json(metric_input)

    # Name not found.
    if not health_file:
        # Look for group.
        ####

    # if not health_file

    # Build metric object and return.
    if health_file and not isinstance(health_file, LogEntry):
        ingested_metric = load_metric_from_json(health_file)
        if verbose and ingested_metric:
            print(f"Ingested and built '{ingested_metric.metric_name}'.")
        metric_objects.append(ingested_metric)

    # Return list only if greater than one, for backwards compat reasons.
    if metric_objects:
        return metric_objects if len(metric_objects) > 1 else metric_objects[0]
    return None


def attempt_ingest_from_name(
    metric_input: Optional[Union[str, list]] = None,
    prompt_verb: str = "load",
    verbose: bool = False,
) -> Optional[Union[list[HealthMetric], HealthMetric]]:
    """
    Helper function, that will attempt to ingest a health metric from file and return as a HealthMetric object.
    If no name is provided, it will prompt the user, using the prompt_verb if provided.
    If unable to load, will return None.
    """
    metric_objects = []
    # If none provided, ask the user for the name.
    if not metric_input:
        print(f"{prompt_verb} which metric file?")
        metric_names = [prompt_user(prompt_verb)]
    elif isinstance(metric_input, list):
        # Argument input from the HLL. May be multiple.
        metric_names = metric_input
    else:
        # Input is valid as is, this case is just for clarity.
        metric_names = [metric_input]

    for metric_name in metric_names:
        # Build health metric object from requested file.
        health_file = read_metric_file_to_json(metric_name) or (
            read_metric_file_to_json(
                get_closest_match(
                    metric_name, get_filenames_without_extension(FILE_DIR_NAME)
                )
            )
            and logger.add(
                "INFO", f"{metric_name} could not be found, matching with closest."
            )
        )

        # Build metric object and return.
        if health_file and not isinstance(health_file, LogEntry):
            ingested_metric = load_metric_from_json(health_file)
            if verbose and ingested_metric:
                print(f"Ingested and built '{ingested_metric.metric_name}'.")
            metric_objects.append(ingested_metric)

    # Return list only if greater than one, for backwards compat reasons.
    if metric_objects:
        return metric_objects if len(metric_objects) > 1 else metric_objects[0]
    return None
