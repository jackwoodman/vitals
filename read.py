from utils import attempt_ingest_from_name


def read_by_name(arguments: list):
    """
    Loop to handle reading a metric file to HealthMetric object. WIP.

    Accepted arguments:
        Position 1: Name of file to read.

    """
    health_metric = attempt_ingest_from_name(arguments, "read_metric")

    # Check nonzero entries:
    if health_metric and len(health_metric.entries) > 0:
        print(f"(Found {len(health_metric.entries)} entries)")
        for measurement in health_metric.entries:
            print(
                " - ",
                f"{str(measurement)}{(" "+measurement.unit) if measurement.unit else ""}",
                " -> ",
                measurement.date,
            )

    else:
        print("File is empty.")

    print("\n")
