import streamlit as st
import graphviz
st.set_page_config(page_title="ABB Demo 01", page_icon="📊", layout="wide")

class Node:
    def __init__(self, element):
        self.element = element
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None
    
    def insert(self, element):
        self.root = self._insert_recursive(self.root, element)
    
    def _insert_recursive(self, node, element):
        if node is None:
            return Node(element)
        
        if element < node.element:
            node.left = self._insert_recursive(node.left, element)
        else:
            node.right = self._insert_recursive(node.right, element)
        
        return node
    
    def contains(self, element):
        if element is None:
            return None
        
        def generate_contains_steps(node, target):
            steps = []
            path = []
            
            def recursive_contains(current_node):
                if current_node is None:
                    steps.append({"type": "node", "node": None, "message": "Nodo actual es null. Búsqueda termina: False"})
                    return False
                
                path.append(current_node)
                steps.append({
                    "type": "node", 
                    "node": current_node, 
                    "path": path.copy(),
                    "message": f"Nodo actual: {current_node.element}"
                })
                
                if target == current_node.element:
                    steps.append({
                        "type": "result", 
                        "node": current_node, 
                        "path": path.copy(),
                        "message": f"Elemento {target} encontrado. Retorna: True"
                    })
                    return True
                
                if target > current_node.element:
                    steps.append({
                        "type": "move", 
                        "node": current_node, 
                        "path": path.copy(),
                        "message": f"{target} > {current_node.element}, moviéndose al hijo derecho"
                    })
                    return recursive_contains(current_node.right)
                
                steps.append({
                    "type": "move", 
                    "node": current_node, 
                    "path": path.copy(),
                    "message": f"{target} < {current_node.element}, moviéndose al hijo izquierdo"
                })
                return recursive_contains(current_node.left)
            
            result = recursive_contains(self.root)
            return steps, result
        
        return generate_contains_steps(self.root, element)
    
    def altura(self):
        def generate_altura_steps(node):
            steps = []
            
            def recursive_altura(current_node):
                if current_node is None:
                    steps.append({
                        "type": "node", 
                        "node": None, 
                        "message": "Nodo null encontrado. Altura: 0"
                    })
                    return 0
                
                steps.append({
                    "type": "node", 
                    "node": current_node, 
                    "message": f"Procesando nodo: {current_node.element}"
                })
                
                altura_izq = recursive_altura(current_node.left)
                
                altura_der = recursive_altura(current_node.right)
                
                max_altura = 1 + max(altura_izq, altura_der)
                steps.append({
                    "type": "result", 
                    "node": current_node, 
                    "message": f"Altura del nodo {current_node.element}: {max_altura}"
                })
                
                return max_altura
            
            altura_total = recursive_altura(node)
            
            return steps, altura_total
        
        return generate_altura_steps(self.root)
    
    def visualize_tree(self, current_path=None, current_node=None):
        graph = graphviz.Digraph()
        
        def add_nodes(node):
            if node:
                node_style = {}
                
                # Nodo actual
                if current_node and node == current_node:
                    node_style = {'style': 'filled', 'fillcolor': 'red', 'color': 'white'}
                # Camino recorrido
                elif current_path and node in current_path:
                    node_style = {'style': 'filled', 'fillcolor': 'lightblue'}
                
                graph.node(str(node.element), **node_style)
                
                if node.left:
                    graph.edge(str(node.element), str(node.left.element))
                    add_nodes(node.left)
                if node.right:
                    graph.edge(str(node.element), str(node.right.element))
                    add_nodes(node.right)
        
        add_nodes(self.root)
        return graph
        
        
def main():
    if 'elements' not in st.session_state:
        st.session_state.elements = [50, 30, 70, 20, 40, 60, 80]
    
    elements =st.session_state.elements
    
    # Inicializar árbol
    if 'bst' not in st.session_state:
        st.session_state.bst = BinarySearchTree()
        for elem in elements:
            st.session_state.bst.insert(elem)
    
    # Sidebar para insertar elementos
    st.sidebar.header("Configuración del Árbol")
    new_element = st.sidebar.number_input("Insertar nuevo elemento (0-100)", min_value=0, max_value=100, value=0)
    if st.sidebar.button("Insertar"):
        if new_element not in elements:
            elements.append(new_element)
            st.session_state.bst.insert(new_element)
        else:
            st.sidebar.write(f"Ya existe: {new_element}")

    # Selección de método
    col1, col2 = st.columns(2)
    with col1:
        metodo = st.sidebar.radio("Selecciona método", ["Altura","Búsqueda"])
    
    # Elemento a buscar o calcular
    with col2:
        if metodo == "Búsqueda":
            search_element = st.number_input("Elemento a buscar", min_value=0, max_value=100, value=0)
        else:
            st.write("Cálculo de Altura")
            search_element = None
    
    # Inicialización de estados
    if 'steps' not in st.session_state:
        st.session_state.steps = []
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 0
    if 'result' not in st.session_state:
        st.session_state.result = None
    
    # Botón de ejecución
    if st.button("Ejecutar"):
        if metodo == "Búsqueda":
            st.session_state.steps, st.session_state.result = st.session_state.bst.contains(search_element)
        else:
            st.session_state.steps, st.session_state.result = st.session_state.bst.altura()
        st.session_state.current_step = 0
    
    tree_graph = st.session_state.bst.visualize_tree()
    st.sidebar.graphviz_chart(tree_graph)
   
    
            
    # Visualización del árbol
    if st.session_state.steps:
        current_step = st.session_state.steps[st.session_state.current_step]
        
        # Determinar el nodo actual y el camino
        current_node = current_step.get('node')
        current_path = current_step.get('path', [])
        
        # Visualizar árbol
        tree_graph = st.session_state.bst.visualize_tree(current_path, current_node)
        st.graphviz_chart(tree_graph)
        
        # Mostrar mensaje del paso
        st.write(f"Paso {st.session_state.current_step + 1}: {current_step['message']}")
        
        # Mostrar resultado final si es el último paso
        if st.session_state.current_step == len(st.session_state.steps) - 1:
            if metodo == "Búsqueda":
                st.success(f"Resultado de la búsqueda: {'Encontrado' if st.session_state.result else 'No encontrado'}")
            else:
                st.success(f"Altura del árbol: {st.session_state.result}")
    
    # Botones de navegación
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("<=="):
            st.session_state.current_step = 0
    with col2:
        if st.button("<=") and st.session_state.current_step > 0:
            st.session_state.current_step -= 1
    with col3:
        if st.button("=>") and st.session_state.current_step < len(st.session_state.steps) - 1:
            st.session_state.current_step += 1
    with col4:
        if st.button("==>>"):
            st.session_state.current_step = len(st.session_state.steps) - 1

if __name__ == "__main__":
    main()