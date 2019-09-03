
def build_goto(pat_set, ab=[chr(i) for i in range(128)]):
    l = len(ab)
    s = len(pat_set)
    goto = [[None for i in range(l)]]
    occ = [[]]
    nxt= 1
    for k in range(s):
        pat = pat_set[k]
        m = len(pat)
        cur = 0
        for j in range(m):
            c = ab.index(pat[j])
            if goto[cur][c]:
                cur = goto[cur][c]
            else:
                goto.append([None for i in range(l)])
                goto[cur][c] = nxt
                occ.append([])
                cur = nxt
                nxt += 1
        occ[cur].append(k)
    for c in range(l):
        if goto[0][c]==None:
            goto[0][c] = 0
    return goto, occ
            
def print_goto(goto, ab):
    print("goto")
    print([c for c in ab])
    for s in goto:
        print([str(x) if (x==0 or x!=None) else '?' for x in s])


def print_occ(occ):
    print(occ)


def compute_labels(goto, ab):
    l = len(ab)
    labels = ["" for s in goto]
    queue = [0]
    while queue: 
        s = queue.pop(0)
        for c in range(l):
            if goto[s][c] > 0:
                labels[goto[s][c]] = labels[s]+ab[c]
                queue.append(goto[s][c])
    print(labels)
    return labels

def build_fail_old(pat_set, labels):
    fail = len(labels)*[0]
    for s in range(len(labels)):
        lbl = labels[s]
        for k in range(1,len(lbl)):
            suf = lbl[k:]
            for pat in pat_set:
                if suf == pat[:len(suf)]:
                    break
            for t in range(len(labels)):
                if labels[t]==suf:
                    fail[s] = t
                    break
    print(fail)
    return fail



def build_fail(goto, ab, occ):
    queue = []
    queue.append(0)
    fail = len(goto) * [0]
    while(queue):
        s = queue.pop(0)
        print("popped",s)
        for a in range(len(ab)):
            if goto[s][a] != None and goto[s][a]>0:
                t = goto[s][a]
                if s == 0:
                    fail[t] = 0
                else:
                    print("     succ following ", ab[a], "is ", t)
                    p = fail[s]
                    print("     trying p= ", p)
                    while goto[p][a] == None:
                        p = fail[p]
                        print("     trying p= ", p)
                    fail[t] = goto[p][a]
                    print("fail=", fail)
                occ[t].extend(occ[fail[t]])
                queue.append(t)
    return fail







def scan(txt, pat_set, ab, goto, occ, fail):
    n = len(txt)
    cur = 0
    for i in range(n):
        #print("position ",i)
        c = ab.index(txt[i])
        while goto[cur][c]==None:
            cur = fail[cur]
            #print ("cur=", cur)
        cur = goto[cur][c]
        for p in occ[cur]:
            print ("found ",pat_set[p], "at position", i-len(pat_set[p])+1)



def main():
    txt = "she sells sea shells at the sea shore to his custormers and said vishe"
    ab = sorted(set(list(txt))) 
    pat_set = ["he", "she", "his", "hers", "vishe"]
    goto, occ = build_goto(pat_set, ab)
    print_goto(goto,ab )
    print_occ(occ)
    labels = compute_labels(goto, ab)    
    fail = build_fail(goto, ab, occ)
    print("fail",fail)
    print("txt=",txt)
    scan(txt, pat_set, ab, goto, occ, fail)



if __name__ == '__main__':
    main()


