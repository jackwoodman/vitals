import json
from pathlib import Path
from classes import GreaterThanMetric, HealthMetric, LessThanMetric, Measurement, MetricType, RangedMetric, BooleanMetric, HealthMetric

FILE_VERS = 7
FILE_DIR = "metric_files"


def read_metric_file_to_json(metric_name: str):
    """
    Return metric JSON data
    """
    filename = f"{FILE_DIR}/{metric_name}.json" if ".json" not in metric_name else metric_name

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
        lower_value, upper_value = metric_guide[1:-2].split(" ")
        metric = RangedMetric(
            metric_name=metric_name, range_minimum=float(lower_value[:-1]), range_maximum=float(upper_value)
        )
    elif metric_type == MetricType.GreaterThan:
        metric = GreaterThanMetric(metric_name=metric_name, minimum_value=float(metric_guide))
    elif metric_type == MetricType.LessThan:
        metric = LessThanMetric(metric_name=metric_name, maximum_value=float(metric_guide))

    for data_point in data_values:
        date = data_point["date"]
        data = float(data_point["value"])

        metric.add_entry(Measurement(data, date))

    return metric


def generate_health_metric_from_file(filepath: str) -> HealthMetric:
    health_data = read_metric_file_to_json(metric_name=filepath)

    metric = load_metric_from_json(health_data)

    return metric


def generate_health_file(health_metric: HealthMetric) -> str:
    with open(f"{FILE_DIR}/{health_metric.metric_name}.json", "w") as health_file:
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


def get_filenames_without_extension(directory):
    """Returns a list of filenames in the given directory without their extensions."""
    directory_path = Path(directory)
    filenames = [file.stem for file in directory_path.iterdir() if file.is_file()]

    return filenames


def add_measurement_to_metric_file(metric_name: str, measurement: Measurement):
    """Adds a new entry (date and value) to an existing health JSON file, accepts a datetime object for the date."""
    # Load existing data
    filename = f"{FILE_DIR}/{metric_name}.json"
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
    old_file = Path(f"health_files/{current_metric_name}.json")
    new_file = Path(f"health_files/{new_metric_name}.json")

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
            print(f" - Changed value of '{key_to_modify}' from '{old_value}' to '{new_metric_name}'")
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
    tab = "    "
    
    metric: HealthMetric = None
    supported_types = {
        "r": "ranged",
        "g": "greater_than",
        "l": "less_than",
        "b": "boolean",
        "m": "metric"
    }
    print("\n -> Parsing new health metric:")
    print("supported types: ")
    for key, name in supported_types.items():
        print(f" - ({key}){name[1:]}")
   
    response = input(tab).lower()

    parsed_metric_type = MetricType(supported_types.get(response, "metric"))

    if parsed_metric_type == MetricType.Ranged:
        print(f"\n{tab} -> Parsing new ranged metric {metric_name}, format is (lower_bound upper_bound):")
        lower, upper = input(2 * tab).split(" ")

        metric = RangedMetric(metric_name=metric_name, range_minimum=float(lower), range_maximum=float(upper))

    elif parsed_metric_type == MetricType.GreaterThan:
        print(f"\n{tab} -> Parsing new GreaterThan metric '{metric_name}', format is (upper_bound):")
        lower = float(input(2 * tab))
        metric = GreaterThanMetric(metric_name=metric_name, minimum_value=lower)

    elif parsed_metric_type == MetricType.LessThan:
        print(f"\n{tab} -> Parsing new LessThan metric '{metric_name}' (lower_bound):")
        upper = float(input("    "))
        metric = LessThanMetric(metric_name=metric_name, maximum_value=upper)

    elif parsed_metric_type == MetricType.Boolean:
        print(f"\n{tab} -> Parsing new Boolean metric '{metric_name}' (boolean):")
        boolean = str(input("    ")).lower() == "true"
        metric = BooleanMetric(metric_name=metric_name, ideal_boolean_value=boolean)

    elif parsed_metric_type == MetricType.Metric:
        print(f"\n{tab} -> Parsing new generic metric '{metric_name}' (metric):")
        metric = HealthMetric(metric_name=metric_name)
    print(get_filenames_without_extension(FILE_DIR))
    print(
        f"\n === New metric file '{metric_name}' generated (reporting {len(get_filenames_without_extension(FILE_DIR))} metric files) === \n"
    )
    return metric