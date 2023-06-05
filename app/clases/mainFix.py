import asyncio
import logging
import websocket
from threading import Thread
from app.clases.socketClient import clientSocket
from app.clases.botManager import botManager
import datetime
import json
from app.clases.class_cola import Cola
#class main para quickfix 
class MainFix():
    def __init__(self,  user,  account,  accountFixId, puertows):
        self.user = user
        self.account = account
        self.accountFixId = accountFixId
        self.port = puertows
        self.threadFix = None
        self.threadCola = None
        self.message_queue = Cola()
        self.stopCola = asyncio.Event()
        #server Broadcaster
        self.log = logging.getLogger("MainFix")
        self.taskToCancel = None
        self.balance = {}
        self.OrdersIds = {}
        self.botManager = botManager()
        self.marketSymbolsSubs = {}
        self.clOrdIdEsperar = {}
        self.ws = websocket.WebSocketApp(f"ws://127.0.0.1:{self.port}",
                              on_open=self.on_open,
                              on_message=self.on_message,
                              on_error=self.on_error,
                              on_close=self.on_close)
    
    def run_client_socket(self):
        self.ws.run_forever(reconnect=5)

    async def run(self):
        try:
            self.threadFix = Thread(target=self.run_client_socket)
            self.threadFix.start()
            #necesito otra tarea para 
            self.threadCola = Thread(target=self.startCola)
            self.threadCola.start()
        finally:
            self.log.error("se cerro el run d ela tarea main fix")

    def startCola(self):
        loop3 = asyncio.new_event_loop()# creo un nuevo evento para asyncio y asi ejecutar todo de aqui en adelante con async await 
        asyncio.set_event_loop(loop3)
        loop3.run_until_complete(self.run_forever())#ejecuto la funcion q quiero
        loop3.close()

    async def run_forever(self):
        #self.log.info(f"estoy en el ciclo start")
        try:
            while not self.stopCola.is_set():
             #   #self.log.info("ciclo infinito")
                task = await self.message_queue.obtener_tarea()
                if task is not None:
                    await self.message_queue.marcar_completada(task)
                    asyncio.create_task(self.process_message(task))
                await asyncio.sleep(0.01)
        except Exception as e:
            # Manejar la excepción adecuadamente
            self.log.error(f"Se ha producido una excepción: {e}")
        finally: 
            self.log.error(f"se cerro el ciclo de cola en main task")

    def on_message(self, ws, message):
        timeA = datetime.datetime.now()
        self.log.info(f"mensaje del puerto: {self.port} y tiempo: {timeA} message: {message}")
        encode_json = json.loads(str(message).replace("'", '"'))
        
        self.message_queue.agregar_tarea_not_await(encode_json)
        #self.ws.send(str({"message": "mensaje de prueba"}))



    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        print("### closed ###")

    async def cancelOrderFix(self, clOrdId, origClOrdId, side, quantity, symbol, cuenta):
        #self.log.info(f"entrando a cancelOrderFix")
        payload = {
            "type": 5,#cancel order
            "user_fix": self.user, 
            "cuenta": cuenta, 
            "clOrdId": clOrdId, 
            "origClOrdId": origClOrdId, 
            "symbol": symbol, 
            "side": side, 
            "quantity": quantity, 
        }
        self.clOrdIdEsperar[clOrdId] = {"clOrdId": clOrdId, "type": 5, "details": payload, "llegoRespuesta": False}
        
        self.ws.send(str(payload))

        task = asyncio.create_task(self.esperarRespuesta(clOrdId, "cancelOrder"))
        response = await task
        return response

    async def modifyOrderFix(self,clOrdId, orderId, origClOrdId, side, orderType, symbol, quantity, price, cuenta):
        #self.log.info(f"entrando a modifyOrderFix")
        payload = {
            "type": 4,#modify order
            "user_fix": self.user, 
            "cuenta": cuenta, 
            "orderId": orderId, 
            "clOrdId": clOrdId, 
            "origClOrdId": origClOrdId, 
            "symbol": symbol, 
            "side": side, 
            "price": price,
            "quantity": quantity, 
            "orderType": orderType
        }
        self.clOrdIdEsperar[clOrdId] = {"clOrdId": clOrdId, "type": 4, "details": payload, "llegoRespuesta": False, "lastQty": 0}
        
        self.ws.send(str(payload))

        task = asyncio.create_task(self.esperarRespuesta(clOrdId, "modifyOrder"))
        response = await task
        return response

    async def newOrderFix(self, clOrdId, symbol, side, quantity, price, orderType,cuenta):
        #self.log.info(f"entrando a newOrderFix")
        
        payload = {
            "type": 3,#new order
            "cuenta": cuenta, 
            "clOrdId": clOrdId, 
            "symbol": symbol, 
            "side": side, 
            "quantity": quantity, 
            "price": price, 
            "orderType": orderType
        }
        self.clOrdIdEsperar[clOrdId] = {"clOrdId": clOrdId, "type": 3, "details": payload, "llegoRespuesta": False, "lastQty": 0}
        self.log.info(f"enviando nueva orden por socket")
        self.ws.send(str(payload))

        task = asyncio.create_task(self.esperarRespuesta(clOrdId, "newOrder"))
        response = await task
        return response

    async def esperarRespuesta(self, clOrdId, typeOrder):
        response = {"llegoRespuesta": False}
        try:
            self.log.info(f"esperando respuesta de {typeOrder}, con el clOrdId: {clOrdId}")
            contador = 0
            contadorParcial = 0
            while True:
                
                if self.clOrdIdEsperar[clOrdId]["llegoRespuesta"] == True:
                    self.log.info(f"llego respuesta en esperar respuesta de: {clOrdId},  contador: {contador} contadorParcial: {contadorParcial}")
                    if contadorParcial>20:
                        response = self.clOrdIdEsperar[clOrdId]
                        del self.clOrdIdEsperar[clOrdId]
                        break
                    contadorParcial+=1
                contador+=1
                if contador > 1000:
                    self.log.info(f"tiempo excedido esperando respuesta para: {typeOrder}, con el clOrdId: {clOrdId} ")
                    response = {
                        "llegoRespuesta": False, "msg": "tiempo excedido, no llego respuesta o algo mas paso"}
                    break
                await asyncio.sleep(0.01)
        except Exception as e:
            self.log.error(f"error en esperarRespuesta: {e}")
        return response

    def on_open(self, ws):
        print("Opened connection")
        self.ws.send(str({"message": "mensaje de prueba"}))
        print("mensaje enviado ")

    async def procesar_orden_filled(self, task):
        self.log.info(f"procesando task orden filled {task}")
        clientOrderID = task["details"]["clOrdId"]
        if clientOrderID in self.clOrdIdEsperar:
            self.clOrdIdEsperar[clientOrderID]["llegoRespuesta"] = True
            self.clOrdIdEsperar[clientOrderID]["data"] = task["details"] 
            self.clOrdIdEsperar[clientOrderID]["lastQty"] = self.clOrdIdEsperar[clientOrderID]["lastQty"] + task["details"]["lastQty"]
        #task = {"type": 1,  "id_bot": id_bot, "typeOrder": typeOrder, "cuenta": accountFixMsg, "details": details }
        details = task["details"]
        clientOrderID = details["clOrdId"]
        if clientOrderID in self.OrdersIds:
            typeOrder = self.OrdersIds[clientOrderID]["typeOrder"]  # N B C
            id_bot = self.OrdersIds[clientOrderID]["id_bot"]
            lastOrderID = self.OrdersIds[clientOrderID]["lastOrderID"]
            if typeOrder == "N":
                #self.log.info(f"pausar cola del bot :{self.botManager.main_tasks[id_bot].paused}")
                #self.log.info(f"contadorOperada: {self.botManager.main_tasks[id_bot].contadorOperada}")
                if self.botManager.main_tasks[id_bot].contadorOperada == 0:
                    #self.log.info(f"contador = 0, pongo pausa")
                    asyncio.create_task(self.botManager.main_tasks[id_bot].pause()) 
                self.botManager.main_tasks[id_bot].contadorOperada+=1
                #self.log.info(f"paused:{self.botManager.main_tasks[id_bot].paused}")
                self.log.info(f"mandar a verificar orden para q opere contraria, hacerlo en nueva hilo")
                taskOperada = asyncio.create_task(self.botManager.main_tasks[id_bot].verificar_orden_operada(details,typeOrder, lastOrderID))
                response = await taskOperada
                #self.log.info(f"luego q termino de verificar la operada y operar la contraria quito el pause")
                #self.log.info(f"paused:{self.botManager.main_tasks[id_bot].paused}")
                self.botManager.main_tasks[id_bot].contadorOperada-=1
                #self.log.info(f"contadorOperada: {self.botManager.main_tasks[id_bot].contadorOperada}")
                if self.botManager.main_tasks[id_bot].contadorOperada == 0:
                    #self.log.info(f"contador = 0, pongo resume")
                    await self.botManager.main_tasks[id_bot].resume()
                #self.log.info(f"paused:{self.botManager.main_tasks[id_bot].paused}")
            elif typeOrder == "B":
                self.log.info(f"esta es una contraria, aqui ya denbe estar en pause solo mando a verificar en un nuevo hilo")
                taskOperada = asyncio.create_task(self.botManager.main_tasks[id_bot].verificar_orden_operada(details,typeOrder, lastOrderID))
                #self.log.info(f"listo aqui ya se verifico la contraria ")
                response = await taskOperada
        
    async def process_message(self, task):
        self.log.info(f"procesando mensaje de fix .....: {task}")
        if "type" in task:
            #{'type': 0, 'symbolTicker': 'MERV - XMEV - AL30 - CI', 'marketData': {'BI': [{'price': 40.0, 'size': 10, 'position': 1}], 'OF': []}}
            if task["type"]==0:
                await self.update_tickers_bot(task)

            if task["type"]==1:
                await self.procesar_orden_filled(task)

            if task["type"]==2:
                #{"type": 2, "cuenta": cuenta, "balance": newBalance}
                #self.log.info(f"balance viejo: {self.balance}")
                self.balance[task["cuenta"]] = task["balance"]
                #self.log.info(f"balance nuevo: {self.balance}")
            
            if task["type"]==3 or  task["type"]==4 or task["type"]==5 or task["type"]==6: 
                #es mensaje de una orden nueva 
                # {"type": 3, "data":details}
                clientOrderID = task["data"]["clOrdId"]
                if clientOrderID in self.clOrdIdEsperar:
                    self.clOrdIdEsperar[clientOrderID]["llegoRespuesta"] = True
                    self.clOrdIdEsperar[clientOrderID]["data"] = task["data"] 

    async def update_tickers_bot(self, task):
        #aqui me llega el ticker y debo enviarlo a cada bot registrado 
        #self.log.info("entrando a update tickers bot")
        symbolTicker = task["symbolTicker"]
        marketData = task["marketData"]
        if symbolTicker in self.marketSymbolsSubs:
            #si existe aqui entonces lo envio a los bots 
            for id_bot in self.marketSymbolsSubs[symbolTicker]:
                if id_bot in self.botManager.main_tasks:
                    #self.log.info(f"tickers antes: {self.botManager.main_tasks[id_bot]._tickers[symbolTicker]}")
                    self.botManager.main_tasks[id_bot]._tickers[symbolTicker] = marketData
                    #self.log.info(f"tickers despues: {self.botManager.main_tasks[id_bot]._tickers[symbolTicker]}")
                    #self.log.info(f"ahora si agregamos tarea al bot para verificar puntas")
                    if self.botManager.main_tasks[id_bot].botData["botIniciado"]==True:
                        await self.botManager.main_tasks[id_bot].add_task(task)
                    #self.log.info(f"listo tarea agregada al bot")
                    #self.log.info(f"self.botManager.tasks: {self.botManager.tasks}")
                    #self.log.info(f"self.botManager.main_tasks: {self.botManager.main_tasks}") 
                else:
                    self.log.error("el bot no esta en el botManager quizas ya se detuvo")
        else:
            self.log.error(f"no nay bots suscritos a este simbolo")