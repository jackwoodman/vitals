from typing import Union
import plotly.graph_objects as go
import plotly.io as pio

default_template = pio.templates["plotly_dark"]

BOUND_LINE_COLOUR = "rgba(255,0,0,0.6)"
BOUND_DASH_SETTING = "dash"


def empty_figure():
    figure = go.Figure()
    figure.layout.template = default_template
    return figure


def plot_metrics(
    metric_objects: Union[list, object],
    starting_figure: go.Figure = None,
    show_bounds: bool = True,
):
    """
    Adds lines and shading for multiple metric objects. Objects with the same .unit attribute
    are plotted on the same y-axis; objects with different units get separate y-axes positioned
    on the left side of the graph, with each new axis further left.

    This implementation shifts the x-axis domain to [0.2, 1] and reduces the left margin so that
    the y-axes are closer to the plot area.

    Args:
        metric_objects: List of HealthMetric objects to be plotted, or a single HealthMetric to plot.
        starting_figure: The Plotly figure to update, if required.
        show_bounds: A bool indicating whether ideal bounds should be plotted. Default True.
    """
    unit_to_axis = {}
    axis_index = 1

    # Check if list of metrics or single metric was provided.
    metric_objects = (
        metric_objects if isinstance(metric_objects, list) else [metric_objects]
    )

    # Check if initial figure was provided.
    fig = starting_figure or empty_figure()

    # Reserve a smaller left space for the axes.
    fig.update_layout(xaxis=dict(domain=[0.2, 1]), margin=dict(l=80))

    # Get the unique units.
    unique_units = list(set([metric.unit for metric in metric_objects]))

    rightmost_pos = 0.2  # The rightmost axis (closest to the plot) is at x=0.2.
    offset = 0.05  # Each additional axis is shifted further left by an offset.

    unit_positions = {
        unit: max(rightmost_pos - unit_index * offset, 0)
        for unit_index, unit in enumerate(unique_units)
    }  # max() ensures value is within [0, 1]

    # Configure y-axes on the left.
    for unit in unique_units:
        pos = unit_positions[unit]
        unit_text = unit if unit else "Unitless"
        if axis_index == 1:
            # Primary y-axis uses the default "y".
            fig.update_layout(
                yaxis=dict(
                    title=f"Y-axis ({unit_text})",
                    side="left",
                    position=pos,
                    anchor="free",
                )
            )
        else:
            # All other axes are offset by 0.05 from the previous axis.
            axis_name = f"yaxis{axis_index}"
            fig.update_layout(
                {
                    axis_name: {
                        "title": f"Y-axis ({unit_text})",
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
    for metric in metric_objects:
        current_axis_index = unit_to_axis[metric.unit]
        yaxis_ref = "y" if current_axis_index == 1 else f"y{current_axis_index}"

        # Extract x and y data.
        x_vals = [measurement.date for measurement in metric.entries]
        y_vals = [measurement.value for measurement in metric.entries]

        # Main line trace.
        fig.add_trace(
            go.Scatter(
                x=x_vals,
                y=y_vals,
                mode="lines+markers",
                name=metric.metric_name,
                yaxis=yaxis_ref,
            )
        )

        # Additional code to show bounding lines.
        if show_bounds:
            # Additional traces based on metric type.
            if metric.metric_type.value == "ranged":
                a, b = metric.range_minimum, metric.range_maximum
                # Lower bound trace.
                fig.add_trace(
                    go.Scatter(
                        x=x_vals,
                        y=[a] * len(x_vals),
                        mode="lines",
                        fill=None,
                        line=dict(color=BOUND_LINE_COLOUR, dash=BOUND_DASH_SETTING),
                        name=f"{metric.metric_name} Lower Bound",
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
                        line=dict(color=BOUND_LINE_COLOUR, dash=BOUND_DASH_SETTING),
                        name=f"{metric.metric_name} Upper Bound",
                        yaxis=yaxis_ref,
                    )
                )
            elif metric.metric_type.value == "greater_than":
                # Minimum bound trace.
                fig.add_trace(
                    go.Scatter(
                        x=x_vals,
                        y=[metric.bound] * len(x_vals),
                        mode="lines",
                        fill=None,
                        line=dict(color=BOUND_LINE_COLOUR, dash=BOUND_DASH_SETTING),
                        name=f"{metric.metric_name} Minimum",
                        yaxis=yaxis_ref,
                    )
                )
            elif metric.metric_type.value == "less_than":
                # Maximum bound trace.
                fig.add_trace(
                    go.Scatter(
                        x=x_vals,
                        y=[metric.bound] * len(x_vals),
                        mode="lines",
                        line=dict(color=BOUND_LINE_COLOUR, dash=BOUND_DASH_SETTING),
                        name=f"{metric.metric_name} Maximum",
                        yaxis=yaxis_ref,
                    )
                )

    return fig
