from dash import html, dcc

from charts import (
    grouped_bar_chart,
    choropleth_map,
    dual_axis_chart,
    time_series_chart,
    bubble_chart,
    stacked_area_chart
)


def create_dashboard(df, reviews_df=None):

    fig1 = grouped_bar_chart(df)

    fig2 = choropleth_map(df)

    fig3 = dual_axis_chart(df)

    fig4 = time_series_chart(df)

    fig5 = bubble_chart(df, reviews_df)

    fig6 = stacked_area_chart(df)

    layout = html.Div(

        [

            html.H1(

                "Google Play Store Analytics Dashboard",

                style={

                    "textAlign": "center",

                    "color": "#2E86C1",

                    "marginBottom": "30px"

                }

            ),

            html.Div(

                [

                    dcc.Graph(

                        figure=fig1,

                        style={"height": "600px"}

                    ),

                    dcc.Graph(

                        figure=fig2,

                        style={"height": "600px"}

                    ),

                ]

            ),

            html.Div(

                [

                    dcc.Graph(

                        figure=fig3,

                        style={"height": "600px"}

                    ),

                    dcc.Graph(

                        figure=fig4,

                        style={"height": "600px"}

                    ),

                ]

            ),

            html.Div(

                [

                    dcc.Graph(

                        figure=fig5,

                        style={"height": "600px"}

                    ),

                    dcc.Graph(

                        figure=fig6,

                        style={"height": "600px"}

                    ),

                ]

            )

        ],

        style={

            "backgroundColor": "#F8F9F9",

            "padding": "20px"

        }

    )

    return layout