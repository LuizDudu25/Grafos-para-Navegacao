# Grafos para Navegação

Este projeto explora o uso de estruturas de grafos e árvores aplicadas à navegação de robôs em ambientes com obstáculos.  
A partir de um mapa bidimensional definido por um arquivo de texto, o sistema é capaz de:

- Gerar o grafo de visibilidade com base na posição dos obstáculos;  
- Construir uma árvore geradora mínima (MST) utilizando algoritmos clássicos (Prim ou Kruskal);  
- Encontrar o caminho mais adequado entre dois pontos (inicial e final) dentro do espaço livre;  
- Visualizar graficamente todas as etapas do processo, mostrando o mapa, o grafo, a árvore e o caminho final.  

O objetivo é demonstrar, de forma prática, como conceitos fundamentais de teoria dos grafos e geometria computacional podem ser aplicados à navegação autônoma — simulando o planejamento de trajetória de um robô em um ambiente com múltiplos obstáculos.

---

##  Tecnologias utilizadas

-  Python 3
- Bibliotecas principais:
  - `matplotlib` → visualização dos grafos e caminhos  
  - `shapely` → operações geométricas (detecção de interseção e visibilidade)  
  - `math`, `itertools`, `heapq` → manipulação de coordenadas e algoritmos de busca  

---

## Objetivo do projeto

Este trabalho foi desenvolvido como uma atividade prática sobre o conceito de árvores e busca em grafos,  
explorando algoritmos clássicos de planejamento de movimento em robótica.  

O código foi construído de forma incremental, seguindo as etapas propostas em sala, com foco na clareza e visualização dos resultados.

---

