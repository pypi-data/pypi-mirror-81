SEP = ' '

def printTree(tree):
    return _printTree([tree], height(tree))

def _printTree(nodes, maxheight):

    if maxheight < 0:
        return ""

    keys = nodeKeys(nodes)

    posFirstElem = 0
    lenBranch = 0
    padding = ''
    spaceBetweenElem = 1

    if maxheight > 0:
        posFirstElem = 2**(maxheight) -1
        lenBranch = 2**(maxheight-1)
        padding = SEP*(posFirstElem - lenBranch)
        spaceBetweenElem = 4*lenBranch-1

    dataLine = padding + SEP*lenBranch + (SEP*(spaceBetweenElem)).join(keys) + SEP*lenBranch + padding + "\n"

    s = dataLine

    for m in range(lenBranch):
        line = padding

        first = True
        for n in nodes:
            leftChar = '/'
            if not hasLeft(n):
                leftChar = SEP

            rightChar = '\\'
            if not hasRight(n):
                rightChar = SEP

            if first:
                line = line + SEP*(lenBranch - m -1) + leftChar + SEP*(m) + SEP + SEP*m+ rightChar + SEP*(lenBranch - m -1)
                first = False
            else:
                line = line + SEP*(spaceBetweenElem - 2*lenBranch) + SEP*(lenBranch - m -1) + leftChar + SEP*(m) + SEP + SEP*m+ rightChar + SEP*(lenBranch - m -1)
  
        s = s + line +"\n"
    
    
    return s + _printTree(getNextLevelNodes(nodes), maxheight - 1)
    

def nodeKeys(nodes):
    keys = []
    for n in nodes:
        if n == None:
            keys.append(' ')
        elif 'key' in n:
            keys.append(str(n['key']))
        else:
            keys.append(' ')

    return keys

def getNextLevelNodes(nodes):
    nl = []
    for n in nodes:
        if n == None:
            nl.append(None)
            nl.append(None)
            continue

        if 'left' in n:
            nl.append(n["left"])
        else:
            nl.append(None)

        if 'right' in n:
            nl.append(n["right"])
        else:
            nl.append(None)
    
    return nl

def hasLeft(node):
    if node == None:
        return False
    if 'left' in node and node['left'] != None:
        return True
    else:
        return False

def hasRight(node):
    if node == None:
        return False
    if 'right' in node and node['right'] != None:
        return True
    else:
        return False

def height(tree):
    if tree == None:
        return -1
    else:
        left = None
        if 'left' in tree:
            left = tree["left"]

        right = None
        if 'right' in tree:
            right = tree["right"]

        return max(height(left), height(right)) + 1
