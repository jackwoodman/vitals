import json
from pathlib import Path
from typing import Optional
from classes import GroupManager, MetricGroup

from file_tools.filepaths import FILE_DIR_NAME, get_filenames_without_extension
from file_tools.metric_file_parsing import (
    MEM_FILE_NAME,
    load_metric_from_json,
    read_metric_file_to_json,
)
from utils.logger import logger
from utils.sequence_matcher import get_closest_match
from utils.utils import attempt_ingest_from_name, flatten_list


def source_metric(metric_input: list[str]) -> MetricGroup:
    """
    Helper function, that will attempt to ingest a health metric from file and return as a HealthMetric object.
    If no name is provided, it will prompt the user, using the prompt_verb if provided.
    If unable to load, will return None.
    """
    found_groups = []

    for target_name in metric_input:
        # Build health metric object from requested file.
        health_file = read_metric_file_to_json(metric_input)

        # Name not found as individual metric.
        if not health_file:
            # Look for group.
            if group_manager.check_if_registered(name=target_name, log_if_found=True):
                metric_group = group_manager.get_group(target_name)
                found_groups.append(metric_group)
                continue

        if not health_file:
            # No group was found ether, find closest match.
            target_name = metric_input[0]
            health_file = read_metric_file_to_json(
                get_closest_match(
                    target_name, get_filenames_without_extension(FILE_DIR_NAME)
                )
            )

        # Build metric object and return.
        if health_file:
            ingested_metric = load_metric_from_json(health_file)
            metric_group = MetricGroup(
                unit=ingested_metric.unit,
                initial_metrics=[ingested_metric],
                group_name="Temporary storage.",
            )
            found_groups.append(metric_group)
        else:
            # Could not match closest. This shouldn't be possible.
            logger.add("Error", f"All attempts at reading {health_file} failed.")

    # Check that any groups were found.
    if len(found_groups) == 0:
        logger.add("warn", "Unable to find any groups from source attempt.")
        return None

    # Combined all found groups.
    main_group: MetricGroup = found_groups[0]
    found_groups.pop(0)
    for found_group in found_groups:
        main_group = main_group.combine_groups(found_group)

    return main_group


def read_group_manager_file_to_json(source_path: str) -> dict:
    """
    Returns JSON object representing the alias file

    Returns:
        JSON dict of alias file.
    """

    try:
        # Write updated data back to the file
        with open(source_path, "r") as alias_file:
            data = json.load(alias_file)
        return data

    except FileNotFoundError:
        warning_text = f"File '{source_path} could not be found."
        logger.add("WARNING", warning_text)
        return None


def load_group_manager_from_json(
    gm_json: dict,
    metric_sourcer: callable,
    group_manager: Optional[GroupManager] = None,
) -> GroupManager:
    """
    Given a JSON dictionary representing a group manager save file, and a
    metric sourcer function, return a GroupManager object.

    If the metric sourcer, or any other part of the loading process fails,
    this function returns an empty GroupManager.

    Args:
        gm_json: Dictionary of the loaded JSON.
        metric_sourcer: Function callable of the required metric sourcer.

    Returns:
        The loaded GroupManager object.

    """
    new_manager = group_manager if group_manager else GroupManager()

    if gm_json:
        for group_name, group in gm_json.get("group_record").items():
            # Generate MetricGroup from input.
            new_group = MetricGroup(unit=group.get("unit", None), group_name=group_name)
            new_group.add_metrics(
                flatten_list(
                    input_list=[
                        metric_sourcer(metric_input=input_metric_name).as_list()
                        for input_metric_name in group.get("metric_dict")
                    ]
                )
            )

            # Register this group with the GroupManager.
            new_manager.register_group(group_name, new_group)

    return new_manager


def remember(arguments: list[str]):
    """
    Gathers a set of Metrics into a MetricGroup with a given name, and
    registers that MetricGroup with the GroupManager.

    Format of arguments is:
        "[METRIC 1], [METRIC 2], ..., [METRIC n] as [GROUP NAME]"

    The keyword "as" is required to separate the list of metric names, with
    the name of the metric group.
    """
    # Cannot distinguish metric names from group name.
    if "as" not in arguments:
        return None

    # Grab names of metrics.
    separator_index = arguments.index("as")
    target_metrics, group_name = arguments[:separator_index], arguments[-1]

    # Initialise group.
    new_group = MetricGroup()

    # Register metrics with new group.
    new_group.add_metrics(
        new_metrics=attempt_ingest_from_name(metric_input=target_metrics)
    )

    # Register group with Group Manager.
    group_manager.register_group(group_name=group_name, group=new_group)
    logger.add(
        "action",
        f"Registered group '{group_name}' containing '{new_group.count}' Metrics with GroupManager.",
        cli_out=True,
    )


def forget(arguments: list[str]):
    """
    For each MetricGroup name provided, deregister that group with the
    GroupManager.

    Arguments:
        arguments: List of strings representing names to be forgotton.

    """
    for name in arguments:
        # Name is recognised, deregister corresponding group.
        if name in group_manager.get_group_names():
            group_manager.remove_group(name)
            logger.add("action", "Forgot group named '{name}'.")
        else:
            # Name not found.
            logger.add("warning", f"Group named '{name}' not found in memory.")


# Initialise GroupManager from source file.
group_manager_source = f"{MEM_FILE_NAME}/aliases.json"
group_manager_json = read_group_manager_file_to_json(source_path=group_manager_source)
group_manager = load_group_manager_from_json(
    gm_json=group_manager_json,
    metric_sourcer=source_metric,
    group_manager=GroupManager(source_file=Path(group_manager_source)),
)
logger.add(
    "info",
    f"GroupManager initialised. Found '{group_manager.record_count}' aliases in '{str(group_manager.get_source_file())}'.",
    cli_out=True,
)

global_function_register: dict[str, callable] = {"remember": remember, "forget": forget}
