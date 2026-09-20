from functools import wraps

def decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Вызов функции: {func.__name__}")
        print(f"Аргументы: {args}, {kwargs}")
        result = func(*args, **kwargs)
        print(f"Результат: {result}")
        return result
    return wrapper

@decorator
def add(a, b):
    return a + b

result = add(5, 3)
