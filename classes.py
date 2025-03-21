from datetime import datetime
from enum import Enum
from typing import Optional, Union
from logger import logger
from plotting import add_single_line, initialise_plot, empty_figure, plot_metrics


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
        return plot_metrics(self)

    def add_to_existing_plot(self, plot):
        return add_single_line(plot, self)

    def get_all_OoR_values(self) -> list[Measurement]:
        OoR_values = [
            oor_measurement
            for oor_measurement in self.entries
            if self.value_is_out_of_range(oor_measurement)
        ]

        return OoR_values

    def __str__(self):
        return (
            f"Metric: {self.metric_name.upper()} -> {len(self.entries)} entries. "
            f"({self.metric_type.value})"
        )

    def metric_guide(self) -> str:
        return "Generic Metric"

    def value_is_out_of_range(self, value: Measurement) -> bool:
        """Must be implemented."""
        pass


class RangedMetric(HealthMetric):
    def __init__(self, metric_name: str, range_minimum: float, range_maximum: float):
        super().__init__(metric_name, MetricType.Ranged)
        self.range_minimum = range_minimum
        self.range_maximum = range_maximum

    def metric_guide(self) -> str:
        return (self.range_minimum, self.range_maximum)

    def value_is_out_of_range(self, value: Measurement) -> bool:
        return not (self.range_minimum < value.value < self.range_maximum)


class GreaterThanMetric(HealthMetric):
    def __init__(self, metric_name: str, minimum_value: float):
        super().__init__(metric_name, MetricType.GreaterThan)
        self.bound = minimum_value

    def metric_guide(self) -> str:
        return self.bound

    def value_is_out_of_range(self, value: Measurement) -> bool:
        return value.value < self.bound


class LessThanMetric(HealthMetric):
    def __init__(self, metric_name: str, maximum_value: float):
        super().__init__(metric_name, MetricType.LessThan)
        self.bound = maximum_value

    def metric_guide(self) -> str:
        return self.bound

    def value_is_out_of_range(self, value: Measurement) -> bool:
        return value.value > self.bound


class BooleanMetric(HealthMetric):
    def __init__(self, metric_name: str, ideal_boolean_value: bool):
        super().__init__(metric_name, MetricType.Boolean)
        self.ideal = ideal_boolean_value

    def metric_guide(self) -> bool:
        return self.ideal

    def value_is_out_of_range(self, value: Measurement) -> bool:
        if type(value) is Measurement:
            return value.value != self.ideal


class MetricGroup:
    def __init__(self, unit: str = None):
        self.metric_dict = {}
        self.count = 0
        self.enforce_units = unit is not None
        self.unit = unit

    def as_list(self):
        return [metric for metric in self.metric_dict.values()]

    def graph_group(self, show_bounds: bool = True):
        figure = plot_metrics(self.as_list(), show_bounds=show_bounds)
        figure.show()

    def add_metric(self, new_metric: HealthMetric) -> bool:
        # Check metric can be registered.
        if new_metric.unit and new_metric.unit != self.unit and self.enforce_units:
            logger.add(
                "warning",
                f"Metric '{new_metric.metric_name}' unit '{new_metric.unit}' does not match MetricGroup unit '{self.unit}'.",
                cli_out=True,
            )
            return False

        self.metric_dict[new_metric.metric_name] = new_metric
        self.count += 1
        return True

    def add_metrics(self, new_metrics: list[HealthMetric]) -> list[bool]:
        """
        Add a list of metrics.
        """
        return [self.add_metric(metric) for metric in new_metrics]

    def remove_metric(self, metric_name: str) -> bool:
        """
        Deregister metric.
        """
        if metric_name in self.metric_dict.keys():
            self.metric_dict.pop(metric_name)
            self.count -= 1
            return True
        logger.add("warning", f"No metric named '{metric_name}'.", cli_out=True)
        return False

    def remove_metrics(self, metric_names: list[str]) -> list[bool]:
        return [self.remove_metric(metric_name) for metric_name in metric_names]
