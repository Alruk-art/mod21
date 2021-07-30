from datetime import datetime, date, time

# Эту функцию мы будем декорировать

def my_decorator(func):
    def wrapper():
        print ("Начало выполнения функции.")
        func ()
        print ("Конец выполнения функции.")
    return wrapper

@my_decorator
def my_first_decorator():
    print ("Это мой первый декоратор!")

my_first_decorator()


def working_hours(func):
    def wrapper():
        if 9 <= datetime.now ().hour < 18:
            func ()
        else:
            pass  # Нерабочее время, выходим

    return wrapper


def writing_tests():
    print ('Сейчас', datetime.now ().hour ,'часов')
    print ("Я пишу тесты на python!")

writing_tests()


