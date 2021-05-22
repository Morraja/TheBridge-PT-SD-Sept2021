"""
Este es el modulo que comprueba si has ganado o perdido o empatado.
Devuelve lo que hay que hacer, imprimir el resultado y terminar o empatar y seguir jugando
"""
def comprueba_resultado(Tu,Ordenador):
    if Tu != Ordenador:
        if Tu == ("papel") and Ordenador == ("tijera"):
            Mensaje="PERDISTE: Las tijeras cortan el papel"
        if Tu == ("papel") and Ordenador == ("piedra"):
            Mensaje="GANASTE: El papel envuelve la piedra"
        if Tu == ("piedra") and Ordenador == ("papel"):
            Mensaje="PERDISTE: El papel envuelve la piedra"
        if Tu == ("piedra") and Ordenador == ("tijera"):
            Mensaje="GANASTE: La piedra machaca las tijeras"
        if Tu == ("tijera") and Ordenador == ("piedra"):
            Mensaje="PERDISTE: La piedra machaca las tijeras"
        if Tu == ("tijera") and Ordenador == ("papel"):
            Mensaje="GANASTE: Las tijeras cortan el papel"
        fin = False
        return fin, Mensaje
    else:
        Mensaje="EMPATE"
        fin = True
        return fin,Mensaje