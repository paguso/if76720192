import sys

def borders(pat) :
    #print("computing borders")
    m = len(pat)
    b = (m+1) * [0]
    b[0] = -1
    i = 1
    j = 0
    while i < m:
        #print("i=%d"%i)
        while j < m and i+j<m and pat[i+j] == pat[j]:
            j += 1
            #print(pat)
            #print("%s%s"%(" "*i,j*"="))
            #print("%s%s"%(" "*i,pat))
            b[i+j] = j
            #print(b)
        i += max(1, j-b[j])
        j = max(0, b[j])
    return b



def badchar(pat):
    bc = 128*[-1]
    for i in range(0, len(pat)):
        bc[ord(pat[i])] = i
    return bc


def goodsuffix_old(pat):
    m = len(pat)
    b = borders(pat)
    gs = m*[b[m]]
    for j in range(0,m):
        U = pat[j+1:]
        lenU = m-1-j
        k = m-1
        while k>b[m]:
            if k>lenU and U==pat[k-lenU:k]:
                gs[j] = k
                break
            #elif k<=lenU and pat[:k]==pat[m-k:]:
            #    gs[j] = k
            #    break
            k -= 1
    return gs    


def goodsuffix(pat):
    m = len(pat)
    Pi = borders(pat)
    PiR = borders(pat[::-1])
    gs = m*[m-Pi[m]]
    for l in range(1,m+1):
        j = m-1-PiR[l]
        if l-PiR[l] < gs[j]:
            gs[j] = l-PiR[l]
    return gs


def bm(txt, pat, gs=None, bc=None) :
    n = len(txt)
    m = len(pat)
    bc = bc or badchar(pat)
    gs = gs or goodsuffix(pat)
    i = 0
    occ = []
    while i <= n-m:
        j = m-1
        while j>=0 and txt[i+j] == pat[j]:
            j -= 1
        if j<0:
            occ.append(i)
        i += max(j-bc[ord(txt[i+j])] if j>=0 else 1, gs[j])
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
        count += 1 if occ else 0 #len(occ)
    txtfile.close()
    print("Total occurrences:",count)

def amain():
    txt = "abracadabra"
    pat = "abracadabra"
    gs = good_suffix(pat)
    print(gs)




if __name__ == "__main__":
    main()
