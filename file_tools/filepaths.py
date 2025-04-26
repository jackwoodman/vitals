from pathlib import Path


FILE_VERS = 9
FILE_DIR_NAME = "metric_files"
FILE_DIR_PATH = Path(FILE_DIR_NAME)


def get_filenames_without_extension(directory):
    """Returns a list of filenames in the given directory without their extensions."""
    directory_path = Path(directory) if isinstance(directory, str) else directory
    filenames = [file.stem for file in directory_path.iterdir() if file.is_file()]

    return filenames
