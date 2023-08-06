from tktl import __version__
from tktl.commands import CommandBase
from tktl.login import login, logout, validate_key, set_api_key


class LogInCommand(CommandBase):
    def execute(self, api_key=None):
        if login(api_key):
            return validate_key()
        return False


class LogOutCommand(CommandBase):
    def execute(self):
        logout()


class ShowVersionCommand(CommandBase):
    def execute(self):
        self.logger.log(__version__)


class SetApiKeyCommand(CommandBase):
    def execute(self, api_key):
        if not api_key:
            self.logger.error("API Key cannot be empty.")
            return
        set_api_key(api_key=api_key)
