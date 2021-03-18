import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from .components import color_group, grid_group, ft_card, vl_card, card, c0, c1, c2, c3, cl_dropdown

default_config = {'displayModeBar': False}

# <p> used for blank space

gen_div = html.Div([
    dbc.Row([dbc.Col(html.H6(dbc.Badge("Color by:", color='info')), width=0.5), dbc.Col([color_group], width=2)],
            style={'padding-left': '10px'}),
    dbc.Row([
        dbc.Col(dcc.Graph(id='gen-scatter', config=default_config), width=9),
        dbc.Col(
            html.Div([
                dbc.Row(html.H6(dbc.Badge("Categories' Centroids", color='info')), justify='center'),
                dbc.Row([dbc.Col(c0), dbc.Col(c1)]),
                dbc.Row([dbc.Col(c2), dbc.Col(c3)], style={'padding-top': '10px', 'padding-bottom': '10px'})
            ]),
        ),
    ], justify='center'),

    dbc.Row([dbc.Col(html.H6(dbc.Badge("Cluster:", color='info')), width=0.5), dbc.Col([cl_dropdown], width=3)],
            style={'padding-left': '10px'}),

    dbc.Row([
        dbc.Col(dcc.Graph(id='pie-chart', config=default_config), width=9),
        dbc.Col(card, width=2)
    ], justify='center', style={'padding-top': '20px'}),

    dbc.Row([
        dbc.Col(grid_group, width=1),
        dbc.Col(ft_card, width=5),
        dbc.Col(vl_card, width=5),
    ])
])

cluster_layout = html.Div(gen_div, style={'padding': '5px 10px 5px 10px'})
