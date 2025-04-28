import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import os

def construir_grafo(caminho_csv, salvar_em=None):
    # Ler o arquivo CSV
    df = pd.read_csv(caminho_csv)

    # Criar o grafo
    G = nx.Graph()

    for idx, row in df.iterrows():
        ingredientes = [i.strip() for i in row['ingredientes'].split(',')]
        categorias = [c.strip() for c in row['categorias'].split(',')]

        # Adicionar nós com o atributo tipo
        for ingrediente, categoria in zip(ingredientes, categorias):
            if ingrediente not in G:
                G.add_node(ingrediente, tipo=categoria)

        # Criar arestas entre ingredientes da mesma receita
        for i in range(len(ingredientes)):
            for j in range(i + 1, len(ingredientes)):
                if G.has_edge(ingredientes[i], ingredientes[j]):
                    G[ingredientes[i]][ingredientes[j]]['peso'] += 1
                else:
                    G.add_edge(ingredientes[i], ingredientes[j], peso=1)

    print(f"Grafo criado com {G.number_of_nodes()} nós e {G.number_of_edges()} arestas.")

    # Salvar o grafo, se for pedido
    if salvar_em:
        nx.write_gexf(G, salvar_em)
        print(f"Grafo salvo em {salvar_em}")

    return G

def apresentar_grafo(G):
    plt.figure(figsize=(18, 12))
    pos = nx.spring_layout(G, seed=42, k=0.3)
    tipos = nx.get_node_attributes(G, 'tipo')

    # Gerar cores únicas para cada tipo
    tipos_unicos = list(set(tipos.values()))
    cmap = cm.get_cmap('tab20', len(tipos_unicos))
    cor_tipo = {tipo: cmap(idx) for idx, tipo in enumerate(tipos_unicos)}

    # Atribuir cores aos nós conforme seu tipo
    node_colors = [cor_tipo[tipos[node]] for node in G.nodes()]

    # Definir tamanho dos nós proporcional ao grau
    degrees = dict(G.degree())
    node_sizes = [300 + degrees[node]*50 for node in G.nodes()]

    nx.draw_networkx_edges(G, pos, alpha=0.3)
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.9)
    nx.draw_networkx_labels(G, pos, font_size=8, font_color='black')

    plt.title("Grafo de Ingredientes", fontsize=20, weight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Localiza o diretório atual
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_csv = os.path.join(diretorio_atual, "50 RECEITAS.csv.csv")

    # Defina onde salvar o grafo (opcional)
    salvar_grafo_em = os.path.join(diretorio_atual, "grafo_ingredientes.gexf")

    # Construir o grafo
    G = construir_grafo(caminho_csv, salvar_em=salvar_grafo_em)

    # Apresentar o grafo
    apresentar_grafo(G)
