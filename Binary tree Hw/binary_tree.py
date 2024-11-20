from binarytree import Node, build
def tree_count(root, value):
    if root is None:
        return 0;

    if root.value == value: count =1
    else: count = 0
    count += tree_count(root.left, value)
    count += tree_count(root.right, value)

    return count

def tree_coontain(root, string):
    for letter in str(string):
        if letter.isdigit():
            if tree_count(root, int(letter)) == 0:
                return False
        else:
            if tree_count(root, letter) == 0:
                return False
    return True