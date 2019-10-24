

# -1 se x <k y
#  0 se x =k y
# +1 se x >k y
def cmpk(x,y,k):
    xk = x[:min(k,len(x))]
    yk = y[:min(k,len(y))]
    if xk==yk:
        return 0
    elif xk<yk:
        return -1
    else:
        return +1

def lcp(X,Y, start_at=0):
    l = start_at
    while l<len(X) and l<len(Y) and X[l]==Y[l]:
        l += 1
    return l

def pred(txt, pat, sa):
    n = len(txt)
    m = len(pat)
    if cmpk(pat, txt[sa[n-1]:], m) >= 0:
        return n-1
    elif cmpk(pat, txt[sa[0]:], m) < 0:
        return -1
    else:
        l = 0
        r = n-1
        while r-l > 1:
            h = (l+r)/2
            if cmpk(pat, txt[sa[h]:], m) >= 0:
                l = h
            else:
                r = h
        return l


def succ_old(txt, pat, sa):
    n = len(txt)
    m = len(pat)
    if cmpk(pat, txt[sa[0]:], m) <= 0:
        return 0
    elif cmpk(pat, txt[sa[n-1]:], m) > 0:
        return n
    else: 
        l = 0
        r = n-1
        while r-l > 1:
            h = (l+r)/2
            if cmpk(pat, txt[sa[h]:], m) <= 0:
                r = h
            else:
                l = h
        return r


def fill_LRlcp(txt, sa, l, r, Llcp, Rlcp):
    if r-l <= 1:
        return 
    h = (l+r)/2
    Llcp[h] = lcp(txt[sa[l]:], txt[sa[h]:])
    Rlcp[h] = lcp(txt[sa[h]:], txt[sa[r]:])
    fill_LRlcp(txt, sa, l, h, Llcp, Rlcp)
    fill_LRlcp(txt, sa, h, r, Llcp, Rlcp)


def compute_LRlcp(txt, sa):
    n = len(txt)
    Llcp = n*[0]
    Rlcp = n*[0]
    fill_LRlcp(txt, sa, 0, n-1, Llcp, Rlcp)
    return Llcp, Rlcp




def succ(txt, pat, sa, Llcp, Rlcp):
    n = len(txt)
    m = len(pat)
    L, R = 0,0
    if cmpk(pat, txt[sa[0]:], m) <= 0:
        return 0
    elif cmpk(pat, txt[sa[n-1]:], m) > 0:
        return n
    # invariante txt[sa[l]:] < pat <= txt[sa[r]:]
    else: 
        l = 0
        r = n-1
        h = (l+r)/2
        L = lcp(pat, txt[sa[l]:])
        R = lcp(pat, txt[sa[r]:])
        #Llcp[h] = lcp(txt[sa[l]:], txt[sa[h]:], min(L,R))
        #Rlcp[h] = lcp(txt[sa[h]:], txt[sa[r]:], min(L,R))
        while r-l > 1:
            h = (l+r)/2
            print("interval l=%d h=%d r=%d"%(l,h,r))
            if L >= R:
                #caso 1
                if L < Llcp[h]:
                    H = L
                #caso 2
                elif  L == Llcp[h]:
                    H = lcp(pat, txt[sa[h]:], L)
                #caso 3
                else:
                    H = Llcp[h]
            else: # Rp[h] >= Lp[h]
                #caso 1
                if R < Rlcp[h]:
                    H = R
                #caso 2
                elif R == Rlcp[h]:
                    H = lcp(pat, txt[sa[h]:], R)
                #caso 3
                else:
                    H = Rlcp[h]
            print("H=lcp(pat=%s, T[%d:]=%s) = %d"%(pat, sa[h], txt[sa[h]:], H))
            if H==m or (sa[h]+H<n and pat[H] <= txt[sa[h]+H]):
                r,R = h,H
            else:
                l,L = h,H
        return r


def search(txt, pat, sa=None):
    sa = sa or build_sarr(txt)
    Rp = pred(txt, pat, sa)
    Lp = succ(txt, pat, sa)
    if Lp <= Rp:
        return sorted(sa[Lp:Rp+1])
    else:
        return []



def build_sarr_bf(txt):
    n = len(txt)
    suf = [(txt[i:],i) for i in range(n)]
    suf.sort()
    return [y for (x,y) in suf]


def print_sarr(txt, sa):
    n = len(txt)
    for i in range(n):
        print ("SA[%d]=%d : %s"%(i,sa[i], txt[sa[i]:]))

def print_RLlcp(txt, sa, Llcp, Rlcp, l, r):
    if r-l <= 1:
        return
    h = (l+r)/2
    print("Llcp[%d] = lcp(T[%d:]=%s, T[%d:]=%s) = %d"%(h, sa[l], txt[sa[l]:], sa[h], txt[sa[h]:], Llcp[h] ))
    print("Rlcp[%d] = lcp(T[%d:]=%s, T[%d:]=%s) = %d"%(h, sa[h], txt[sa[h]:], sa[r], txt[sa[r]:], Rlcp[h] ))
    print_RLlcp(txt, sa, Llcp, Rlcp, l, h)
    print_RLlcp(txt, sa, Llcp, Rlcp, h, r)


def sort_index(x):
    n = len(x)
    if n==0:
        return []
    pairs = zip(x, range(n))
    pairs.sort()
    ranks = n*[0]
    r = 1
    ranks[pairs[0][1]] = r
    for i in range(1,n):
        if pairs[i][0] != pairs[i-1][0]:
            r += 1
        ranks[pairs[i][1]] = r
    return ranks
    

def build_P(txt):
    n = len(txt)
    P = []
    P.append(sort_index(txt))
    k = 0
    twopowerk=1
    while twopowerk < n:
        pairs = [ (P[k][i], P[k][i+twopowerk] if i+twopowerk<n else 0)  for i in range(n) ]
        P.append(sort_index(pairs))
        k += 1
        twopowerk *= 2
    return P

def invert_P(P):
    n = len(P)
    inv = n*[0]
    for i in range(n):
        inv[P[i]-1] = i
    return inv

def compute_lcp(P, i, j):
    n = len(P[0])
    k = len(P)-1
    twopowerk = 1<<k
    lcp = 0
    while k>=0 and i<n and j<n:
        if P[k][i] == P[k][j]:
            lcp += twopowerk
            i += twopowerk
            j += twopowerk
        k -= 1
        twopowerk /= 2
    return lcp

def fill_LRlcp_P(txt, sa, P,l, r, Llcp, Rlcp):
    if r-l <= 1:
        return 
    h = (l+r)/2
    Llcp[h] = compute_lcp(P, sa[l], sa[h])
    print("lcp(%s,%s)=%d"%(txt[sa[l]:], txt[sa[h]:], Llcp[h]))
    Rlcp[h] = compute_lcp(P, sa[h], sa[r])
    fill_LRlcp_P(txt, sa, P, l, h, Llcp, Rlcp)
    fill_LRlcp_P(txt, sa, P, h, r, Llcp, Rlcp)



def compute_LRlcp_P(txt, sa, P):
    n = len(sa)
    Llcp = n*[0]
    Rlcp = n*[0]
    fill_LRlcp_P(txt, sa,P, 0, n-1, Llcp, Rlcp)
    return Llcp, Rlcp

def build_sarr(txt):
    P = build_P(txt)
    for pi in P:
        print(pi)
    sa =  invert_P(P[-1])
    Llcp, Rlcp = compute_LRlcp_P(txt, sa, P)
    return sa, Llcp, Rlcp


def main():
    txt = "senselesssensess"
    sa, Llcp, Rlcp = build_sarr(txt)
    print(txt)
    print(sa)
    print(Llcp)
    print(Rlcp)


if __name__ == "__main__":
    main()
