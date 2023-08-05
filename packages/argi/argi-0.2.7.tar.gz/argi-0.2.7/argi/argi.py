
import pandas as pd
from adtk.data import validate_series
from adtk.detector import PersistAD

import numpy as np
from datetime import datetime, timedelta
from tslearn.clustering import KShape
from tslearn.datasets import CachedDatasets
from tslearn.preprocessing import TimeSeriesScalerMeanVariance
import numpy
import matplotlib.pyplot as plt
import networkx as nx
persist_ad = PersistAD(c=3.0, side='positive')
from sklearn import preprocessing



class argi:

  G = nx.MultiGraph()
  agregados = pd.DataFrame()
  columnas = {'src': 'IPsrc',
              'dst': 'IPdst',
              'value': '# bytes',
              'label': 'label',
              'timestamp': 'fecha'}
  num_cluster = 5


  def set_num_cluster(self, num_cluster):
    self.num_cluster= num_cluster

  def set_columns(self, values):
    self.columnas = values

  def df_transform(self, datos):
    
    datos[self.columnas['timestamp']] =  pd.to_datetime(datos[self.columnas['timestamp']])
    datos = datos.set_index(self.columnas['timestamp'])
    le = preprocessing.LabelEncoder()
    le.fit(datos['label'])
    datos['label']= le.transform(datos[self.columnas['label']])
    entrada = datos.groupby([pd.Grouper(freq='S'), self.columnas['src'], self.columnas['dst']])[[self.columnas['value'],self.columnas['label']]].sum().reset_index()
    entrada[self.columnas['timestamp']] =  pd.to_datetime(entrada[self.columnas['timestamp']], unit='s')
    entrada = entrada.set_index(self.columnas['timestamp'])
    self.agregados = datos.groupby([pd.Grouper(freq='S'), self.columnas['src'],self.columnas['dst']]).agg({self.columnas['value']: 'sum', self.columnas['label']: 'max'}).reset_index()

  def graph_clear(self):
    self.G.clear

  def graph_get(self):
    return(self.G)


  def graph_create(self,datos):

    self.G = nx.MultiGraph()
    datos2 = datos.groupby([self.columnas['src'],self.columnas['dst']])[[self.columnas['value'],self.columnas['label']]]
    nodes1 = datos[self.columnas['src']].unique().tolist()
    nodes2 = datos[self.columnas['dst']].unique().tolist()
    nodes = set(nodes1 + nodes2)
    self.G.add_nodes_from(nodes)

    for (src,dst), df_group in datos2:
      self.G.add_edge(src, dst, ts_len=len(df_group), ts= df_group)


  def count_anomalies(self,start, stop, freq):
    ts_clustering =[]
    for node1, node2, data in self.G.edges(data=True):
      timeseries = data['ts']
      salida = data['ts']
      if len(salida) > 1:
        salida['fecha'] =  pd.to_datetime(salida[self.columnas['timestamp']])
        salida= salida.set_index(self.columnas['timestamp'],drop=False)
        salida= salida.set_index(self.columnas['timestamp'])
        idx = pd.date_range(start, stop, freq=freq)
        salida = salida.resample(freq).sum()
        salida=salida.reindex(idx, fill_value='0')

        s = validate_series(salida[self.columnas['value']])
        ts_clustering.append(salida[self.columnas['value']].array)
        anomalies = persist_ad.fit_detect(s)
        total_anomalies = anomalies.tolist().count(1)
        #print( src + ' '+ dst, end='')
        self.G[node1][node2][0]['anomalies'] =  total_anomalies # , anomalies = total_anomalies)


  def create_clustering(self,start,stop, freq):
    ts_clustering = []


    #for node1, node2, data in G2.edges(data=True):
    attr = nx.get_edge_attributes(self.G, "ts")
    for ((src,dst,index), values) in attr.items():
        values[[self.columnas['timestamp'],self.columnas['value']]]
        values[self.columnas['timestamp']] =  pd.to_datetime(values[self.columnas['timestamp']])
        
        idx = pd.date_range(start, stop, freq=freq)
        values = values.set_index(self.columnas['timestamp']).resample(freq).sum().reindex(idx, fill_value=0)
        ts_clustering.append(values[self.columnas['value']].tolist())

    my_array = np.array(ts_clustering)

        
    my_array=my_array.reshape((my_array.shape[0],my_array.shape[1],1))
    my_array.shape

    seed = 0
    numpy.random.seed(seed)

    # kShape clustering
    ks = KShape(n_clusters=self.num_cluster, verbose=True, random_state=seed)
    y_pred = ks.fit_predict(my_array)
    contador = 0
    for (key, values) in attr.items():
      ts_clustering.append(values[self.columnas['value']])

      attrs = {}
      attrs[key] = {}
      attrs[key]['cluster'] = y_pred[contador]
      nx.set_edge_attributes(self.G, attrs)
      contador = contador +1

  def clustering_description():
    for num_cluster in range(self.num_cluster):
      H = nx.Graph(((u, v, e) for u,v,e in grafo.edges(data=True) if e['cluster'] == num_cluster))
      print("Cluster: "+str(num_cluster) + " num_edges: " +str(H.number_of_edges())+ " num_nodes: "+str(H.number_of_nodes()))
      num_neighbors = []
      for node in H.nodes():
        salida= len(list(nx.all_neighbors(H, node)))
        num_neighbors.append([node,salida]) 
      df = pd.DataFrame.from_records(num_neighbors)
      print(df.sort_values(by=[1],ascending=False).head(5))


  def graph_plot(self):
    import plotly.graph_objects as go
    pos = nx.random_layout(self.G)
    nx.set_node_attributes(self.G, pos, 'pos')

    #G = nx.random_geometric_graph(200, 0.125)
    #pos=nx.spring_layout(G)
    #nx.set_node_attributes(G,pos) 

    edge_x = []
    edge_y = []
    for edge in self.G.edges():
        x0, y0 = self.G.nodes[edge[0]]['pos']
        x1, y1 = self.G.nodes[edge[1]]['pos']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in self.G.nodes():
        x, y = self.G.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='Blues',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(self.G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append('# of connections: '+str(len(adjacencies[1])))

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                width=1000,
                height=1000,
                title='<br>Network graph',
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text="Python code: <a href='https://plot.ly/ipython-notebooks/network-graphs/'> https://plot.ly/ipython-notebooks/network-graphs/</a>",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )
    fig.show()
