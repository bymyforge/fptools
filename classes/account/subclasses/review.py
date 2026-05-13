import json

from models.account import Review
from utils.errors import AnswerReviewError
'''
СДЕЛАТЬ ФУНКЦИИ ПРОСМОТРА ОТЗЫВОВ, ОТВЕТА НА ОТЗЫВ(хотя через ордер дата можно получить инфу о отзыве, завтра надо разобратся)
'''


class ReviewManager:
    def __init__(self, account):
        self.account = account

    async def get_review(self, order_id):
        r = await self.account.order.get_order_details(order_id)
        rev = r.review
        review = Review(text=rev.get('text'), stars=rev.get('stars'), answer=rev.get('answer'))
        return review

    async def review_answer(self, order_id, text):
        '''
        Отвечает на отзыв, оставленный покупателем. Принимает: 
        order_id - айди заказа, на отзыв которого хотите ответить,  
        text - текст, которым вы хотите ответить на отзыв.  
        Возвращает True при успехе,
        При ошибке (ответ не совпадает заданному/сервер не вернул ничего) рейзит AnswerReviewError
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
        