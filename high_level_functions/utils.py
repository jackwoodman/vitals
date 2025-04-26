import json
from classes import GroupManager
from file_tools.metric_file_parsing import MEM_FILE_PATH
from utils.logger import logger
from global_functions import group_manager


def generate_group_manager_file(group_manager: GroupManager) -> str:
    """
    Provided a health metric object, generate a metric file to store the currently
    contained data. File is named using the metric_name attribute and saved to the
    required directory.

    Arguments:
        health_metric: The metric to be saved to file.

    Returns:
        A string path to the generated file.
    """
    file_path = MEM_FILE_PATH / "aliases.json"

    group_record = {
        group_name: {
            "enforce_units": group.enforce_units,
            "unit": group.unit,
            "count": group.count,
            "metric_dict": [
                metric.metric_name for metric in group.metric_dict.values()
            ],
        }
        for group_name, group in group_manager.group_record.items()
    }

    preformed_dictionary = {
        "record_count": str(group_manager.record_count),
        "group_record": group_record,
    }

    try:
        file_path.write_text(json.dumps(preformed_dictionary, indent=4))
    except IOError as e:
        logger.add("ERROR", f"Failed to write GM file: {e}")
        raise

    logger.add("action", f"Created new metric file `gm_{group_manager.id}.json`.")
    return str(file_path)


def exit(_: list):
    """End high level loop."""
    generate_group_manager_file(group_manager=group_manager)
    logger.add("action", "Exiting high level loop now.")
    logger.dump_to_file()
