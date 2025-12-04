mport pytest
from service_body_test.py import Order


def test_total_basic():
    o = Order(1, [
        {'price': 10, 'quantity': 2},
        {'price': 5, 'quantity': 1}
    ])
    assert o.total() == 25


def test_total_empty_items():
    o = Order(2, [])
    assert o.total() == 0


def test_total_extreme_values():
    o = Order(3, [
        {'price': 1_000_000, 'quantity': 3},
        {'price': 999_999, 'quantity': 1}
    ])
    assert o.total() == 3_000_000 + 999_999


def test_most_expensive_basic():
    o = Order(4, [
        {'price': 10, 'quantity': 1},
        {'price': 20, 'quantity': 1},
        {'price': 15, 'quantity': 3},
    ])
    assert o.most_expensive()['price'] == 20


def test_most_expensive_single_item():
    o = Order(5, [{'price': 7, 'quantity': 3}])
    assert o.most_expensive()['price'] == 7


def test_most_expensive_equal_prices():
    o = Order(6, [
        {'price': 5, 'quantity': 1},
        {'price': 5, 'quantity': 10}
    ])

    assert o.most_expensive()['price'] == 5


def test_apply_discount_valid():
    items = [
        {'price': 100, 'quantity': 1},
        {'price': 50, 'quantity': 2}
    ]
    o = Order(7, items)
    o.apply_discount(10)
    assert items[0]['price'] == 90
    assert items[1]['price'] == 45


def test_apply_discount_zero_percent():
    items = [{'price': 10, 'quantity': 1}]
    o = Order(8, items)
    o.apply_discount(0)
    assert items[0]['price'] == 10


def test_apply_discount_full_100():
    items = [{'price': 50, 'quantity': 2}]
    o = Order(9, items)
    o.apply_discount(100)
    assert items[0]['price'] == 0


def test_apply_discount_invalid_negative():
    o = Order(10, [{'price': 10, 'quantity': 1}])
    with pytest.raises(ValueError):
        o.apply_discount(-1)


def test_apply_discount_invalid_over_100():
    o = Order(11, [{'price': 10, 'quantity': 1}])
    with pytest.raises(ValueError):
        o.apply_discount(101)


def test_repr_normal():
    o = Order(12, [
        {'price': 1, 'quantity': 1},
        {'price': 2, 'quantity': 2}
    ])
    r = repr(o)
    assert r == "<Order 12: 2 items>"


def test_repr_empty():
    o = Order(13, [])
    r = repr(o)
    assert r == "<Order 13: 0 items>"