def __all__():
    pass


def test_func(arg:None) -> None:
    """Name: TestFunc; Description: This is the test function"""
    print('The basic test passed!')
    return None

#print(test_func.__annotations__)
#print(test_func.__doc__.split(':')[1].split(';')[0].lstrip())