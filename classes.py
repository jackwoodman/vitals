from datetime import datetime
from enum import Enum
from typing import Union
from plotting import initialize_plot, add_lines

AllowedMetricTypes = Union[bool, float]


class MetricType(Enum):
    Ranged = "ranged"
    GreaterThan = "greater_than"
    LessThan = "less_than"
    Boolean = "boolean"
    Metric = "metric"


class Measurement:
    def __init__(self, value: AllowedMetricTypes, date: datetime):
        self.value = value
        self.date = date


class HealthMetric:
    def __init__(self, metric_name: str, metric_type: MetricType = MetricType.Metric):
        self.metric_name: str = metric_name
        self.entries: list[Measurement] = []
        self.metric_type: MetricType = metric_type

    def metric_count(self) -> int:
        return len(self.entries)

    def add_entry(self, new_entry: Measurement):
        self.entries.append(new_entry)

    def generate_plot(self):
        single_plot = initialize_plot()
        return add_lines(single_plot, [self.entries])

    def __str__(self):
        return (
            f"Metric: {self.metric_name.upper()} -> {len(self.entries)} entries. "
            f"({self.metric_type.value})"
        )

    def metric_guide(self) -> str:
        return "Generic Metric"


class RangedMetric(HealthMetric):
    def __init__(self, metric_name: str, range_minimum: float, range_maximum: float):
        super().__init__(metric_name, MetricType.Ranged)
        self.range_minimum = range_minimum
        self.range_maximum = range_maximum

    def metric_guide(self) -> str:
        return (self.range_minimum, self.range_maximum)


class GreaterThanMetric(HealthMetric):
    def __init__(self, metric_name: str, minimum_value: float):
        super().__init__(metric_name, MetricType.GreaterThan)
        self.bound = minimum_value

    def metric_guide(self) -> str:
        return self.bound


class LessThanMetric(HealthMetric):
    def __init__(self, metric_name: str, maximum_value: float):
        super().__init__(metric_name, MetricType.LessThan)
        self.bound = maximum_value

    def metric_guide(self) -> str:
        return self.bound


class BooleanMetric(HealthMetric):
    def __init__(self, metric_name: str, ideal_boolean_value: bool):
        super().__init__(metric_name, MetricType.Boolean)
        self.ideal = ideal_boolean_value

    def metric_guide(self) -> bool:
        return self.ideal
