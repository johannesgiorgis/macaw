class Node:
    """doc-string"""
    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next

    def __repr__(self):
        dummy, pointer = self, self
        result = 'head -> '
        while pointer:
            result += str(pointer.data) + ' -> '
            pointer = pointer.next
        result += 'tail'
        return result


def get_linked_list(input_string):
    rev_string = input_string[::-1]
    dummy = Node()
    pointer = dummy
    for item in rev_string:
        pointer.next = Node(item)
        pointer = pointer.next
    return dummy.next


def add_linked_list(list_1, list_2):
    carry = 0
    dummy = Node()
    pointer = dummy
    while carry == 1 or list_1 or list_2:
        digit_1, digit_2 = 0, 0
        if list_1:
            digit_1 = int(list_1.data)
            list_1 = list_1.next
        if list_2:
            digit_2 = int(list_2.data)
            list_2 = list_2.next
        partial = str(carry + digit_1 + digit_2)
        carry = 0
        if len(partial) == 2:
            carry = 1
        pointer.next = Node(partial[-1])
        pointer = pointer.next
    return dummy.next


if __name__ == '__main__':
    tests = [
        ("", ""),
        ("1", ""),
        ("", "2"),
        ("123", "3456")
    ]
    for s1, s2 in tests:
        l1, l2 = get_linked_list(s1), get_linked_list(s2)
        l3 = add_linked_list(l1, l2)
        print(f"list_1: {l1}, list_2: {l2}, list_3: {l3}")

