import sys


def bruteforce(txt, pat) :
    n = len(txt)
    m = len(pat)
    i = 0
    occ = []
    while i <= n-m:
        j = 0
        while j < m and txt[i+j] == pat[j]:
            j += 1
        if j == m:
            occ.append(i)
        i += 1
    return occ



def main() :
    filename = sys.argv[1]
    pat = sys.argv[2]
    txtfile  = open(filename, "r")
    for txt in txtfile:
        occ = bruteforce(txt, pat)
        if occ:
            print(txt)
            print(occ)
    txtfile.close()


if __name__ == "__main__":
    main()
