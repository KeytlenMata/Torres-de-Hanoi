#!/usr/bin/env python3
"""
Torres de Hanoi - Interfaz de Consola
Por: Keytlen Mata
"""

import sys
from hanoi import TorresHanoi, Movimiento


def imprimir_menu():
    """Muestra el menú principal de opciones."""
    print("\n" + "🗼" * 25)
    print("   TORRES DE HANOI - Solucionador")
    print("🗼" * 25)
    print("\n1. Resolver recursivamente (con visualización)")
    print("2. Resolver iterativamente (con visualización)")
    print("3. Ver movimientos paso a paso")
    print("4. Ver historial completo de movimientos")
    print("5. Cambiar número de discos")
    print("6. Ver estadísticas del problema")
    print("0. Salir")
    return input("\n👉 Selecciona una opción: ")


def imprimir_movimientos(hanoi: TorresHanoi, paso_a_paso: bool = False):
    """Imprime el historial de movimientos."""
    if not hanoi.historial:
        print("⚠️ No hay movimientos registrados.")
        return
    
    print(f"\n📋 Historial de Movimientos ({len(hanoi.historial)} total):")
    print("-" * 50)
    
    for i, mov in enumerate(hanoi.historial, 1):
        print(mov)
        if paso_a_paso and i < len(hanoi.historial):
            input("⏸️ Presiona Enter para siguiente movimiento...")
            print(hanoi.visualizar())


def imprimir_estadisticas(n: int):
    """Muestra información teórica sobre el problema."""
    movimientos_minimos = (2 ** n) - 1
    tiempo_estimado_seg = movimientos_minimos * 0.5  # 0.5 seg por movimiento
    
    print(f"\n📊 Estadísticas para {n} discos:")
    print(f"• Movimientos mínimos requeridos: {movimientos_minimos:,}")
    print(f"• Complejidad temporal: O(2^{n})")
    print(f"• Complejidad espacial (recursivo): O({n})")
    print(f"• Tiempo estimado (0.5s/mov): {tiempo_estimado_seg/60:.2f} minutos")
    
    if n == 64:
        print("\n🌟 Dato curioso: Con 64 discos y 1 mov/segundo,")
        print("   se tardarían ~585 mil millones de años en resolverlo!")


def main():
    """Función principal del programa."""
    print("🎮 Iniciando Torres de Hanoi...")
    
    # Configuración inicial
    n_discos = 3
    hanoi = TorresHanoi(n_discos)
    
    while True:
        try:
            opcion = imprimir_menu()
            
            if opcion == "1":
                print(f"\n🔄 Resolviendo recursivamente {n_discos} discos...")
                hanoi.reiniciar()
                hanoi.resolver_recursivo()
                print(hanoi.visualizar())
                print(f"✅ ¡Resuelto en {hanoi.contador_movimientos} movimientos!")
                
            elif opcion == "2":
                print(f"\n🔄 Resolviendo iterativamente {n_discos} discos...")
                hanoi.reiniciar()
                hanoi.resolver_iterativo()
                print(hanoi.visualizar())
                print(f"✅ ¡Resuelto en {hanoi.contador_movimientos} movimientos!")
                
            elif opcion == "3":
                print(f"\n👣 Modo paso a paso para {n_discos} discos...")
                hanoi.reiniciar()
                hanoi.resolver_recursivo()
                imprimir_movimientos(hanoi, paso_a_paso=True)
                print(hanoi.visualizar())
                
            elif opcion == "4":
                imprimir_movimientos(hanoi, paso_a_paso=False)
                
            elif opcion == "5":
                try:
                    nuevo_n = int(input("\n🔢 Nuevo número de discos (1-20): "))
                    if 1 <= nuevo_n <= 20:
                        n_discos = nuevo_n
                        hanoi = TorresHanoi(n_discos)
                        print(f"✅ Configurado para {n_discos} discos.")
                    else:
                        print("❌ Número fuera de rango.")
                except ValueError:
                    print("❌ Entrada inválida. Debe ser un número.")
                    
            elif opcion == "6":
                imprimir_estadisticas(n_discos)
                
            elif opcion == "0":
                print("\n👋 ¡Gracias por usar Torres de Hanoi! Hasta pronto.")
                sys.exit()
                
            else:
                print("⚠️ Opción no válida. Intenta de nuevo.")
                
            input("\n⏸️ Presiona Enter para continuar...")
            
        except KeyboardInterrupt:
            print("\n\n⚠️ Ejecución interrumpida por el usuario.")
            sys.exit(1)
        except Exception as e:
            print(f"\n💥 Error inesperado: {type(e).__name__}: {e}")
            input("Presiona Enter para continuar...")


if __name__ == "__main__":
    main()