from classes import MetricGroup
from file_tools.metric_file_parsing import (
    load_metric_from_json,
    read_metric_file_to_json,
)

from global_functions import group_manager
from utils.sequence_matcher import get_closest_match
from file_tools.filepaths import FILE_DIR_NAME, get_filenames_without_extension


def source_metric(metric_input: str) -> MetricGroup:
    """
    Helper function, that will attempt to ingest a health metric from file and return as a HealthMetric object.
    If no name is provided, it will prompt the user, using the prompt_verb if provided.
    If unable to load, will return None.
    """

    # Build health metric object from requested file.
    health_file = read_metric_file_to_json(metric_input)

    # Name not found.
    if not health_file:
        # Look for group.
        if metric_input in group_manager.get_group_names():
            metric_group = group_manager.get_group(metric_input)
            return metric_group

    if not health_file:
        health_file = read_metric_file_to_json(
            get_closest_match(
                metric_input, get_filenames_without_extension(FILE_DIR_NAME)
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
        return metric_group

    return None
