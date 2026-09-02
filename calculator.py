def get_item(lst, index):
    """Safely fetch an item from a list, returning None if out of range."""
    if index < 0 or index > len(lst):
        return None
    return lst[index]
def add(a, b):
    return a + b
