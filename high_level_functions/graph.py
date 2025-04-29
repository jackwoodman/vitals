from global_functions import source_metric
from utils.plotting import plot_metrics


def from_names(arguments: list):
    # Read requested file.
    health_metrics = source_metric(arguments).as_list()

    if health_metrics:
        if len(health_metrics) == 1:
            current_plot = health_metrics[0].graph_metric()
        else:
            current_plot = plot_metrics(health_metrics, show_bounds=True)

        current_plot.show()
