import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import time
import heapq

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

# Algoritmo Dijkstra com Mini-Heap
def dijkstra_min_heap(G, origem, destino):
    dist = {n: float('inf') for n in G.nodes}
    dist[origem] = 0
    pai = {n: None for n in G.nodes}
    pq = [(0, origem)]  # Fila de prioridade (distância, nó)

    while pq:
        d, no_atual = heapq.heappop(pq)  # Extraímos o nó com a menor distância
        if d > dist[no_atual]:
            continue  # Se já processamos o nó com uma distância menor, ignoramos

        for vizinho in G[no_atual]:
            peso = G[no_atual][vizinho][0]['length']
            nova_dist = dist[no_atual] + peso
            if nova_dist < dist[vizinho]:
                dist[vizinho] = nova_dist
                pai[vizinho] = no_atual
                heapq.heappush(pq, (nova_dist, vizinho))  # Adicionamos o vizinho à fila

    # Reconstruir o caminho
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
    caminho, distancia = dijkstra_min_heap(G, orig_node, dest_node)
    end = time.time()

    print(f"- Distância: {distancia:.2f} metros")
    print(f"- Tempo de execução: {end - start:.2f} segundos")

    # Plotar o caminho com melhorias no estilo
    fig, ax = ox.plot_graph_route(
        G, caminho, route_linewidth=6, node_size=0, bgcolor='white', show=False, close=False,
        route_color='green', edge_color='gray', edge_linewidth=0.5
    )

    # Melhorar o layout e a aparência
    ax.set_title(f"Rota para {bairro}", fontsize=18, fontweight='bold', color='darkgreen')
    ax.annotate(
        f'Distância: {distancia:.2f}m', 
        xy=(0.5, 0.95), xycoords='axes fraction', ha='center', fontsize=12, color='black',
        weight='bold', backgroundcolor='white', alpha=0.7
    )

    plt.tight_layout()  # Ajusta o layout para evitar sobreposição de elementos
    plt.show()
