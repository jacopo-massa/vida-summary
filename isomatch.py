import math
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.manifold import Isomap
from sklearn.metrics import pairwise_distances_argmin_min
from sklearn.preprocessing import MinMaxScaler
from yellowbrick.cluster import KElbowVisualizer

from config import *


def iso_map(d: pd.DataFrame):
    iso = Isomap(n_components=2, n_jobs=-1)
    iso.fit(d)
    app = iso.transform(d)

    df = pd.DataFrame(app, columns=['comp1', 'comp2'], index=d.index)
    df.to_csv(ISOMAP_FILE, index=True)

    return df


def chunks(lst, n):
    n = max(1, n)
    return [lst[i:i + n] for i in range(0, len(lst), n)]


def coarse_alignment(d: pd.DataFrame, clt_num, sub_num, show_img=False):
    print(f"Cluster {clt_num}.{sub_num} ({len(d)} elems):")

    # calculate number of boxes, based on dataframe length
    n_boxes = 100
    num = math.floor(math.sqrt(n_boxes))

    d = d.to_numpy()

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
    app = dict(zip(l, c))
    a = {}
    for i in range(n_boxes):
        a[i] = app.get(i, 0)

    if show_img:
        cmap = plt.get_cmap('plasma')
        k = [t for t in range(num)]
        print(k)
        v = chunks(list(a.values()), n=10)
        print(v)
        fig, ax = plt.subplots()
        im = ax.imshow(v, cmap=cmap, aspect='auto')

        ax.set_xticks(np.arange(len(k)))
        ax.set_yticks(np.arange(len(k)))
        ax.set_xticklabels(k)
        ax.set_yticklabels(k)

        name = f"Cluster {clt_num}_{sub_num}_({len(d)}) elems"
        ax.set_title(name)
        fig.colorbar(im)
        fig.tight_layout()
        plt.show()

    return centers, clusters


def clustering(d: pd.DataFrame, n_clusters=None, scale='linear', show_img=False):
    scaler = MinMaxScaler()
    kdata = scaler.fit_transform(d.values)

    km = KMeans(max_iter=400)
    visualizer = KElbowVisualizer(
        km, k=(1, 20), metric='distortion', timings=False)
    visualizer.fit(kdata)

    if show_img:
        visualizer.show()

    n = n_clusters if n_clusters is not None else visualizer.elbow_value_
    kmeans = KMeans(n_clusters=n, max_iter=400)
    kmeans.fit(kdata)

    l, c = np.unique(kmeans.labels_, return_counts=True)
    print("Total: ", len(d), dict(zip(l, c)))

    centers = scaler.inverse_transform(kmeans.cluster_centers_)

    if show_img:

        cmap = plt.cm.get_cmap('hsv', n + 1)

        df_copy = d.copy()
        df_copy["cluster"] = kmeans.labels_
        for i in l:
            plt.scatter(df_copy.loc[df_copy['cluster'] == i, 'comp1'], df_copy.loc[df_copy['cluster'] == i, 'comp2'],
                        label="Cluster %s" % i, s=20, color=cmap(i))

        plt.title(f"K-Means ({n_clusters} clusters)")
        plt.scatter(centers[:, 0], centers[:, 1], s=200, marker='*', c='k')
        plt.tick_params(axis='both', which='major', labelsize=10)
        plt.xscale(scale)
        plt.legend()
        plt.show()

    return centers, kmeans.labels_


if __name__ == "__main__":

    if os.path.exists(ISOMAP_FILE):
        iso_df = isomap_df
    else:
        # need to recompute features
        # my_d = pd.read_csv(FEATURES_FILE, index_col=0)
        print("DataFrame read!")

        iso_df = iso_map()

    print("IsoMap done!")

    if 'cluster' not in iso_df.columns:

        # compute clustering
        centers, labels = clustering(iso_df[['comp1', 'comp2']], show_img=True)
        arr = iso_df[['comp1', 'comp2']].to_numpy()
        closest, _ = pairwise_distances_argmin_min(centers, arr)

        for c in closest:
            print(iso_df.iloc[c])

        # save clusters' labels
        iso_df["cluster"] = labels
        iso_df.to_csv(ISOMAP_FILE, index=True)

    print("First clustering done!\n")

    grp = iso_df.groupby(by=['cluster'])

    # do something
