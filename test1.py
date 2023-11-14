import traceback
def es_orden_mia( orden, futuro, side, type_order="NEW", orderBot=0):
    from app import redis_cliente as redis_client
    response = {"status": False}
    id_bot = "654d66878b26b58cf6bb1664"
    sideDb = "Buy" 
    cuenta = "REM7654"
    try:
        sideDb = "Buy" if side == "OF" else "Sell"
        parametros = {
            "price": orden["price"],
            "leavesQty": orden["size"],
            "symbol": futuro,
            "side": "Buy",
            "ordStatus": type_order,
            "id_bot": id_bot,
            "cuenta": cuenta
        }

        claves = [
            f"symbol:{futuro}",
            f"id_bot:{id_bot}",
            f"ordStatus:{type_order}",
            f"side:{sideDb}",
            f"cuenta:{cuenta}",
            f"active:True"
        ]
        
        # Usar SINTER para obtener la intersección directamente
        claves_interseccion = redis_client.sinter(*claves)

        detalles_ordenes = []
        for clave in claves_interseccion:
            orden = redis_client.hgetall(clave)
            orden_decodificada = {campo.decode('utf-8'): valor.decode('utf-8') for campo, valor in orden.items()}
            orden_decodificada["clave"] = clave.decode('utf-8')
            detalles_ordenes.append(orden_decodificada)

        if detalles_ordenes:
            response = {"status": True, "orden": detalles_ordenes[0]}
    except Exception as e:
        print(f"error en es_orden_mia: {e}")
        traceback.print_exc()
    return response

def update_order(claveRedis, orden):
    from app import redis_cliente as redis_client
    response = {"status": False}
    try:
        redis_client.hset(claveRedis, mapping=orden)
        response = {"status": True}
    except Exception as e:
        print(f"error en update_order: {e}")
        traceback.print_exc()
    return response

orden = {"price": 240.1, "size": "1.0"}
futuro = "TRI.ROS/DIC23"
side = "OF"
type_order = "NEW"
orderBot = 0

print(es_orden_mia(orden, futuro, side, type_order, orderBot))
update_order("orden:20231113153215452990", {"active": "True"})
print(es_orden_mia(orden, futuro, side, type_order, orderBot))
