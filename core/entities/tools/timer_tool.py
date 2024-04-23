import threading

def set_interval(interval):
    def decorator(func):
        def wrapper(*args, **kwargs):
            while True:
                func(*args, **kwargs)
                threading.Event().wait(interval)
        return wrapper
    return decorator
