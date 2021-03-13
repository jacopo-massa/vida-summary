import dash
import plotly.express as px
from dash.dependencies import Input, Output, State

from app import app
from config import cat, get_image
from .utils import *


@app.callback(
    Output('cat-table', 'data'),
    Output('cat-barchart', 'figure'),
    Input('cat-table', 'sort_by')
)
def update_barchart(sort_by):
    if len(sort_by):
        df = cat.sort_values([c['column_id'] for c in sort_by], ascending=[c['direction'] == 'asc' for c in sort_by],
                             inplace=False)
    else:
        df = cat

    fig = px.bar(df, labels={'name': 'Name', 'count': 'Count'}, x='name', y='count',
                 title="<b>Categories Distribution</b>", color='count', color_continuous_scale=COLOR_SCALE)
    fig.update_yaxes(visible=False, showticklabels=False)
    fig.update_layout(xaxis_title="")
    fig.update_layout(transparent_layout)
    fig.update_traces(hovertemplate="<b>%{x}</b> <br><br>Count: <i>%{y}</i>")

    return df.to_dict('records'), fig


@app.callback(
    Output('summary-plot', 'figure'),
    Output('x-col', 'options'),
    Output('y-col', 'options'),
    Output('btn-group-scale', 'children'),
    Input('x-col', 'value'),
    Input('y-col', 'value'),
    Input('btn-linear', 'n_clicks'),
    Input('btn-log', 'n_clicks')
)
def update_summary_plot(x_value, y_value, btn_linear, btn_log):
    x_lbl = x_value[:-5].title()
    y_lbl = y_value[:-5].title()

    fig = px.scatter(data, x=x_value, y=y_value, labels={x_value: x_lbl, y_value: y_lbl}, hover_data=[x_value, y_value],
                     hover_name=data['name'].str.title(), custom_data=[data.index],
                     title="<b>Numerical Attributes' Correlation</b>",
                     color=y_value, color_continuous_scale=COLOR_SCALE)

    ctx = dash.callback_context
    if ctx.triggered:
        comps = ctx.triggered[0]['prop_id'].split('.')[0].split('-')
        if comps[0] == 'btn':
            scale = comps[1]
        else:
            scale = "log"
            btn_log = True  # default option
    else:
        scale = "log"
        btn_log = True

    fig.update_xaxes(type=scale)
    fig.update_layout(transparent_layout)
    fig.update_traces(hovertemplate=f"<b>%{{hovertext}}</b><br><br>"
                                    f"{x_lbl}: <i>%{{x}}</i><br>"
                                    f"{y_lbl}: <i>%{{y}}</i>")

    # change options so that we can't select the same option for both axis
    x_options = [{'label': i[:-5].title(), 'value': i, 'disabled': (i == y_value)} for i in COUNTABLE_ATTR]
    y_options = [{'label': i[:-5].title(), 'value': i, 'disabled': (i == x_value)} for i in COUNTABLE_ATTR]

    group = create_scale_group(disable_lnr=bool(btn_linear), disable_log=bool(btn_log))
    return fig, x_options, y_options, group


@app.callback(
    Output('summary-card-img', 'src'),
    Output('summary-card-hdr', 'children'),
    Input('summary-plot', 'clickData')
)
def update_category_card(click_data):
    if click_data:
        img_uid = click_data['points'][0]['customdata'][0]
        name = data.loc[img_uid, 'name']
    else:
        img_uid = "no_image"
        name = "Select a point"

    return get_image(img_name=img_uid), name


@app.callback(
    Output('x-col', 'value'),
    Output('y-col', 'value'),
    Input('invert-axes-btn', 'n_clicks'),
    State('x-col', 'value'),
    State('y-col', 'value')
)
def invert_axes_summary_plot(n_clicks, x_value, y_value):
    if n_clicks:
        return y_value, x_value
    else:
        return x_value, y_value
