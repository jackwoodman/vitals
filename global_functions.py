from classes import GroupManager, MetricGroup
from file_tools.metric_file_parsing import (
    load_group_manager_from_json,
    read_group_manager_file_to_json,
)
from utils.logger import logger
from utils.utils import attempt_ingest_from_name
from sourcer import source_metric


def remember(arguments: list[str]):
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
    for name in arguments:
        if name in group_manager.get_group_names():
            group_manager.remove_group(arguments)


group_manager = GroupManager()
group_manager_json = read_group_manager_file_to_json()
group_manager = load_group_manager_from_json(
    gm_json=group_manager_json, metric_sourcer=source_metric
)

global_function_register: dict[str, callable] = {"remember": remember, "forget": forget}
