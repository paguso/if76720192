
from bitarray import bitarray
import sys

def shift(b):
    b.pop(0)
    b.append(0)

def shift_left(b):
    r = b[1:]
    r.append(0)
    return r


def char_mask(ab, pat):
    m = len(pat)
    c = {}
    one = bitarray((m-1)*"0"+"1")
    stamp = bitarray((m-1)*"1"+"0")
    for a in ab:
        c[a] = bitarray(m*"1")
    for a in pat:
        c[a] &= stamp
        shift(stamp) 
        stamp |= one
    return c


def shift_or(ab, txt, pat, cmask=None):
    c = cmask if cmask else char_mask(ab,pat)
    m = len(pat)
    n = len(txt)
    s = bitarray(m*"1")
    #print ("init s=", s)
    occ = []
    for i in range(n):
        shift(s)
        s |= c[txt[i]]
        #print ("s[",i,"]=",s)
        if not s[0]:
            occ.append(i-m+1)
    return occ


def wumanber(ab, txt, pat, err, cmask=None):
    n = len(txt)
    m = len(pat)
    C = cmask if cmask else char_mask(ab,pat)
    Sprev = []
    Sprev.append(bitarray(m*'1'))
    for q in range(err):
        Sprev.append(shift_left(Sprev[q]))
    #print Sprev
    occ = []
    for j in range(n):
        S = [ shift_left(Sprev[0]) | C[txt[j]] ]
        for q in range(1,err+1):
            S.append( (shift_left(Sprev[q]) | C[txt[j]]) & shift_left(Sprev[q-1]) & shift_left(S[q-1]) & Sprev[q-1] )
        if not S[err][0]:
            occ.append(j)
        Sprev = S
    return occ


def main() :
    ab = [chr(c) for c in range(128)]
    filename = sys.argv[1]
    pat = sys.argv[2]
    err = int(sys.argv[3])
    c = char_mask(ab,pat)
    txtfile  = open(filename, "r")
    count = 0
    for txt in txtfile:
        occ = wumanber(ab, txt, pat, err, c)
        if occ:
            print(txt)
            print(occ)
        count += 1 if occ else 0 #len(occ)
    txtfile.close()
    print("Total occurrences:",count)

def amain():
    ab="abcdr"
    txt = "abracadabra"
    pat = "abra"
    c = char_mask(ab, pat)
    err = 1
    occ = wumanber(ab, txt, pat, err,  c)
    print(occ)



if __name__ == "__main__":
    main()

