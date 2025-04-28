import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import nxviz as nv


def construir_grafo(caminho_csv, salvar_em=None):
    """
    Lê o CSV de receitas e constrói um grafo onde cada ingrediente é um nó
    com atributo 'tipo' (categoria), e as arestas representam co-ocorrência em receitas.
    """
    df = pd.read_csv(caminho_csv)
    G = nx.Graph()

    for _, row in df.iterrows():
        ingredientes = [i.strip() for i in row['ingredientes'].split(',')]
        categorias = [c.strip() for c in row['categorias'].split(',')]
        for ingr, cat in zip(ingredientes, categorias):
            if ingr not in G:
                G.add_node(ingr, tipo=cat)
        for i in range(len(ingredientes)):
            for j in range(i + 1, len(ingredientes)):
                u, v = ingredientes[i], ingredientes[j]
                if G.has_edge(u, v):
                    G[u][v]['peso'] += 1
                else:
                    G.add_edge(u, v, peso=1)

    print(f"Grafo criado com {G.number_of_nodes()} nós e {G.number_of_edges()} arestas.")
    if salvar_em:
        nx.write_gexf(G, salvar_em)
        print(f"Grafo salvo em {salvar_em}")
    return G


def calcular_assortatividade(G):
    """
    Calcula e retorna o coeficiente de assortatividade pelo atributo 'tipo'.
    """
    coef = nx.attribute_assortativity_coefficient(G, 'tipo')
    print(f"Coeficiente de assortatividade por tipo: {coef:.4f}")
    return coef


def apresentar_grafo_spring(G):
    plt.figure(figsize=(18, 12))
    pos = nx.spring_layout(G, seed=42, k=0.3)
    tipos = nx.get_node_attributes(G, 'tipo')
    tipos_unicos = list(set(tipos.values()))
    cmap = plt.get_cmap('tab20', len(tipos_unicos))
    cor_tipo = {t: cmap(i) for i, t in enumerate(tipos_unicos)}
    node_colors = [cor_tipo[tipos[n]] for n in G.nodes()]
    graus = dict(G.degree())
    node_sizes = [300 + graus[n] * 50 for n in G.nodes()]

    nx.draw_networkx_edges(G, pos, alpha=0.3)
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.9)
    nx.draw_networkx_labels(G, pos, font_size=8)

    plt.title("Grafo de Ingredientes", fontsize=18)
    plt.axis('off')
    plt.tight_layout()
    plt.show()


def apresentar_grafo_circos(G):
    """
    Visualiza o grafo em Circos Plot usando a API funcional de nxviz,
    agrupando e colorindo por categoria.
    """
    plt.figure(figsize=(10, 10))
    # Função funcional alto-nível: nv.circos
    ax = nv.circos(
        G,
        node_grouping='tipo',
        node_color='tipo',
        group_legend=True
    )
    plt.title("Circos Plot: Ingredientes por Categoria", fontsize=18)
    plt.axis('off')
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    base = os.path.dirname(os.path.abspath(__file__))
    possiveis = ['50 RECEITAS.csv', '50 RECEITAS.csv.csv']
    csv_path = None
    for nome in possiveis:
        caminho = os.path.join(base, nome)
        if os.path.exists(caminho):
            csv_path = caminho
            break
    if csv_path is None:
        arquivos = os.listdir(base)
        raise FileNotFoundError(
            f"Nenhum arquivo CSV encontrado em {base}. Arquivos: {arquivos}"
        )

    gexf_path = os.path.join(base, 'grafo_ingredientes.gexf')

    G = construir_grafo(csv_path, salvar_em=gexf_path)
    calcular_assortatividade(G)
    apresentar_grafo_spring(G)
    apresentar_grafo_circos(G)