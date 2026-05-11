

class AccountError(Exception):
    def __init__(self, message='Account error'):
        self.message = message
        super().__init__(self.message)

class ParseException(Exception):
    def __init__(self, message='Data parsing error'):
        self.message = message
        super().__init__(self.message)

class NullData(ParseException):
    message = 'Null Data'

class MessageNotDelivered(AccountError):
    message = 'Message is not delivered'

class RaisingLotError(AccountError):
    message = 'Raising lot error'

class FunPayRefundError(AccountError):
    message = 'Refunding error'

class RequestError(AccountError):
    """Error by get and parsing response"""
    pass