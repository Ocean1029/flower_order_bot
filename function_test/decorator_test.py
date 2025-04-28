# decorator

def decorator(func):
    def wrapper(*args, **kwargs):
        print("Before function call")
        result = func(*args, **kwargs)
        print("After function call")
        return result
    return wrapper

@decorator
def test_function():
    print("Inside test_function")

# test_function = decorator(test_function)

# an example of a function is with arguments, but decorator isn't

@decorator
def test_function_with_args(arg1, arg2):
    print(f"Inside test_function_with_args with arguments: {arg1}, {arg2}")
    return arg1 + arg2

# test_function_with_args = decorator(test_function_with_args)


def decorator_with_args(arg1, arg2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print("Before function call with decorator arguments")
            print(f"Decorator arguments: {arg1}, {arg2}")
            result = func(*args, **kwargs)
            print("After function call with decorator arguments")
            return result
        return wrapper
    return decorator

@decorator_with_args("Hello", "World")
def test_function_with_args_both_side(arg1, arg2):
    print(f"Inside test_function_with_args with arguments: {arg1}, {arg2}")
    return arg1 + arg2
# test_function_with_args = decorator_with_args("Hello", "World")(test_function_with_args)

if __name__ == "__main__":
    test_function_with_args(5, 10)

    print()

    result = test_function_with_args(5, 10)
    print(f"Result of test_function_with_args: {result}")

    print()    
    result = test_function_with_args_both_side(5, 10)
    print(f"Result of test_function_with_args_both_side: {result}")



from functools import wraps

def limit_calls(n):
    def decorator(func):
        count = 0

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal count
            if count >= n:
                raise RuntimeError(f"{func.__name__} 已經達到呼叫上限 ({n} 次)")
            count += 1
            print(f"[限制呼叫] 第 {count}/{n} 次執行 {func.__name__}")
            return func(*args, **kwargs)
        return wrapper
    return decorator


@limit_calls(3)
def greet(name):
    print(f"Hi {name}!")

greet("Alice")
greet("Bob")
greet("Charlie")
# greet("Dora")  # 這行會噴錯


import time
from functools import wraps

def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        print(f"[計時] 開始執行 {func.__name__}...")
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[計時] {func.__name__} 執行時間：{(end - start):.6f} 秒")
        return result
    return wrapper

@timed
def slow_task():
    time.sleep(1.2)
    print("任務完成！")

slow_task()
