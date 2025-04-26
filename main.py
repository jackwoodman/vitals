import sys
from file_tools.utils import create_metric_dir
from high_level_functions.entry_points import (
    analyse,
    graph,
    manage,
    memorise,
    read,
    write,
)
from high_level_functions.utils import exit
from utils.cli_displays import welcome
from utils.logger import logger

from utils.utils import function_mapping_t, generic_hll_function


from global_functions import global_function_register


def high_level_loop():
    # Defines mapping of commands to their respective functions.
    function_mapping: function_mapping_t = {
        "write": write,
        "read": read,
        "graph": graph,
        "manage": manage,
        "analyse": analyse,
        "memorise": memorise,
        "exit": exit,
    } | global_function_register

    generic_hll_function(sub_func_map=function_mapping, hll_name="main")
    exit(None)


if __name__ == "__main__":
    welcome()
    # If no directory exists, generate one.
    create_metric_dir()

    # Start high level loop
    try:
        high_level_loop()
    except KeyboardInterrupt:
        # Do some cleanup before allowing program to close.
        print()
        logger.add("WARNING", "HLL terminated due to interrupt signal.", cli_out=True)
        logger.dump_to_file()
        exit(None)
        sys.exit()
