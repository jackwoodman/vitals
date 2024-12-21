from datetime import datetime
from classes import Measurement
from metric_file_tools import add_measurement_to_metric_file, generate_metric_file, parse_health_metric


def parse_metric_entry() -> Measurement:
    print("\n -> Parsing new metric entry (metric_name value date):")
    met_name, value_str, date_str = input("    ").split(" ")

    return met_name, Measurement(
        value=float(value_str), date=datetime.strptime(date_str, "%d/%m/%Y")
    )


def old_write():
    direction = input("-> write new (metric) or new (entry)?\n")
    if direction == "metric":
        new_metric = parse_health_metric()
        generate_metric_file(health_metric=new_metric)
    else:
        metric_name, new_entry = parse_metric_entry()

        add_measurement_to_metric_file(metric_name=metric_name, measurement=new_entry)
        print(f"\n === New entry for '{metric_name}' added === \n")
