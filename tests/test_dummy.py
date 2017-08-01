# content of test_sample.py
def inc(x):
    return x + 1

def test_answer():
    assert inc(3) == 4

def test_true():
    assert True is True

def test_list():
    name_letters = ['B', 'O', 'L', 'A', 'J', 'I']
    assert 'O' in name_letters
