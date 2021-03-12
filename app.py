import os

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State

from config import DATA_DIR

# setup default layout

# NAVBAR
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Categories & Countables", id='nav-cat-btn', href="categories")),
        dbc.NavItem(dbc.NavLink("Clusters", id='nav-cluster-btn', href="clusters")),
        dbc.NavItem(dbc.NavLink("Project Info", id='nav-info-btn', href="#", external_link=False)),
        dbc.DropdownMenu(children=[
            dbc.DropdownMenuItem("Tools", header=True),

            dbc.DropdownMenuItem("Plotly + Dash", href="https://plotly.com/",
                                 external_link=True, target="_blank"),
            dbc.DropdownMenuItem("Dash Bootstrap", href="https://dash-bootstrap-components.opensource.faculty.ai/",
                                 external_link=True, target="_blank"),

            dbc.DropdownMenuItem("Code References", header=True),

            dbc.DropdownMenuItem("GitHub", href="https://github.com/jacopo-massa/sldv-project",
                                 external_link=True, target="_blank"),
            dbc.DropdownMenuItem("ViDA 3D", href="http://vcg.isti.cnr.it/Publications/2020/AFBCPCG20/",
                                 external_link=True, target="_blank")
        ],
            nav=True, in_navbar=True, label="More")
    ],
    brand="ViDA Summary", color="info", dark=True, sticky='top', style={'margin': '0px 0px 0px 0px'}
)

# callback to open/close modal is in apps/categories/callbacks.py
modal = dbc.Modal([
    dbc.ModalHeader("Dataset Summary Visualization"),
    dbc.ModalBody([
        dbc.Card([
            dbc.CardHeader(
                dbc.Tabs([
                    dbc.Tab(label="Italian 🇮🇹", tab_id='ita'),
                    dbc.Tab(label="English 🇬🇧", tab_id='eng'),
                ], id="card-tabs", card=True, active_tab='ita')
            ),
            dbc.CardBody(id="card-content"),
        ], color='info', outline=True)
    ]),
    dbc.ModalFooter(dbc.Button("Close", id="close-modal-btn", color='info'))

], id='modal-info', size='xl', backdrop="static", fade=True, scrollable=True, keyboard=True, centered=True)

default_layout = html.Div([dcc.Location(id="url", refresh=True), navbar,
                           modal, html.Div(id='page-content', style={'background-color': 'azure'})])

# create app
APP_NAME = "ViDA Summary"

app = dash.Dash(APP_NAME, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = APP_NAME
app.layout = default_layout


# callback to open/close the project info modal
@app.callback(
    Output("modal-info", "is_open"),
    Input("nav-info-btn", "n_clicks"),
    Input("close-modal-btn", "n_clicks"),
    State("modal-info", "is_open"),
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    Output("card-content", "children"),
    Input("card-tabs", "active_tab")
)
def tab_content(tab):
    with open(os.path.join(DATA_DIR, f"{tab}.md"), "r") as f:
        div = dcc.Markdown(f.read())
    return div
