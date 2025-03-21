from utils.plotting import plot_metrics
from utils.utils import attempt_ingest_from_name


def from_names(arguments: list):
    # Read requested file.
    health_metrics = attempt_ingest_from_name(arguments, "graph")

    if health_metrics:
        if not isinstance(health_metrics, list):
            current_plot = health_metrics.graph_metric()
        else:
            current_plot = plot_metrics(health_metrics, show_bounds=True)

        current_plot.show()
