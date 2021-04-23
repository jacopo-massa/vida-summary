import dash_bootstrap_components as dbc
import plotly.express as px

from config import isomap_df, data, data_cat, cross_cat, zoomable

CONTINUOUS_SCALE = px.colors.sequential.haline
DISCRETE_SCALE = px.colors.cyclical.HSV
CLUSTERS = ["Architecture", "Characters & Creatures (1)",
            "Characters & Creatures (2)", "Cultural Heritage & History"]

CLUSTERS_ALL = ["Architecture", "Architecture (other classes)",
                "Characters & Creatures (1)", "Characters & Creatures (1) (other classes)",
                "Characters & Creatures (2)", "Characters & Creatures (2) (other classes)",
                "Cultural Heritage & History", "Cultural Heritage & History (other classes)"]

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
                 color_discrete_sequence=CONTINUOUS_SCALE)
    pie.update_layout(zoomable(False, False))
    pie.update_layout(transparent_layout)
    pie.update_layout(margin=dict(t=30, b=10, l=10, r=10))
    pie.update_traces(hovertemplate="<b>%{label}</b>: %{value}")
    return pie


def create_gen_scatter(c='cluster'):
    if c == 'cluster':
        colors = {k: f"{CLUSTERS_ALL[k]} - (<b>{len(isomap_df.loc[isomap_df['colors'] == k])}</b>)"
                  for k in range(len(CLUSTERS_ALL))}

        cols = isomap_df.sort_values(by=['colors'])['colors'].map(colors)
        size = None
    else:
        column_name = c + "Count"
        cols = data[column_name]
        size = cols

    # categories = data_cat['names'].apply(lambda x: x[2:-2].replace("'", ""))
    categories = [data_cat.loc[idx, 'names'][2:-2].replace("'", "") for idx in isomap_df.index]

    fig = px.scatter(isomap_df, x='comp1', y='comp2', labels={'color': (c.title() + "s")},
                     custom_data=['cluster', isomap_df.index, categories], title="Models' Clustering",
                     hover_name="name", color=cols, size=size, color_continuous_scale=CONTINUOUS_SCALE,
                     color_discrete_sequence=DISCRETE_SCALE)

    fig.update_layout(no_axis_layout)
    fig.update_layout(transparent_layout)

    fig.update_traces(hovertemplate="<b>%{hovertext}</b><br><br>%{customdata[2]}<extra></extra>")

    return fig


def create_btn_grid(disable_all=False, disable_sample=True):
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