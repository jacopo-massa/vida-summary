**ViDA Summary** project has been carried out by 
[Jacopo Massa](https://jacopomassa.netlify.app) 
as part of the _Scientific & Large Data Visualization_ 
course at the _University of Pisa_, under the supervision of teachers
[Daniela Giorgi](http://vcg.isti.cnr.it/~giorgi/) and
[Massimiliano Corsini](http://vcg.isti.cnr.it/~corsini/).

Analyzed models are a subset of the
[ViDA 3D](http://vcg.isti.cnr.it/Publications/2020/AFBCPCG20/) dataset, 
in particular there are [**6970** models](https://www.dropbox.com/sh/bazjfdx7d40oy2j/AAD7RGjB-Nw4YRPTbE4Dku6ca?dl=0) described by some attributes, including:

- _Name_
- _Categories_
- _\#Likes_
- _\#Views_

Model analyzes were divided into two web pages, described in
subsequent sections.

### 1 - Categories Distribution

**Bar Chart** and **Treemap** show a subsantial imbalance 
in favor of only 3 categories:

- _Characters & Creatures_
- _Architecture_
- _Cultural Heritage & History_

With the **scatter plot**, correlation between any couple of 
models' numerical attributes can be observed.

### 2 - Feature Analysis

Models were given in input to a
[ResNet](https://en.wikipedia.org/wiki/Residual_neural_network),
in particular a `ResNet50`, that extracted 2048 features per model.

Starting from these data, a simplified version of 
the [IsoMatch](https://gfx.cs.princeton.edu/pubs/Fried_2015_ICI/index.php) 
algorithm was applied, in order to obtain a compact grid representation and
possibly find some correlation between the analyzed models.

First step of the algorithm consists in reducing the dimensionality
features (in this case `dim = 2` to represent models on 2D 
Cartesian graphs).

A first representation was obtained by applying a _clustering algorithm_ 
([K-Means](https://it.wikipedia.org/wiki/K-means))
to the "reduced" data. Clustering has confirmed what was observed
in the first part, that is, that models can be grouped 
in the 3 most present macro-categories.

Finally, models were placed in a variable size grid 
(based on each cluster's cardinality).
This representation provided a summarized view of the analyzed subset.

**N.B.** Web pages and plots were generated with the graphing libraries
[Plotly](https://plotly.com/) and [Dash](https://plotly.com/dash/).