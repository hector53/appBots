import redis
import time
import datetime
def enviar_mensaje(cliente_redis, mensaje):
    cliente_redis.publish('canal_compartido', mensaje)

if __name__ == "__main__":
    cliente_redis = redis.StrictRedis(host='localhost', port=6379, db=0)

    while True:
        # Enviar mensaje a A
        mensaje_b_a = input("App B: ")
        
        print("antes de enviar msg: ",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
        enviar_mensaje(cliente_redis, mensaje_b_a)
        print("despues de enviado: ", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
