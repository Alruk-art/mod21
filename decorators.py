import functools


def do_twice(call_me):
    def wrapper():
        # global nn; nn=''
        nn='первый'
        print(nn)
        call_me()
        nn = 'второй';print(nn)
        call_me()
    return wrapper

def do_twice2(func):
  @functools.wraps(func)
  def wrapper(*args, **kwargs):
      func(*args, **kwargs)
      return func(*args, **kwargs)
  return wrapper

import functools

def debug(func):
    """Выводит сигнатуру функции и возвращаемое значение"""
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"Вызываем {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"{func.__name__!r} вернула значение - {value!r}")
        return value
    return wrapper_debug
@debug
def age_passed(name, age=None):
  if age is None:
    return "Необходимо передать значение age"
  else:
    return "Аргументы по умолчанию заданы!"

age_passed("Роман")
age_passed("Роман", age=21)