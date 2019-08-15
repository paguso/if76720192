import sys


def badchar(pat):
    bc = 128*[-1]
    for i in range(0, len(pat)):
        bc[ord(pat[i])] = i
    return bc


def goodsuffix(pat):
    m = len(pat)
    gs = m*[0]
    for j in range(0,m):
        U = pat[j+1:]
        lenU = m-1-j
        k = m-1
        while k>0:
            if k>lenU and U==pat[k-lenU:k]:
                gs[j] = k
                break
            elif k<=lenU and pat[:k]==pat[m-k:]:
                gs[j] = k
                break
            k -= 1
    return gs    

def bm(txt, pat, gs=None, bc=None) :
    n = len(txt)
    m = len(pat)
    bc = bc or badchar(pat)
    gs = gs or goodsuffix(pat)
    i = 0
    occ = []
    while i <= n-m:
        j = 0
        while j<m and txt[i+m-1-j] == pat[m-1-j]:
            j += 1
        if j==m:
            occ.append(i)
            s = 1
        else:
            d = gs[m-1-j]
            l = bc[ord(txt[i+m-1-j])]
            s = max(1, m-d, m-j-1-l)
        i += s
    return occ



def main() :
    filename = sys.argv[1]
    pat = sys.argv[2]
    bc = badchar(pat)
    gs = goodsuffix(pat)
    txtfile  = open(filename, "r")
    count = 0
    for txt in txtfile:
        occ = bm(txt, pat, gs, bc)
        if occ:
            print(txt)
            print(occ)
        count += len(occ)
    txtfile.close()
    print("Total occurrences:",count)

def amain():
    txt = "abracadabra"
    pat = "abra"
    occ = bm(txt, pat)
    print(occ)




if __name__ == "__main__":
    main()
