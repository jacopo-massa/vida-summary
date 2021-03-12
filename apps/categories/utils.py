import dash_bootstrap_components as dbc

from config import data

# Layout settings
transparent_layout = dict(paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=1, r=1))

COLOR_SCALE = 'haline'

# Category settings
CAT_HEIGHT = 400
COUNTABLE_ATTR = [s for s in list(data.columns) if "Count" in s]


def create_scale_group(disable_lnr=True, disable_log=False):
    btn1 = dbc.Button("Linear", id='btn-linear', color='info', outline=True, n_clicks=0, disabled=disable_lnr)
    btn2 = dbc.Button("Log", id='btn-log', color='info', outline=True, n_clicks=0, disabled=disable_log)

    group = dbc.ButtonGroup([btn1, btn2], size='sm', id='btn-group-scale')
    return group
