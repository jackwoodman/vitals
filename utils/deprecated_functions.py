from datetime import datetime
from classes import Measurement
from file_tools.metric_file_tools import (
    add_measurement_to_metric_file,
    generate_metric_file,
    parse_health_metric,
)


def parse_metric_entry() -> Measurement:
    print("\n -> Parsing new metric entry (metric_name value date):")
    met_name, value_str, date_str = input("    ").split(" ")

    return met_name, Measurement(
        value=float(value_str), date=datetime.strptime(date_str, "%d/%m/%Y")
    )


def old_write():
    direction = input("-> write new (metric) or new (entry)?\n")
    if direction == "metric":
        new_metric = parse_health_metric()
        generate_metric_file(health_metric=new_metric)
    else:
        metric_name, new_entry = parse_metric_entry()

        add_measurement_to_metric_file(metric_name=metric_name, measurement=new_entry)
        print(f"\n === New entry for '{metric_name}' added === \n")


def add_single_line(fig, metric_object):
    """Adds lines and shading to the plot. Each object can be:
    - ranged: Displays a shaded region for the range [a, b]
    - greater than: Displays a faint line at min_value (a)
    - less than: Displays a faint line at max_value (b)

    Args:
        fig: The plotly figure to update.
        objects: List of objects to plot, where each object has:
            - obj.list: A list of [x, y] values to plot.
            - obj.name: The name of the line to use in the legend.
            - obj.type: Type of the object ("ranged", "greater_than", "less_than")
            - obj.range: A tuple (a, b) for ranged objects.
            - obj.min_value: Minimum value (a) for greater_than objects.
            - obj.max_value: Maximum value (b) for less_than objects.
    """
    num_axes = 1  # Keep track of how many y-axes we have

    # Extract x, y data
    y_vals = [p.value for p in metric_object.entries]
    x_vals = [p.date for p in metric_object.entries]

    # Create a new y-axis if needed (each new line will get its own y-axis)
    axis_name = "yaxis1"
    fig.update_layout(
        {
            axis_name: {
                "title": f"Y-axis {metric_object.metric_name}",
                "overlaying": "y",
                "side": "right",
                "position": 1,  # Adjust position for each new axis
            }
        }
    )
    y_axis_ref = f"y{num_axes+1}"

    # Plot the main line for the object
    fig.add_trace(
        go.Scatter(
            x=x_vals,
            y=y_vals,
            mode="lines+markers",
            name=metric_object.metric_name,
            yaxis=y_axis_ref,
        )
    )

    # Handle special cases for different object types (ranged, greater_than, less_than)
    if metric_object.metric_type.value == "ranged":
        a, b = metric_object.range_minimum, metric_object.range_maximum

        # Add shading between the range [a, b]
        fig.add_trace(
            go.Scatter(
                x=x_vals,
                y=[a] * len(x_vals),
                fill=None,
                mode="lines",
                line=dict(color="rgba(255,0,0,0.8)", dash=BOUND_DASH_SETTING),
                name=f"{metric_object.metric_name} Lower Bound",
                yaxis=y_axis_ref,
            )
        )

        fig.add_trace(
            go.Scatter(
                x=x_vals,
                y=[b] * len(x_vals),
                fill=None,
                mode="lines",
                line=dict(color="rgba(255,0,0,0.8)", dash=BOUND_DASH_SETTING),
                name=f"{metric_object.metric_name} Upper Bound",
                yaxis=y_axis_ref,
            )
        )

    elif metric_object.metric_type.value == "greater_than":
        # Add a faint line for the minimum value
        fig.add_trace(
            go.Scatter(
                x=x_vals,
                y=[metric_object.bound] * len(x_vals),
                mode="lines",
                fill=None,
                line=dict(color="rgba(255,0,0,0.5)", dash=BOUND_DASH_SETTING),
                name=f"{metric_object.metric_name} Mininmum",
                yaxis=y_axis_ref,
            )
        )
    elif metric_object.metric_type.value == "less_than":
        # Add a faint line for the maximum value
        fig.add_trace(
            go.Scatter(
                x=x_vals,
                y=[metric_object.bound] * len(x_vals),
                mode="lines",
                line=dict(color="rgba(255,0,0,0.3)", dash=BOUND_DASH_SETTING),
                name=f"{metric_object.metric_name} Maximum",
                yaxis=y_axis_ref,
            )
        )

    return fig
