# charts_creator.py
import plotly.express as px


def plot_beveridge_curve(df, country):
    # Create a customdata array with the date, unemployment rate, and job vacancy rate
    df['date'] = df['original_period'].dt.strftime('%Y-%m')
    df['customdata'] = df.apply(lambda row: [row['date'], row['unemployment rate'], row['job vacancy']], axis=1)

    # Create a scatter plot
    fig = px.scatter(
        df,
        x="unemployment rate",
        y="job vacancy",
        title=f"Beveridge curve for {country}",
        labels={
            "job vacancy": "Job Vacancy rate (%)",
            "unemployment rate": "Unemployment rate (%)",
        },
        custom_data=['date', 'unemployment rate', 'job vacancy']
    )

    # Add a line trace
    line_fig = px.line(df, x="unemployment rate", y="job vacancy")
    for trace in line_fig.data:
        fig.add_trace(trace)

    # Update hover template to include the custom data
    fig.update_traces(
        hovertemplate="<br>".join([
            "Date: %{customdata[0]}",
            "Unemployment rate (%): %{customdata[1]}",
            "Job Vacancy rate (%): %{customdata[2]}"
        ])
    )
    return fig
