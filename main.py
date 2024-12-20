from metric_file_tools import (
    FILE_DIR_NAME,
    create_metric_dir,
    load_metric_from_json,
    read_metric_file_to_json,
    get_filenames_without_extension,
    generate_health_file,
    add_measurement_to_metric_file,
    rename_health_file
)
from logger import LogCollector, LogEntry
from datetime import datetime
from classes import HealthMetric, MetricType, RangedMetric, GreaterThanMetric, LessThanMetric, Measurement
logger = LogCollector()

from metric_file_tools import parse_health_metric


def parse_metric_entry() -> Measurement:
    print("\n -> Parsing new metric entry (metric_name value date):")
    met_name, value_str, date_str = input("    ").split(" ")

    return met_name, Measurement(
        value=float(value_str), date=datetime.strptime(date_str, "%d/%m/%Y")
    )


def write():
    direction = input("-> write new (metric) or new (entry)?\n")
    if direction == "metric":
        new_metric = parse_health_metric()
        generate_health_file(health_metric=new_metric)
    else:
        metric_name, new_entry = parse_metric_entry()

        add_measurement_to_metric_file(metric_name=metric_name, measurement=new_entry)
        print(f"\n === New entry for '{metric_name}' added === \n")

def new_write():

    from data_entry import ManualEntryHandler
    from metric_file_tools import get_filenames_without_extension

    handler = ManualEntryHandler(recognised_metrics=get_filenames_without_extension(FILE_DIR_NAME))

    while True:
        new_input = input("New input: ")
        handler.handle_input(new_input)


def read():
    target_metric = input("-> read which metric file? ")
    health_file = read_metric_file_to_json(target_metric)
    health_metric = load_metric_from_json(health_file)

    plot = input("plot? ")

    if plot == "yes":
        from plotting import initialize_plot, add_lines

        figure = initialize_plot()
        figure = add_lines(figure, [health_metric])
        figure.show()

    print(health_metric)
    

def rename():
    old_metric_name = input("-> rename which metric file? ")
    new_metric_name = input(f"-> rename '{old_metric_name}' to what? ")

    print(f"Renaming '{old_metric_name}' to '{new_metric_name}'...")
    rename_health_file(current_metric_name=old_metric_name, new_metric_name=new_metric_name)

    logger.add(LogEntry("ACTN", f"Renamed metric '{old_metric_name}' to '{new_metric_name}'"))




if __name__ == "__main__":
    # If no directory exists, generate one.
    create_metric_dir()
    

    while True:
        requirement = input("\n-> (read), (write), (rename), or (new_write)? ")

        if requirement == "read":
            read()
        elif requirement == "write":
            write()
        elif requirement == "rename":
            rename()
        elif requirement == "new_write":
            new_write()
