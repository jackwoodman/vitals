from pathlib import Path
from cli_displays import prompt_user
from metric_file_tools import rename_health_file, update_measurement_units
from logger import logger
from data_entry import generate_new_metric


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


def update_units():
    """
    Quickly update all the units for a given metric, includnig the default value if
    required.
    """
    print("\nStarting input loop, format is 'metric_name new_unit update_default'")
    print("    ('exit' to leave update_units.)")

    while True:
        new_input = prompt_user(["main", "manage", "update_units"]).split(" ")
        bool_input = (new_input[2].strip().lower()) == "true"

        if new_input[0] == "exit":
            break

        update_measurement_units(
            metric_name=new_input[0],
            new_unit=new_input[1],
            update_file_level_unit=bool_input,
        )

    logger.add("info", "Exiting update_units.")


def instantiate():
    """ "
    Quickly instantiate empty helath files for population later. This is useful
    when a new report has multiple new metrics. You create files with this tool
    for the new metrics, and then use a fast-entry mode (e.g. 2 or 3) in the `write`
    tool to quickly fill them out.
    """
    created_metrics = []  # This is just for record keeping.
    created_count = 0

    print("\nStarting input loop, format is 'metric_name, unit (optional)'")
    print("    ('exit' to leave instantiate.)")

    while True:
        new_input = prompt_user(["main", "manage", "instantiate"]).split(" ")

        if new_input[0] == "exit":
            break

        created_metrics.append(
            generate_new_metric(
                metric_name=new_input[0],
                unit=new_input[1] if len(new_input) == 2 else None,
                log_creation=True,
            )
        )
        created_count += 1

    logger.add(
        "action",
        f"Exiting instantiate, created '{created_count}' new metrics.",
        cli_out=True,
    )
