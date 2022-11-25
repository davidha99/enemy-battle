import sys
import numpy as np
import random

def imprimir_mensaje_ayuda():
    print("Para ejecutar el programa:")
    print("\npython3 main.py [OPCIÓN]")
    print("\nOpciones:")
    print("\t-r: correr el programa con valores aleatorios.")
    print("\t-m: correr el programa ingresando valores manualmente.")

def configurar_matriz(n: int):
    matriz = np.zeros((n,n))
    for i in range(n):
        probabilidad = 100
        for j in range(n):
            if i == j:
                matriz[i][j] = 0
            elif j == n-1 or (i == n-1 and j == n-2):
                matriz[i][j] = probabilidad / 100
            else:
                sig_probabilidad = random.randint(1, probabilidad) if probabilidad != 0 else 0
                matriz[i][j] = sig_probabilidad / 100
                probabilidad -= sig_probabilidad
    return matriz


if __name__ == "__main__":
    try:
        if sys.argv[1] == "-m":
            # Pasar los datos manualmente
            pass
        elif sys.argv[1] == "-r":
            # Generar valores aleatorios
            n_grupos = np.random.randint(2, 10)
            matriz = configurar_matriz(n=n_grupos)
            print(matriz)

        elif sys.argv[1] == "-h":
            # Imprimir mensaje de ayuda
            imprimir_mensaje_ayuda()
        else:
            imprimir_mensaje_ayuda()
    except IndexError:
        imprimir_mensaje_ayuda()