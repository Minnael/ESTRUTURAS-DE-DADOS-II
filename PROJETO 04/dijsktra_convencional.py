import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import time

# Baixar o grafo
place = "Natal, Rio Grande do Norte, Brazil"
G = ox.graph_from_place(place, network_type='drive')

# Definir origem e destinos
origem = ox.geocode("Avenida Prudente de Morais, Natal, Brazil")
destinos = {
    "Neópolis": ox.geocode("Neópolis, Natal, Brazil"),
    "Candelária": ox.geocode("Candelária, Natal, Brazil"),
    "Capim Macio": ox.geocode("Capim Macio, Natal, Brazil"),
}

orig_node = ox.distance.nearest_nodes(G, *origem[::-1])
dest_nodes = {bairro: ox.distance.nearest_nodes(G, *coord[::-1]) for bairro, coord in destinos.items()}

# Algoritmo Dijkstra tradicional
def dijkstra_tradicional(G, origem, destino):
    visitado = set()
    dist = {n: float('inf') for n in G.nodes}
    pai = {n: None for n in G.nodes}
    dist[origem] = 0

    while len(visitado) < len(G.nodes):
        no_atual = min((n for n in G.nodes if n not in visitado), key=lambda n: dist[n], default=None)
        if no_atual is None or dist[no_atual] == float('inf'):
            break
        visitado.add(no_atual)
        for vizinho in G[no_atual]:
            peso = G[no_atual][vizinho][0]['length']
            if dist[no_atual] + peso < dist[vizinho]:
                dist[vizinho] = dist[no_atual] + peso
                pai[vizinho] = no_atual

    caminho = []
    atual = destino
    while atual:
        caminho.insert(0, atual)
        atual = pai[atual]
    return caminho, dist[destino]

# Configurações de estilo do gráfico
plt.rcParams["figure.figsize"] = (12, 8)  # Aumenta o tamanho do gráfico
plt.rcParams["font.size"] = 14  # Define o tamanho da fonte

# Executar e medir para cada bairro
for bairro, dest_node in dest_nodes.items():
    print(f"\n🏁 Rota para {bairro}")
    
    start = time.time()
    caminho, distancia = dijkstra_tradicional(G, orig_node, dest_node)
    end = time.time()

    print(f"- Distância: {distancia:.2f} metros")
    print(f"- Tempo de execução: {end - start:.2f} segundos")

    # Plotar o caminho com melhorias no estilo
    fig, ax = ox.plot_graph_route(
        G, caminho, route_linewidth=6, node_size=0, bgcolor='white', show=False, close=False,
        route_color='blue', edge_color='gray', edge_linewidth=0.5
    )

    # Melhorar o layout e a aparência
    ax.set_title(f"Rota para {bairro}", fontsize=18, fontweight='bold', color='darkblue')
    ax.annotate(
        f'Distância: {distancia:.2f}m', 
        xy=(0.5, 0.95), xycoords='axes fraction', ha='center', fontsize=12, color='black',
        weight='bold', backgroundcolor='white', alpha=0.7
    )

    plt.tight_layout()  # Ajusta o layout para evitar sobreposição de elementos
    plt.show()
