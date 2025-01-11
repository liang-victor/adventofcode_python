from collections import deque

DECRYPTION_KEY = 811589153


def load_data(file):
    with open(f'input/{file}.txt') as f:
        data = f.read().split('\n')
        return [int(n) for n in data]


# listnode class for doubly linked list

class ListNode:
    def __init__(self, value, position=None):
        self.value = value
        self.position = position
        self.next = None
        self.prev = None

    def __repr__(self):
        return f"⇌ {self.value} "


# construct circular doubly linked list from input
def create_circular_doubly_linked_list(values):
    prev = None
    for i, value in enumerate(values):
        node = ListNode(value, position=i)
        if i == 0:
            head = node

        node.prev = prev
        if prev:
            prev.next = node

        prev = node

    # attach head to tail
    head.prev = node
    node.next = head
    return head


def print_list(head, count):
    i = 0
    p = head
    while i <= count:
        print(p, end='')
        p = p.next
        i += 1


def list_of_nodes(head):
    """Returns a list of the nodes so we can iterate in original order"""
    i = 0
    result = []
    p = head
    while i <= head.prev.position:
        result.append(p)
        p = p.next
        i += 1
    return result


def mix_node(node, list_size):
    i = 0
    p = node
    reduced_steps = abs(node.value) % (list_size - 1)

    # no change on 0
    if reduced_steps == 0:
        return

    if node.value > 0:
        while i < reduced_steps:
            p = p.next
            i += 1

    elif node.value < 0:
        while i > -1 * reduced_steps - 1:
            p = p.prev
            i -= 1

    # travel to destination based on value
    original_prev = node.prev
    original_next = node.next

    # directly connect current prev and next to cover hole
    original_prev.next = original_next
    original_next.prev = original_prev

    # splice node into destination
    target_after = p.next
    p.next = node
    node.prev = p
    node.next = target_after
    target_after.prev = node


def get_node_at_value(starting_node, value):
    p = starting_node
    while p.value != value:
        p = p.next
    return p


if __name__ == '__main__':
    input_data = load_data("day_20")

    head = create_circular_doubly_linked_list(input_data)

    list_size = head.prev.position + 1

    original_list = list_of_nodes(head)

    for i, node in enumerate(original_list):
        mix_node(node, list_size)

    zero_head = get_node_at_value(head, 0)

    sub_result = []
    p = zero_head

    for i in range(3000):
        p = p.next
        if (i + 1) % 1000 == 0:
            sub_result.append(p.value)

    result_p1 = sum(sub_result)
    print(f"The sum of the grove coordinates is {result_p1}")

    # part 2

    head = create_circular_doubly_linked_list(map(lambda x: x * DECRYPTION_KEY, input_data))

    list_size = head.prev.position + 1

    original_list = list_of_nodes(head)

    for _ in range(10):
        for i, node in enumerate(original_list):
            mix_node(node, list_size)

    zero_head = get_node_at_value(head, 0)

    sub_result = []
    p = zero_head

    for i in range(3000):
        p = p.next
        if (i + 1) % 1000 == 0:
            sub_result.append(p.value)
    print(sub_result)

    result_p2 = sum(sub_result)
    print(f"The sum of the grove coordinates is {result_p2}")
