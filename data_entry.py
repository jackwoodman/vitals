from typing import Optional
from classes import AllowedMetricTypes, Measurement
from datetime import datetime
from sequence_matcher import get_closest_matches
from metric_file_tools import (
    add_measurement_to_metric_file,
    generate_metric_file,
    parse_health_metric,
)
from utils import is_verbatim

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


def generate_new_metric(metric_name: str):
    """
    Given a metric name, parse from the user the required information to generate
    a new metric. Use this to generate a new metric file.

    """
    new_health_metric = parse_health_metric(metric_name=metric_name)
    generate_metric_file(health_metric=new_health_metric)


def add_to_metric(metric_name: str, value: AllowedMetricTypes, date: datetime):
    # Create new metric entry.
    add_measurement_to_metric_file(
        metric_name=metric_name, measurement=Measurement(value=value, date=date)
    )
    pass


class InputHandlerFunction:
    last_metric_used: str = None
    last_value_used: AllowedMetricTypes = None
    last_date_recorded: datetime = datetime(year=1, month=1, day=1)

    def __init__(self, recognised_metrics: list[str]):
        self.recognised_metrics = recognised_metrics

    def parse_input_str(
        self, input_str: str
    ) -> Optional[tuple[str, AllowedMetricTypes, datetime]]:
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
        date = (
            self.last_date_recorded
            if date_str == "*"
            else datetime.strptime(date_str, data_entry_strptime_format)
        )
        metric_name = (
            self.last_metric_used if metric_name_str == "*" else metric_name_str.lower()
        )

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

        # Check for verbatim here just in case user mistakes this
        # for a different handler. Makes no difference, just need to
        # strip the verbatim signifier.
        if verbatim_result := is_verbatim(metric_name):
            metric_name = verbatim_result

        # Check if generating new metric, or adding to metric;
        if metric_name in self.recognised_metrics:
            add_to_metric(metric_name, value, date)
        else:
            generate_new_metric(metric_name, value, date)
            add_to_metric(metric_name, value, date)


class AssistedEntryHandler(InputHandlerFunction):
    required_close_matches = 3

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
            # Check first for verbatim request.
            if verbatim_result := is_verbatim(metric_name):
                print(
                    f"Creating new metric '{verbatim_result}' and adding measurement."
                )
                generate_new_metric(verbatim_result, value, date)
                add_to_metric(verbatim_result, value, date)
            else:
                # Not recognised, find close to.
                similar_metrics = get_closest_matches(
                    metric_name, self.recognised_metrics, self.required_close_matches
                )
                print(
                    f"'{metric_name}' is not recognised, choose from one of the below close matches,\n"
                    " or (v) to create a new metric using the input name:"
                )

                # Display closest matches and ask user to choose one, or to use their input (v)erbatim.
                for i, similar in enumerate(similar_metrics):
                    print(f"({i+1}) {similar}")
                print(f"(v) {metric_name}")
                user_response = input(" -> ")

                # Use chose (v)erbatim.
                if user_response == "v":
                    print(
                        f"Creating new metric '{metric_name}' and adding measurement."
                    )
                    generate_new_metric(metric_name, value, date)
                    add_to_metric(metric_name, value, date)
                else:
                    # User chose from existing names.
                    metric_name = similar_metrics[int(user_response) - 1]
                    print(f"Adding measurement to {metric_name}.")
                    add_to_metric(metric_name, value, date)


class SpeedyEntryHandler(InputHandlerFunction):
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
            # Check first for verbatim request.
            if verbatim_result := is_verbatim(metric_name):
                print(
                    f"Creating new metric '{verbatim_result}' and adding measurement."
                )
                generate_new_metric(verbatim_result, value, date)
                add_to_metric(verbatim_result, value, date)
            else:
                # Not recognised and not verbatim, use the closest match.
                similar_metrics = get_closest_matches(
                    metric_name, self.recognised_metrics, 1
                )

                metric_name = similar_metrics[0]
                add_to_metric(metric_name, value, date)
