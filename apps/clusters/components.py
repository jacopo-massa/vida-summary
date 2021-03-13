from config import get_image
from .utils import *

import dash_core_components as dcc


def create_card(hdr="", id_hdr="", img=None, id_img=""):
    return dbc.Card(
        [
            dbc.CardHeader(hdr, id=id_hdr, style={'font-weight': 'bold'}),
            dcc.Loading(children=[dbc.CardImg(src=img, id=id_img, bottom=True)], type='cube', color='#5bc0de'),
        ], color='info', outline=True)


# CLUSTER IMAGE CARD
card = create_card(id_hdr='cluster-card-hdr', id_img='cluster-card-img')

# CENTROID CARDS
uid0 = "e76b67070de9427ca6df3b17ce129103"
uid1 = "1a916749203c46c0a6ad074b4ac55cbc"
uid2 = "d09e1d8691f44dbd876fa3c7b269637b"
uid3 = "5a4087f865064a1d8f61299ab9173e50"
c0 = create_card(hdr="Architecture", img=get_image(uid0))
c1 = create_card(hdr="Ch. & Cr. (1)", img=get_image(uid1))
c2 = create_card(hdr="Ch. & Cr. (2)", img=get_image(uid2))
c3 = create_card(hdr="Cult. & Hist.", img=get_image(uid3))

# GRID CARDS
ft_card = create_card(hdr=FT_HDR, id_hdr='ft-grid-hdr', id_img='ft-grid-img', img='no_image')
vl_card = create_card(hdr=VL_HDR, id_hdr='vl-grid-hdr', id_img='vl-grid-img', img='no_image')

# BUTTON GROUP to change grid cards
grid_group = create_btn_grid()

# BUTTON GROUP to color gen-scatter
color_group = create_btn_gen_scatter()

# ALL CLUSTERS SCATTER
isomap_df.sort_values(by=['cluster'], inplace=True)

# change cluster to string to have punctual legend
isomap_df['cluster'] = isomap_df['cluster'].astype(str)
