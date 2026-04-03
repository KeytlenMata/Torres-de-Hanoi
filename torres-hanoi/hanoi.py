"""
Módulo: hanoi.py
Descripción: Implementación del algoritmo de Torres de Hanoi
Por: Keytlen Mata
"""

from typing import List, Tuple, Optional
from dataclasses import dataclass, field


@dataclass
class Movimiento:
    """Representa un movimiento válido entre varillas."""
    disco: int
    origen: str
    destino: str
    numero_movimiento: int

    def __str__(self) -> str:
        return f"#{self.numero_movimiento}: Mover disco {self.disco} de {self.origen} → {self.destino}"


class TorresHanoi:
    """
    Clase que resuelve el problema de las Torres de Hanoi.
    Implementa versión recursiva, iterativa y visualización.
    """

    VARILLAS = ['A', 'B', 'C']  # Nombres de las varillas

    def __init__(self, n_discos: int, origen: str = 'A', destino: str = 'C', auxiliar: str = 'B'):
        if n_discos < 1 or n_discos > 20:
            raise ValueError("Número de discos debe estar entre 1 y 20")
        
        self.n_discos = n_discos
        self.origen = origen.upper()
        self.destino = destino.upper()
        self.auxiliar = auxiliar.upper()
        
        # Validar que las varillas sean distintas
        if len({self.origen, self.destino, self.auxiliar}) != 3:
            raise ValueError("Las tres varillas deben ser diferentes")
        
        # Estado de las varillas (pilas)
        self.varillas: dict[str, List[int]] = {
            self.origen: list(range(n_discos, 0, -1)),  # Disco mayor abajo
            self.auxiliar: [],
            self.destino: []
        }
        
        # Historial de movimientos
        self.historial: List[Movimiento] = []
        self.contador_movimientos = 0

    def _validar_movimiento(self, origen: str, destino: str) -> bool:
        """Verifica si un movimiento es válido según las reglas del juego."""
        if origen not in self.varillas or destino not in self.varillas:
            return False
        if not self.varillas[origen]:  # Varilla origen vacía
            return False
        
        disco_superior = self.varillas[origen][-1]
        
        # Regla: no colocar disco mayor sobre menor
        if self.varillas[destino] and self.varillas[destino][-1] < disco_superior:
            return False
        
        return True

    def _ejecutar_movimiento(self, origen: str, destino: str) -> bool:
        """Ejecuta físicamente un movimiento entre varillas."""
        if not self._validar_movimiento(origen, destino):
            return False
        
        disco = self.varillas[origen].pop()
        self.varillas[destino].append(disco)
        
        self.contador_movimientos += 1
        self.historial.append(Movimiento(
            disco=disco,
            origen=origen,
            destino=destino,
            numero_movimiento=self.contador_movimientos
        ))
        return True

    def resolver_recursivo(self, n: Optional[int] = None, 
                        origen: Optional[str] = None,
                        destino: Optional[str] = None,
                        auxiliar: Optional[str] = None,
                        registrar: bool = True) -> List[Movimiento]:
        """
        Solución recursiva clásica del problema.
        
        Algoritmo:
        1. Mover n-1 discos de origen a auxiliar (usando destino como temporal)
        2. Mover disco n de origen a destino
        3. Mover n-1 discos de auxiliar a destino (usando origen como temporal)
        
        Complejidad: O(2^n) movimientos, O(n) espacio en pila de recursión
        """
        # Parámetros por defecto
        n = n if n is not None else self.n_discos
        origen = origen if origen is not None else self.origen
        destino = destino if destino is not None else self.destino
        auxiliar = auxiliar if auxiliar is not None else self.auxiliar

        # 📌 Caso base: mover un solo disco
        if n == 1:
            if registrar:
                self._ejecutar_movimiento(origen, destino)
            return self.historial.copy()

        # 🔁 Paso 1: Mover n-1 discos a varilla auxiliar
        self.resolver_recursivo(n - 1, origen, auxiliar, destino, registrar)
        
        # 📦 Paso 2: Mover disco más grande a destino
        if registrar:
            self._ejecutar_movimiento(origen, destino)
        
        # 🔁 Paso 3: Mover n-1 discos desde auxiliar a destino
        self.resolver_recursivo(n - 1, auxiliar, destino, origen, registrar)
        
        return self.historial.copy()

    def resolver_iterativo(self) -> List[Movimiento]:
        """
        Solución iterativa usando pila explícita.
        Evita el límite de recursión del intérprete.
        
        Algoritmo basado en patrón cíclico:
        - Si n es par: intercambiar destino y auxiliar
        - Movimientos válidos siguen patrón: A→B, A→C, B→C (cíclico)
        """
        # Reiniciar estado
        self.__init__(self.n_discos, self.origen, self.destino, self.auxiliar)
        
        # Para n par, intercambiar destino y auxiliar para mantener patrón
        varillas_temp = [self.origen, self.destino, self.auxiliar]
        if self.n_discos % 2 == 0:
            varillas_temp[1], varillas_temp[2] = varillas_temp[2], varillas_temp[1]
        
        total_movimientos = (2 ** self.n_discos) - 1
        
        for i in range(1, total_movimientos + 1):
            if i % 3 == 1:
                # Movimiento entre origen y destino
                self._mover_entre(varillas_temp[0], varillas_temp[1])
            elif i % 3 == 2:
                # Movimiento entre origen y auxiliar
                self._mover_entre(varillas_temp[0], varillas_temp[2])
            else:
                # Movimiento entre auxiliar y destino
                self._mover_entre(varillas_temp[1], varillas_temp[2])
        
        return self.historial.copy()

    def _mover_entre(self, var1: str, var2: str) -> bool:
        """Intenta mover entre dos varillas en ambas direcciones, ejecuta la válida."""
        if self._validar_movimiento(var1, var2):
            return self._ejecutar_movimiento(var1, var2)
        elif self._validar_movimiento(var2, var1):
            return self._ejecutar_movimiento(var2, var1)
        return False

    def obtener_estado(self) -> dict[str, List[int]]:
        """Retorna copia del estado actual de las varillas."""
        return {k: v.copy() for k, v in self.varillas.items()}

    def esta_resuelto(self) -> bool:
        """Verifica si todos los discos están en la varilla destino."""
        return len(self.varillas[self.destino]) == self.n_discos

    def reiniciar(self):
        """Reinicia el juego a estado inicial."""
        self.__init__(self.n_discos, self.origen, self.destino, self.auxiliar)

    def visualizar(self) -> str:
        """Genera representación ASCII del estado actual."""
        altura = self.n_discos
        lineas = []
        
        # Encabezado
        lineas.append(f"\n🗼 Torres de Hanoi - {self.n_discos} discos")
        lineas.append(f"Movimientos realizados: {self.contador_movimientos}")
        lineas.append("=" * 50)
        
        # Dibujar cada nivel de las torres
        for nivel in range(altura - 1, -1, -1):
            fila = ""
            for varilla in self.VARILLAS:
                discos = self.varillas[varilla]
                if nivel < len(discos):
                    # Dibujar disco con tamaño proporcional
                    tamano = discos[nivel]
                    fila += f"{' ' * (altura - tamano)}{'█' * (2 * tamano - 1)}{' ' * (altura - tamano)}  "
                else:
                    # Espacio vacío o poste
                    fila += f"{' ' * altura}│{' ' * altura}  "
            lineas.append(fila.rstrip())
        
        # Base de las varillas
        lineas.append("-" * 50)
        lineas.append(f"{'A':^{2 * altura + 2}}{'B':^{2 * altura + 2}}{'C':^{2 * altura + 2}}")
        
        return "\n".join(lineas)

    def __str__(self) -> str:
        return self.visualizar()