def do_twice(func):
    def wrapper():
        func()
        func()
    return wrapper
@do_twice
def test_twice():
    print("Это вызов функции test_twice!")