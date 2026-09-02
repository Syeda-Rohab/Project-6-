from calculator import get_item, add

def test_get_item_valid():
    assert get_item([1, 2, 3], 1) == 2

def test_get_item_out_of_range():
    assert get_item([1, 2, 3], 3) is None

def test_get_item_none_list():
    assert get_item(None, 0) is None

def test_add():
    assert add(2, 3) == 5
