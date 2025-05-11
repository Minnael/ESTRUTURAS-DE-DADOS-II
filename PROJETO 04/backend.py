from flask import Flask, jsonify, render_template, request
import osmnx as ox
import networkx as nx
from geopy.distance import geodesic

app = Flask(__name__)

place = "Santa Cruz, Rio Grande do Norte, Brazil"
G = ox.graph_from_place(place, network_type='drive')
destino = ox.geocode("IFRN, Santa Cruz, Brazil")
dest_node = ox.distance.nearest_nodes(G, X=destino[1], Y=destino[0])

# Rota anterior
rota_atual = []

def saiu_da_rota(posicao_atual, caminho, tolerancia_metros=30):
    for ponto in caminho:
        if geodesic(posicao_atual, ponto).meters <= tolerancia_metros:
            return False
    return True

@app.route('/')
def index():
    return render_template('index.html')
    

@app.route('/rota')
def get_rota():
    lat = float(request.args.get('lat'))
    lng = float(request.args.get('lng'))

    orig_node = ox.distance.nearest_nodes(G, X=lng, Y=lat)
    caminho = nx.shortest_path(G, source=orig_node, target=dest_node, weight='length')
    coordenadas = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in caminho]

    return jsonify({
        'origem': [lat, lng],
        'destino': destino,
        'caminho': coordenadas
    })

if __name__ == '__main__':
    app.run(debug=True)
