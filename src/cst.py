node_count = 0

class Node(object):
    def __init__(self, st=None, end=None):
        global node_count
        self.start = st
        self.end = end
        self.chd = {}
        self.id = node_count
        node_count += 1

    def is_leaf(self):
        return self.end==float('inf')

def _print_cst(root, level, ab, txt, txt_len):
    print("%s[id=%d in_edge=%s]"%(level*"  ", root.id, txt[root.start:min(root.end, txt_len)] ))
    for c in ab:
        if c in root.chd:
            _print_cst(root.chd[c], level+1, ab, txt, txt_len)


def print_cst(root, ab, txt, txt_len):
    _print_cst(root, 0, ab, txt, txt_len)





def find_locus(root, lbl, txt_len):
    print("looking for locus of '%s'"%lbl)
    j = 0
    cur = root
    m = len(lbl)
    while j < m:
        nxt = cur.chd[lbl[j]]
        edge_len = min(nxt.end, txt_len) - nxt.start
        if j + edge_len <= m:
            cur = nxt
            j += edge_len
        else:
            return (cur,(nxt.start, nxt.start+(m-j)))
    return (cur,(0,0))

# testa se no implicito v tem c-transicao.
# caso nao tenha, cria uma
# se for necessario, torna-o explicito
def test_and_split(v, c, i, txt):
    (u,(l,r)) = v
    if l==r: # no explicito
        if c not in u.chd:
            u.chd[c] = Node(i, float('inf'))
    else: 
        if txt[r] != c:
            w = u.chd[txt[l]]
            w.start = r
            new_v = Node(l,r)
            new_v.chd[txt[r]] = w
            u.chd[txt[l]] = new_v
            new_v.chd[c] = Node(i, float('inf'))



# acrescentar o caractere txt[i] aa CST
def update(grnd, root, txt, i):
    c = txt[i]
    for s in range(i+1):
        (u,(l,r)) = find_locus(root, txt[s:i], i)
        print("locus of %s is (%d,(%d,%s))"%(txt[s:i], u.id, l, str(r)))
        if u.is_leaf():
            pass
        else:
            test_and_split((u,(l,r)), c, i, txt)


def build_cst(txt, ab):
    n = len(txt)
    grnd = Node()
    root = Node(0,0)
    for c in ab:
        grnd.chd[c] = root
    print("T0:")
    print_cst(root, ab, txt, 0)
    for i in range(n):
        # add txt[i] to T_i-1
        update(grnd, root, txt, i)
        print("T%d"%(i+1))
        print_cst(root, ab, txt, i+1)


def main():
    txt = "ababc"
    ab = "abc"
    build_cst(txt, ab)

if __name__ == "__main__":
    main()
