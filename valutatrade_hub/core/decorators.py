def handler_log_action(func):
    def wrapper(*args,**kwargs):
        result =  func(*args,**kwargs)
        if result:
            print(f'Command: {result.get("cmd")}')
        return result 
    return wrapper

def handler_errors(func):
    def wrapper(*args,**kwargs):
        try:
            result = func(*args,**kwargs)
            return result
        except Exception as e:
            print(f'Error: {e}')
    return wrapper


def handler_log_feedback(func):
    def wrapper(*args,**kwargs):
        result =  func(*args,**kwargs)
        if result:
            print(f'Operation result: {result}')
        return result 
    return wrapper

def handler_api_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs) 
        except Exception as e:
            print(f'API Error in {func.__name__}: {e}')
            return None
    return wrapper