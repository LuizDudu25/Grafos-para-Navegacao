Este documento apresenta uma avaliação técnica detalhada do projeto desenvolvido para a
 atividade sobre o uso de **árvores e grafos no contexto de navegação de robôs**. O objetivo do
 trabalho é implementar, passo a passo, a leitura de um mapa, a geração de um grafo de
 visibilidade, a construção de uma árvore geradora mínima (MST), e a busca de caminhos entre
 dois pontos do ambiente.
 Estrutura Modular do Projeto
 O projeto está organizado em módulos independentes, cada um responsável por uma etapa do
 processo:
 1 **`mapa.py`** — leitura e validação de arquivos de mapa (texto).
 2 **`geometria.py`** — funções geométricas de interseção e detecção de obstáculos.
 3 **`grafo.py`** — construção e plotagem do grafo de visibilidade.
 4 **`arvore.py`** — implementação do algoritmo de Prim e visualização da MST.
 5 **`caminho.py`** — busca de caminho na árvore e geração de visualização final.
 6 **`main.py`** — integra todas as etapas (1 a 6) em uma execução sequencial.
 Avaliação das Etapas da Atividade
 1
 Leitura do mapa: Implementada em `mapa.py`, com leitura validada, tratamento de exceções
 e suporte a múltiplos obstáculos. Atende integralmente ao formato solicitado.
 2
 Criação do grafo de visibilidade: Feita em `grafo.py`, usando as funções de `geometria.py`
 para garantir que as conexões só ocorram quando não há interseções com obstáculos.
 3
 Implementação de Kruskal/Prim: O projeto utiliza o algoritmo de Prim (`arvore.py`) com
 cálculo de pesos, validação e estatísticas. Inclui visualização gráfica colorida da árvore.
 4
 Função verticeMaisProximo: Função robusta (`arvore.py`), com validações e opção de
 retornar distância. Inclui função de plotagem dedicada.
 5
 Busca de caminho: Implementada em `caminho.py` com algoritmo DFS, cálculo de distância
 acumulada e geração de estatísticas adicionais (razão entre caminho e linha reta).
 6
 Plotagem do caminho final: Função `plotarCaminho()` exibe de forma detalhada obstáculos,
 árvore e caminho. Interface visual completa e informativa, adequada para demonstrações.
 Pontos Fortes do Projeto
 1 Estrutura modular e reutilizável.
 2 Visualizações detalhadas e intuitivas com `matplotlib`.
 3 Tratamento robusto de erros e validações consistentes.
4 Comentários claros e código bem documentado.
 5 Cumprimento integral de todos os requisitos da atividade.
 Conclusão
 O projeto **atende plenamente aos seis requisitos da atividade**, apresentando excelente clareza
 estrutural, organização lógica e qualidade visual. Todas as etapas — da leitura do mapa à
 plotagem final — estão implementadas com coerência e robustez. >  Avaliação Final: **Projeto
 completo, funcional e tecnicamente excelente.*
