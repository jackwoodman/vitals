import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio


def initialise_plot():
    """Initializes an empty plotly figure with a base layout."""
    fig = go.Figure(
        layout={
            "xaxis": {"title": "X-axis"},
            "yaxis": {"title": "Y-axis1", "side": "left"},
        }
    )

    fig.layout.template = pio.templates["plotly_dark"]
    return fig


def add_lines(fig, objects):
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
    for i, obj in enumerate(objects):
        # Extract x, y data
        x_vals = [p.value for p in obj.entries]
        y_vals = [p.date for p in obj.entries]

        # Create a new y-axis if needed (each new line will get its own y-axis)
        if i > 0:
            axis_name = f"yaxis{i+1}"
            fig.update_layout(
                {
                    axis_name: {
                        "title": f"Y-axis{i+1}",
                        "overlaying": "y",
                        "side": "right",
                        "position": 1 - (i * 0.05),  # Adjust position for each new axis
                    }
                }
            )
            y_axis_ref = f"y{i+1}"
        else:
            y_axis_ref = "y"

        # Plot the main line for the object
        fig.add_trace(
            go.Scatter(
                x=x_vals,
                y=y_vals,
                mode="lines",
                name=obj.metric_name,
                yaxis=y_axis_ref,  # Refer to the appropriate y-axis
            )
        )

        # Handle special cases for different object types (ranged, greater_than, less_than)
        if obj.metric_type.value == "ranged":
            a, b = obj.range_minimum, obj.range_maximum
            print(a, b)
            # Add shading between the range [a, b]
            fig.add_trace(
                go.Scatter(
                    x=x_vals,
                    y=[a] * len(x_vals),
                    fill=None,
                    mode="lines",
                    line=dict(color="rgba(255,0,0,0.2)", dash="dash"),
                    name=f"{obj.metric_name} Lower Bound",
                    yaxis=y_axis_ref,
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=x_vals,
                    y=[b] * len(x_vals),
                    fill="tonexty",
                    mode="lines",
                    line=dict(color="rgba(255,0,0,0.2)", dash="dash"),
                    name=f"{obj.metric_name} Upper Bound",
                    yaxis=y_axis_ref,
                )
            )
        elif obj.metric_type.value == "greater_than":
            # Add a faint line for the minimum value
            fig.add_trace(
                go.Scatter(
                    x=x_vals,
                    y=[obj.min_value] * len(x_vals),
                    mode="lines",
                    line=dict(color="rgba(0,255,0,0.3)", dash="dash"),
                    name=f"{obj.metric_name} Min Value",
                    yaxis=y_axis_ref,
                )
            )
        elif obj.metric_type.value == "less_than":
            # Add a faint line for the maximum value
            fig.add_trace(
                go.Scatter(
                    x=x_vals,
                    y=[obj.max_value] * len(x_vals),
                    mode="lines",
                    line=dict(color="rgba(0,0,255,0.3)", dash="dash"),
                    name=f"{obj.metric_name} Max Value",
                    yaxis=y_axis_ref,
                )
            )

    return fig


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
                line=dict(color="rgba(255,0,0,0.8)", dash="dash"),
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
                line=dict(color="rgba(255,0,0,0.8)", dash="dash"),
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
                line=dict(color="rgba(255,0,0,0.5)", dash="dash"),
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
                line=dict(color="rgba(255,0,0,0.3)", dash="dash"),
                name=f"{metric_object.metric_name} Maximum",
                yaxis=y_axis_ref,
            )
        )

    return fig
