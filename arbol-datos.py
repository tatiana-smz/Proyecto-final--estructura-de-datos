"""
EXAMEN FINAL - ESTRUCTURAS DE DATOS
Árbol AVL Interactivo (Terminal)
Estudiante: MEDINA ZAMBRANO TATIANA STEFANY
Codigo: 20252578026 - Estudiante #15
Secuencia: 77, 47, 102, 37, 62, 87, 107, 60, 61, 59, 58, 63
"""

#  NODO DEL ÁRBOL AVL _______________________________________________

class NodoAVL:
    def __init__(self, valor):
        self.valor = valor
        self.izq = None   # hijo izquierdo
        self.der = None   # hijo derecho
        self.altura = 1      # altura del nodo

#  ÁRBOL AVL _______________________________________________

class ArbolAVL:

    def __init__(self):
        self.raiz = None
        self.rotaciones = 0
        self.log = []   # registro de operaciones

    # Utilidades de altura _______________________________________________

    def altura(self, nodo):
        """Devuelve la altura de un nodo (0 si es None)."""
        return nodo.altura if nodo else 0

    def factor_equilibrio(self, nodo):
        """FE = altura_izq - altura_der"""
        return self.altura(nodo.izq) - self.altura(nodo.der) if nodo else 0

    def actualizar_altura(self, nodo):
        if nodo:
            nodo.altura = 1 + max(self.altura(nodo.izq), self.altura(nodo.der))

    # Rotaciones _______________________________________________

    def rotar_derecha(self, y):
        x  = y.izq
        T2 = x.der
        x.der = y
        y.izq = T2
        self.actualizar_altura(y)
        self.actualizar_altura(x)
        self.rotaciones += 1
        self._log(f" Rotacion DERECHA sobre nodo {y.valor}")
        return x

    def rotar_izquierda(self, x):
        y  = x.der
        T2 = y.izq
        y.izq = x
        x.der = T2
        self.actualizar_altura(x)
        self.actualizar_altura(y)
        self.rotaciones += 1
        self._log(f" Rotacion IZQUIERDA sobre nodo {x.valor}")
        return y

    # Balancear _______________________________________________

    def balancear(self, nodo):
        self.actualizar_altura(nodo)
        fe = self.factor_equilibrio(nodo)

        if fe > 1 and self.factor_equilibrio(nodo.izq) >= 0:
            self._log(f" Desbalance en {nodo.valor}: caso Izq-Izq")
            return self.rotar_derecha(nodo)

        if fe > 1 and self.factor_equilibrio(nodo.izq) < 0:
            self._log(f" Desbalance en {nodo.valor}: caso Izq-Der")
            nodo.izq = self.rotar_izquierda(nodo.izq)
            return self.rotar_derecha(nodo)

        if fe < -1 and self.factor_equilibrio(nodo.der) <= 0:
            self._log(f" Desbalance en {nodo.valor}: caso Der-Der")
            return self.rotar_izquierda(nodo)

        if fe < -1 and self.factor_equilibrio(nodo.der) > 0:
            self._log(f" Desbalance en {nodo.valor}: caso Der-Izq")
            nodo.der = self.rotar_derecha(nodo.der)
            return self.rotar_izquierda(nodo)

        return nodo

    # Insertar _______________________________________________

    def _insertar(self, nodo, valor):
        if nodo is None:
            return NodoAVL(valor)
        if valor < nodo.valor:
            nodo.izq = self._insertar(nodo.izq, valor)
        elif valor > nodo.valor:
            nodo.der = self._insertar(nodo.der, valor)
        else:
            self._log(f"{valor} ya existe, se ignora")
            return nodo
        return self.balancear(nodo)

    def insertar(self, valor):
        self._log(f"INSERT {valor}")
        self.raiz = self._insertar(self.raiz, valor)
        self._log(f"-> Altura arbol: {self.altura(self.raiz)} - FE raiz: {self.factor_equilibrio(self.raiz)}")

    # Eliminar _______________________________________________

    def _minimo(self, nodo):
        while nodo.izq:
            nodo = nodo.izq
        return nodo

    def _eliminar(self, nodo, valor):
        if nodo is None:
            return None
        if valor < nodo.valor:
            nodo.izq = self._eliminar(nodo.izq, valor)
        elif valor > nodo.valor:
            nodo.der = self._eliminar(nodo.der, valor)
        else:
            if not nodo.izq:
                return nodo.der
            if not nodo.der:
                return nodo.izq
            sucesor = self._minimo(nodo.der)
            nodo.valor = sucesor.valor
            nodo.der = self._eliminar(nodo.der, sucesor.valor)
        return self.balancear(nodo)

    def eliminar(self, valor):
        if not self.buscar(valor, silencioso=True):
            self._log(f"DELETE {valor} -> No existe")
            return
        self._log(f"DELETE {valor}")
        self.raiz = self._eliminar(self.raiz, valor)
        self._log(f" -> Altura arbol: {self.altura(self.raiz)} - FE raiz: {self.factor_equilibrio(self.raiz)}")

    # Buscar _______________________________________________

    def buscar(self, valor, silencioso=False):
        camino = []
        nodo   = self.raiz
        while nodo:
            camino.append(nodo.valor)
            if valor == nodo.valor:
                if not silencioso:
                    self._log(f"SEARCH {valor} -> Camino: {'-> '.join(map(str, camino))} ENCONTRADO")
                return True
            nodo = nodo.izq if valor < nodo.valor else nodo.der
        if not silencioso:
            self._log(f"SEARCH {valor} -> Camino: {'-> '.join(map(str, camino))} NO ENCONTRADO")
        return False

    # Imprimir árbol ──────────────────────────────────────────────────
    # Cada nodo se muestra como (valor | fe)
    #   valor = el número guardado en ese nodo
    #   fe = factor de equilibrio  (izq - der)
    #           0 -> balanceado
    #           1 -> pesa más a la izquierda
    #          -1 -> pesa más a la derecha
    # ────────────────────────────────────────────────────────────────────

    def imprimir(self):
        if not self.raiz:
            print("  (arbol vacio)")
            return

        print()
        print("  Referencia de cada nodo:  (valor | fe)")
        print("    valor = numero del nodo")
        print("    fe    = factor de equilibrio  [0 balanceado | 1 pesa izq | -1 pesa der]")
        print()

        # asignar posición X a cada nodo usando inorden ______________
        # El inorden da los nodos de izquierda a derecha en orden,
        # entonces cada nodo recibe una columna única y nunca se enciman.
        self._pos = {}          # nodo -> columna (número entero)
        self._contador = [0]    # usamos lista para poder modificarlo dentro de la función

        def asignar_pos(nodo):
            if nodo is None:
                return
            asignar_pos(nodo.izq)                      # primero todo lo de la izquierda
            self._pos[id(nodo)] = self._contador[0]    # le doy la siguiente columna libre
            self._contador[0] += 1                     # avanzo la columna
            asignar_pos(nodo.der)                      # luego todo lo de la derecha

        asignar_pos(self.raiz)

        total_nodos   = self._contador[0]
        ancho_celda   = 9          # caracteres por columna — sube si se enciman
        ancho_total   = total_nodos * ancho_celda

        #recorrer nivel por nivel y dibujar ______________
        # Se guarfa (nodo, nivel) en una cola simple
        cola = [(self.raiz, 0)]
        niveles = {}                # nivel -> lista de nodos

        while cola:
            nodo, nivel = cola.pop(0)
            if nodo is None:
                continue
            if nivel not in niveles:
                niveles[nivel] = []
            niveles[nivel].append(nodo)
            cola.append((nodo.izq, nivel + 1))
            cola.append((nodo.der, nivel + 1))

        #imprimir cada nivel ___________
        for nivel in sorted(niveles):
            nodos_nivel = niveles[nivel]

            # Línea de nodos
            linea = [" "] * ancho_total
            for nodo in nodos_nivel:
                col  = self._pos[id(nodo)]
                fe   = self.factor_equilibrio(nodo)
                txt  = f"({nodo.valor}|{fe})"
                x    = col * ancho_celda + ancho_celda // 2 - len(txt) // 2
                for k, c in enumerate(txt):
                    if 0 <= x + k < ancho_total:
                        linea[x + k] = c
            print("".join(linea).rstrip())

            # Línea de ramas  /  \
            if nivel + 1 in niveles:
                ramas = [" "] * ancho_total
                for nodo in nodos_nivel:
                    col_padre = self._pos[id(nodo)]
                    cx = col_padre * ancho_celda + ancho_celda // 2

                    if nodo.izq:
                        col_hijo = self._pos[id(nodo.izq)]
                        hx = col_hijo * ancho_celda + ancho_celda // 2
                        # punto medio entre hijo y padre
                        pm = (hx + cx) // 2
                        if 0 <= pm < ancho_total:
                            ramas[pm] = "/"

                    if nodo.der:
                        col_hijo = self._pos[id(nodo.der)]
                        hx = col_hijo * ancho_celda + ancho_celda // 2
                        # punto medio entre padre e hijo
                        pm = (cx + hx) // 2
                        if 0 <= pm < ancho_total:
                            ramas[pm] = "\\"
                print("".join(ramas).rstrip())
        print()

    # Recorridos _______________________________________________

    def inorden(self):
        resultado = []
        def _rec(n):
            if n:
                _rec(n.izq)
                resultado.append(n.valor)
                _rec(n.der)
        _rec(self.raiz)
        return resultado

    def preorden(self):
        resultado = []
        def _rec(n):
            if n:
                resultado.append(n.valor)
                _rec(n.izq)
                _rec(n.der)
        _rec(self.raiz)
        return resultado

    def postorden(self):
        resultado = []
        def _rec(n):
            if n:
                _rec(n.izq)
                _rec(n.der)
                resultado.append(n.valor)
        _rec(self.raiz)
        return resultado

    # Estadísticas

    def contar_nodos(self):
        def _c(n): return 0 if not n else 1 + _c(n.izq) + _c(n.der)
        return _c(self.raiz)

    def estadisticas(self):
        print("\n" + "="*45)
        print(" ESTADISTICAS DEL ARBOL")
        print("="*45)
        print(f" Nodos: {self.contar_nodos()}")
        print(f" Altura: {self.altura(self.raiz)}")
        fe = self.factor_equilibrio(self.raiz) if self.raiz else "N/A"
        print(f" FE raiz: {fe}")
        print(f" Rotaciones: {self.rotaciones}")
        print(f" Inorden: {self.inorden()}")
        print(f" Preorden: {self.preorden()}")
        print(f" Postorden: {self.postorden()}")
        print("="*45)

    # Log

    def _log(self, mensaje):
        self.log.append(mensaje)
        print(mensaje)

    def mostrar_log(self):
        print("\n" + "="*45)
        print(" LOG COMPLETO DE OPERACIONES")
        print("="*45)
        for linea in self.log:
            print(linea)
        print("="*45)


#  MENÚ PRINCIPAL _______________________________________________

SECUENCIA_15 = [77, 47, 102, 37, 62, 87, 107, 60, 61, 59, 58, 63]

def menu():
    arbol = ArbolAVL()
    print("\n" + "="*45)
    print(" ARBOL AVL INTERACTIVO - Terminal")
    print(" Tatiana Stefany Medina Zambrano - Estudiante #15")
    print("="*45)

    while True:
        print("""
*─────────────────────────────────*
|  1. Insertar nodo               |
|  2. Eliminar nodo               |
|  3. Buscar nodo                 |
|  4. Ver arbol                   |
|  5. Cargar secuencia #15        |
|  6. Generar aleatorio           |
|  7. Estadisticas                |
|  8. Ver log completo            |
|  9. Reiniciar arbol             |
|  0. Salir                       |
*─────────────────────────────────*""")

        opcion = input(" Opcion: ").strip()

        if opcion == "1":
            val = input(" Valor a insertar: ").strip()
            if val.lstrip("-").isdigit():
                arbol.insertar(int(val))
            else:
                print(" Ingresa un numero valido")

        elif opcion == "2":
            val = input(" Valor a eliminar: ").strip()
            if val.lstrip("-").isdigit():
                arbol.eliminar(int(val))
            else:
                print(" Ingresa un numero valido")

        elif opcion == "3":
            val = input(" Valor a buscar: ").strip()
            if val.lstrip("-").isdigit():
                arbol.buscar(int(val))
            else:
                print(" Ingresa un numero valido")

        elif opcion == "4":
            arbol.imprimir()

        elif opcion == "5":
            arbol = ArbolAVL()
            print(f"\n Cargando secuencia #15: {SECUENCIA_15}\n")
            for v in SECUENCIA_15:
                arbol.insertar(v)
                print()
            print(" Secuencia cargada. Arbol:")
            arbol.imprimir()

        elif opcion == "6":
            import random
            arbol = ArbolAVL()
            n    = random.randint(5, 15)
            vals = random.sample(range(1, 150), n)
            print(f"\n Generando {n} valores aleatorios: {vals}\n")
            for v in vals:
                arbol.insertar(v)
            print("\n Arbol generado:")
            arbol.imprimir()

        elif opcion == "7":
            arbol.estadisticas()

        elif opcion == "8":
            arbol.mostrar_log()

        elif opcion == "9":
            arbol = ArbolAVL()
            print(" Arbol reiniciado")

        elif opcion == "0":
            print("Hasta luego")
            break

        else:
            print("Opcion no valida")


if __name__ == "__main__":
    menu()