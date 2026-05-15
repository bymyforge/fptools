import json

from models.account import Review
from utils.errors import AnswerReviewError


class ReviewManager:
    def __init__(self, account):
        self.account = account

    async def get_review(self, order_id):
        '''
        Забирает отзыв от заказа.

        Args:
            order_id (str | int): Айди заказа.
        Returns:
            Review: Объект с данными отзыва:  
                - text (str): Текст отзыва. 
                - stars (int): Количество звёзд в отзыве.   
                - answer (str): Ваш ответ на отзыв, может быть пустой строкой.  
        '''
        r = await self.account.order.get_order_details(order_id)
        rev = r.review
        review = Review(text=rev.get('text'), stars=rev.get('stars'), answer=rev.get('answer'))
        return review

    async def review_answer(self, order_id, text):
        '''
        Отвечает на отзыв, оставленный покупателем.
        
        Args:
            order_id (str | int): ID заказа, на отзыв которого хотите ответить,  
            text (str): Текст, которым вы хотите ответить на отзыв.  
        Returns:
            bool: True при успехе
        Raises:
            AnswerReviewError: При ошибке (ответ не совпадает заданному/сервер не вернул ничего).
        '''
        if not self.account.user_id or not self.account.csrf_token:
            await self.account.profile.get_user_data()
        r = await self.account.client.answer_review(self.account.user_id, text, self.account.csrf_token, order_id)
        try:
            response = r.json()
        except json.JSONDecodeError:
            raise AnswerReviewError(message='Сервер не вернул ничего')
        if text in response['content']:
            return True
        raise AnswerReviewError(message='Ответ не сохранился')
        