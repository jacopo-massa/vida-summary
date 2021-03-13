Il progetto **ViDA Summary** è stato realizzato da
[Jacopo Massa](https://jacopo-massa.github.io/) 
nell'ambito del corso di _Scientific & Large Data Visualization_ 
dell'_Università di Pisa_, sotto la supervisione dei docenti
[Daniela Giorgi](http://vcg.isti.cnr.it/~giorgi/) e 
[Massimiliano Corsini](http://vcg.isti.cnr.it/~corsini/).

I modelli analizzati sono un sottoinsieme del dataset 
[ViDA 3D](http://vcg.isti.cnr.it/Publications/2020/AFBCPCG20/), 
nello specifico **6970** modelli descritti da una serie di attributi, tra cui:

- _Nome_
- _Categoria/e_
- _\# "Mi Piace"_
- _\# Visualizzazioni_

Le analisi sui modelli sono state divise in due pagine web, descritte nelle
successive sezioni.

### 1 - Distribuzione delle categorie

L'**istogramma** e il **treemap** mostrano un evidente sbilanciamento in favore di 
sole 3 categorie:

- _Characters & Creatures_
- _Architecture_
- _Cultural Heritage & History_

Il **grafico a dispersione** permette di osservare la correlazione fra 
due qualsiasi degli attributi numerici dei modelli.

### 2 - Analisi delle features

I modelli sono stati dati in input ad una 
[Resnet](https://en.wikipedia.org/wiki/Residual_neural_network),
in particolare è stata utilizzata una `ResNet50`, tramite cui sono state
estratte 2048 features per modello.

A partire da questi dati, è stato applicata una versione semplificata
del'algoritmo [IsoMatch](https://gfx.cs.princeton.edu/pubs/Fried_2015_ICI/index.php), 
per poter ottenere una rappresentazione compatta in forma di griglia e
possibilmente scovare una qualche correlazione fra i modelli analizzati.

Il primo passo dell'algoritmo consiste nel ridurre la dimensionalità
delle features (in questo caso `dim = 2` in modo da poter rappresentare
i modelli su grafici cartesiani 2D).

Una prima rappresentazione è stata ottenuta applicando un _algoritmo di 
clustering_ ([K-Means](https://it.wikipedia.org/wiki/K-means)) 
ai dati "ridotti". Il clustering ha confermato quanto osservato
nella prima parte, ovvero che i modelli sono raggruppabili nelle
3 macro-categorie più presenti.

Infine, i modelli sono stati posizionati in una griglia
di dimensione variabile (in base alla cardinalità di ogni cluster).
Ciò ha fornito una visualizzazione riassuntiva del subset analizzato.

**N.B.** Le pagine web e i grafici sono stati generati con la librerie
[Plotly](https://plotly.com/) e [Dash](https://plotly.com/dash/). 