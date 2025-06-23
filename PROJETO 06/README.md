<p align="center">
  <img src="IMGs/DCA.png" alt="Logo da UFRN" width=300/>
</p>

<h3 align="center"><strong>UNIVERSIDADE FEDERAL DO RIO GRANDE DO NORTE</strong></h3>

<p align="center"> 
DEPARTAMENTO DE ENGENHARIA DE COMPUTAÇÃO E AUTOMAÇÃO 
<br> 
DCA3702 - ALGORITMOS E ESTRUTURAS DE DADOS II  
</p>

<h1 align="center"><strong>PROJETO 06 - MST aplicada ao grafo urbano da cidade de Natal</strong></h1>

<strong>DISCENTES:</strong>  
- MINNAEL CAMPELO DE OLIVEIRA  

<strong>DOCENTE:</strong>  
- IVANOVITCH MEDEIROS DANTAS DA SILVA  

**Natal/RN — 2025**

---

## <strong>1. PROBLEMÁTICA</strong>

Com o crescimento das cidades, o planejamento de redes urbanas torna-se cada vez mais desafiador. Interligar múltiplos pontos de interesse, como bases de táxi, exige não apenas uma abordagem intuitiva, mas também métodos matemáticos eficientes que respeitem a malha viária real. Considerando esse cenário, este projeto propõe o uso de algoritmos de grafos para resolver um problema clássico de conectividade urbana: como interligar todas as bases de táxi de forma otimizada, utilizando apenas as ruas existentes da cidade de Natal-RN. A complexidade aumenta por se tratar de um problema de otimização, em que o objetivo é minimizar o custo total de deslocamento sem criar rotas redundantes ou ciclos desnecessários.

---

## <strong>2. DESENVOLVIMENTO</strong>

Para abordar o problema proposto, utilizou-se a biblioteca **OSMnx** com dados da plataforma **OpenStreetMap**, que permitiram extrair a malha viária da cidade de Natal com alta precisão, considerando apenas as vias motorizadas. A partir dessa malha, construiu-se um grafo urbano representando as interconexões reais entre os cruzamentos e ruas da cidade.  

Em seguida, pontos de interesse classificados como `amenity=taxi` foram filtrados diretamente da base de dados geográfica. Quando esses não estavam disponíveis, pontos alternativos foram utilizados apenas para fins de teste e visualização. As coordenadas geográficas desses pontos foram associadas aos nós mais próximos do grafo da cidade.

A etapa central do projeto consistiu em construir um grafo completo entre os pontos de táxi, onde cada aresta representava o menor caminho real (em metros) entre dois pontos, calculado com base no comprimento das ruas. A partir desse grafo completo, aplicou-se o **algoritmo de Kruskal** (disponível na biblioteca **NetworkX**) para encontrar a **Árvore Geradora Mínima (MST)** — uma estrutura eficiente que conecta todos os pontos com o menor custo possível, sem formar ciclos.

Por fim, a visualização foi realizada sobre o mapa da cidade, destacando as conexões mínimas da MST em vermelho, os pontos de táxi em azul e as ruas da cidade em cinza. O resultado final é uma representação clara e objetiva da rede de interligação otimizada entre as bases.

---

## <strong>3. RESULTADOS</strong>

A execução do algoritmo gerou uma Árvore Geradora Mínima conectando todos os pontos de interesse utilizando apenas as vias urbanas reais. O comprimento total dessa MST foi de aproximadamente **34.088 metros**, valor que representa a soma das menores distâncias reais necessárias para interligar todas as bases de táxi da cidade.

A visualização gráfica reforça a qualidade do modelo, permitindo compreender como os pontos foram conectados com eficiência e respeito à geografia urbana. Essa abordagem é útil não apenas para redes de táxi, mas também para o planejamento de transporte público, logística de entregas urbanas e redes de serviços essenciais.

O projeto demonstrou que a combinação de dados abertos, bibliotecas especializadas em grafos e algoritmos clássicos pode fornecer soluções práticas e eficazes para desafios reais enfrentados em cidades em crescimento. Além disso, reforça o potencial de uso de algoritmos de grafos no contexto da engenharia urbana e mobilidade inteligente.

<p align="center">
  <img src="IMGs/result.png" alt="Logo da UFRN" width=300/>
</p>

---

## <strong>Informações Complementares</strong>

Este repositório reúne todos os materiais utilizados para desenvolvimento do projeto, incluindo os notebooks com comentários detalhados, os arquivos de visualização e os links externos de apoio e divulgação do trabalho.

- O artigo completo está publicado no Medium e pode ser acessado [neste link](https://medium.com/@minaelcampelo3/otimizando-redes-de-t%C3%A1xi-com-algoritmos-de-grafos-um-estudo-de-caso-em-natal-rn-20951540e9b2).
- Um podcast explicativo foi gerado no NotebookLM e pode ser ouvido [aqui](https://notebooklm.google.com/notebook/1ef43f50-b5ad-4cc4-8924-2207106b0489/audio).
- Os prompts utilizados durante o processo estão documentados na pasta [`MD`](https://github.com/Minnael/ESTRUTURAS-DE-DADOS-II/tree/master/PROJETO%2006/MD).
- O notebook em Python com toda a lógica do algoritmo está disponível na pasta [`JUPYTER`](https://github.com/Minnael/ESTRUTURAS-DE-DADOS-II/tree/master/PROJETO%2006/JUPYTER).

---

