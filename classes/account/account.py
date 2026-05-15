
from api.client import FunPayClient
from api.parsers import FunPayParser
from classes.account.subclasses.chat import ChatManager
from classes.account.subclasses.addons import AddonsManager
from classes.account.subclasses.profile import ProfileManager
from classes.account.subclasses.order import OrderManager
from classes.account.subclasses.lot import LotManager
from classes.account.subclasses.editor import FunPayEditor
from classes.account.subclasses.review import ReviewManager

class Account:
    '''
    Взаимодействует с аккаунтом.
    '''
    def __init__(self, client):
        self.http_client = client
        self.client = FunPayClient(self.http_client)
        self.parser = FunPayParser()
        self.user_id = None
        self.csrf_token = None
        self.last_msg_ids = {}
        self.node_names = {}
        self.chat = ChatManager(self)
        self.addons = AddonsManager(self)
        self.profile = ProfileManager(self)
        self.order = OrderManager(self)
        self.lot = LotManager(self)
        self.editor = FunPayEditor(self)
        self.review = ReviewManager(self)