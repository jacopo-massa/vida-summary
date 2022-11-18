from dash import dash_table as dt
from dash import dcc
import plotly.express as px

from config import cat, sub_cat
from .utils import *

# CATEGORIES table with counts
cat_table = dt.DataTable(
    id='cat-table',
    columns=[{"name": "Category", "id": "name"},
             {"name": "Count", "id": "count"}],
    data=cat.to_dict('records'),
    sort_action='custom',
    sort_by=[{'column_id': 'count', 'direction': 'desc'}],
    page_action='none',
    fixed_rows={'headers': True},
    style_table={'height': CAT_HEIGHT},
    style_header={'fontWeight': 'bold', 'backgroundColor': 'rgba(37, 162, 183, 0.8)', 'textAlign': 'center',
                  'fontSize': 15},
    style_cell={'textAlign': 'left', 'backgroundColor': 'rgba(0, 230, 230, 0.2)'},
    style_cell_conditional=[
        {'if': {'column_id': 'name'}, 'width': '70%'},
        {'if': {'column_id': 'count'}, 'width': '30%', 'textAlign': 'center'},
    ],
    style_data_conditional=[
        {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'}
    ],
    virtualization=True
)

# CATEGORIES treemap
sub_cat['all'] = "All"
cat_treemap = px.treemap(sub_cat, path=['all', 'category', 'subcategory'], values='count', branchvalues='total',
                         labels={'count': 'Count'}, title='<b>Categories Treemap</b>',
                         color='count', color_continuous_scale=COLOR_SCALE,
                         hover_name=(sub_cat['category'] + ", " + sub_cat['subcategory']))
cat_treemap.update_traces(hovertemplate="<b>%{parent},%{label}</b> <br><br>Count: <i>%{value}</i>")
cat_treemap.update_layout(transparent_layout)

# SUMMARY PLOT dropdown menus
x_dropdown = dcc.Dropdown(id='x-col', value=COUNTABLE_ATTR[0], clearable=False,
                          options=[{'label': i[:-5].title(), 'value': i} for i in COUNTABLE_ATTR])
y_dropdown = dcc.Dropdown(id='y-col', value=COUNTABLE_ATTR[1], clearable=False,
                          options=[{'label': i[:-5].title(), 'value': i} for i in COUNTABLE_ATTR])

# SUMMARY PLOT buttons
invert_button = dbc.Button("Invert axes", id='invert-axes-btn', n_clicks=0,
                           outline=False, color='info', size='sm')

scale_group = create_scale_group()

# SUMMARY IMAGE CARD
card = dbc.Card(
    [
        dbc.CardHeader("", id='summary-card-hdr', style={'font-weight': 'bold'}),
        dcc.Loading(children=[dbc.CardImg(id='summary-card-img', bottom=True)], type='cube', color='#5bc0de')
    ])
