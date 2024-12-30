
# Manual Técnico del Sistema de Gestión de Transporte

## Descripción General
Este sistema es una solución robusta para gestionar clientes, vehículos, rutas y viajes en una empresa de transporte. Se basa en diversas estructuras de datos y algoritmos que garantizan la eficiencia en las operaciones.

### Estructuras y Componentes Principales
- **Lista Circular Doblemente Enlazada**: Para manejar clientes.
- **Árbol B**: Para gestionar vehículos.
- **Grafo con Listas de Adyacencia**: Para representar rutas.
- **Lista Simple**: Para registrar las rutas de los viajes.

---

## Descripción de Clases

### 1. Clase `Nodo`
Esta clase implementa nodos para diversas estructuras de datos.

```python
class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None
```

---

### 2. Clase `ListaCircularDoblementeEnlazada`
**Propósito**: Manejar clientes en una lista circular eficiente.

#### Métodos Principales:
- `insertar(cliente)`: Inserta un cliente en orden por DPI.
- `eliminar_cliente_por_dpi(dpi)`: Elimina un cliente especificado por su DPI.
- `estructura_cliente_graphviz()`: Genera una visualización de la lista.

---

### 3. Clase `ArbolB`
**Propósito**: Gestionar vehículos utilizando un árbol B de grado configurable.

#### Métodos Principales:
- `insertar_vehiculo(vehiculo)`: Inserta un vehículo en el árbol.
- `buscar_vehiculo(placa)`: Busca un vehículo por su placa.
- `imprimir_grafica()`: Genera una representación visual del árbol.
- `eliminar_vehiculo(placa)`: Elimina un vehículo por su placa.

---

### 4. Clase `GrafoRutas`
**Propósito**: Representar rutas y calcular caminos óptimos.

#### Métodos Principales:
- `agregar_ruta(origen, destino, tiempo)`: Añade una conexión entre dos nodos con un peso.
- `calcular_mejor_ruta(origen, destino)`: Calcula el camino más corto entre dos nodos usando Dijkstra.
- `generar_grafo_graphviz()`: Genera una visualización del grafo.

---

### 5. Clase `GestorViajes`
**Propósito**: Gestionar viajes utilizando las estructuras de datos.

#### Métodos Principales:
- `crear_viaje(dpi_cliente, placa_vehiculo, origen, destino, fecha_hora_inicio)`: Registra un viaje asociando cliente, vehículo y ruta.
- `obtener_ruta_por_id(viaje_id)`: Recupera la información de un viaje por su ID.

---

## Visualización
Se emplea la biblioteca **Graphviz** para generar representaciones visuales de:
- Árbol B de vehículos.
- Grafo de rutas.
- Lista circular de clientes.

Ejemplo de visualización:
- **Lista de Clientes**: Se generan conexiones para representar nodos circulares y sus relaciones.

---

## Dependencias
1. **Python 3.8+**
2. Bibliotecas adicionales:
    ```bash
    pip install graphviz pillow
    ```

---

## Diagramas de Estructuras
El sistema utiliza **Graphviz** para generar gráficos automáticamente en formato `.svg` o `.png`.

Comando para generar un gráfico del Árbol B:
```python
arbol_vehiculos.imprimir_grafica()
```

Comando para visualizar la lista circular:
```python
lista_clientes.estructura_cliente_graphviz()
```

---

## Módulos Importados
### Clases de soporte:
- `Clientes`: Maneja la entidad Cliente.
- `Vehiculos`: Maneja la entidad Vehículo.
- `Viajes`: Define los viajes.
- `Rutas`: Representa cada ruta.

### Estructuras:
- `ListaCircularDoblementeEnlazada`: Para gestionar clientes.
- `ArbolB`: Para almacenar vehículos.
- `GrafoRutas`: Para las rutas y caminos.

---

## Archivos Generados
- **`Estructura_Clientes.svg`**: Representación de la lista circular.
- **`arbol_b_graph.svg`**: Gráfico del árbol B.
- **`grafo_rutas.png`**: Visualización del grafo de rutas.

---

## Funcionalidades del Sistema
1. **Gestión de Clientes**:
   - Añadir, modificar y eliminar clientes.
2. **Gestión de Vehículos**:
   - Registrar y administrar vehículos en el Árbol B.
3. **Gestión de Rutas**:
   - Crear y visualizar rutas.
4. **Gestión de Viajes**:
   - Crear viajes asociando clientes, vehículos y rutas óptimas.

---

## Notas Finales
El sistema está diseñado para ser extensible y eficiente, facilitando la integración de nuevos módulos. Se recomienda realizar pruebas exhaustivas al añadir nuevas funcionalidades.
