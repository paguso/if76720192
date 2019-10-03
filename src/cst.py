node_count = 0

class Node(object):
    def __init__(self, st=None, end=None):
        global node_count
        self.start = st
        self.end = end
        self.chd = {}
        self.id = node_count
        self.slink = None
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

# testa se no implicito v tem c-transicao
# input: v=(u,(l,r)) vert canonico da fronteira.
# output: is_term = booleano se v eh terminador i.e. tem c-trans
#         w = forma explicita de v se nao for terminador
def test_and_split(v, c, i, txt):
    (u,(l,r)) = v
    if l==r: # no explicito
        return (c in u.chd, v)
    else: 
        w = u.chd[txt[l]]
        a = txt[w.start+(r-l)]
        if a != c:
            x = Node(l,r)
            x.chd[a] = w
            u[txt[l]] = x
            w.start += (r-l)
            return (False,(x,(0,0)))
        else:
            true (True, v)
        


# acrescentar o caractere txt[i] aa CST
# input: vertice ativo canonico de Ti
# output: vertice terminador de Ti

def update((u,(l,r)), txt, i):
    c = txt[i]
    (is_term, (v,(s,t))) = test_and_split((u,(l,r)))
    while not is_term:
        v.chd[c] = Node(i,float('inf'))


def build_cst(txt, ab):
    n = len(txt)
    grnd = Node()
    root = Node(0,0)
    root.slink = grnd
    for c in ab:
        grnd.chd[c] = root
    leaf = Node(0,float('inf'))
    root.chd[txt[0]] = leaf
    print("T0:")
    print_cst(root, ab, txt, 0)
    (u,(l,r)) = (root, (0,0))
    for i in range(1,n):
        # add txt[i] to T_i-1
        # (u,(l,r)) eh o vert ativo canonico de Ti
        (u,(l,r)) = update((u,(l,r)), txt, i)
        # Ti+1 esta pronta e
        # (u,(l,r)) eh o vert terminador de Ti
        print("T%d"%(i+1))
        (u,(l,r)) = canonise((u,(l,r)))
        # (u,(l,r)) eh o vert ativo canonico de Ti+1
        print_cst(root, ab, txt, i+1)


def main():
    txt = "ababc"
    ab = "abc"
    build_cst(txt, ab)

if __name__ == "__main__":
    main()
