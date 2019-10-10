

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


def succ(txt, pat, sa):
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
