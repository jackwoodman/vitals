from pathlib import Path
from cli_displays import prompt_user
from metric_file_tools import rename_health_file
from logger import logger


def rename():
    """
    Helper function to rename name of metric, both file and contents.
    """
    old_metric_name = input("-> rename which metric file? ")
    new_metric_name = input(f"-> rename '{old_metric_name}' to what? ")

    print(f"Renaming '{old_metric_name}' to '{new_metric_name}'...")
    rename_health_file(
        current_metric_name=old_metric_name, new_metric_name=new_metric_name
    )

    logger.add("action", f"Renamed metric '{old_metric_name}' to '{new_metric_name}'")


def show():
    """
    Show all files in the metric_files directory.
    """
    count = 0

    for file in Path("metric_files/").iterdir():
        print(file.stem)
        count += 1

    print(f"\nFound {count} files.")


def search():
    """
    Show all files in the metric_files directory matching a given string.
    """
    count = 0
    found = 0
    print("Input file to search for: ")
    to_search = prompt_user(["manage", "search"])
    print("\nresults:")
    for file in Path("metric_files/").iterdir():
        if to_search in file.stem:
            print("    ", file.stem)
            found += 1
        count += 1

    print(f"\nSearched {count} files, found {found} matches.\n")
