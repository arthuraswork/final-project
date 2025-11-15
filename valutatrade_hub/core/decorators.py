def handler_logger(func):
    def wrapper(*args,**kwargs):
        result =  func(*args,**kwargs)
        if result:
            print(f'command: {result.get('cmd')}')
        return result 
    return wrapper

def handler_errors(func):
    def wrapper(*args,**kwargs):
        try:
            result = func(*args,**kwargs)
            return result
        except Exception as e:
            print(f'error: {e}')
    return wrapper
