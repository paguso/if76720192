
import sys


def borders_bf(pat):
    m = len(pat)
    b = []
    for j in range(0,m+1):
        k = j-1
        while k > 0 and pat[:k] != pat[j-k:j] :
            k -= 1
        b.append(k)
    return b


def borders(pat) :
    print("computing borders")
    m = len(pat)
    b = (m+1) * [0]
    b[0] = -1
    i = 1
    j = 0
    while i < m:
        print("i=%d"%i)
        while j < m and i+j<m and pat[i+j] == pat[j]:
            j += 1
            print(pat)
            print("%s%s"%(" "*i,j*"="))
            print("%s%s"%(" "*i,pat))
            b[i+j] = j
            print(b)
        i += max(1, j-b[j])
        j = max(0, b[j])
    return b



def kmp(txt, pat, b=None) :
    n = len(txt)
    m = len(pat)
    b = b if b else borders(pat) 
    i = 0
    occ = []
    j = 0
    while i <= n-m:
        while j < m and txt[i+j] == pat[j]:
            j += 1
        if j == m:
            occ.append(i)
        i += max(1, j-b[j])
        j = max(0, b[j])
    return occ



def main() :
    filename = sys.argv[1]
    pat = sys.argv[2]
    txtfile  = open(filename, "r")
    count = 0
    b= borders(pat)
    for txt in txtfile:
        occ = kmp(txt, pat, b)
        if occ:
            print(txt)
            print(occ)
        count += len(occ)
    txtfile.close()
    print("Total occurrences:",count)

def amain():
    txt = "abracadabra"
    pat = "abracadabra"
    brd = borders(pat)
    print(brd)




if __name__ == "__main__":
    main()
