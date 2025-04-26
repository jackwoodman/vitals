
from file_tools.filepaths import FILE_DIR_PATH


def create_metric_dir():
    """
    Creates a dir at the required path, if not existing already.

    Returns:
        Bool indicating if a directory was created (True) or not (False).
    """
    if FILE_DIR_PATH.exists():
        return False

    FILE_DIR_PATH.mkdir(parents=True, exist_ok=True)
    return True

def is_inequality_value_str(input_str: str) -> bool:
    """
    Test whether input string is a candidate for representing an "InequalityValue".

    Arguments:
        input_str: The string, representing a value, to be tested.

    Returns:
        Bool indicating whether value looks like an inequality value, or not.
    """
    if "<" in str(input_str) or ">" in str(input_str):
        return True
    return False
