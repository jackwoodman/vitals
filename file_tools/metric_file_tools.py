import json
from pathlib import Path
from utils.cli_displays import cli_warn
from classes import (
    HealthMetric,
    InequalityMeasurement,
    Measurement,
)
from utils.logger import logger

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


def write_json_to_metric_file(metric_name: str, json_dict: dict) -> bool:
    """
    Given the name of a health metric file, and a JSON dict, write
    JSON dict to file.

    Arguments:
        metric_name: Name of metric file, without the .json.
        json: The JSON dict.

    Returns:
        Bool indicating write success.
    """
    filepath = Path(
        f"{FILE_DIR_NAME}/{metric_name}.json"
        if ".json" not in metric_name
        else metric_name
    )

    try:
        filepath.write_text(json.dumps(json_dict, indent=4))
    except IOError as e:
        logger.add("ERROR", f"Failed to write metric file: {e}")
        return False

    return True


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
    directory_path = Path(directory) if isinstance(directory, str) else directory
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


def update_measurement_units(
    metric_name: str, new_unit: str, update_file_level_unit: bool = False
) -> int:
    """
    Update all measurements in a given metric file with a new unit value.

    Arguments:
        metric_name: Name of the metric file to be modified.
        new_unit: New unit string to be applied.
        update_file_level_unit: If true, also update the metric file level unit.

    Returns:
        Number of measurements that were modified.
    """
    modified_units = 0
    file_json = read_metric_file_to_json(metric_name)

    if file_json:
        for measurement in file_json.get("data"):
            measurement["unit"] = new_unit
            modified_units += 1

        # Update file level value if needed.
        if update_file_level_unit:
            file_json["unit"] = new_unit
            logger.add(
                "action", f"'{metric_name}' unit changed to '{new_unit}'.", cli_out=True
            )

        # Save the modified JSON back to the file
        write_json_to_metric_file(metric_name=metric_name, json_dict=file_json)
        logger.add(
            "action",
            f"Updated {modified_units} measurements from {metric_name} with unit '{new_unit}'.",
            cli_out=True,
        )

    else:
        logger.add("WARNING", "Can't mass update file.")

    return modified_units


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
