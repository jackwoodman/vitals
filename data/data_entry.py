from typing import Optional
from classes import (
    AllowedMetricValueTypes,
    HealthMetric,
    InequalityMeasurement,
    InequalityValue,
    Measurement,
)
from datetime import datetime
from file_tools.metric_file_parsing import (
    parse_health_metric,
    add_measurement_to_metric_file,
    generate_metric_file,
)
from utils.sequence_matcher import get_closest_matches
from file_tools.utils import (
    is_inequality_value_str,
)
from utils.utils import is_verbatim
from utils.logger import logger
from file_tools.filepaths import get_filenames_without_extension

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


def generate_new_metric(
    metric_name: str, unit: Optional[str] = None, log_creation: bool = False
) -> HealthMetric:
    """
    Given a metric name, parse from the user the required information to generate
    a new metric. Use this to generate a new metric file.

    """
    new_health_metric = parse_health_metric(metric_name=metric_name, unit=unit)
    generate_metric_file(health_metric=new_health_metric)

    if log_creation:
        logger.add("action", f"Created new health metric '{metric_name}'")

    return new_health_metric


def add_to_metric(
    metric_name: str,
    value: AllowedMetricValueTypes,
    date: datetime,
    unit: Optional[str] = None,
):
    if isinstance(value, InequalityValue):
        measurement = InequalityMeasurement(
            bound=value.value, inequality=value.inequality_type, date=date, unit=unit
        )
    else:
        measurement = Measurement(value=value, date=date, unit=unit)

    # Create new metric entry.
    add_measurement_to_metric_file(metric_name=metric_name, measurement=measurement)


class InputHandler:
    """
    Class to represent an input handler. An input handler receives input from the user,
    specifically for a new data entry, and decides how to ingest, process and log the input.

    This parent class defines the `parse_input_str()` function, which handles the raw user input
    and decides how to return this. Classes that extend this one *should not* need to override this,
    but are more than welcome to to add new functionality.

    Attributes:
        last_metric_used: Records the most recent metric name processed by this handler.
        last_value_used: Records the most recent metric value processed by this handler.
        last_date_recorded: Records the most recent datetime processed by this handler.
        last_unit_used: Records the most recent unit processed by this handler.
    """

    last_metric_used: str = None
    last_value_used: AllowedMetricValueTypes = None
    last_date_recorded: datetime = datetime(year=1, month=1, day=1)
    last_unit_used: str = None

    def __init__(self, metric_file_path: str):
        """
        Initialises a new handler.

        Attributes:
            metric_file_path: Path to metric file dir.
        """
        self.metric_file_path = metric_file_path
        self.update_recognised_metrics()

    def update_recognised_metrics(self) -> int:
        """
        Updates the list of recognised metrics, returning the count.
        """

        self.recognised_metrics = get_filenames_without_extension(self.metric_file_path)

    def parse_input_str(
        self, input_str: str
    ) -> Optional[tuple[str, AllowedMetricValueTypes, datetime]]:
        """
        Accepts a string representing the triplet of input values. Returns required information
        for input handling. Resolves any wildcards at this stage, and manages their storage.

        This function should only be overridden to provide subclass specific parsing functionality,
        but this is fine. Just don't modify this function, as it is inherited by most subclasses.

        Arguments:
            input_str: Raw input from the user.

        Returns:
            A tuple representing the classic 3 element input required for a new measurement, or
            None if unable to parse correctly.
        """

        # Split Input - entries are positional.
        try:
            distinct_entries = list(input_str.split(" "))

            # Base input - name, value, date.
            if len(distinct_entries) == 3:
                metric_name_str, value_str, date_str = distinct_entries
                unit_str = None
            # Second case - units included.
            elif len(distinct_entries) == 4:
                metric_name_str, value_str, date_str, unit_str = distinct_entries
            else:
                # This many values is not recognised (yet).
                raise ValueError()

        except ValueError:
            # Could not find three distinct values.
            logger.add("warning", f"InputHandler unable to parse input: {input_str}")
            return None

        # Convert input to datatypes.
        if value_str == "*":
            value: AllowedMetricValueTypes = self.last_value_used
        else:
            # If value is boolean, try to parse.
            if value_str.lower() in ["true", "false"]:
                value = value_str.lower() == "true"
            elif is_inequality_value_str(input_str=value_str):
                # Is an inequality.
                value = InequalityValue(value_str)
            else:
                # Not bool or inequality, may be floating point.
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
        self.last_unit_used = unit_str or None

        return (metric_name.lower(), value, date, unit_str or None)

    def handle_input():
        """*MUST BE IMPLEMENTED*"""
        logger.add(
            "warning", "`handle_input()` called from InputHandler(), not a subclass."
        )
        pass


class ManualEntryHandler(InputHandler):
    """
    The ManualEntryHandler is used for mode 1 data entry. This assumes the user
    input is correct and intentional. If a recognised metric name is entered,
    the user measurement will be added to the existing metric. If an unrecognised metric
    name is entered, this handler *assumes this is intentional* and starts creating
    a new metric.

    """

    def handle_input(self, input_string: str) -> Entry_T:
        parsing_result = self.parse_input_str(input_string)

        # Unable to parse, can skip.
        if not parsing_result:
            return None

        # Parse succesful, unpack.
        metric_name, value, date, unit = parsing_result

        # Check for verbatim here just in case user mistakes this
        # for a different handler. Makes no difference, just need to
        # strip the verbatim signifier.
        if verbatim_result := is_verbatim(metric_name):
            metric_name = verbatim_result

        # Check if generating new metric, or adding to metric;
        if metric_name in self.recognised_metrics:
            add_to_metric(metric_name, value, date, unit)
        else:
            generate_new_metric(metric_name, unit)
            add_to_metric(metric_name, value, date, unit)
            self.update_recognised_metrics()


class AssistedEntryHandler(InputHandler):
    """
    The AssistedEntryHandler is used for mode 2 data entry. This assumes the user
    input is incorrect if not recognised, and needs to be matched to the closest
    recognised metric name by presenting the user with a list of similar
    metrics and allowing them to choose whether to use one of those, or read
    their input verbatim.
    """

    required_close_matches = 3

    def set_required_close_matches(self, required_matches: int):
        if required_matches > 0:
            self.required_close_matches = required_matches
        else:
            logger.add("warning", "Can't set required matches to less than zero.")

    def handle_input(self, input_string: str) -> Entry_T:
        parsing_result = self.parse_input_str(input_string)

        # Unable to parse, can skip.
        if not parsing_result:
            return None

        # Parse succesful, unpack.
        metric_name, value, date, unit = parsing_result

        # Check if generating new metric, or adding to metric;
        if metric_name in self.recognised_metrics:
            add_to_metric(metric_name, value, date)
        else:
            # Check first for verbatim request.
            if verbatim_result := is_verbatim(metric_name):
                print(
                    f"Creating new metric '{verbatim_result}' and adding measurement."
                )
                generate_new_metric(verbatim_result, unit)
                add_to_metric(verbatim_result, value, date, unit)
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
                    generate_new_metric(metric_name, unit)
                    add_to_metric(metric_name, value, date, unit)
                    self.update_recognised_metrics()
                else:
                    # User chose from existing names.
                    metric_name = similar_metrics[int(user_response) - 1]
                    print(f"Adding measurement to {metric_name}.")
                    add_to_metric(metric_name, value, date, unit)


class SpeedyEntryHandler(InputHandler):
    """
    The SpeedyEntryHandler is used for mode 3 data entry. This assumes the user
    input is incorrect if not recognised, and needs to be matched to the closest
    recognised metric name. This matching occurs without user input.
    """

    def handle_input(self, input_string: str) -> Entry_T:
        parsing_result = self.parse_input_str(input_string)

        # Unable to parse, can skip.
        if not parsing_result:
            return None

        # Parse succesful, unpack.
        metric_name, value, date, unit = parsing_result

        # Check if generating new metric, or adding to metric;
        if metric_name in self.recognised_metrics:
            add_to_metric(metric_name, value, date, unit)
        else:
            # Check first for verbatim request.
            if verbatim_result := is_verbatim(metric_name):
                print(
                    f"Creating new metric '{verbatim_result}' and adding measurement."
                )
                generate_new_metric(verbatim_result, unit)
                add_to_metric(verbatim_result, value, date, unit)
                self.update_recognised_metrics()
            else:
                # Not recognised and not verbatim, use the closest match.
                similar_metrics = get_closest_matches(
                    metric_name, self.recognised_metrics, 1
                )

                logger.add(
                    "action",
                    f"{metric_name} not recognised, MODE 3 matched to {similar_metrics[0]}.",
                )
                print(f"[matched '{metric_name}' to '{similar_metrics[0]}']")

                metric_name = similar_metrics[0]
                add_to_metric(metric_name, value, date, unit)
