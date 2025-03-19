import json
import os
from pathlib import Path
from typing import Optional
from cli_displays import cli_warn
from classes import (
    GreaterThanMetric,
    HealthMetric,
    InequalityMeasurement,
    InequalityValue,
    LessThanMetric,
    Measurement,
    MetricType,
    RangedMetric,
    BooleanMetric,
)
from logger import logger

FILE_VERS = 9
FILE_DIR_NAME = "metric_files"
FILE_DIR_PATH = Path(FILE_DIR_NAME)


def create_metric_dir():
    """
    Creates a dir at the required path, if not existing already.

    Returns:
        Bool indicating if a directory was created (True) or not (False).
    """
    if FILE_DIR_PATH.exists():
        return False

    FILE_DIR_PATH.mkdir(parents=True, exist_ok=True)
    return True


def is_inequality_value_str(input_str: str) -> bool:
    """
    Test whether input string is a candidate for representing an "InequalityValue".

    Arguments:
        input_str: The string, representing a value, to be tested.

    Returns:
        Bool indicating whether value looks like an inequality value, or not.
    """
    if "<" in str(input_str) or ">" in str(input_str):
        return True
    return False


def read_metric_file_to_json(metric_name: str) -> dict:
    """
    Given the name of a health metric file, load said file and return
    JSON dict.

    Arguments:
        metric_name: Name of metric file, without the .json.

    Returns:
        JSON dict of metric_name.
    """
    filename = (
        f"{FILE_DIR_NAME}/{metric_name}.json"
        if ".json" not in metric_name
        else metric_name
    )

    try:
        # Write updated data back to the file
        with open(filename, "r") as health_file:
            data = json.load(health_file)
        return data

    except FileNotFoundError:
        warning_text = f"File '{filename} could not be found."
        logger.add("WARNING", warning_text)
        cli_warn(warning_text)
        return None


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
        fv_warn = f"file `{metric_name}` is outdated by {version_delta}. (File vers: {file_version}, operating vers: {FILE_VERS})\n"
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
        default_unit = health_data.get("unit")
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


def generate_metric_file(health_metric: HealthMetric) -> str:
    """
    Provided a health metric object, generate a metric file to store the currently
    contained data. File is named using the metric_name attribute and saved to the
    required directory.

    Arguments:
        health_metric: The metric to be saved to file.

    Returns:
        A string path to the generated file.
    """
    file_path = Path(FILE_DIR_NAME) / f"{health_metric.metric_name}.json"

    preformed_dictionary = {
        "metric_name": health_metric.metric_name,
        "file_version": FILE_VERS,
        "metric_type": health_metric.metric_type.value,
        "metric_guide": health_metric.metric_guide(),
        "data": [],
    }

    if health_metric.unit:
        preformed_dictionary["unit"] = health_metric.unit

    try:
        file_path.write_text(json.dumps(preformed_dictionary, indent=4))
    except IOError as e:
        logger.add("ERROR", f"Failed to write metric file: {e}")
        raise

    logger.add("action", f"Created new metric file `{health_metric.metric_name}.json`.")
    return str(file_path)


def get_filenames_without_extension(directory):
    """Returns a list of filenames in the given directory without their extensions."""
    directory_path = Path(directory)
    filenames = [file.stem for file in directory_path.iterdir() if file.is_file()]

    return filenames


def add_measurement_to_metric_file(metric_name: str, measurement: Measurement) -> bool:
    """Adds a new entry (date and value) to an existing health JSON file, accepts a datetime object for the date.

    Arguments:
        metric_name: Name of the metric to be added to.
        measurement: Measurement to be added.

    Returns:
        Bool indicating write success.
    """
    # Load existing data
    file_path = Path(FILE_DIR_NAME) / f"{metric_name}.json"

    if not file_path.exists():
        print(f"Error: File {file_path} not found. Please create the file first.")
        return False

    try:
        data = json.loads(file_path.read_text())
    except json.JSONDecodeError as e:
        logger.add("ERROR", f"Failed to parse JSON from {file_path}: {e}")
        return False

    # Convert datetime to string in ISO format
    date_str = measurement.date.isoformat()

    # Add new entry
    new_entry = {
        "date": date_str,
        "value": measurement.value
        if not isinstance(measurement, InequalityMeasurement)
        else str(measurement),
    }
    # Check measurement has own unit.
    if measurement.unit:
        new_entry["unit"] = measurement.unit
    elif unit_from_file := data.get("unit"):
        # If no unit, try to use value default.
        new_entry["unit"] = unit_from_file

    data["data"].append(new_entry)

    try:
        file_path.write_text(json.dumps(data, indent=4))
    except IOError as e:
        logger.add("ERROR", f"Failed to write to metric file {file_path}: {e}")
        return False

    logger.add("action", f"Added new measurement to '{file_path.name}'.")
    return True


def rename_health_file(current_metric_name: str, new_metric_name: str):
    # Specify the old and new file names
    old_file = Path(FILE_DIR_NAME) / f"{current_metric_name}.json"
    new_file = Path(FILE_DIR_NAME) / f"{new_metric_name}.json"

    # Rename the file
    try:
        old_file.rename(new_file)
        print(f" - File renamed successfully to {new_file}")
    except FileNotFoundError:
        print(f"The file {old_file} does not exist.")
    except PermissionError:
        print("Permission denied. Make sure you have the right access.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Read the JSON data from the renamed file.
    try:
        with open(str(new_file), "r") as file:
            data = json.load(file)
        key_to_modify = "metric_name"

        # Update metric_name.
        if key_to_modify in data:
            old_value = data[key_to_modify]
            data[key_to_modify] = new_metric_name
            print(
                f" - Changed value of '{key_to_modify}' from '{old_value}' to '{new_metric_name}'"
            )
        else:
            print(f" - The key '{key_to_modify}' does not exist in the JSON file.")

        # Save the modified JSON back to the file
        with open(str(new_file), "w") as file:
            json.dump(data, file, indent=4)

    except FileNotFoundError:
        print(f"The file {str(new_file)} does not exist.")
    except json.JSONDecodeError:
        print("Error decoding JSON. Please ensure the file contains valid JSON.")
    except Exception as e:
        print(f"An error occurred: {e}")


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
