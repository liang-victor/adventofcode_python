from day_20 import create_circular_doubly_linked_list, mix_node


def to_list(head, n):
    p = head
    i = 0
    result = [p.value]
    while i < n - 1:
        p = p.next
        result.append(p.value)
        i += 1
    return result


def test_mix_node_positive_number_no_overflow():
    head = create_circular_doubly_linked_list([1, 2, 3, 4, 5, 6, 7])

    mix_node(head.next, 7)

    assert to_list(head, 7) == [1, 3, 4, 2, 5, 6, 7]


def test_mix_node_negative_number_no_overflow():
    head = create_circular_doubly_linked_list([1, 2, 3, 4, 5, -2, 7])

    mix_node(head.prev.prev, 7)

    assert to_list(head, 7) == [1, 2, 3, -2, 4, 5, 7]


def test_mix_node_positive_overflow():
    head = create_circular_doubly_linked_list([1, 3, 4, 5, 6, 2, 7])
    mix_node(head.prev.prev, 7)

    assert to_list(head, 7) == [1, 2, 3, 4, 5, 6, 7]


def test_mix_node_negative_overflow():
    head = create_circular_doubly_linked_list([1, -2, 3, 4, 5, 6, 7])
    mix_node(head.next, 7)

    assert to_list(head, 7) == [1, 3, 4, 5, 6, -2, 7]


def test_mix_node_no_change_with_zero_node():
    head = create_circular_doubly_linked_list([1, 0, 3, 4, 5, 6, 7])
    mix_node(head.next, 7)
    assert to_list(head, 7) == [1, 0, 3, 4, 5, 6, 7]


def test_mix_node_no_change_when_value_equal_to_one_less_than_list_length():
    head = create_circular_doubly_linked_list([0, 1, 2, 3, 4, 5, 6, 7])
    mix_node(head.prev, 8)
    assert to_list(head, 8) == [0, 1, 2, 3, 4, 5, 6, 7]


def test_mix_node_no_change_when_negative_value_equal_to_one_less_than_list_length():
    head = create_circular_doubly_linked_list([0, 1, 2, 3, 4, 5, 6, -7])
    mix_node(head.prev, 8)
    assert to_list(head, 8) == [0, 1, 2, 3, 4, 5, 6, -7]


def test_overflow_past_self():
    head = create_circular_doubly_linked_list([1, 5, 2, 3, 4])
    mix_node(head.next, 5)
    assert to_list(head, 5) == [1, 2, 5, 3, 4]


def test_negative_overflow_past_self():
    head = create_circular_doubly_linked_list([1, 2, 3, 4, -5])
    mix_node(head.prev, 5)
    assert to_list(head, 5) == [1, 2, 3, -5, 4]


def test_put_at_end_2():
    head = create_circular_doubly_linked_list([0, 0, 0, 5, 0])
    mix_node(head.prev.prev, 5)
    print(to_list(head, 5))
    assert to_list(head, 5) == [0, 0, 0, 0, 5]


def test_put_at_end():
    head = create_circular_doubly_linked_list([1, 2, 3, 5, 4])
    mix_node(head.prev.prev, 5)
    print(to_list(head, 5))
    assert to_list(head, 5) == [1, 2, 3, 4, 5]
