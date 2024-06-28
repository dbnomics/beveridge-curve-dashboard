# charts_creator.py
import plotly.express as px


def plot_beveridge_curve(df, country):
    # Create a scatter plot
    fig = px.scatter(
        df,
        x="job vacancy",
        y="unemployment rate",
        title=f"Beveridge curve for {country}",
        labels={
            "job vacancy": "Job Vacancy rate (%)",
            "unemployment rate": "Unemployment rate (%)",
        },
    )

    # Add a line trace
    line_fig = px.line(df, x="job vacancy", y="unemployment rate")
    for trace in line_fig.data:
        fig.add_trace(trace)

    # Update text position
    fig.update_traces(textposition="bottom right")
    return fig
