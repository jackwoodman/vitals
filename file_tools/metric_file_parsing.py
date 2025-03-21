from typing import Optional

from classes import (
    BooleanMetric,
    GreaterThanMetric,
    HealthMetric,
    InequalityMeasurement,
    InequalityValue,
    LessThanMetric,
    Measurement,
    MetricType,
    RangedMetric,
)
from file_tools.metric_file_tools import (
    FILE_DIR_NAME,
    FILE_DIR_PATH,
    FILE_VERS,
    get_filenames_without_extension,
    is_inequality_value_str,
    read_metric_file_to_json,
)
from utils.logger import logger
from utils.cli_displays import cli_warn


def get_all_metric_files() -> list[HealthMetric]:
    return [
        generate_health_metric_from_file(metric)
        for metric in get_filenames_without_extension(FILE_DIR_PATH)
    ]


def load_metric_from_json(health_data: dict) -> Optional[HealthMetric]:
    """
    Given the JSON object from reading a health file, produce a HealthMetric
    object representing this file.

    Arguments:
        health_data: A JSON dict representing an input health file.

    Returns:
        A HealthMetric object representing the input file, or None if parsing failed.
    """

    # All versions of health files have a name and a version. If missing, file is misformed.
    try:
        metric_name = health_data["metric_name"]
        file_version = health_data["file_version"]
    except KeyError as e:
        cli_warn(f"Missing required assumed key: {e}")
        logger.add("WARNING", f"Missing required assumed key in health data: {e}")
        return None

    file_is_outdated = False
    # Check for outdated file.
    if file_version < FILE_VERS:
        version_delta = FILE_VERS - file_version
        fv_warn = f"file `{metric_name}` is outdated by {version_delta}. (File vers: {file_version}, operating vers: {FILE_VERS})"
        cli_warn(fv_warn)
        logger.add("WARNING", fv_warn)
        file_is_outdated = True

    try:
        metric_type = MetricType(health_data["metric_type"])
        metric_guide = health_data["metric_guide"]
        data_values = health_data["data"]

        if metric_type == MetricType.Ranged:
            lower_value, upper_value = metric_guide
            metric = RangedMetric(
                metric_name=metric_name,
                range_minimum=lower_value,
                range_maximum=upper_value,
            )
        elif metric_type == MetricType.GreaterThan:
            metric = GreaterThanMetric(
                metric_name=metric_name, minimum_value=float(metric_guide)
            )
        elif metric_type == MetricType.LessThan:
            metric = LessThanMetric(
                metric_name=metric_name, maximum_value=float(metric_guide)
            )
        elif metric_type == MetricType.Boolean:
            metric = BooleanMetric(
                metric_name=metric_name, ideal_boolean_value=metric_guide
            )
        elif metric_type == MetricType.Metric:
            metric = HealthMetric(metric_name=metric_name)
        else:
            # Metric type doesn't match supported types.
            fv_warn = f"Metric file type `{metric_type}` is not recognised.\n"
            cli_warn(fv_warn)
            logger.add("WARNING", fv_warn)
            return None

        # Process individual data entries.
        default_unit = health_data.get("unit", None)
        metric.assign_unit(unit=default_unit)

        for entry_number, data_point in enumerate(data_values):
            # Date should be included with each entry.
            date = data_point["date"]
            if not date:
                warning_text = f"Skipping entry '{entry_number}' - no date found."
                logger.add("WARNING", warning_text)
                continue

            # Value is implied to exist, it shouldn't be possible for this to not exist.
            data_point_unit = data_point.get("unit", default_unit)
            data_point_value = data_point["value"]

            # Inequality measurements are handled uniquely.
            if is_inequality_value_str(data_point_value):
                value_parsed = InequalityValue(data_point_value)
                measurement = InequalityMeasurement(
                    value_parsed.value,
                    value_parsed.inequality_type,
                    date,
                    unit=data_point_unit,
                )

            else:
                # Non-equality measurement parsing.
                measurement = Measurement(data_point_value, date, unit=data_point_unit)

            metric.add_entry(measurement)
    except Exception as e:
        # If file was outdated, this is likely the cause, though this should be refined.
        if file_is_outdated:
            cli_warn(
                "Unable to parse, likely because file is outdated. Update file and try again."
            )
            logger.add(
                "WARNING", f"Couldn't parse, outdated file may be the cause. {e}"
            )
        else:
            cli_warn("Unable to parse. File was up to date.")
            logger.add("WARNING" "Couldn't parse, reason is unknown. {e}")
        return None
    return metric


def generate_health_metric_from_file(filepath: str) -> HealthMetric:
    """
    Given the filepath or name of a metric file, load said metric file
    and return the generated HealthMetric object.

    Arguments:
        filepath: String filepath or name of metric file.

    Returns:
        HealthMetric object, or None if parsing was not possible.
    """
    health_data = read_metric_file_to_json(metric_name=filepath)
    metric = load_metric_from_json(health_data)

    return metric


def parse_health_metric(metric_name: str, unit: Optional[str] = None) -> HealthMetric:
    """
    Given the name of a new metric file, prompt the user to select the type of metric,
    and generate the required HealthMetric object to store this data.

    Arguments:
        str: The name of the new metric.

    Returns:
        A HealthMetric meeting the user requirements.

    """

    prompt = " -> "

    metric: HealthMetric = None
    supported_types = {
        "r": "ranged",
        "g": "greater_than",
        "l": "less_than",
        "b": "boolean",
        "m": "metric",
    }

    type_descriptions = {
        "ranged": "Measurements should fall between two values (e.g. x < m < y)",
        "greater_than": "Measurements should be greater than some value (e.g. m > x)",
        "less_than": "Measurements should be less than some value (e.g. m < x)",
        "boolean": "Measurements should be of a certain truth value (e.g. m is True)",
        "metric": "Measurements have no ideal value (e.g. age)",
    }
    print("\nParsing new health metric:")
    print(
        f"Vitals currently supports {len(supported_types.items())} types of metric. These are:"
    )

    for key, name in supported_types.items():
        print(f" ({key}){name[1:]}: {type_descriptions[name]}")

    print("\nInput the first letter of the type of metric you'd like to create:")
    response = input(prompt).strip().lower()
    metric_type_str = supported_types.get(response, metric)
    parsed_metric_type = MetricType(metric_type_str)

    if parsed_metric_type == MetricType.Ranged:
        print(
            f"\nInput ideal range for new ranged metric '{metric_name}'. Format: 'lower_bound upper_bound'"
        )
        try:
            lower_str, upper_str = input(prompt).split()
            lower, upper = float(lower_str), float(upper_str)
        except ValueError:
            print(
                "Invalid input. Please provide two numeric values separated by a space."
            )
            return None
        metric = RangedMetric(
            metric_name=metric_name, range_minimum=lower, range_maximum=upper
        )

    elif parsed_metric_type == MetricType.GreaterThan:
        print(
            f"\nInput ideal minimum value for new GreaterThan metric '{metric_name}':"
        )
        try:
            lower = float(input(prompt).strip())
        except ValueError:
            print("Invalid input. Please provide a numeric value.")
            return None
        metric = GreaterThanMetric(metric_name=metric_name, minimum_value=lower)

    elif parsed_metric_type == MetricType.LessThan:
        print(f"\nInput ideal maximum value for new LessThan metric '{metric_name}':")
        try:
            upper = float(input(prompt).strip())
        except ValueError:
            print("Invalid input. Please provide a numeric value.")
            return None
        metric = LessThanMetric(metric_name=metric_name, maximum_value=upper)

    elif parsed_metric_type == MetricType.Boolean:
        print(
            f"\nInput ideal boolean value for new Boolean metric '{metric_name}' (True/False):"
        )
        bool_input = input(prompt).strip().lower()
        if bool_input not in {"true", "false"}:
            print("Invalid input. Please enter 'True' or 'False'.")
            return None
        metric = BooleanMetric(
            metric_name=metric_name, ideal_boolean_value=(bool_input == "true")
        )

    elif parsed_metric_type == MetricType.Metric:
        print(f"\nCreating new generic metric '{metric_name}':")
        metric = HealthMetric(metric_name=metric_name)

    else:
        print(f"Metric type '{parsed_metric_type}' is not supported.")
        return None

    print(
        f"\n === New metric file '{metric_name}' generated (reporting {len(get_filenames_without_extension(FILE_DIR_NAME)) + 1} metric files) === \n"
    )

    # Assign default unit if provided.
    if unit:
        metric.assign_unit(unit=unit)

    return metric
