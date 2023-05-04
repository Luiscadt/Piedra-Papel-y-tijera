## Piedra, papel y tijera

from pickletools import read_decimalnl_long
import random

def jugar():
    usuario = input("Escoge una opcion 'pi' para pidera 'pa' para papel 'ti' para tijera: ").lower()

    validate = validar_usuario(usuario)
    
    while validate == False:
        usuario = input("Escoge una opcion valida por favor 'pi' para pidera 'pa' para papel 'ti' para tijera: ").lower()
        validate = validar_usuario(usuario)
        
    computadora = random.choice(['pi', 'pa', 'ti'])
    
    if usuario == computadora:
        return '¡Empate!'
    elif gano_el_jugador(usuario, computadora):
        return "¡Ganates!"

    return "Perdiste"

def gano_el_jugador(jugador, oponente):
    if(
        (jugador == 'pi' and oponente == 'ti')
        or (jugador == 'ti' and oponente == 'pa')
        or (jugador == 'pa' and oponente == 'pi')
    ):
        return True
    else:
        return False
    

def validar_usuario(respuesta):
    if (
        (respuesta == 'pi')
        or (respuesta == 'pa')
        or (respuesta == 'ti')
        ):
            return True
    else:
        return False
        
        
    
print(jugar())