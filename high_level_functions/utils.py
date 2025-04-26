from file_tools.metric_file_parsing import generate_group_manager_file
from sourcer import logger
from global_functions import group_manager


def exit(_: list):
    """End high level loop."""
    generate_group_manager_file(group_manager=group_manager)
    logger.add("action", "Exiting high level loop now.")
    logger.dump_to_file()
