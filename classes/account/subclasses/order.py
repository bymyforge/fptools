from models.account import Order
from utils.errors import FunPayRefundError

class OrderManager:
    def __init__(self, account):
        self.account = account
    
    async def get_order_details(self, order_id):
        '''
        Func get data in /orders/{order_id}/
        return object with:
            status: str
            review
        '''
        html = await self.account.client.get_order_info(order_id)
        data = self.account.parser.parse_order_page(html)
        order = Order(status=data['status'], review=data['review'])
        return order

    async def refund_order(self, order_id):
        '''
        Func post data to /orders/refund
        Return True is 200, if error raise FunPayRefundError
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