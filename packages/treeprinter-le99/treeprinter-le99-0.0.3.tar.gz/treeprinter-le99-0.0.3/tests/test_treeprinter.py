import treeprinter

def node(key, left, right):
    return {
        'key': key,
        'left': left,
        'right': right
    }

def test_print1():
    a = node('1', None, None)
    print(treeprinter.printTree(a))
    assert treeprinter.printTree(a) == "1" + "\n"

def test_print2left():
    a = node('1', node('0', None, None), None)
    print(treeprinter.printTree(a))
    print(a)
    assert treeprinter.printTree(a) == " 1 "+"\n" +"/  " +"\n" + "0  " + "\n"

def test_print2right():
    a = node('1', None, node('2', None, None))
    print(treeprinter.printTree(a))
    print(a)
    assert treeprinter.printTree(a) == " 1 "+"\n" +"  \\" +"\n" + "  2" + "\n"