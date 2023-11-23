import gc
from app import mongo, ObjectId
from app.models import DbUtils
from app import time, logging
import asyncio
import os
import json
from app.clases.botManager import botManager
from app.clases.class_logs import logsMain
log = logsMain("utilsController")


class UtilsController:
    @staticmethod
    async def iniciar_bot_ci_48_bb(botM: botManager, id_fix, id_bot, cuenta, symbols, opciones, soloEscucharMercado, fix):
        from app.clases.botManager.bots.bot_bb import botBB
        # en este punto sabemos que la sesion fix esta iniciada y todo bien
        # ahora tenemos que entrar al bot manager y iniciar este bot como tarea

        log.logInfo(
            f"id_fix : {id_fix}, id_bot: {id_bot}, symbols: {symbols}, opciones: {opciones}")
        log.logInfo(
            f"minRate: {opciones['minRate']}, maxRate: {opciones['maxRate']}, sizeMax: {opciones['sizeMax']}")
        log.logInfo(f"symbols: {symbols[0]}, {symbols[1]}")
        response = {"status": False}
        try:
            bot_bb = botBB(symbols[0], symbols[1], float(opciones["minRate"]), float(
                opciones["maxRate"]), fix, id_bot, cuenta, mongo)
            bot_bb.botData["sizeMax"] = int(opciones["sizeMax"])
            bot_bb.botData["type_side"] = int(opciones["type_side"])
            bot_bb.botData["market"] = opciones["market"]
            bot_bb.botData["maximizarGanancias"] = opciones["maximizarGanancias"]
            bot_bb.botData["periodoBB"] = opciones["periodoBB"]
            bot_bb.botData["soloEscucharMercado"] = soloEscucharMercado
            bot_bb.botData["ruedaA"]["sizeDisponible"] = int(
                opciones["sizeMax"])
            bot_bb.botData["ruedaB"]["sizeDisponible"] = int(
                opciones["sizeMax"])
            # agregar con el bot manager
            log.logInfo(f"botM: {botM}")
            log.logInfo(f"voy a iniciar la tarea en el botManager")
            taskBotManager = await botM.add_task(bot_bb)
            # response = UtilsController.esperar_bot_iniciado(id_fix, id_bot, cuenta)
            # await asyncio.sleep(4)
         #   if response["status"]==True:
            await asyncio.sleep(4)
            log.logInfo("el bot ha sido iniciado")
            # actualizar el status del bot
            status = 1
            if soloEscucharMercado == True:
                status = 2
            await DbUtils.update_bot_ejecutandose(id_bot, status)
            response = {"status": True, "statusBot": status}

        except Exception as e:
            response = {"status": False, "error": str(e)}
            log.logInfo(f"error: {str(e)}")
        return response

    async def iniciar_bot_ci_48(botM: botManager, id_fix, id_bot, cuenta, symbols, opciones, soloEscucharMercado, fix):
        from app.clases.botManager.bots.bot_ci_48 import botCi48
        # en este punto sabemos que la sesion fix esta iniciada y todo bien
        # ahora tenemos que entrar al bot manager y iniciar este bot como tarea
        log.logInfo(
            f"id_fix : {id_fix}, id_bot: {id_bot}, symbols: {symbols}, opciones: {opciones}")
        log.logInfo(
            f"minRate: {opciones['minRate']}, maxRate: {opciones['maxRate']}, sizeMax: {opciones['sizeMax']}")
        log.logInfo(f"symbols: {symbols[0]}, {symbols[1]}")
        response = {"status": False}
        try:
            bot_bb = botCi48(symbols[0], symbols[1], float(opciones["minRate"]), float(
                opciones["maxRate"]), fix, id_bot, cuenta, mongo)
            bot_bb.botData["sizeMax"] = int(opciones["sizeMax"])
            bot_bb.botData["soloEscucharMercado"] = soloEscucharMercado
            bot_bb.botData["market"] = opciones["market"]
            bot_bb.botData["maximizarGanancias"] = opciones["maximizarGanancias"]

            bot_bb.botData["ruedaA"]["sizeDisponible"] = int(
                opciones["sizeMax"])
            bot_bb.botData["ruedaB"]["sizeDisponible"] = int(
                opciones["sizeMax"])
            # agregar con el bot manager
            log.logInfo(f"botM: {botM}")
            log.logInfo(f"voy a iniciar la tarea en el botManager")
            taskBotManager = await botM.add_task(bot_bb)
            # response = UtilsController.esperar_bot_iniciado(id_fix, id_bot, cuenta)
            # await asyncio.sleep(4)
         #   if response["status"]==True:
            await asyncio.sleep(4)
            log.logInfo("el bot ha sido iniciado")
            # actualizar el status del bot
            status = 1
            if soloEscucharMercado == True:
                status = 2
            await DbUtils.update_bot_ejecutandose(id_bot, status)
            response = {"status": True, "statusBot": status}

        except Exception as e:
            response = {"status": False, "error": str(e)}
            log.logInfo(f"error: {str(e)}")
        return response

    async def iniciar_bot_ci_ci(botM: botManager, id_fix, id_bot, cuenta, symbols, opciones, soloEscucharMercado, fix):
        from app.clases.botManager.bots.bot_ci_ci import botCiCi
        # en este punto sabemos que la sesion fix esta iniciada y todo bien
        # ahora tenemos que entrar al bot manager y iniciar este bot como tarea

        log.logInfo(
            f"id_fix : {id_fix}, id_bot: {id_bot}, symbols: {symbols}, opciones: {opciones}")
        log.logInfo(
            f"minRate: {opciones['minRate']}, maxRate: {opciones['maxRate']}, sizeMax: {opciones['sizeMax']}")
        log.logInfo(f"symbols: {symbols[0]}, {symbols[1]}")
        response = {"status": False}
        try:
            bot = botCiCi(symbols[0], symbols[1], float(opciones["minRate"]), float(
                opciones["maxRate"]), fix, id_bot, cuenta, mongo)
            bot.botData["sizeMax"] = int(opciones["sizeMax"])
            bot.botData["type_side"] = int(opciones["type_side"])
            bot.botData["conBB"] = opciones["conBB"]
            bot.botData["market"] = opciones["market"]
            bot.botData["maximizarGanancias"] = opciones["maximizarGanancias"]
            bot.botData["porcentual"] = opciones["porcentual"]
            bot.botData["soloEscucharMercado"] = soloEscucharMercado
            bot.botData["ruedaA"]["sizeDisponible"] = int(
                opciones["sizeMax"])
            bot.botData["ruedaB"]["sizeDisponible"] = int(
                opciones["sizeMax"])
            # agregar con el bot manager
            log.logInfo(f"botM: {botM}")
            log.logInfo(f"voy a iniciar la tarea en el botManager")
            taskBotManager = await botM.add_task(bot)
            # response = UtilsController.esperar_bot_iniciado(id_fix, id_bot, cuenta)
            # await asyncio.sleep(4)
         #   if response["status"]==True:
            await asyncio.sleep(4)
            log.logInfo("el bot ha sido iniciado")
            # actualizar el status del bot
            status = 1
            if soloEscucharMercado == True:
                status = 2
            await DbUtils.update_bot_ejecutandose(id_bot, status)
            response = {"status": True, "statusBot": status}

        except Exception as e:
            response = {"status": False, "error": str(e)}
            log.logInfo(f"error: {str(e)}")
        return response

    async def iniciar_bot_triangulo(botM: botManager, id_fix, id_bot, cuenta, symbols, opciones, soloEscucharMercado, fix):
        from app.clases.botManager.bots.bot_triangulo import botTriangulo
        # en este punto sabemos que la sesion fix esta iniciada y todo bien
        # ahora tenemos que entrar al bot manager y iniciar este bot como tarea

        log.logInfo(
            f"id_fix : {id_fix}, id_bot: {id_bot}, symbols: {symbols}, opciones: {opciones}")

        response = {"status": False}
        try:
            bot = botTriangulo(
                symbols[0], symbols[1], symbols[2], fix, id_bot, cuenta, mongo)
            bot.botData["sizeMax"] = int(opciones["sizeMax"])
            bot.botData["soloEscucharMercado"] = soloEscucharMercado
            bot.botData["market"] = opciones["market"]
            bot.botData["ruedaA"]["sizeDisponible"] = int(
                opciones["sizeMax"])
            bot.botData["ruedaB"]["sizeDisponible"] = int(
                opciones["sizeMax"])
            # agregar con el bot manager
            log.logInfo(f"botM: {botM}")
            log.logInfo(f"voy a iniciar la tarea en el botManager")
            taskBotManager = await botM.add_task(bot)
            # response = UtilsController.esperar_bot_iniciado(id_fix, id_bot, cuenta)
            # await asyncio.sleep(4)
         #   if response["status"]==True:
            await asyncio.sleep(4)
            log.logInfo("el bot ha sido iniciado")
            # actualizar el status del bot
            status = 1
            if soloEscucharMercado == True:
                status = 2
            await DbUtils.update_bot_ejecutandose(id_bot, status)
            response = {"status": True, "statusBot": status}

        except Exception as e:
            response = {"status": False, "error": str(e)}
            log.logInfo(f"error: {str(e)}")
        return response

    def esperar_bot_iniciado(id_fix, id_bot, cuenta):
        response = {"status": False}
        try:
            inicio = time.time()  # inicio contador de tiempo de espera
            while True:
                if sesionesFix[id_fix].application.triangulos[cuenta][id_bot].botData["botIniciado"] != None:
                    if sesionesFix[id_fix].application.triangulos[cuenta][id_bot].botData["botIniciado"] == True:
                        response = {"status": True}
                        break
                    else:
                        break
                fin = time.time()
                tiempoEsperado = fin-inicio
                if tiempoEsperado > 30:  # si paso mas de 30 segundos, no llego la respuesta
                    response = {
                        "status": False, "msg": "tiempo excedido, no llego respuesta o algo mas paso"}
                    break
                time.sleep(0.1)
        except Exception as e:
            log.error(f"error en esperar_bot_iniciado: {e}")
        return response

    async def detener_bot_by_id_viejo(fix, id_bot):
        from app import fixM
        log.logInfo(f"entrando a detener bot byid: {id_bot} ")
        response = {"status": False}
        id_fix = fix["user"]
        cuenta = fix["account"]
        log.logInfo(f"fixM: {fixM}")
        getFixTask = await fixM.get_fixTask_by_id_user(id_fix)
        if getFixTask:
            log.logInfo(f"si existe a session: {id_fix}")
            try:

                if id_bot in getFixTask.botManager.main_tasks:
                    log.logInfo(f"borrar ordenes del bot")
                    log.logInfo(f"si existe a bot: {id_bot}")
                    # buscar en db las ordenes de este bot y cancelarlas
                    log.logInfo("pausar y detener cola del bot")
                    await getFixTask.botManager.main_tasks[id_bot].pause()
                    await getFixTask.botManager.main_tasks[id_bot].detenerBot()
                    ordenes = mongo.db.ordenes.find(
                        {"active": True, "id_bot": id_bot, "cuenta": cuenta}, {"_id": 0})

                    if ordenes:
                        ordenesBorrar = list(ordenes)
                        log.logInfo(f"ordenes: {ordenesBorrar}")
                        log.logInfo(f"hay {len(ordenesBorrar)} ordenes")
                        contadorOrdenesCanceladas = 0
                        tasks = []
                        for x in ordenesBorrar:
                            log.logInfo(f"borrar orden: {x}")
                            task = asyncio.create_task(UtilsController.cancelar_orden_async(
                                id_fix, id_bot, x["orderId"], x["clOrdId"], x["side"], x["leavesQty"], x["symbol"], cuenta))
                            tasks.append(task)
                        await asyncio.gather(*tasks)
                    #ahora quitar la suscripcion a mercado
                    #necesito los simbolos del bot 
                    symbolsBot = getFixTask.botManager.main_tasks[id_bot].botData["symbols2"]
                    log.logInfo(f"symbolsBot: {symbolsBot}")
                    symbolsToUnsus = []
                    #ahora verificar si existe en mainFIx en la variable de la suscripcion
                    log.logInfo(f"getFixTask.marketSymbolsSubs: {getFixTask.marketSymbolsSubs}")
                    for symbol in symbolsBot:
                        if symbol in getFixTask.marketSymbolsSubs:
                            #si existe entonces remover el id del bot 
                            getFixTask.marketSymbolsSubs[symbol].remove(id_bot)
                            if len(getFixTask.marketSymbolsSubs[symbol])==0: 
                                symbolsToUnsus.append(symbol)
                    log.logInfo(f"getFixTask.marketSymbolsSubs: {getFixTask.marketSymbolsSubs}")

                    if len(symbolsToUnsus)>0:
                        #enviar a unsuscribir los simbolos 
                        asyncio.create_task(getFixTask.botManager.main_tasks[id_bot].clientR.suscribir_mercado_off(symbolsToUnsus)) 
                    await getFixTask.botManager.stop_task_by_id(id_bot)
                    log.logInfo(
                        f"botManager Yasks: {getFixTask.botManager.tasks}")
                await DbUtils.update_status_bot_ejecuntadose(id_bot, 0)
                log.logInfo(f"fixM: {fixM}")
                response = {"status": True}
            except Exception as e:
                log.logInfo(
                    f"error en: {e}")
                response = {"status": False}
        else:
            log.logInfo(f"no existe la session")
            response = {"status": True}
        return response

    async def get_ordenes_by_id_bot(id_bot, cuenta):
        from app import redis_cliente as redis_client
        log.logInfo(f"entrando a get_ordenes_by_id_bot { id_bot, cuenta}")
        detalles_ordenes = []
        claves = [
                f"id_bot:{id_bot}",
                f"cuenta:{cuenta}",
                f"active:True"
            ]
        claves_interseccion = redis_client.sinter(*claves)
        for clave in claves_interseccion:
            log.logInfo(f"clave: {clave}")
            orden = redis_client.hgetall(clave)
            orden_decodificada = {campo.decode('utf-8'): valor.decode('utf-8') for campo, valor in orden.items()}
            orden_decodificada["price"] = float(orden_decodificada["price"])
            orden_decodificada["leavesQty"] = int(float(orden_decodificada["leavesQty"])) 
            orden_decodificada["cumQty"] = int(float(orden_decodificada["cumQty"]))
            orden_decodificada["orderQty"] = int(float(orden_decodificada["orderQty"]))
            orden_decodificada["lastQty"] = int(float(orden_decodificada["lastQty"]))
            orden_decodificada["clave"] = clave.decode('utf-8')
            detalles_ordenes.append(orden_decodificada)
        return detalles_ordenes
            

    async def detener_bot_by_id(fix, id_bot):
        from app import fixM
        log.logInfo(f"entrando a detener bot byid: {id_bot} ")
        response = {"status": False}
        id_fix = fix["user"]
        cuenta = fix["account"]
        log.logInfo(f"fixM: {fixM}")
        getFixTask = await fixM.get_fixTask_by_id_user(id_fix)
        if getFixTask:
            log.logInfo(f"si existe a session: {id_fix}")
            try:

                if id_bot in getFixTask.botManager.main_tasks:
                    log.logInfo(f"borrar ordenes del bot")
                    log.logInfo(f"si existe a bot: {id_bot}")
                    # buscar en db las ordenes de este bot y cancelarlas
                    log.logInfo("pausar y detener cola del bot")
                    await getFixTask.botManager.main_tasks[id_bot].pause()
                    await getFixTask.botManager.main_tasks[id_bot].detenerBot()
                    ordenes = await UtilsController.get_ordenes_by_id_bot(id_bot, cuenta)
                    log.logInfo(f"ordenes: {ordenes}")
                    if ordenes:
                        ordenesBorrar = ordenes
                        log.logInfo(f"ordenes: {ordenesBorrar}")
                        log.logInfo(f"hay {len(ordenesBorrar)} ordenes")
                        contadorOrdenesCanceladas = 0
                        tasks = []
                        for x in ordenesBorrar:
                            log.logInfo(f"borrar orden: {x}")
                            task = asyncio.create_task(UtilsController.cancelar_orden_async(
                                id_fix, id_bot, x["orderId"], x["clOrdId"], x["side"], x["leavesQty"], x["symbol"], cuenta))
                            tasks.append(task)
                        await asyncio.gather(*tasks)
                    #ahora quitar la suscripcion a mercado
                    #necesito los simbolos del bot 
                    symbolsBot = getFixTask.botManager.main_tasks[id_bot].botData["symbols2"]
                    log.logInfo(f"symbolsBot: {symbolsBot}")
                    symbolsToUnsus = []
                    #ahora verificar si existe en mainFIx en la variable de la suscripcion
                    log.logInfo(f"getFixTask.marketSymbolsSubs: {getFixTask.marketSymbolsSubs}")
                    for symbol in symbolsBot:
                        if symbol in getFixTask.marketSymbolsSubs:
                            #si existe entonces remover el id del bot 
                            getFixTask.marketSymbolsSubs[symbol].remove(id_bot)
                            if len(getFixTask.marketSymbolsSubs[symbol])==0: 
                                symbolsToUnsus.append(symbol)
                    log.logInfo(f"getFixTask.marketSymbolsSubs: {getFixTask.marketSymbolsSubs}")

                    if len(symbolsToUnsus)>0:
                        #enviar a unsuscribir los simbolos 
                        asyncio.create_task(getFixTask.botManager.main_tasks[id_bot].clientR.suscribir_mercado_off(symbolsToUnsus)) 
                    await getFixTask.botManager.stop_task_by_id(id_bot)
                    log.logInfo(
                        f"botManager Yasks: {getFixTask.botManager.tasks}")
                await DbUtils.update_status_bot_ejecuntadose(id_bot, 0)
                log.logInfo(f"fixM: {fixM}")
                response = {"status": True}
            except Exception as e:
                log.logInfo(
                    f"error en: {e}")
                response = {"status": False}
        else:
            log.logInfo(f"no existe la session")
            response = {"status": True}
        return response


    async def editar_bot_triangulo(id_bot, fix, opciones):
        from app import fixM
        response = {"status": False}
        id_fix = fix["user"]
        cuenta = fix["account"]
        try:
            if id_fix in fixM.main_tasks and id_bot in fixM.main_tasks[id_fix].botManager.main_tasks:
                fixM.main_tasks[id_fix].botManager.main_tasks[id_bot].botData["varGan"] = int(
                    opciones["spreadMin"])
                fixM.main_tasks[id_fix].botManager.main_tasks[id_bot].botData["sizeMax"] = int(opciones["sizeMax"])
                fixM.main_tasks[id_fix].botManager.main_tasks[id_bot].botData["market"] = opciones["market"]
                task = {"type": 0}
                await fixM.main_tasks[id_fix].botManager.main_tasks[id_bot].add_task(task)
            # ahora guardar los datos en db
            result = mongo.db.bots_ejecutandose.update_one(
                {'_id': ObjectId(id_bot)}, {'$set': {'opciones': opciones}})
            response = {"status": True}

        except Exception as e:
            response = {"status": False, "error": str(e)}
            log.error(f"error: {str(e)}")
        return response
    
    async def editar_bot_ci_48(id_bot, fix, opciones):
        from app import fixM
        response = {"status": False}
        id_fix = fix["user"]
        cuenta = fix["account"]
        try:
            if id_fix in fixM.main_tasks and id_bot in fixM.main_tasks[id_fix].botManager.main_tasks:
                fixM.main_tasks[id_fix].botManager.main_tasks[id_bot].minimum_arbitrage_rate = float(
                    opciones["minRate"])
                fixM.main_tasks[id_fix].botManager.main_tasks[id_bot].maximum_arbitrage_rate = float(
                    opciones["maxRate"])
                fixM.main_tasks[id_fix].botManager.main_tasks[id_bot].botData["type_side"] = int(
                    opciones["type_side"])
                fixM.main_tasks[id_fix].botManager.main_tasks[id_bot].botData["periodoBB"] = opciones["periodoBB"]

                fixM.main_tasks[id_fix].botManager.main_tasks[id_bot].botData["market"] = opciones["market"]

                fixM.main_tasks[id_fix].botManager.main_tasks[id_bot].botData["maximizarGanancias"] = opciones["maximizarGanancias"]

                task = {"type": 0}
                await fixM.main_tasks[id_fix].botManager.main_tasks[id_bot].add_task(task)
            # ahora guardar los datos en db
            result = mongo.db.bots_ejecutandose.update_one(
                {'_id': ObjectId(id_bot)}, {'$set': {'opciones': opciones}})
            response = {"status": True}

        except Exception as e:
            response = {"status": False, "error": str(e)}
            log.error(f"error: {str(e)}")
        return response

    async def editar_bot_ci_ci(id_bot, fix, opciones):
        from app import fixM
        response = {"status": False}
        id_fix = fix["user"]
        cuenta = fix["account"]
        try:
            if id_fix in fixM.main_tasks and id_bot in fixM.main_tasks[id_fix].botManager.main_tasks:
                fixM.main_tasks[id_fix].botManager.main_tasks[id_bot].minimum_arbitrage_rate = float(
                    opciones["minRate"])
                fixM.main_tasks[id_fix].botManager.main_tasks[id_bot].maximum_arbitrage_rate = float(
                    opciones["maxRate"])
                fixM.main_tasks[id_fix].botManager.main_tasks[id_bot].botData["type_side"] = int(
                    opciones["type_side"])
                fixM.main_tasks[id_fix].botManager.main_tasks[id_bot].botData["periodoBB"] = opciones["periodoBB"]

                fixM.main_tasks[id_fix].botManager.main_tasks[id_bot].botData["market"] = opciones["market"]
                fixM.main_tasks[id_fix].botManager.main_tasks[id_bot].botData["maximizarGanancias"] = opciones["maximizarGanancias"]

                task = {"type": 0}
                await fixM.main_tasks[id_fix].botManager.main_tasks[id_bot].add_task(task)
            # ahora guardar los datos en db
            result = mongo.db.bots_ejecutandose.update_one(
                {'_id': ObjectId(id_bot)}, {'$set': {'opciones': opciones}})
            response = {"status": True}

        except Exception as e:
            response = {"status": False, "error": str(e)}
            log.error(f"error: {str(e)}")
        return response

    async def editar_bot_ci_48_bb(id_bot, fix, opciones):
        from app import fixM
        response = {"status": False}
        id_fix = fix["user"]
        cuenta = fix["account"]
        try:
            if id_fix in fixM.main_tasks and id_bot in fixM.main_tasks[id_fix].botManager.main_tasks:
                fixM.main_tasks[id_fix].botManager.main_tasks[id_bot].minimum_arbitrage_rate = float(
                    opciones["minRate"])
                fixM.main_tasks[id_fix].botManager.main_tasks[id_bot].maximum_arbitrage_rate = float(
                    opciones["maxRate"])
                fixM.main_tasks[id_fix].botManager.main_tasks[id_bot].botData["type_side"] = int(
                    opciones["type_side"])
                fixM.main_tasks[id_fix].botManager.main_tasks[id_bot].botData["periodoBB"] = opciones["periodoBB"]

                fixM.main_tasks[id_fix].botManager.main_tasks[id_bot].botData["market"] = opciones["market"]
                fixM.main_tasks[id_fix].botManager.main_tasks[id_bot].botData["maximizarGanancias"] = opciones["maximizarGanancias"]


                fixM.main_tasks[id_fix].botManager.main_tasks[id_bot].botData["editandoBot"] = True
                task = {"type": 0}
                await fixM.main_tasks[id_fix].botManager.main_tasks[id_bot].add_task(task)
            # ahora guardar los datos en db
            result = mongo.db.bots_ejecutandose.update_one(
                {'_id': ObjectId(id_bot)}, {'$set': {'opciones': opciones}})
            response = {"status": True}

        except Exception as e:
            response = {"status": False, "error": str(e)}
            log.error(f"error: {str(e)}")
        return response

    def get_tenencias_bot(posiciones):
        log.logInfo(f"entrando a get tenencias bot: {posiciones}")
        arrayTenencias = []
        try:
            for x in posiciones:
                log.logInfo(f"tenencia: {posiciones[x]}")
                symbol = x
                tenencia = int(posiciones[x]["BI"]) - int(posiciones[x]["OF"])
                objTenencia = {
                    "symbol": symbol,
                    "tenencia": tenencia
                }
                arrayTenencias.append(objTenencia)
        except Exception as e:
            log.error(f"error en get tenencias bot: {e}")
        return arrayTenencias

    async def cancelar_orden_async(id_fix, id_bot, orderID, OrigClOrdID, side, quantity, symbol, cuenta):
        from app import fixM
        log.logInfo("entrando a cancelar orden async")
        response = {"llegoRespuesta": False}
        try:
            sideFix = 1
            if side == "Sell":
                sideFix = 2
            response = await fixM.main_tasks[id_fix].botManager.main_tasks[id_bot].clientR.cancelar_orden(
                orderID, OrigClOrdID, sideFix, quantity, symbol)
        except Exception as e:
            log.error(f"error en cancelar_orden_async: {e}")
        return response

    def guardar_security_in_fix(data, id_fix):
        from app import fixM
        for x in data:
            fixM.main_tasks[id_fix].application.securitysList[x["symbol"]] = x
        return True

    def fetch_securitys_data(id_fix):
        from app import fixM
        log.logInfo("fetch_securitys_data")
        lista = fixM.main_tasks[id_fix].application.securitysList
        arraySecuritys = []
        for x in lista:
            arraySecuritys.append(lista[x])
        log.logInfo(f"lista de securitys {len(arraySecuritys)} ")
        for security in arraySecuritys:
            securityDesc = security['securityDesc']
            securityDescUnicode = securityDesc.encode(
                'ascii', 'ignore').decode('utf-8')
            security['securityDesc'] = securityDescUnicode

        return arraySecuritys

    def get_precios_bonos():
        ruta_archivo = os.path.join(os.getcwd(), "app/dataJson/precios.json")
        with open(ruta_archivo) as archivo:
            json_data = json.load(archivo)
        return json_data
