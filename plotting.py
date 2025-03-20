import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

default_template = pio.templates["plotly_dark"]


def empty_figure():
    figure = go.Figure()
    figure.layout.template = default_template
    return figure


def initialise_plot():
    """Initializes an empty plotly figure with a base layout."""
    fig = go.Figure(
        layout={
            "xaxis": {"title": "X-axis"},
            "yaxis": {"title": "Y-axis1", "side": "left"},
        }
    )

    fig.layout.template = default_template
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


def add_multiple_lines(fig, metric_objects):
    """
    Adds lines and shading for multiple metric objects. Objects with the same .unit attribute
    are plotted on the same y-axis; objects with different units get separate y-axes positioned
    on the left side of the graph, with each new axis further left.

    This implementation shifts the x-axis domain to [0.2, 1] and reduces the left margin so that
    the y-axes are closer to the plot area.

    Args:
        fig: The Plotly figure to update.
        metric_objects: List of objects to plot, where each object has:
            - entries: List of data points with attributes .date and .value.
            - metric_name: The name of the metric (used for the legend).
            - metric_type: An object with attribute .value ("ranged", "greater_than", or "less_than").
            - range_minimum, range_maximum: For "ranged" objects, the bounds of the shaded region.
            - bound: For "greater_than" or "less_than" objects, the value at which to draw the line.
            - unit: A string representing the measurement unit (used for grouping traces on the same axis).
    """
    # Reserve a smaller left space for the axes.
    fig.update_layout(xaxis=dict(domain=[0.2, 1]), margin=dict(l=80))

    # Get the unique units in the order they appear.
    unique_units = []
    for obj in metric_objects:
        if obj.unit not in unique_units:
            unique_units.append(obj.unit)
    n = len(unique_units)

    # Define positions for y-axes in the reserved left margin.
    # The rightmost axis (closest to the plot) is at x=0.2.
    # Each additional axis is shifted further left by an offset.
    rightmost_pos = 0.2
    offset = 0.05
    unit_positions = {}
    for i, unit in enumerate(unique_units):
        pos = rightmost_pos - i * offset
        if pos < 0:
            pos = 0  # Ensure the position stays within [0,1]
        unit_positions[unit] = pos

    # Map each unit to an axis index.
    unit_to_axis = {}
    axis_index = 1

    # Configure y-axes on the left.
    for unit in unique_units:
        pos = unit_positions[unit]
        if axis_index == 1:
            # Primary y-axis uses the default "y"
            fig.update_layout(
                yaxis=dict(
                    title=f"Y-axis ({unit})", side="left", position=pos, anchor="free"
                )
            )
        else:
            axis_name = f"yaxis{axis_index}"
            fig.update_layout(
                {
                    axis_name: {
                        "title": f"Y-axis ({unit})",
                        "side": "left",
                        "overlaying": "y",
                        "position": pos,
                        "anchor": "free",
                    }
                }
            )
        unit_to_axis[unit] = axis_index
        axis_index += 1

    # Add traces for each metric object using the corresponding y-axis.
    for obj in metric_objects:
        current_axis_index = unit_to_axis[obj.unit]
        yaxis_ref = "y" if current_axis_index == 1 else f"y{current_axis_index}"

        # Extract x and y data.
        x_vals = [p.date for p in obj.entries]
        y_vals = [p.value for p in obj.entries]

        # Main line trace.
        fig.add_trace(
            go.Scatter(
                x=x_vals,
                y=y_vals,
                mode="lines+markers",
                name=obj.metric_name,
                yaxis=yaxis_ref,
            )
        )

        # Additional traces based on metric type.
        if obj.metric_type.value == "ranged":
            a, b = obj.range_minimum, obj.range_maximum
            # Lower bound trace.
            fig.add_trace(
                go.Scatter(
                    x=x_vals,
                    y=[a] * len(x_vals),
                    mode="lines",
                    fill=None,
                    line=dict(color="rgba(255,0,0,0.8)", dash="dash"),
                    name=f"{obj.metric_name} Lower Bound",
                    yaxis=yaxis_ref,
                )
            )
            # Upper bound trace.
            fig.add_trace(
                go.Scatter(
                    x=x_vals,
                    y=[b] * len(x_vals),
                    mode="lines",
                    fill=None,
                    line=dict(color="rgba(255,0,0,0.8)", dash="dash"),
                    name=f"{obj.metric_name} Upper Bound",
                    yaxis=yaxis_ref,
                )
            )
        elif obj.metric_type.value == "greater_than":
            # Minimum bound trace.
            fig.add_trace(
                go.Scatter(
                    x=x_vals,
                    y=[obj.bound] * len(x_vals),
                    mode="lines",
                    fill=None,
                    line=dict(color="rgba(255,0,0,0.5)", dash="dash"),
                    name=f"{obj.metric_name} Minimum",
                    yaxis=yaxis_ref,
                )
            )
        elif obj.metric_type.value == "less_than":
            # Maximum bound trace.
            fig.add_trace(
                go.Scatter(
                    x=x_vals,
                    y=[obj.bound] * len(x_vals),
                    mode="lines",
                    line=dict(color="rgba(255,0,0,0.3)", dash="dash"),
                    name=f"{obj.metric_name} Maximum",
                    yaxis=yaxis_ref,
                )
            )

    return fig
