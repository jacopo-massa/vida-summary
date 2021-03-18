import dash
from dash.dependencies import Input, Output

from app import app
from config import get_image
from .utils import *


@app.callback(
    Output('gen-scatter', 'figure'),
    Output('btn-group-gen', 'children'),
    Input('btn-cluster', 'n_clicks'),
    Input('btn-view', 'n_clicks'),
    Input('btn-like', 'n_clicks'),
)
def update_btn_group_gen(btn_cluster, btn_view, btn_like):
    ctx = dash.callback_context

    if ctx.triggered:
        color = ctx.triggered[0]['prop_id'].split('.')[0].split('-')[1]
    else:
        color = "cluster"
        btn_cluster = True  # default option

    gen_scatter = create_gen_scatter(color)
    btn_group = create_btn_gen_scatter(disable_cluster=bool(btn_cluster),
                                       disable_view=bool(btn_view),
                                       disable_like=bool(btn_like))

    return gen_scatter, btn_group


@app.callback(
    Output('ft-grid-img', 'src'),
    Output('ft-grid-hdr', 'children'),
    Output('vl-grid-img', 'src'),
    Output('vl-grid-hdr', 'children'),
    Output('btn-group-grid', 'children'),
    Input('btn-all', 'n_clicks'),
    Input('btn-sample', 'n_clicks'),
    Input('cl-menu', 'value')
)
def update_btn_group_grid(btn_all, btn_sample, cluster):

    ctx = dash.callback_context
    if ctx.triggered:
        comps = ctx.triggered[0]['prop_id'].split('.')[0].split('-')
        if comps[0] == 'btn':
            show = comps[1]
        else:
            show = "sample"
            btn_sample = True  # default option
    else:
        show = "sample"
        btn_sample = True

    ft_img = get_image(f"grid{cluster}-{show}-ft", grid=True)
    vl_img = get_image(f"grid{cluster}-{show}-vl", grid=True)

    ft_hdr = f"{FT_HDR} - {CLUSTERS[cluster]}"
    vl_hdr = f"{VL_HDR} - {CLUSTERS[cluster]}"

    btn_group = create_btn_grid(disable_all=bool(btn_all), disable_sample=bool(btn_sample))

    return ft_img, ft_hdr, vl_img, vl_hdr, btn_group


@app.callback(
    Output('cluster-card-img', 'src'),
    Output('cluster-card-hdr', 'children'),
    Input('gen-scatter', 'clickData'),
)
def update_cluster_card(gen_cluster):
    if gen_cluster:
        img_uid = gen_cluster['points'][0]['customdata'][1]
        name = isomap_df.loc[img_uid, 'name']
    else:
        img_uid = "no_image"
        name = "Select a point"

    return get_image(img_name=img_uid), name


@app.callback(
    Output('pie-chart', 'figure'),
    Input('cl-menu', 'value')
)
def update_pie_chart(cluster):
    pie = create_pie_chart(cluster)

    return pie
