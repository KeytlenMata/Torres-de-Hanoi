#!/usr/bin/env python3
"""
Pruebas unitarias para el módulo de Torres de Hanoi.
Ejecutar con: python -m pytest tests.py -v
"""

import pytest
from hanoi import TorresHanoi, Movimiento


class TestTorresHanoi:
    """Suite de pruebas para la clase TorresHanoi."""

    def test_inicializacion_valida(self):
        """Verifica que la inicialización funcione con parámetros válidos."""
        hanoi = TorresHanoi(3)
        assert hanoi.n_discos == 3
        assert len(hanoi.varillas['A']) == 3
        assert hanoi.varillas['A'] == [3, 2, 1]  # Mayor abajo
        assert hanoi.varillas['B'] == []
        assert hanoi.varillas['C'] == []

    def test_inicializacion_invalida_discos(self):
        """Debe lanzar error con número de discos inválido."""
        with pytest.raises(ValueError):
            TorresHanoi(0)
        with pytest.raises(ValueError):
            TorresHanoi(21)

    def test_inicializacion_invalida_varillas(self):
        """Debe lanzar error si las varillas no son distintas."""
        with pytest.raises(ValueError):
            TorresHanoi(3, origen='A', destino='A', auxiliar='B')

    def test_resolver_recursivo_3_discos(self):
        """Verifica solución correcta para 3 discos."""
        hanoi = TorresHanoi(3)
        hanoi.resolver_recursivo()
        
        assert hanoi.esta_resuelto()
        assert hanoi.contador_movimientos == 7  # 2^3 - 1
        assert len(hanoi.varillas['C']) == 3
        assert hanoi.varillas['C'] == [3, 2, 1]  # Orden correcto

    def test_resolver_iterativo_vs_recursivo(self):
        """Ambos métodos deben producir misma cantidad de movimientos."""
        n = 4
        h1 = TorresHanoi(n)
        h2 = TorresHanoi(n)
        
        h1.resolver_recursivo()
        h2.resolver_iterativo()
        
        assert h1.contador_movimientos == h2.contador_movimientos
        assert h1.contador_movimientos == (2 ** n) - 1

    def test_validacion_movimiento_invalido(self):
        """No debe permitir mover disco mayor sobre menor."""
        hanoi = TorresHanoi(3)
        # Mover disco 1 de A a C (válido)
        assert hanoi._ejecutar_movimiento('A', 'C') == True
        # Intentar mover disco 2 de A a C (inválido: 2 > 1)
        assert hanoi._validar_movimiento('A', 'C') == False

    def test_historial_movimientos(self):
        """El historial debe registrar todos los movimientos correctamente."""
        hanoi = TorresHanoi(2)
        hanoi.resolver_recursivo()
        
        assert len(hanoi.historial) == 3
        assert isinstance(hanoi.historial[0], Movimiento)
        assert hanoi.historial[0].disco == 1
        assert hanoi.historial[0].numero_movimiento == 1

    def test_visualizacion_no_vacia(self):
        """La visualización debe generar string no vacío."""
        hanoi = TorresHanoi(3)
        visual = hanoi.visualizar()
        assert len(visual) > 0
        assert 'A' in visual and 'B' in visual and 'C' in visual

    def test_reiniciar_estado(self):
        """Reiniciar debe devolver al estado inicial."""
        hanoi = TorresHanoi(3)
        hanoi.resolver_recursivo()
        assert hanoi.esta_resuelto()
        
        hanoi.reiniciar()
        assert not hanoi.esta_resuelto()
        assert len(hanoi.varillas['A']) == 3
        assert hanoi.contador_movimientos == 0


def test_complejidad_movimientos():
    """Verifica que el número de movimientos siga la fórmula 2^n - 1."""
    for n in range(1, 8):
        hanoi = TorresHanoi(n)
        hanoi.resolver_recursivo()
        esperado = (2 ** n) - 1
        assert hanoi.contador_movimientos == esperado, f"Falló para n={n}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])