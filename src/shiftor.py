from bitarray import bitarray
import sys

def shift(b):
    b.pop(0)
    b.append(0)


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
    

def main() :
    ab = [chr(c) for c in range(128)]
    filename = sys.argv[1]
    pat = sys.argv[2]
    c = char_mask(ab,pat)
    txtfile  = open(filename, "r")
    count = 0
    for txt in txtfile:
        occ = shift_or(ab, txt, pat, c)
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
    occ = shift_or(ab, txt, pat, c)
    print(occ)



if __name__ == "__main__":
    main()

