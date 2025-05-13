import json
from classes import GroupManager
from file_tools.metric_file_parsing import MEM_FILE_PATH
from utils.logger import logger
from global_functions import group_manager


def generate_group_manager_file(group_manager: GroupManager, gm_file_name: str) -> str:
    """
    Provided a health metric object, generate a metric file to store the currently
    contained data. File is named using the metric_name attribute and saved to the
    required directory.

    Arguments:
        health_metric: The metric to be saved to file.

    Returns:
        A string path to the generated file.
    """
    file_path = MEM_FILE_PATH / gm_file_name
    total_group_size = group_manager.record_count

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
        "record_count": str(total_group_size),
        "group_record": group_record,
    }

    try:
        file_path.write_text(json.dumps(preformed_dictionary, indent=4))
    except IOError as e:
        logger.add("ERROR", f"Failed to write GM file: {e}")
        raise

    plural = "" if total_group_size == 1 else "es"
    logger.add(
        "action",
        f"Updated '{gm_file_name}', containing {total_group_size} alias{plural}.",
    )
    return str(file_path)


def exit(_: list) -> None:
    """
    End high level loop. Generates an updated group manager file from the current in-memory
    group manager, and logs the end of program.
    """
    generate_group_manager_file(
        group_manager=group_manager, gm_file_name="aliases.json"
    )
    logger.add("action", "Exiting high level loop now.")
    logger.dump_to_file()
