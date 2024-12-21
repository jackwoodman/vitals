from metric_file_tools import rename_health_file
from logger import logger


def rename():
    old_metric_name = input("-> rename which metric file? ")
    new_metric_name = input(f"-> rename '{old_metric_name}' to what? ")

    print(f"Renaming '{old_metric_name}' to '{new_metric_name}'...")
    rename_health_file(
        current_metric_name=old_metric_name, new_metric_name=new_metric_name
    )

    logger.add("action", f"Renamed metric '{old_metric_name}' to '{new_metric_name}'")
