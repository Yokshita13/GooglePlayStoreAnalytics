import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pytz


# ---------------------------------------------------------
# FUNCTION TO CHECK IST TIME
# ---------------------------------------------------------
def check_time(start_hour, end_hour):

    india = pytz.timezone("Asia/Kolkata")

    current_time = datetime.now(india)

    current_hour = current_time.hour

    if start_hour <= current_hour < end_hour:
        return True

    return False


# ---------------------------------------------------------
# CHART 1
# GROUPED BAR CHART
# ---------------------------------------------------------
def grouped_bar_chart(df):

    # Show only between 3 PM and 5 PM IST
    if not check_time(15, 17):
        return go.Figure()

    temp = df.copy()

    # Rating >= 4
    temp = temp[temp["Rating"] >= 4]

    # Size >10 MB
    temp = temp[temp["Size_MB"] >= 10]

    # January only
    temp = temp[temp["Month"] == "January"]

    # Top 10 Categories by Installs
    top_categories = (
        temp.groupby("Category")["Installs"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .index
    )

    temp = temp[temp["Category"].isin(top_categories)]

    chart_data = (
        temp.groupby("Category")
        .agg(
            Average_Rating=("Rating", "mean"),
            Total_Reviews=("Reviews", "sum")
        )
        .reset_index()
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=chart_data["Category"],
            y=chart_data["Average_Rating"],
            name="Average Rating"
        )
    )

    fig.add_trace(
        go.Bar(
            x=chart_data["Category"],
            y=chart_data["Total_Reviews"],
            name="Total Reviews"
        )
    )

    fig.update_layout(

        title="Average Rating vs Total Reviews",

        xaxis_title="Category",

        yaxis_title="Values",

        barmode="group",

        template="plotly_white"

    )

    return fig












# ---------------------------------------------------------
# CHART 2
# CHOROPLETH MAP
# ---------------------------------------------------------
def choropleth_map(df):

    # Show only between 6 PM and 8 PM IST
    if not check_time(18, 20):
        return go.Figure()

    temp = df.copy()

    # Remove categories starting with A, C, G, S
    temp = temp[
        ~temp["Category"].str.startswith(
            ("A", "C", "G", "S"),
            na=False
        )
    ]

    # Top 5 Categories by installs
    top_categories = (
        temp.groupby("Category")["Installs"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .index
    )

    temp = temp[temp["Category"].isin(top_categories)]

    # Total installs per category
    chart_data = (
        temp.groupby("Category", as_index=False)["Installs"]
        .sum()
    )

    # Dummy country mapping (replace if your dataset has countries)
    country_mapping = {
        chart_data.iloc[0]["Category"]: "India",
        chart_data.iloc[1]["Category"]: "United States",
        chart_data.iloc[2]["Category"]: "Brazil",
        chart_data.iloc[3]["Category"]: "Germany",
        chart_data.iloc[4]["Category"]: "Australia"
    }

    chart_data["Country"] = chart_data["Category"].map(country_mapping)

    # Highlight installs > 1 million
    chart_data["Highlight"] = chart_data["Installs"] > 1_000_000

    fig = px.choropleth(
        chart_data,
        locations="Country",
        locationmode="country names",
        color="Installs",
        hover_name="Category",
        hover_data=["Installs", "Highlight"],
        color_continuous_scale="Viridis",
        title="Global Installs by Top 5 Categories"
    )

    fig.update_layout(
        template="plotly_white",
        margin=dict(l=10, r=10, t=60, b=10)
    )

    return fig















# ---------------------------------------------------------
# CHART 3
# DUAL AXIS CHART
# ---------------------------------------------------------

def dual_axis_chart(df):

    # Show only between 1 PM and 2 PM IST
    if not check_time(13, 14):
        return go.Figure()

    temp = df.copy()

    # ----------------------------
    # Apply Filters
    # ----------------------------

    temp = temp[temp["Installs"] >= 10000]

    temp = temp[temp["Revenue"] >= 10000]

    temp = temp[temp["Android Version Numeric"] > 4.0]

    temp = temp[temp["Size_MB"] > 15]

    temp = temp[temp["Content Rating"] == "Everyone"]

    temp = temp[
        temp["App"].astype(str).str.len() <= 30
    ]

    # ----------------------------
    # Top 3 Categories
    # ----------------------------

    top_categories = (
        temp.groupby("Category")["Installs"]
        .sum()
        .sort_values(ascending=False)
        .head(3)
        .index
    )

    temp = temp[
        temp["Category"].isin(top_categories)
    ]

    # ----------------------------
    # Aggregate Data
    # ----------------------------

    chart_data = (
        temp.groupby(["Category", "Type"])
        .agg(
            Average_Installs=("Installs", "mean"),
            Revenue=("Revenue", "sum")
        )
        .reset_index()
    )

    # ----------------------------
    # Create Figure
    # ----------------------------

    fig = go.Figure()

    # Average Installs (Bar)

    fig.add_trace(

        go.Bar(

            x=chart_data["Category"] + " (" + chart_data["Type"] + ")",

            y=chart_data["Average_Installs"],

            name="Average Installs",

            yaxis="y1"

        )

    )

    # Revenue (Line)

    fig.add_trace(

        go.Scatter(

            x=chart_data["Category"] + " (" + chart_data["Type"] + ")",

            y=chart_data["Revenue"],

            mode="lines+markers",

            name="Revenue",

            yaxis="y2"

        )

    )

    # ----------------------------
    # Layout
    # ----------------------------

    fig.update_layout(

        title="Average Installs vs Revenue (Free & Paid Apps)",

        template="plotly_white",

        xaxis=dict(

            title="Category (Free / Paid)"

        ),

        yaxis=dict(

            title="Average Installs"

        ),

        yaxis2=dict(

            title="Revenue",

            overlaying="y",

            side="right"

        ),

        legend=dict(

            orientation="h",

            y=1.1

        )

    )

    return fig















# ---------------------------------------------------------
# CHART 4
# TIME SERIES LINE CHART
# ---------------------------------------------------------

def time_series_chart(df):

    # Show only between 6 PM and 9 PM IST
    if not check_time(18, 21):
        return go.Figure()

    temp = df.copy()

    # -----------------------------------
    # Filters
    # -----------------------------------

    temp = temp[
        temp["Category"].isin(["Beauty", "Business", "Education"])
    ]

    temp = temp[
        ~temp["App"].str.startswith(("X", "Y", "Z"), na=False)
    ]

    temp = temp[
        ~temp["App"].str.contains("S", case=False, na=False)
    ]

    temp = temp[
        temp["Reviews"] > 500
    ]

    # -----------------------------------
    # Translate Categories
    # -----------------------------------

    translation = {
        "Beauty": "सौंदर्य",
        "Business": "வணிகம்",
        "Dating": "Dating (Deutsch)"
    }

    temp["Display Category"] = (
        temp["Category"]
        .replace(translation)
    )

    # -----------------------------------
    # Monthly Installs
    # -----------------------------------

    chart_data = (

        temp.groupby(
            ["Last Updated", "Display Category"]
        )["Installs"]

        .sum()

        .reset_index()

    )

    chart_data = chart_data.sort_values(
        "Last Updated"
    )

    # -----------------------------------
    # Month-over-Month Growth
    # -----------------------------------

    chart_data["Growth"] = (

        chart_data
        .groupby("Display Category")["Installs"]
        .pct_change()

    )

    chart_data["Highlight"] = (

        chart_data["Growth"] > 0.20

    )

    # -----------------------------------
    # Plot
    # -----------------------------------

    fig = go.Figure()

    categories = chart_data["Display Category"].unique()

    for cat in categories:

        data = chart_data[
            chart_data["Display Category"] == cat
        ]

        # Main Line

        fig.add_trace(

            go.Scatter(

                x=data["Last Updated"],

                y=data["Installs"],

                mode="lines",

                name=cat

            )

        )

        # Highlight Growth >20%

        highlight = data[
            data["Highlight"]
        ]

        fig.add_trace(

            go.Scatter(

                x=highlight["Last Updated"],

                y=highlight["Installs"],

                mode="markers",

                marker=dict(

                    size=12,

                    color="red"

                ),

                name=cat + " Growth >20%"

            )

        )

        # Shade Area

        fig.add_trace(

            go.Scatter(

                x=highlight["Last Updated"],

                y=highlight["Installs"],

                fill="tozeroy",

                mode="none",

                opacity=0.20,

                showlegend=False

            )

        )

    # -----------------------------------
    # Layout
    # -----------------------------------

    fig.update_layout(

        title="Monthly Install Trend by Category",

        xaxis_title="Last Updated",

        yaxis_title="Installs",

        template="plotly_white",

        hovermode="x unified"

    )

    return fig



















# ---------------------------------------------------------
# CHART 5
# BUBBLE CHART
# ---------------------------------------------------------

def bubble_chart(df, reviews_df=None):

    # Show only between 5 PM and 7 PM IST
    if not check_time(17, 19):
        return go.Figure()

    temp = df.copy()

    # -----------------------------------
    # Merge Sentiment Dataset (if available)
    # -----------------------------------

    if reviews_df is not None:

        sentiment = (
            reviews_df.groupby("App")["Sentiment_Subjectivity"]
            .mean()
            .reset_index()
        )

        temp = temp.merge(
            sentiment,
            on="App",
            how="left"
        )

    else:
        temp["Sentiment_Subjectivity"] = 1

    # -----------------------------------
    # Category Filter
    # -----------------------------------

    categories = [

        "GAME",

        "BEAUTY",

        "BUSINESS",

        "COMICS",

        "COMMUNICATION",

        "DATING",

        "ENTERTAINMENT",

        "SOCIAL",

        "EVENTS"

    ]

    temp = temp[
        temp["Category"].str.upper().isin(categories)
    ]

    # -----------------------------------
    # Apply Filters
    # -----------------------------------

    temp = temp[
        temp["Rating"] > 3.5
    ]

    temp = temp[
        temp["Reviews"] > 500
    ]

    temp = temp[
        temp["Installs"] > 50000
    ]

    temp = temp[
        temp["Sentiment_Subjectivity"] > 0.5
    ]

    temp = temp[
        ~temp["App"].str.contains(
            "S",
            case=False,
            na=False
        )
    ]

    # -----------------------------------
    # Category Translation
    # -----------------------------------

    translation = {

        "Beauty": "सौंदर्य",

        "Business": "வணிகம்",

        "Dating": "Dating (Deutsch)"

    }

    temp["Display Category"] = (
        temp["Category"]
        .replace(translation)
    )

    # -----------------------------------
    # Bubble Color
    # -----------------------------------

    temp["BubbleColor"] = temp["Display Category"]

    temp.loc[
        temp["Category"].str.upper() == "GAME",
        "BubbleColor"
    ] = "GAME"

    color_map = {

        "GAME": "pink",

        "सौंदर्य": "purple",

        "வணிகம்": "green",

        "Dating (Deutsch)": "orange"

    }

    # -----------------------------------
    # Bubble Chart
    # -----------------------------------

    fig = px.scatter(

        temp,

        x="Size_MB",

        y="Rating",

        size="Installs",

        color="BubbleColor",

        hover_name="App",

        color_discrete_map=color_map,

        title="App Size vs Rating"

    )

    fig.update_layout(

        template="plotly_white",

        xaxis_title="App Size (MB)",

        yaxis_title="Average Rating"

    )

    return fig























# ---------------------------------------------------------
# CHART 6
# STACKED AREA CHART
# ---------------------------------------------------------

def stacked_area_chart(df):

    # Show only between 4 PM and 6 PM IST
    if not check_time(16, 18):
        return go.Figure()

    temp = df.copy()

    # ------------------------------------
    # Filters
    # ------------------------------------

    temp = temp[temp["Rating"] >= 4.2]

    temp = temp[temp["Reviews"] > 1000]

    temp = temp[
        (temp["Size_MB"] >= 20) &
        (temp["Size_MB"] <= 80)
    ]

    # Category starts with T or P
    temp = temp[
        temp["Category"].str.startswith(
            ("T", "P"),
            na=False
        )
    ]

    # Remove App Names containing numbers
    temp = temp[
        ~temp["App"].str.contains(
            r"\d",
            regex=True,
            na=False
        )
    ]

    # ------------------------------------
    # Category Translation
    # ------------------------------------

    translation = {

        "Travel & Local": "Voyage et Local",

        "Productivity": "Productividad",

        "Photography": "写真"

    }

    temp["Display Category"] = (
        temp["Category"]
        .replace(translation)
    )

    # ------------------------------------
    # Monthly Installs
    # ------------------------------------

    chart_data = (

        temp.groupby(

            ["Month", "Display Category"]

        )["Installs"]

        .sum()

        .reset_index()

    )

    # ------------------------------------
    # Month Order
    # ------------------------------------

    month_order = [

        "January",

        "February",

        "March",

        "April",

        "May",

        "June",

        "July",

        "August",

        "September",

        "October",

        "November",

        "December"

    ]

    chart_data["Month"] = pd.Categorical(

        chart_data["Month"],

        categories=month_order,

        ordered=True

    )

    chart_data = chart_data.sort_values("Month")

    # ------------------------------------
    # Growth Calculation
    # ------------------------------------

    chart_data["Growth"] = (

        chart_data

        .groupby("Display Category")["Installs"]

        .pct_change()

    )

    chart_data["Highlight"] = (

        chart_data["Growth"] > 0.25

    )

    # ------------------------------------
    # Plot
    # ------------------------------------

    fig = px.area(

        chart_data,

        x="Month",

        y="Installs",

        color="Display Category",

        title="Cumulative Installs Over Time"

    )

    # Highlight months with >25% growth
    highlight = chart_data[
        chart_data["Highlight"]
    ]

    fig.add_trace(

        go.Scatter(

            x=highlight["Month"],

            y=highlight["Installs"],

            mode="markers",

            marker=dict(

                size=12,

                color="red"

            ),

            name="Growth >25%"

        )

    )

    fig.update_layout(

        template="plotly_white",

        hovermode="x unified",

        xaxis_title="Month",

        yaxis_title="Total Installs"

    )

    return fig
