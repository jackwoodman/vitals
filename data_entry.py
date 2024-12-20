from typing import Optional
from classes import HealthMetric, AllowedMetricTypes, Measurement
from datetime import datetime
from metric_file_tools import add_measurement_to_metric_file, generate_health_file, parse_health_metric


Entry_T = Optional[str]
data_entry_strptime_format = "%d%m%Y"

"""

Should be 3 different modes.
1. Manual -> Unrecognised metric names are considered new metrics.
2. Assisted -> Recognised metric names are suggested for unrecognised metric names. 
3. Speedy -> Unrecognised metric names are replaced with recognised metric names.

input should be:
metricname metricvalue daterecorded

rules:
 if * in any position, use last value.
"""

def generate_new_metric(metric_name: str, value: AllowedMetricTypes, date: datetime):
    # Create new metric file.
    new_health_metric = parse_health_metric(metric_name=metric_name)
    generate_health_file(health_metric=new_health_metric)

    pass

def add_to_metric(metric_name: str, value: AllowedMetricTypes, date: datetime):
    # Create new metric entry.
    add_measurement_to_metric_file(metric_name=metric_name, measurement=Measurement(value=value, date=date))
    pass

class InputHandlerFunction():

    last_metric_used: str = None
    last_value_used: AllowedMetricTypes = None
    last_date_recorded: datetime = datetime(year=1, month=1, day=1)

    def __init__(self, recognised_metrics: list[str]):
        self.recognised_metrics = recognised_metrics

    def parse_input_str(self, input_str: str) -> Optional[tuple[str, AllowedMetricTypes, datetime]]:
        """
        Accepts a string representing the triplet of input values. Returns required information
        for input handling. Resolves any wildcards at this stage, and manages their storage.
        """
        
        # Split Input.
        try:
            metric_name_str, value_str, date_str = input_str.split(" ")

        except ValueError:
            # Could not find three distinct values.
            # TODO: Log here.
            return None
        
        # Convert input to datatypes.
        if value_str == "*":
            value: AllowedMetricTypes = self.last_value_used
        else:
            # If value is boolean, try to parse.
            if value_str.lower() in ["true", "false"]:
                value = value_str.lower() == "true"
            else:
                # Not bool, may be floating point.
                try:
                    value = float(value_str)
                except ValueError:
                    # Not float, must be string.
                    value = value_str
        date = self.last_date_recorded if date_str == "*" else datetime.strptime(date_str, data_entry_strptime_format)
        metric_name = self.last_metric_used if metric_name_str == "*" else metric_name_str.lower()

        # Assign last used values.
        self.last_metric_used = metric_name
        self.last_value_used = value
        self.last_date_recorded = date

        return (metric_name, value, date)



class ManualEntryHandler(InputHandlerFunction):
    def handle_input(self, input_string: str) -> Entry_T:
        parsing_result = self.parse_input_str(input_string)

        # Unable to parse, can skip.
        if not parsing_result:
            return None

        # Parse succesful, unpack.
        metric_name, value, date = parsing_result

        # Check if generating new metric, or adding to metric;
        if metric_name in self.recognised_metrics:
            add_to_metric(metric_name, value, date)
        else:
            generate_new_metric(metric_name, value, date)
            add_to_metric(metric_name, value, date)


class AssistedEntryHandler(InputHandlerFunction):
    def handle_input(self, input_string: str) -> Entry_T:
        pass

class SpeedyEntryHandler(InputHandlerFunction):
    def handle_input(self, input_string: str) -> Entry_T:
        pass
    