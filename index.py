from dash.dependencies import Input, Output

from app import app
from apps import categories, clusters


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == "/" or pathname == "/categories":
        return categories.layout
    else:
        return clusters.layout


if __name__ == '__main__':
    app.run_server()
