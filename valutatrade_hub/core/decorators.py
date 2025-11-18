from valutatrade_hub.infra.logger import log

def handler_log_action(func):
    def wrapper(*args,**kwargs):
        result =  func(*args,**kwargs)
        if result:
            log.info(f'[CLI info]: {result.get("cmd")}')
        return result 
    return wrapper

def handler_errors(func):
    def wrapper(*args,**kwargs):
        try:
            result = func(*args,**kwargs)
            return result
        except Exception as e:
            log.alert(f'{e}')
    return wrapper


def handler_log_feedback(func):
    def wrapper(*args,**kwargs):
        result =  func(*args,**kwargs)
        if result:
            log.info(f'{result}')
        return result 
    return wrapper

def handler_api_errors(func):
    def wrapper(*args, **kwargs):
        try:
            log.info('Starting rates update...')
            return func(*args, **kwargs) 
        except Exception as e:
            log.alert(f'Error in {func.__name__}: {e}')
            return None
    return wrapper