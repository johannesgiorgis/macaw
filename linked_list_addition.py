class Node():
    """Stuff"""
    def __init__(self, data=None, next=None):
        self.data = data
        self.next = None

    def __repr__(self):
        pointer = self
        result = 'head -> '
        while pointer is not None:
            result += str(pointer.data) + ' -> '
            pointer = pointer.next
        result += 'tail'
        return result

    def append(self, new_element):
        pointer = self
        trail = pointer
        while pointer:
            trail = pointer
            pointer = pointer.next
        trail.next = new_element


def get_linked_list(input_string):
    mod_string = input_string[::-1]
    dummy = Node()
    tail = dummy
    for item in mod_string:
        tail.next = Node(item)
        tail = tail.next
    return dummy.next


def add_list(list_1, list_2):
    cap_1, cap_2 = None, None
    dummy = Node()
    result_pointer = dummy
    carry = 0
    while list_1 or list_2 or carry == 1:
        data_1, data_2 = 0, 0
        if list_1:
            data_1 = list_1.data
            list_1 = list_1.next

        if list_2:
            data_2 = list_2.data
            list_2 = list_2.next

        # print(f"data_1: {data_1}, data_2: {data_2}, carry: {carry}")
        partial = str(carry + int(data_1) + int(data_2))
        # print(f"sum: {partial}")
        result_pointer.append(Node(partial[-1]))
        result_pointer = result_pointer.next
        if len(partial) == 2:
            carry = 1
        else:
            carry = 0



    return dummy.next


if __name__ == '__main__':
    pairs = [("", ""),
             ("1", ""),
             ("1", "1"),
             ("9", "0"),
             ("9", "9")
            ]
    for string_1, string_2 in pairs:
        print(f"\nString 1: '{string_1}', String 2 '{string_2}'")
        list_a = get_linked_list(string_1)
        list_b = get_linked_list(string_2)
        print(f"list_a: {list_a}\nlist_b {list_b}")
        answer = add_list(list_a, list_b)
        print(f"Answer: {answer}")
