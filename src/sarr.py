

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



def succ(txt, pat, sa):
    n = len(txt)
    m = len(pat)
    Lp = n * [-1]
    Rp = n * [-1]
    Llcp = n * [-1]
    Rlcp = n * [-1]
    if cmpk(pat, txt[sa[0]:], m) <= 0:
        return 0
    elif cmpk(pat, txt[sa[n-1]:], m) > 0:
        return n
    # invariante txt[sa[l]:] < pat <= txt[sa[r]:]
    else: 
        l = 0
        r = n-1
        h = (l+r)/2
        Lp[h] = lcp(pat, txt[sa[l]:])
        Rp[h] = lcp(pat, txt[sa[r]:])
        Llcp[h] = lcp(txt[sa[l]:], txt[sa[h]:], min(Lp[h],Rp[h]))
        Rlcp[h] = lcp(txt[sa[h]:], txt[sa[r]:], min(Lp[h],Rp[h]))
        while r-l > 1:
            h = (l+r)/2
            if Lp[h] > Rp[h]:
                #caso 1
                if Llcp[h] > Lp[h]:
                    H = Lp[h]
                #caso 2
                elif  Llcp[h] == Lp[h]:
                    H = Lp[h] + lcp(pat, txt[sa[h]:], Lp[h])
                #caso 3
                else:
                    H = Llcp[h]
            else: # Rp[h] >= Lp[h]
                #caso 1
                if Rlcp[h] > Rp[h]:
                    H = Rlcp[h]
                #caso 2
                #caso 3

        return r


def search(txt, pat, sa=None):
    sa = sa or build_sarr(txt)
    Rp = pred(txt, pat, sa)
    Lp = succ(txt, pat, sa)
    if Lp <= Rp:
        return sorted(sa[Lp:Rp+1])
    else:
        return []



def build_sarr(txt):
    n = len(txt)
    suf = [(txt[i:],i) for i in range(n)]
    suf.sort()
    return [y for (x,y) in suf]


def main():
    txt = "senselessness"
    sa = build_sarr(txt)
    pat = "se"
    occ = search(txt, pat)
    print(occ)


if __name__ == "__main__":
    main()
