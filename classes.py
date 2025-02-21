from datetime import datetime
from enum import Enum
from typing import Optional, Union
from plotting import add_single_line, initialize_plot, add_lines


class InequalityValue:
    def __init__(self, raw_value: str):
        operator = raw_value[0]
        possible_value = float(raw_value[1:])

        if operator == "<":
            self.value = possible_value
            self.inequality_type = InequalityType("less_than")
        elif operator == ">":
            self.value = possible_value
            self.inequality_type = InequalityType("greater_than")


AllowedMetricValueTypes = Union[bool, float, str, InequalityValue]


class InequalityType(Enum):
    GreaterThan = "greater_than"
    LessThan = "less_than"


class MetricType(Enum):
    Ranged = "ranged"
    GreaterThan = "greater_than"
    LessThan = "less_than"
    Boolean = "boolean"
    Metric = "metric"


class Measurement:
    def __init__(
        self, value: AllowedMetricValueTypes, date: datetime, unit: Optional[str] = None
    ):
        self.value = value
        self.date = date
        self.unit = unit

    def update_unit(self, data: dict):
        if found_unit := data.get("unit"):
            self.unit = found_unit

    def __str__(self) -> str:
        return str(self.value)


class InequalityMeasurement(Measurement):
    def __init__(
        self,
        bound: float,
        inequality: InequalityType,
        date: datetime,
        unit: Optional[str] = None,
    ):
        super().__init__(bound, date, unit)
        self.inequality = inequality

    def __str__(self) -> str:
        """
        String representation for writing to file.
        """
        operator = ">" if self.inequality == InequalityType.GreaterThan else "<"
        return f"{operator}{self.value}"


class HealthMetric:
    def __init__(self, metric_name: str, metric_type: MetricType = MetricType.Metric):
        self.metric_name: str = metric_name
        self.entries: list[Measurement] = []
        self.metric_type: MetricType = metric_type
        self.unit = None

    def assign_unit(self, unit: str):
        self.unit = unit

    def metric_count(self) -> int:
        return len(self.entries)

    def add_entry(self, new_entry: Measurement):
        self.entries.append(new_entry)

    def generate_plot(self):
        single_plot = initialize_plot()
        return add_single_line(single_plot, self)

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
