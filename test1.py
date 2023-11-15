def get_order_limit_by_symbol_side( symbol, side, ordStatus="NEW", ordenBot=0):
        from app import redis_cliente as redis_client
        print("entrando a get_order_limit_by_symbol_side")
        try:
            id_bot = "654d66878b26b58cf6bb1664"
            cuenta = "REM7654"
            print(f"symbol: {symbol}, side: {side}")
            claves = [
            f"symbol:{symbol}",
            f"id_bot:{id_bot}",
            f"side:{side}",
            f"cuenta:{cuenta}",
            f"active:True"
            ]
            # Usar SINTER para obtener la intersección directamente
            claves_interseccion = redis_client.sinter(*claves)
            print("claves interseccion", claves_interseccion)

            # Obtener detalles de órdenes a partir de las claves obtenidas
            detalles_ordenes =[]
            for clave in claves_interseccion:
                orden = redis_client.hgetall(clave)
                orden_decodificada = {campo.decode('utf-8'): valor.decode('utf-8') for campo, valor in orden.items()}
                print(f"orden_decodificada: {orden_decodificada}")
                #convertir campos a float
                orden_decodificada["price"] = float(orden_decodificada["price"])
                orden_decodificada["leavesQty"] = int(float(orden_decodificada["leavesQty"])) 
                orden_decodificada["cumQty"] = int(float(orden_decodificada["cumQty"]))
                orden_decodificada["orderQty"] = int(float(orden_decodificada["orderQty"]))
                orden_decodificada["lastQty"] = int(float(orden_decodificada["lastQty"]))
                orden_decodificada["clave"] = clave.decode('utf-8')

                if  orden_decodificada["leavesQty"]  > 0:
                    detalles_ordenes.append(orden_decodificada)

            if len(detalles_ordenes) > 0:
              #  self.log.info("si existe la orden")
               # self.log.info(f"la orden es esta: {detalles_ordenes}")
                return {"status": True, "data": detalles_ordenes[0]}
            else:
              #  self.log.info("no existe orden con esos parametros ")
                return {"status": False, "msg": "no hay orden limit con esos parametros"}
        except Exception as e:
            print(f"error en get_order_limit_by_symbol_side: {e} ")
            return {"status": False}
        
getOrdenes = get_order_limit_by_symbol_side("TRI.ROS/DIC23", "Buy")
print(getOrdenes)