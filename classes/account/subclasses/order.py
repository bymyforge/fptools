from models.account import Order
from utils.errors import FunPayRefundError

class OrderManager:
    def __init__(self, account):
        self.account = account
    
    async def get_order_details(self, order_id):
        '''
        Функция запрашивает детали заказа из /orders/{order_id}/.

        Args:
            order_id (str | int): Айди заказа
        Returns:
            Order: Объект с данными:  
                - status (str): Статус заказа.  
                - review (dict): Словарь с данными отзыва, который оставили к заказу.  
        '''
        html = await self.account.client.get_order_info(order_id)
        data = self.account.parser.parse_order_page(html)
        order = Order(status=data['status'], review=data['review'])
        return order

    async def refund_order(self, order_id):
        '''
        Делает возврат заказа.

        Args:
            order_id (str | int): Айди заказа
        Returns:
            bool: True если возврат прошёл успешно. 
        Raises:
            FunPayRefundError: Не удалось сделать возврат.  
        
        '''
        if not self.account.csrf_token:
            await self.account.profile.get_user_data()
        response = await self.account.client.refund_order(self.account.csrf_token, order_id)
        if response.status_code == 200:
            s = await self.get_order_details(order_id)
            status = s.status
            if status == 'Возврат':
                return True
            raise FunPayRefundError(f'Cant make refund. Now order status is: {status}')