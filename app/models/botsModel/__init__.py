from app import mongo
from bson import json_util
import logging
import traceback
log = logging.getLogger(__name__)

class BotsModel:
    @staticmethod
    def get_ordenes_bot_fecha(id_bot, cuenta, fecha):
        from app import redis_cliente as redis_client
        log.info("entrando a get_ordenes_bot_fecha")
        try:
            clave_id_bot = f"id_bot:{id_bot}"
            clave_cuenta = f"cuenta:{cuenta}"
            # Obtener claves para órdenes que cumplen con las condiciones
            claves_id_bot = redis_client.smembers(clave_id_bot)
            claves_cuenta = redis_client.smembers(clave_cuenta)

            # Calcular la intersección de claves que cumplen con todas las condiciones
            claves_interseccion = ( claves_cuenta &   claves_id_bot  )

            # Obtener detalles de órdenes a partir de las claves obtenidas
            detalles_ordenes =[]
            for clave in claves_interseccion:
                orden = redis_client.hgetall(clave)
                orden_decodificada = {campo.decode('utf-8'): valor.decode('utf-8') for campo, valor in orden.items()}
               # log.info(f"orden_decodificada: {orden_decodificada}")
                #convertir campos a float
                orden_decodificada["price"] = float(orden_decodificada["price"])
                orden_decodificada["leavesQty"] = int(float(orden_decodificada["leavesQty"])) 
                orden_decodificada["cumQty"] = int(float(orden_decodificada["cumQty"]))
                orden_decodificada["orderQty"] = int(float(orden_decodificada["orderQty"]))
                orden_decodificada["lastQty"] = int(float(orden_decodificada["lastQty"]))
                orden_decodificada["active"] = True if orden_decodificada["active"] == "True" else False

                if  fecha in orden_decodificada["transactTime"]:
                    detalles_ordenes.append(orden_decodificada)

            if len(detalles_ordenes) > 0:
                return detalles_ordenes
            else:
                log.info("no existe orden con esos parametros ")
                return []
        except Exception as e:
            log.error(f"error en get_ordenes_bot_fecha {e}")
            log.error(f"traceback: {traceback.format_exc()}")
            return []

    def get_all(id_user, fix):
        user_fix = fix["user"]
        cuenta = fix["account"]
        arrayBots=[]
        try:
            print("consultando ")
            count = mongo.db.bots.count_documents({})
            print("len bots", count)
            if count>0:
                bots = mongo.db.bots.find({"id_user": id_user})
                for doc in bots:
                    doc['_id'] = str(doc['_id'])
                    #ahora quiero el listado no, el status del bot que debe estar ejecutandose siempre y cuando haya uno
                    ejecutandose = mongo.db.bots_ejecutandose.find_one({"id_bot": doc['_id'], 
                                                                        "user_fix": user_fix, 
                                                                        "cuenta":cuenta
                                                                        })
                    if ejecutandose: 
                        print("si tiene documentos ")
                        doc["status"] = ejecutandose["status"]
                        doc["id_ejecutandose"] = str(ejecutandose["_id"])
                    else: 
                        doc['status'] = 0
                    arrayBots.append(doc)
                response = {"arrayBots": arrayBots, "status": True}
            else:
                response = {"arrayBots": arrayBots, "status": False}
        except Exception as e: 
            print("error ", e)
            response = {"arrayBots": arrayBots, "status": False, "msg": e}
        return response
    
    

