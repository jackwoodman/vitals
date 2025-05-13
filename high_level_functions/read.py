from classes import HealthMetric
from global_functions import source_metric


def read_by_name(arguments: list):
    """
    Loop to handle reading a metric file to HealthMetric object. WIP.

    Accepted arguments:
        Position 1: Name of file to read.

    """
    source_group = source_metric(arguments)

    # Check nonzero entries:
    if source_group and len(source_group.as_list()) > 0:
        metrics: list[HealthMetric] = source_group.as_list()

        # For each metric, display associated entries.
        for metrid in metrics:
            print(f"\nMetric: {metrid.metric_name}")
            entries = metrid.entries
            print(f"(Found {len(entries)} entries)")
            for measurement in entries:
                print(
                    " - ",
                    f"{str(measurement)}{(" "+measurement.unit) if measurement.unit else ""}",
                    " -> ",
                    measurement.date,
                )

    else:
        print(f"read_by_name() was unable to load from arguemnts: {arguments}")

    print("\n")
