import pytest

def strange_string_func(str):
    if len(str) > 5:
        return str + '?'
    elif len(str) < 5:
        return str + '!'
    else:
        return str + '.'


@pytest.fixture(scope="function", params=[
    ("asdfhg", "asdfhg?"),
    ("asdfg", "asdfg."),
    ("1234", "1234!")
])
def param_test(request):
    return request.param


def test_strange_string_func(param_test):
    (input, expected_output) = param_test
    result = strange_string_func(input)
    print('input: {0}, output: {1}, expected: {2}'.format(input, result, expected_output))
    assert result == expected_output


def calc(x):
    return (10 ** x) + x


@pytest.mark.parametrize('x', [1,2,3,4,5,6])
def test_no_1(x):
    print(calc(x))

#str = 'asdfg'
# print(strange_string_func(str))

# print(calc(4))
# test_strange_string_func()