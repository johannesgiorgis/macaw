class Node():
    """doc-string"""
    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next

    def __str__(self):
        result = 'head -> '
        pointer = self
        while pointer:
            result += str(pointer.data) + ' -> '
            pointer = pointer.next
        result += 'tail'
        return result


def get_linked_list(input_string):
    reversed_string = input_string[::-1]
    dummy = Node()
    pointer = dummy
    for item in reversed_string:
        pointer.next = Node(item)
        pointer = pointer.next
    return dummy.next


def add_linked_lists(list_x, list_y):
    carry = 0
    result = ""
    while list_x or list_y or carry == 1:
        part_x, part_y = 0, 0
        if list_x:
            part_x = list_x.data
            list_x = list_x.next
        if list_y:
            part_y = list_y.data
            list_y = list_y.next

        partial = str(carry + int(part_x) + int(part_y))
        result += partial[-1]
        carry = 0
        if len(partial) == 2:
            carry = 1


    return get_linked_list(result[::-1])

if __name__ == "__main__":
    tests = [
        ("", ""),
        ("1", ""),
        ("1", "2"),
        ("9", "2"),
        ("999", "1")
    ]
    for string_a, string_b in tests:
        list_a = get_linked_list(string_a)
        list_b = get_linked_list(string_b)
        list_c = add_linked_lists(list_a, list_b)
        print(f"list_a: {list_a}, list_b: {list_b}, list_c: {list_c}")


