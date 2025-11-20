from valutatrade_hub.infra.logger import log


def handler_log_action(func):
    """отлов и лог словарей результирующих функций"""
    def wrapper(*args,**kwargs):
        result =  func(*args,**kwargs)
        if result:
            log.info(f'{result.get("cmd")}')
        return result 
    return wrapper

def handler_errors(func):
    """обработка ошибок"""
    def wrapper(*args,**kwargs):
        try:
            result = func(*args,**kwargs)
            return result
        except Exception as e:
            log.alert(f'{e}')
    return wrapper


def handler_log_feedback(func):
    """отлов и лог результатов любых функций"""
    def wrapper(*args,**kwargs):
        result =  func(*args,**kwargs)
        if result:
            log.info(f'{result}')
        return result 
    return wrapper

def handler_api_errors(func):
    """отлов ошибок в апи"""
    def wrapper(*args, **kwargs):
        try:
            log.info('Starting rates update...')
            return func(*args, **kwargs) 
        except Exception as e:
            if str(e) == "'conversion_rates'":
                log.alert('Set env var EXCHENGE_API_KEY')
                return None
            log.alert(f'Error in {func.__name__}: {e}')
    return wrapper