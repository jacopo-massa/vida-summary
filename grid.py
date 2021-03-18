# Module for image grid creation

import math
import numpy as np

from config import *


def make_image_grid(images, d, img_dim=64, n=None, name='grid.png'):
    ilen = len(images)
    if n is None:
        n = ilen

    assert ilen >= n, f"Too few images! {ilen} given, {n} required"

    grid_dim = math.floor(math.sqrt(n)) * img_dim
    grid_im = Image.new('RGB', (grid_dim, grid_dim))

    idx = 0
    for i in range(0, grid_dim, img_dim):
        for j in range(0, grid_dim, img_dim):
            if idx >= n:
                break
            else:
                print(f"{idx} ({images[idx]}): {d[idx, 0]}, {d[idx, 1]} --> {j},{i}")
                im = get_image(images[idx])
                im.thumbnail((img_dim, img_dim))
                grid_im.paste(im, (j, i))
                idx += 1

        if idx >= n:
            break
    grid_im.save(os.path.join(GRID_DIR, name))


def set_grid(tot=True, vl=False, cluster=0, n=400):

    if vl:
        df = isomap_df.loc[isomap_df['cluster'] == cluster, ['views', 'likes']]
    else:
        df = isomap_df.loc[isomap_df['cluster'] == cluster, ['comp1', 'comp2']]

    if not tot:
        df = df.sample(n=n)

    df_dict = df.to_dict(orient='split')
    d = np.array(df_dict['data'], dtype=float)

    for i in range(2):
        c = d[:, i]
        d[:, i] = np.interp(c, (c.min(), c.max()), (0.0, 1536.0))

    ind = np.lexsort((d[:, 1], d[:, 0]))

    d = d[ind]
    filenames = np.array(df_dict['index'])
    filenames = filenames[ind]

    img_name = "grid{}-{}-{}.png".format(cluster, ("all" if tot else "sample"), ("vl" if vl else "ft"))

    make_image_grid(filenames, d, name=img_name)


if __name__ == '__main__':

    set_grid(tot=True, vl=True, cluster=0)
