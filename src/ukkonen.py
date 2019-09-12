

def next_column(pat, col, a):
    m = len(pat)
    ret = (m+1)*[0]
    for i in range(1,m+1):
        ret[i] = min( col[i]+1, ret[i-1]+1, col[i-1] + (1 if a==pat[i-1] else 0) )
    return tuple(ret)



def build_fsm(pat, err, ab):
    m = len(pat)
    states = {} 
    q0 = tuple(range(0,m+1))
    states[q0] = 0
    state_count = 1
    queue = [q0]
    delta = {}
    final = set()
    while queue:
        st = queue.pop(0)
        i_st = states[st]
        for a in ab:
            next_st = next_column(pat, st, a)
            if next_st not in states:
                states[next_st] = state_count
                i_nxt = state_count
                state_count += 1
                queue.append(next_st)
                if next_st[m]<= err :
                    final.add(i_nxt)
                print ("next_st="+str(next_st)+"="+str(i_nxt))
            else:
                i_nxt = states[next_st]
            delta[(i_st,a)] = i_nxt
    print (delta)
    print (final)
    return delta, final  



def scan( (delta, final), txt):
    cur = 0
    n = len(txt)
    occ = []
    if cur in final:
        occ.append(0)
    for j in range(n):
        cur = delta[(cur,txt[j])]
        if cur in final:
            occ.append(j)
    return occ





def main():
    txt = "abadac"
    pat = "cada"
    ab = "abcdr"
    err = 2
    fsm = build_fsm(pat, err, ab)
    occ = scan(fsm, txt)
    print occ

if __name__ == "__main__":
    main()


