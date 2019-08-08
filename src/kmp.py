
import sys


def borders(pat):
    m = len(pat)
    b = []
    for j in range(0,m+1):
        k = j-1
        while k > 0 and pat[:k] != pat[j-k:j] :
            k -= 1
        b.append(k)
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
    pat = "abra"
    occ = kmp(txt,pat)
    print(occ)



if __name__ == "__main__":
    main()
