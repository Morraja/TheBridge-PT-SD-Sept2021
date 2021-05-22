"""
Funcion principal que pide al usuario la eleccion de piedra,papel o tijera, genera
automaticamente la eleccion del ordenador y pregunta en la otra parte para saber el resultado 
"""
import random

import Comprueba

if __name__ == '__main__':
    fin = False
    while fin == False:
        print("Bienvenido al juego: PIEDRA, PAPEL O TIJERA")
        Ordenador = random.choice(["piedra", "papel", "tijera"])
        Tu = input("Que eliges: Piedra, Papel o Tijera: ")
        Tu = Tu.lower()
        while Tu != ("piedra") and Tu != ("papel") and Tu != ("tijera"):
            Tu = input("Solo vale \'piedra\',\'papel\' o \'tijera\': ")
            Tu = Tu.lower()
        print("Tu:", Tu.upper())
        print("Ordenador:", Ordenador.upper())

        Resultado = Comprueba.comprueba_resultado(Tu,Ordenador)
        if Resultado[0]:
            print("Seguimos jugando para desempatar")
        else:
            print(f"{Resultado[1]}")
            fin = True
            break


