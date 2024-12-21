from metric_file_tools import (
    FILE_DIR_NAME,
    create_metric_dir,
    load_metric_from_json,
    read_metric_file_to_json,
    get_filenames_without_extension,
    rename_health_file,
)
from data_entry import AssistedEntryHandler
from logger import logger


def new_write():
    handler = AssistedEntryHandler(
        recognised_metrics=get_filenames_without_extension(FILE_DIR_NAME)
    )

    while True:
        new_input = input("New input: ")
        if new_input == "exit":
            break
        handler.handle_input(new_input)


def read():
    target_metric = input("-> read which metric file? ")
    health_file = read_metric_file_to_json(target_metric)
    health_metric = load_metric_from_json(health_file)

    print(f"Ingested '{health_metric.metric_name}':")
    for measurement in health_metric.entries:
        print("    ", measurement.value, measurement.date)


def rename():
    old_metric_name = input("-> rename which metric file? ")
    new_metric_name = input(f"-> rename '{old_metric_name}' to what? ")

    print(f"Renaming '{old_metric_name}' to '{new_metric_name}'...")
    rename_health_file(
        current_metric_name=old_metric_name, new_metric_name=new_metric_name
    )

    logger.add("action", f"Renamed metric '{old_metric_name}' to '{new_metric_name}'")


if __name__ == "__main__":
    # If no directory exists, generate one.
    create_metric_dir()

    while True:
        requirement = input("\n-> (read), (write), (rename), or (new_write)? ")

        if requirement == "read":
            read()
        elif requirement == "rename":
            rename()
        elif requirement == "new_write":
            new_write()
        elif requirement == "exit":
            logger.add("info", "Exiting.")
            logger.dump_to_file()
            break
