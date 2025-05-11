import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import time

# Baixar o grafo da cidade
place = "Natal, Rio Grande do Norte, Brazil"
G = ox.graph_from_place(place, network_type='drive')

# Definir origem e destinos
origem = ox.geocode("Avenida Prudente de Morais, Natal, Brazil")
destinos = {
    "Neópolis": ox.geocode("Neópolis, Natal, Brazil"),
    "Candelária": ox.geocode("Candelária, Natal, Brazil"),
    "Capim Macio": ox.geocode("Capim Macio, Natal, Brazil"),
}

# Encontrar os nós mais próximos
orig_node = ox.distance.nearest_nodes(G, *origem[::-1])
dest_nodes = {bairro: ox.distance.nearest_nodes(G, *coord[::-1]) for bairro, coord in destinos.items()}

# Configuração de gráficos
plt.rcParams["figure.figsize"] = (12, 8)
plt.rcParams["font.size"] = 14

# Executar algoritmo de Dijkstra com OSMnx/NetworkX
for bairro, dest_node in dest_nodes.items():
    print(f"\n🏁 Rota para {bairro}")

    start = time.time()
    caminho = nx.shortest_path(G, source=orig_node, target=dest_node, weight='length', method='dijkstra')
    distancia = nx.shortest_path_length(G, source=orig_node, target=dest_node, weight='length', method='dijkstra')
    end = time.time()

    print(f"- Distância: {distancia:.2f} metros")
    print(f"- Tempo de execução: {end - start:.4f} segundos")

    # Plotar o caminho com estilo profissional
    fig, ax = ox.plot_graph_route(
        G, caminho, route_linewidth=6, node_size=0, bgcolor='white', show=False, close=False,
        route_color='purple', edge_color='gray', edge_linewidth=0.5
    )

    ax.set_title(f"Rota para {bairro}", fontsize=18, fontweight='bold', color='purple')
    ax.annotate(
        f'Distância: {distancia:.2f}m',
        xy=(0.5, 0.95), xycoords='axes fraction', ha='center', fontsize=12,
        weight='bold', backgroundcolor='white', alpha=0.7
    )

    plt.tight_layout()
    plt.show()
