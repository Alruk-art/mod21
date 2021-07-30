def parent():
    print("Printing from the parent() function")

    def first_child():
        print("Printing from the first_child() function")

    def second_child():
        print("Printing from the second_child() function")

    second_child()
    first_child()


def parent2(num):
    def first_child():
        print ( "Hi, I am Emma")

    def second_child():
        print ( "Call me Liam" )

    if num == 1:
        return first_child()
    else:
        return second_child()


# parent()
first = parent2(2)
