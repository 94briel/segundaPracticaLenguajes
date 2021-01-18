from nodo_simple import NodoSimple


# Creamos la clase LSL

class LSL:

    # Inicialización de la estructura de datos
    def __init__(self):
        self.primero = None
        self.ultimo = None

    # Método para verificar si la LSL es vacía
    def es_vacia(self):
        return self.primero == None

    # Método para agregar elementos al final de la LSL
    def anadir(self, clase, dato):
        nuevo_nodo = NodoSimple(clase=clase, dato=dato)
        if self.es_vacia():
            self.primero = nuevo_nodo
            self.ultimo = nuevo_nodo
            return self
        self.ultimo.liga = nuevo_nodo
        self.ultimo = nuevo_nodo
        return self

    # Método para eliminar nodos
    def eliminar_nodo(self, dato):
        nodo_actual = self.primero
        nodo_anterior = None
        while nodo_actual and nodo_actual.dato != dato:
            nodo_anterior = nodo_actual
            nodo_actual = nodo_actual.liga
        if nodo_anterior is None:
            self.primero = nodo_actual.liga
        elif nodo_actual:
            nodo_anterior.liga = nodo_actual.liga
        if nodo_actual.liga is None:
            self.ultimo = nodo_anterior
        return self

    def __len__(self):
        i = 0
        node = self.primero
        while node is not None:
            i += 1
            node = node.liga
        return i

    # Método para representar la LSL en el programa
    def __str__(self):
        lsl_string = ""
        node = self.primero
        while node is not None:
            lsl_string += "["
            lsl_string += str(node.clase)
            lsl_string += ", "
            lsl_string += str(node.dato)
            lsl_string += "]"
            if node.liga is not None:
                lsl_string += " => "
            node = node.liga
        return lsl_string
