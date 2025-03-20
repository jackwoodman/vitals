from classes import HealthMetric
from metric_file_tools import get_all_metric_files
import time


def find_oor(_):
    """
    Show all metrics which are defined as "Out of Range".
    """
    start_time = time.time()
    metrics = find_all_oor_metrics()
    num_metrics = len(metrics)

    print(f"\nFound {num_metrics} Out of Range health metrics:")
    for i, metric in enumerate(metrics):
        oor_values = [measurement.value for measurement in metric.get_all_OoR_values()]
        oor_measurement_count = len(oor_values)
        plural = "s" if oor_measurement_count != 1 else ""
        print(
            f" ({i+1}): {metric.metric_name} -> {oor_measurement_count} measurement{plural}: {oor_values}. Should be '{metric.metric_guide()}'"
        )
    print(f"(time taken: {time.time() - start_time:.2f})")


def find_all_oor_metrics() -> list[HealthMetric]:
    """
    Find a list of all metric files that contain at least one measurement that is defined
    as Out of Range for that metric type.

    Returns:
        List of out of range containing HealthMetric objects.

    """

    return [metric for metric in get_all_metric_files() if metric.get_all_OoR_values()]
