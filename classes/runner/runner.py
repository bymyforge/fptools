import asyncio
import httpx
from types import SimpleNamespace

from utils.errors import CriticalRunnerError
from classes.runner.subclasses.chat import ChatRunner
from classes.runner.subclasses.order import OrderRunner

class Runner:
    def __init__(self, account):
        self.account = account
        self.chat = ChatRunner(self)
        self.order = OrderRunner(self)
        self.msgs = []
        self.old_msgs = []
        self.orders = []
        self.old_orders = []
        self.message_handlers = []
        self.order_handlers = []
    
    async def runner_polling(self, timer):
        '''
        Принимает timer - количество секунд, раз в который будет проверка новых событий
        Запускает цикл раннера(поиск событий), раннер сравнивает старый кеш с новым в timer секунд, рекомендуемая задержка 3-5 сек
        '''
        while True:
            try:
                await self.cache_runner()
                await asyncio.sleep(timer)
            except (httpx.ConnectTimeout, httpx.RemoteProtocolError, httpx.ReadTimeout, httpx.ConnectError):
                await asyncio.sleep(timer)
            except Exception as e:
                raise CriticalRunnerError(message=str(e))

    def message_handler(self):
        def decorator(func):
            self.message_handlers.append(func)
            return func
        return decorator

    def order_handler(self):
        def decorator(func):
            self.order_handlers.append(func)
            return func
        return decorator

    async def cache_runner(self):

        #   проверка чатов
        await self.chat.update_chat_cache()
        chats = await self.chat.compare_chat_cache()
        if chats:
            for handler in self.message_handlers:
                await handler(chats)
        #   проверка заказов
        await self.order.update_order_cache()
        orders = await self.order.compare_order_cache()
        if orders:
            for handler in self.order_handlers:
                await handler(orders)