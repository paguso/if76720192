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
    print("%s[id=%d in_edge=%s slink=%s]"%(level*"  ", root.id, txt[root.start:min(root.end, txt_len)] , str(root.slink.id) if root.slink else "?"))
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
def test_and_split(v, c, txt):
    (u,(l,r)) = v
    print("test&split node (%d, (%d,%d)=%s)"%(u.id, l,r, txt[l:r]))
    if l==r: # no explicito
        return (c in u.chd, v)
    else: 
        w = u.chd[txt[l]]
        a = txt[w.start+(r-l)]
        if a != c:
            x = Node(l,r)
            x.chd[a] = w
            u.chd[txt[l]] = x
            w.start += (r-l)
            return (False,(x,(0,0)))
        else:
            return (True, v)
        
# input: no implicito
# output: no na forma canonica
def canonise((u,(l,r)), txt):
    print("canonising (%d, (%d,%d)=%s)"%(u.id, l,r, txt[l:r]))
    while r>l:
        v = u.chd[txt[l]]
        if v.is_leaf():
            break
        else: 
            v_edge_len = v.end - v.start
            #print("v_edge_len=%d"%v_edge_len)
            if v_edge_len <= (r-l):
                u = v
                l += v_edge_len
            else:
                break
    print("return canonical (%d, (%d,%d)=%s)"%(u.id, l,r, txt[l:r]))
    return (u,(l,r))


# acrescentar o caractere txt[i] aa CST
# input: vertice ativo canonico de Ti
# output: vertice terminador de Ti

def update((u,(l,r)), txt, i):
    print("updating from active node (%d, (%d,%d)=%s)"%(u.id, l,r, txt[l:r]))
    c = txt[i]
    (is_term, (v,(s,t))) = test_and_split((u,(l,r)), txt[i], txt )
    v_prev = None
    while not is_term:
        print("... is not terminator. add new leaf")
        v.chd[c] = Node(i,float('inf'))
        if v_prev:
            v_prev.slink = v
        v_prev = v
        (u,(l,r)) = canonise((u.slink,(l,r)), txt ) 
        (is_term, (v,(s,t))) = test_and_split((u,(l,r)), txt[i], txt)
    if v_prev and (s==t):
        v_prev.slink = v
    print("return terminator (%d, (%d,%d)=%s)"%(v.id, s,t, txt[s:t]))
    return (v,(s,t))


def build_cst(txt, ab):
    n = len(txt)
    grnd = Node(-1,-1)
    root = Node(-1,0)
    root.slink = grnd
    for c in ab:
        grnd.chd[c] = root
    leaf = Node(0,float('inf'))
    root.chd[txt[0]] = leaf
    print("T0:")
    print_cst(root, ab, txt, 1)
    (u,(l,r)) = (root, (1,1))
    for i in range(1,n):
        print("\n\n%d: adding %c"%(i,txt[i]))
        # add txt[i] to T_i-1
        # (u,(l,r)) eh o vert ativo canonico de Ti
        (u,(l,r)) = update((u,(l,r)), txt, i)
        # Ti+1 esta pronta e
        # (u,(l,r)) eh o vert terminador de Ti
        (u,(l,r)) = canonise((u,(l,i+1)), txt)
        # (u,(l,r)) eh o vert ativo canonico de Ti+1
        print("T%d"%(i+1))
        print_cst(root, ab, txt, i+1)
    return root


def main():
    txt = "senselessness"
    ab = "elns"
    root = build_cst(txt, ab)
    (u,(l,r)) = find_locus(root, "sense", len(txt))
    print ("(%d,(%d,%d)=%s)"%(u.id,l,r,txt[l:r]))

if __name__ == "__main__":
    main()
