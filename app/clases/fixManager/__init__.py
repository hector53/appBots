import asyncio
from app.clases.mainFix import MainFix
import logging
import queue
import threading
import gc

class fixManager:
    def __init__(self):
        self.tasks = asyncio.Queue()
        self.main_tasks = {}  # Diccionario para mantener un registro de los objetos MainTask
        self.log = logging.getLogger("fixManager")

    async def add_task(self, task):
        print("entrando a agragar task")
        await self.tasks.put(task)
        print("ya la agregue")
        task.taskToCancel = asyncio.create_task(task.run())
        print("ya la guarde en tasktoancel")
        if isinstance(task, MainFix):
            # Agregar el objeto MainTask al diccionario
            self.main_tasks[task.user] = task
            print("ya la guarde en main_task")
            
      

    async def remove_task(self, task):
        self.tasks.remove(task)

    def stop_task(self, task):
        task.stop()

    async def stop_all_tasks(self):
        print("entrando a detener todas")
        while not self.tasks.empty():
            print("obtener tarea a deteber")
            task = await self.tasks.get()
            print(f"tarea: {task}")
            task.stop()

    async def stop_task_by_id(self, user):
        while not self.tasks.empty():
            task = await self.tasks.get()
            if task.user == user:
                task.taskToCancel.cancel()
                del self.main_tasks[user]
                gc.collect()
                self.log.info(f"se borro la tarea correctamente")
        self.log.info("se salio del ciclo de borrar tarea")
            
        

    async def get_fixTask_by_id_user(self, user):
        taskReturn = None
        if user in self.main_tasks: 
            return self.main_tasks[user]
        return taskReturn

