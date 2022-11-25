# El siguiente programa simula una batalla de Grupos Guerreros usando Cadenas de Markov.
# Para correr el programa:
#   python3 main.py [-m | -r | -h]
#       Opciones:
#           -m: Correr el programa ingresando los datos manuales.
#           -r: Correr el programa con valores aleatorios generados por el programa.
#           -h: Mostrar el mensaje de ayuda.
# Para ambas opciones, el usuario tiene que especificar el # de grupos.
#
# Omar David Hernández Aguirre      |       A01383543
# Tec de Monterrey
# 25 de noviembre de 2022


import sys
import numpy as np
import pandas as pd
import random


def imprimir_mensaje_ayuda():
    print("Para ejecutar el programa:")
    print("\npython3 main.py [OPCIÓN]")
    print("\nOpciones:")
    print("\t-r: correr el programa con valores aleatorios.")
    print("\t-m: correr el programa ingresando valores manualmente.")


def configurar_matriz(vivos: dict):
    lista_vivos = [k for k in vivos if vivos[k] == True]
    n = len(lista_vivos)
    restantes = n-1
    matriz = np.zeros((n, n))
    for i in range(n):
        probabilidad = 100
        for j in range(n):
            try:
                reparticion = probabilidad // (restantes)
                restantes -= 1
            except ZeroDivisionError:
                reparticion = probabilidad
            if i == j:
                matriz[i][j] = 0
            elif j == n-1 or (i == n-1 and j == n-2):
                matriz[i][j] = probabilidad / 100
            else:
                sig_probabilidad = random.randint(
                    1, reparticion) if probabilidad != 0 else 0
                matriz[i][j] = sig_probabilidad / 100
                probabilidad -= sig_probabilidad
    df = pd.DataFrame(matriz)
    df = df.set_axis(lista_vivos, axis=0)
    df = df.set_axis(lista_vivos, axis=1)
    return df


def escribir_matriz_en_archivo(m: pd.DataFrame, vivos: dict):
    lista_vivos = [k for k in vivos if vivos[k] == True]
    with open(archivo, "a") as f:
        f.write(m.to_string(columns=lista_vivos))


def crear_guerreros(n: int):
    grupos = []
    for _ in range(n):
        n_guerreros = random.randint(40, 60)
        # n_guerreros = random.randint(3,5)
        grupos.append(n_guerreros)
    return grupos


def checar_eliminados(g: list, a: list):
    for i in range(len(g)):
        if (g[i] == 0) and (i+1 not in a):
            return True
    return False


def calcular_siguiente_atacante(grupos, aniquilados):
    posibles = []
    for i in range(len(grupos)):
        if i+1 not in aniquilados:
            posibles.append(i+1)
    n = len(posibles)
    idx = random.randint(0, n-1)
    return posibles[idx]


def calcular_siguiente_atacado(atacante, probabilidades, vivos):
    # Crear lista de 100, y distribuir la probabilidad del atacado con el número de veces
    # en las que va a aparacer en la lista. Por ejemplo, si la probabilidad de un atacado
    # es de .50 entonces aparacerá 50 veces en la lista.
    lista_vivos = [k for k in vivos if vivos[k] == True]
    posibles_grupos_atacados = []

    for grupo in lista_vivos:
        if grupo == atacante:
            continue
        else:
            probabilidad = probabilidades[grupo][atacante]
            n_veces = int(probabilidad * 100)
            posibles_grupos_atacados += [grupo for _ in range(n_veces)]

    idx = random.randint(0, len(posibles_grupos_atacados)-1)

    return posibles_grupos_atacados[idx]


def escribir_mensaje_estado_actual(g: list, a: list):
    with open(archivo, "a") as f:
        f.write("\n\nNumber of warriors for each group")
        for i in range(len(g)):
            if i+1 not in a:
                f.write(f"\nGroup {i+1}: {g[i]}")
        f.write("\n==================================\n\n")


def escribir_mensaje_de_ataque(atacante, atacado):
    with open(archivo, "a") as f:
        f.write(f"\nGroup {atacante} attacked Group {atacado}!\n")


def escribir_mensaje_aniquilacion(grupo):
    with open(archivo, "a") as f:
        f.write(f"\nGroup {grupo} is annihilated!")
        f.write("\n\n==================================\n")


def escribir_mensaje_reconfiguracion():
    with open(archivo, "a") as f:
        f.write("\nReconfiguring stochastic matrix\n\n")


def escribir_mensaje_ganador(ganador):
    with open(archivo, "a") as f:
        f.write("\n\n==================================\n")
        f.write(f"Group {ganador} is the winner!")
        f.write("\n==================================\n")


def limpiar_archivo_resultados():
    open(archivo, 'w').close()


def agregar_grupo_a_lista_de_aniquilados(grupos: list, aniquilados: list):
    # Encuentra el grupo que tiene 0 guerreros y que todavía no esté
    # en la lista de aniquilados
    for i in range(len(grupos)):
        if (grupos[i] == 0) and (i+1 not in aniquilados):
            aniquilados.append(i+1)
    return aniquilados


def obtener_ganador(grupos: list):
    for i in range(len(grupos)):
        if grupos[i] != 0:
            return i + 1


def configurar_matriz_manual(vivos: dict):
    lista_vivos = [k for k in vivos if vivos[k] == True]
    n = len(lista_vivos)
    matriz = np.zeros((n, n))

    i = 0
    j = 0

    while i < n:
        atacante = lista_vivos[i]
        acumulador = 0
        while j < n:
            atacado = lista_vivos[j]
            if atacante == atacado:
                matriz[i][j] = 0.0
                j += 1
            else:
                try:
                    probabilidad = int(
                        input(f"Probabilidad (1-100) para el ataque [{atacante}][{atacado}]: "))
                    acumulador += probabilidad
                    matriz[i][j] = probabilidad / 100
                    j += 1
                except ValueError:
                    print(
                        "Las probabilidades deben ser números en el rango de 1-100. Intente de nuevo.")
                    j -= 1
        if acumulador == 100:
            j = 0
            i += 1
        else:
            print("La suma de las probabilidades debe dar 100. Intente de nuevo.")
            j = 0

    df = pd.DataFrame(matriz)
    df = df.set_axis(lista_vivos, axis=0)
    df = df.set_axis(lista_vivos, axis=1)
    return df


def crear_guerreros_manuales(n: int):
    i = 0
    grupos = []
    while i < n:
        try:
            n_guerreros = int(input(f"# of warriors for Group {i+1}: "))
            i += 1
            grupos.append(n_guerreros)
        except ValueError:
            print("# of warrios must be an integer value > 0. Try again.")
    return grupos


if __name__ == "__main__":

    manual = False
    archivo = "resultados/resultados.txt"

    if len(sys.argv) == 2:
        if sys.argv[1] == "-m":
            manual = True
            limpiar_archivo_resultados()
            n_grupos = int(input("# of groups: "))
            grupos_vivos = {i+1: True for i in range(n_grupos)}
            matriz = configurar_matriz_manual(vivos=grupos_vivos)
            grupos = crear_guerreros_manuales(n=n_grupos)
        elif sys.argv[1] == "-r":
            limpiar_archivo_resultados()
            # Generar valores aleatorios
            n_grupos = int(input("# of groups: "))
            grupos_vivos = {i+1: True for i in range(n_grupos)}
            matriz = configurar_matriz(vivos=grupos_vivos)
            grupos = crear_guerreros(n=n_grupos)
        elif sys.argv[1] == "-h":
            # Imprimir mensaje de ayuda
            imprimir_mensaje_ayuda()
            exit()
        else:
            imprimir_mensaje_ayuda()
            exit()
    else:
        imprimir_mensaje_ayuda()
        exit()

    # Para comprobar matriz estocastica
    # print(matriz.sum(1))

    hay_ganador = False
    aniquilados = []
    escribir_matriz_en_archivo(m=matriz, vivos=grupos_vivos)

    while (not hay_ganador):
        escribir_mensaje_estado_actual(g=grupos, a=aniquilados)
        sig_atacante = calcular_siguiente_atacante(
            grupos=grupos, aniquilados=aniquilados)
        sig_atacado = calcular_siguiente_atacado(
            atacante=sig_atacante, probabilidades=matriz, vivos=grupos_vivos)
        grupos[sig_atacado-1] -= 1
        escribir_mensaje_de_ataque(atacante=sig_atacante, atacado=sig_atacado)
        hay_grupo_aniquilado = checar_eliminados(g=grupos, a=aniquilados)

        if hay_grupo_aniquilado:
            n_grupos -= 1
            aniquilados = agregar_grupo_a_lista_de_aniquilados(
                grupos=grupos, aniquilados=aniquilados)
            aniquilado = aniquilados[-1]
            escribir_mensaje_aniquilacion(grupo=aniquilado)
            grupos_vivos[aniquilado] = False
            if n_grupos == 1:
                hay_ganador = True
                break
            escribir_mensaje_reconfiguracion()
            if manual:
                matriz = configurar_matriz_manual(vivos=grupos_vivos)
            else:
                matriz = configurar_matriz(vivos=grupos_vivos)
            escribir_matriz_en_archivo(m=matriz, vivos=grupos_vivos)

    ganador = obtener_ganador(grupos=grupos)
    escribir_mensaje_ganador(ganador=ganador)
