import json
from pathlib import Path
from classes import (
    GreaterThanMetric,
    HealthMetric,
    LessThanMetric,
    Measurement,
    MetricType,
    RangedMetric,
    BooleanMetric,
)
from logger import logger

FILE_VERS = 7
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


def read_metric_file_to_json(metric_name: str):
    """
    Return metric JSON data
    """
    filename = (
        f"{FILE_DIR_NAME}/{metric_name}.json"
        if ".json" not in metric_name
        else metric_name
    )

    # Write updated data back to the file
    with open(filename, "r") as health_file:
        data = json.load(health_file)

    return data


def load_metric_from_json(health_data: dict) -> HealthMetric:
    metric_name = health_data["metric_name"]
    file_version = health_data["file_version"]

    if file_version < FILE_VERS:
        print(f" -> warning, file {metric_name} is outdated.")

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

    for data_point in data_values:
        date = data_point["date"]
        value = float(data_point["value"])

        metric.add_entry(Measurement(value, date))

    return metric


def generate_health_metric_from_file(filepath: str) -> HealthMetric:
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
    file_path = f"{FILE_DIR_NAME}/{health_metric.metric_name}.json"

    with open(file_path, "w") as health_file:
        json.dump(
            {
                "metric_name": health_metric.metric_name,
                "file_version": FILE_VERS,
                "metric_type": health_metric.metric_type.value,
                "metric_guide": health_metric.metric_guide(),
                "data": [],
            },
            health_file,
        )

    logger.add("action", f"Created new metric file `{health_metric.metric_name}.json`.")
    return file_path


def get_filenames_without_extension(directory):
    """Returns a list of filenames in the given directory without their extensions."""
    directory_path = Path(directory)
    filenames = [file.stem for file in directory_path.iterdir() if file.is_file()]

    return filenames


def add_measurement_to_metric_file(metric_name: str, measurement: Measurement):
    """Adds a new entry (date and value) to an existing health JSON file, accepts a datetime object for the date."""
    # Load existing data
    filename = f"{FILE_DIR_NAME}/{metric_name}.json"
    try:
        with open(filename, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File {filename} not found. Please create the file first.")
        return

    # Convert datetime to string in ISO format
    date_str = measurement.date.isoformat()

    # Add new entry
    new_entry = {"date": date_str, "value": measurement.value}
    data["data"].append(new_entry)

    # Write updated data back to the file
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def rename_health_file(current_metric_name: str, new_metric_name: str):
    # Specify the old and new file names
    old_file = Path(f"{FILE_DIR_NAME}/{current_metric_name}.json")
    new_file = Path(f"{FILE_DIR_NAME}/{new_metric_name}.json")

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

    # Rename attribute.
    try:
        with open(str(new_file), "r") as file:
            data = json.load(file)
        key_to_modify = "metric_name"

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


def parse_health_metric(metric_name: str) -> HealthMetric:
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
    response = input(prompt).lower()

    parsed_metric_type = MetricType(supported_types.get(response, "metric"))

    if parsed_metric_type == MetricType.Ranged:
        print(
            f"\nParsing new ranged metric {metric_name}, format is (lower_bound upper_bound):"
        )
        lower, upper = input(prompt).split(" ")
        metric = RangedMetric(
            metric_name=metric_name,
            range_minimum=float(lower),
            range_maximum=float(upper),
        )

    elif parsed_metric_type == MetricType.GreaterThan:
        print(
            f"\nParsing new GreaterThan metric '{metric_name}', format is (upper_bound):"
        )
        lower = float(input(prompt))
        metric = GreaterThanMetric(metric_name=metric_name, minimum_value=lower)

    elif parsed_metric_type == MetricType.LessThan:
        print(f"\nParsing new LessThan metric '{metric_name}' (lower_bound):")
        upper = float(input(prompt))
        metric = LessThanMetric(metric_name=metric_name, maximum_value=upper)

    elif parsed_metric_type == MetricType.Boolean:
        print(f"\nParsing new Boolean metric '{metric_name}' (boolean):")
        boolean = str(input(prompt)).lower() == "true"
        metric = BooleanMetric(metric_name=metric_name, ideal_boolean_value=boolean)

    elif parsed_metric_type == MetricType.Metric:
        print(f"\nParsing new generic metric '{metric_name}' (metric):")
        metric = HealthMetric(metric_name=metric_name)

    print(
        f"\n === New metric file '{metric_name}' generated (reporting {len(get_filenames_without_extension(FILE_DIR_NAME)) + 1} metric files) === \n"
    )
    return metric
