import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from .components import cat_table, cat_treemap, invert_button, scale_group, x_dropdown, y_dropdown, card

default_config = {'displayModeBar': False}

hist_table_div = html.Div([
    dbc.Row([
        dbc.Col(cat_table, width=3),
        dbc.Col(dcc.Graph(id='cat-barchart', config=default_config)),
    ]),
    dbc.Row(dbc.Col(html.Div(dcc.Graph(id='cat-treemap', config=default_config, figure=cat_treemap))))
])

summary_div = html.Div([
    dbc.Row([
        dbc.Col(invert_button, width=1.5, style={'margin-right': '10px'}),
        dbc.Col(dbc.Badge("X:", color='info'), width=0.1), dbc.Col(x_dropdown, width=2),
        dbc.Col(dbc.Badge("Y:", color='info'), width=0.1), dbc.Col(y_dropdown, width=2),
        dbc.Col(dbc.Badge("X Scale:", color='info'), width=0.1), dbc.Col(scale_group, width=1),
    ], justify='center'),
    dbc.Row([
        dbc.Col(dcc.Graph(id='summary-plot', config=default_config), width=9),
        dbc.Col(card, style={'padding-top': '20px'})
    ])
])

cat_layout = html.Div([hist_table_div, summary_div], style={'margin': '5px 10px 5px 10px'})
