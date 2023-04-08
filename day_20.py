
def load_data(file):
    with open(f'input/{file}.txt') as f:
        data = f.read().split('\n')
        return [int(n) for n in data]

# listnode class for doubly linked list

class ListNode:
    def __init__(self, value, position = None):
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
    while i<= head.prev.position:
        result.append(p)
        p = p.next
        i+=1
    return result

def mix_node(node):
    i = 0
    p = node

    # no change on 0
    if node.value == 0:
        return

    # travel to destination based on value
    if node.value > 0:
        while i < node.value:
            p = p.next
            i+=1

    if node.value < 0:
        while i > node.value:
            p = p.prev
            i -= 1


    original_prev = node.prev
    original_next = node.next

    # splice node into destination
    target_after = p.next
    p.next = node
    node.prev = p
    node.next = target_after
    target_after.prev = node.next

    # directly connect current prev and next to cover hole
    original_prev.next = original_next
    original_next.prev = original_prev


if __name__ == '__main__':
    input_data = load_data("day_20_example")
    head = create_circular_doubly_linked_list(input_data)

    max_position = head.prev.position

    original_list = list_of_nodes(head)

    # original_list[3].value = 18
    # print(original_list)
    print_list(head, max_position)
    print()

    mix_node(original_list[0])
    print()
    print_list(head, max_position)

    mix_node(original_list[1])
    print()
    print_list(head, max_position)

    mix_node(original_list[2])
    print()
    print_list(head, max_position)

    # for node in original_list:
    #     mix_node(node)
    #     print()
    #     print_list(head, max_position)

    # print_list(head, max_position)

