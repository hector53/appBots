import websocket
from threading import Thread
import time
import datetime
class clientSocket(Thread):
    def __init__(self, port):
        Thread.__init__(self)
        self.port = port
        self.ws = websocket.WebSocketApp(f"ws://127.0.0.1:{self.port}",
                              on_open=self.on_open,
                              on_message=self.on_message,
                              on_error=self.on_error,
                              on_close=self.on_close)
        
    def on_message(self, ws, message):
        timeA = datetime.datetime.now()
        print(f"mensaje del puerto: {self.port} y tiempo: {timeA}", message)

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        print("### closed ###")

    def on_open(self, ws):
        print("Opened connection")

    def run(self):
        self.ws.run_forever(reconnect=5)
        
"""
async def main():
    client1 = clientSocket(5100)
    client1.start()

    client2 = clientSocket(5200)
    client2.start()
    
    client1.join()
    client2.join()

if __name__ == "__main__":
    asyncio.run(main())
"""

