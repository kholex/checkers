class AuthorizeResponse:
    def __init__(self, result: bool):
        self.type = "authorize_response"
        self.result = result

    @staticmethod
    def authorize_response_decoder(obj):
        return AuthorizeResponse(obj['result'])
