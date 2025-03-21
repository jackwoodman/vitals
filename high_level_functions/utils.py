from utils import logger


def exit(_: list):
    """End high level loop."""
    logger.add("action", "Exiting high level loop now.")
    logger.dump_to_file()
