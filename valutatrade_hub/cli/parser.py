from valutatrade_hub.infra.decorators import handler_log_action
from valutatrade_hub.infra.consts import TokenArgs, TokenCmdType


class ParserCLI:
    """
    парсер cli
    """
    @handler_log_action
    def run(self, input: str):
        """
        входная функция
        """
        try:
            return self.parse(input)
        except Exception as e:
            return {'cmd':'exception', 'exception': e}

    def parse(self, input: str):
        """
        парсит комманды и аргументы - что то не то, улетаем
        в ошибку(это фича)
        """
        tokenized = input.split()
        args: dict = {}
        command_type: str = tokenized[0] if tokenized[0] in [
            e.value for e in list(TokenCmdType)
            ] else 'unknown'
        if command_type in ['exit']:
            return {'cmd':command_type}
        for i, token in enumerate(tokenized):
            if token in [e.value for e in list(TokenArgs)]:
                args[token] = tokenized[i+1]
        return {'cmd':command_type, 'args':args}