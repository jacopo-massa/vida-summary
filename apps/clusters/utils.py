import dash_bootstrap_components as dbc
import math
import numpy as np
import pandas as pd
import plotly.express as px

from config import isomap_df, data, data_cat, cross_cat, zoomable

CLUSTERS = ["Architecture", "Characters & Creatures (1)", "Characters & Creatures (2)", "Cultural Heritage & History"]
COLOR_SCALE = px.colors.sequential.haline

FT_HDR = "Features' Embedding"
VL_HDR = "Views/Likes' Embedding"

# Layout Settings
no_axis_layout = dict(yaxis={'visible': True, 'showticklabels': False},
                      xaxis={'visible': True, 'showticklabels': False})

transparent_layout = dict(paper_bgcolor='rgba(0,0,0,0)')


def create_pie_chart(cluster=0):
    col = f"cluster{cluster}"
    df = cross_cat.sort_values(by=['name']).nlargest(10, col)

    pie = px.pie(df, values=col, names='name', title=f"Top 10 categories in <b>{CLUSTERS[cluster]}</b>",
                 color_discrete_sequence=COLOR_SCALE)
    pie.update_layout(zoomable(False, False))
    pie.update_layout(transparent_layout)
    pie.update_layout(margin=dict(t=30, b=10, l=10, r=10))
    pie.update_traces(hovertemplate="<b>%{label}</b>: %{value}")
    return pie


def create_gen_scatter(c='cluster'):
    if c == 'cluster':
        # colors = {str(k): v for (k, v) in enumerate(CLUSTERS)}
        colors = {str(k): f"{CLUSTERS[k]} - (<b>{len(isomap_df.loc[isomap_df['cluster'] == str(k)])}</b>)" for k in
                  range(4)}
        cols = isomap_df['cluster'].map(colors)
        size = None
    else:
        column_name = c + "Count"
        cols = data[column_name]
        size = cols

    categories = data_cat['names'].apply(lambda x: x[2:-2].replace("'", ""))

    fig = px.scatter(isomap_df, x='comp1', y='comp2', labels={'cluster': 'Cluster', 'color': (c.title() + "s")},
                     custom_data=['cluster', isomap_df.index, categories], title="Models' Clustering",
                     hover_name="name", color=cols, size=size, color_continuous_scale=COLOR_SCALE)

    fig.update_layout(no_axis_layout)
    fig.update_layout(transparent_layout)
    # fig.update_layout(zoomable(True, True))

    fig.update_traces(hovertemplate="<b>%{hovertext}</b><br><br>%{customdata[2]}<extra></extra>")

    return fig


def create_btn_grid(disable_all=True, disable_sample=False):
    btn1 = dbc.Button("All models", id='btn-all', color='info', outline=True, n_clicks=0, disabled=disable_all)
    btn2 = dbc.Button("Random samples", id='btn-sample', color='info', outline=True, n_clicks=0,
                      disabled=disable_sample)

    group = dbc.ButtonGroup([btn1, btn2], size='sm', id='btn-group-grid', vertical=True)
    return group


def create_btn_gen_scatter(disable_cluster=True, disable_view=False, disable_like=False):
    btn1 = dbc.Button("Clusters", id='btn-cluster', color='info', outline=True, n_clicks=0, disabled=disable_cluster)
    btn2 = dbc.Button("Views", id='btn-view', color='info', outline=True, n_clicks=0, disabled=disable_view)
    btn3 = dbc.Button("Likes", id='btn-like', color='info', outline=True, n_clicks=0, disabled=disable_like)
    group = dbc.ButtonGroup([btn1, btn2, btn3], size='sm', id='btn-group-gen')
    return group


def chunks(lst, n):
    n = max(1, n)
    return [lst[i:i + n] for i in range(0, len(lst), n)]


def heatmap(d: pd.DataFrame, cluster=0, sub_cluster=0):
    n_boxes = 100
    num = math.floor(math.sqrt(n_boxes))

    d = d[['comp1', 'comp2']].to_numpy()

    for i in range(2):
        c = d[:, i]
        mx, mn = int(c.max()), int(c.min())
        d[:, i] = np.interp(c, (c.min(), c.max()), (0, mx - mn - 1))

    comp1 = d[:, 0]
    comp2 = d[:, 1]
    x = np.linspace(comp1.min(), comp1.max(), num=(num * 2) + 1)[1:]
    y = np.linspace(comp2.min(), comp2.max(), num=(num * 2) + 1)[1:]
    x1 = x[::2].astype(int)
    y1 = y[::2].astype(int)

    centers = []
    for i in y1[::-1]:
        for j in x1:
            centers.append([j, i])

    centers = np.asarray(centers)

    clusters = []
    for v in d:
        dist = np.sum((centers - v) ** 2, axis=1)
        clusters.append(np.argmin(dist))

    l, c = np.unique(clusters, return_counts=True)

    values = dict(zip(l, c))

    # create complete dictionary (with 0 for cells that don't appear in 'values')
    tot = {}
    for i in range(n_boxes):
        tot[i] = values.get(i, 0)

    v = chunks(list(tot.values()), n=10)

    fig = px.imshow(v, title=f"{CLUSTERS[cluster]} {sub_cluster} - (<b>{len(d)}</b> elements)",
                    color_continuous_scale=COLOR_SCALE)
    fig.update_xaxes(tickmode="linear", tick0=0, dtick=1)
    fig.update_yaxes(tickmode="linear", tick0=0, dtick=1)
    fig.update_layout(zoomable(False, False))
    fig.update_layout(transparent_layout)
    fig.update_layout(no_axis_layout)
    fig.update(data=[{'hovertemplate': "<b>Count:</b> %{z} <extra></extra>"}])
    return fig
