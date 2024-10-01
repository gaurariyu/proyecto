import graphviz

class VisualizadorArbol:
    @staticmethod
    def graficar_arbol(nodo, dot=None, parent_id=None, node_id=0):
        if dot is None:
            dot = graphviz.Digraph()

        current_id = f'node{node_id}'
        dot.node(current_id, nodo.valor)

        if parent_id is not None:
            dot.edge(parent_id, current_id)

        for hijo in nodo.hijos:
            node_id += 1
            node_id = VisualizadorArbol.graficar_arbol(hijo, dot, current_id, node_id)

        return node_id

    @staticmethod
    def generar_arbol_grafico(nodo):
        dot = graphviz.Digraph()
        VisualizadorArbol.graficar_arbol(nodo, dot)
        dot.render('arbol_sintactico', format='png', view=True)
