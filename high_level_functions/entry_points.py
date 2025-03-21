from high_level_functions.manage import instantiate, rename, search, show, update_units
from high_level_functions.graph import from_names
from high_level_functions.read import read_by_name
from high_level_functions.write import data_entry_mode
from utils.utils import generic_hll_function
from utils.utils import function_mapping_t
from data.analysis_tools import find_oor


def memorise(_: list):
    function_mapping: function_mapping_t = {}

    generic_hll_function(
        sub_func_map=function_mapping, hll_name="memorise", proper_name="memory"
    )


def analyse(_: list):
    function_mapping: dict[str, callable] = {
        "find_oor": find_oor,
    }

    generic_hll_function(
        sub_func_map=function_mapping, hll_name="analyse", proper_name="analysis"
    )


def graph(_: list):
    function_mapping: dict[str, callable] = {
        "from_names": from_names,
    }

    generic_hll_function(
        sub_func_map=function_mapping, hll_name="graph", proper_name="graphing"
    )


def read(_: list):
    function_mapping: function_mapping_t = {"read_metric": read_by_name}

    generic_hll_function(
        sub_func_map=function_mapping, hll_name="read", proper_name="reading"
    )


def write(_: list):
    function_mapping: function_mapping_t = {"data_entry": data_entry_mode}

    generic_hll_function(
        sub_func_map=function_mapping, hll_name="write", proper_name="writing"
    )


def manage(_: list):
    function_mapping: dict[str, callable] = {
        "rename": rename,
        "show": show,
        "search": search,
        "instantiate": instantiate,
        "update_units": update_units,
    }

    generic_hll_function(
        sub_func_map=function_mapping, hll_name="manage", proper_name="management"
    )
