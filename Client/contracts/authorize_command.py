class AuthorizeCommand:
    def __init__(self, login: str):
        self.type = "authorize_command"
        self.login = login
