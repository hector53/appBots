import multiprocessing
import time

def enviar_mensaje(memoria_compartida, mensaje):
    with memoria_compartida.get_lock():
        memoria_compartida.value = mensaje

if __name__ == "__main__":
    asdas = multiprocessing.Array('c', b' ' * 1024, lock=True)

    while True:
        # Enviar mensaje a A
        mensaje_b_a = input("App B: ")
        enviar_mensaje(memoria_ab, mensaje_b_a.encode('utf-8'))

        time.sleep(1)  # Evitar el uso intensivo de la CPU
