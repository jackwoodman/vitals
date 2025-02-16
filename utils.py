from typing import Optional, Union

from classes import HealthMetric
from cli_displays import prompt_user
from metric_file_tools import (
    FILE_DIR_NAME,
    get_filenames_without_extension,
    load_metric_from_json,
    read_metric_file_to_json,
)
from sequence_matcher import get_closest_match


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


def attempt_ingest_from_name(
    metric_input: Optional[Union[str, list]] = None,
    prompt_verb: str = "load",
    verbose: bool = False,
    match_close_names: bool = False,
) -> Optional[HealthMetric]:
    """
    Helper function, that will attempt to ingest a health metric from file and return as a HealthMetric object.
    If no name is provided, it will prompt the user, using the prompt_verb if provided.
    If unable to load, will return None.
    """

    # If none provided, ask the user for the name.
    if not metric_input:
        print(f"{prompt_verb} which metric file?")
        metric_name = prompt_user(prompt_verb)
    elif isinstance(metric_input, list):
        # Argument input from the HLL.
        metric_name = metric_input[0]
    else:
        # Input is valid as is, this case is just for clarity.
        metric_name = metric_input

    # Build health metric object from requested file.
    health_file = read_metric_file_to_json(metric_name) or (
        read_metric_file_to_json(
            get_closest_match(
                metric_name, get_filenames_without_extension(FILE_DIR_NAME)
            )
        )
        and print("Matching nearest. REPLACE ME WITH A LOG.")
    )

    # Build metric object and return.
    if health_file:
        ingested_metric = load_metric_from_json(health_file)
        if verbose and ingested_metric:
            print(f"Ingested and built '{ingested_metric.metric_name}'.")

        return ingested_metric

    return None
