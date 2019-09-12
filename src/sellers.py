import sys

def phi(a,b):
    return 0 if a==b else 1

def dist(x,y):
    n = len(x)
    m = len(y)
    if n > m:
        return dist(y,x)
    # m >= n
    d = [ range(n+1), (n+1)*[1] ]
    prev = 0
    cur = 1
    for i in range(1,m+1):
        d[cur][0] = i
        for j in range(1,n+1):
            d[cur][j] = min( d[prev][j-1] + phi(x[j-1],y[i-1]) , d[prev][j] + 1, d[cur][j-1] + 1 )
        print(d[prev])
        cur = (cur+1)%2
        prev = (prev+1)%2
    print(d[prev])
    return d[prev][n]



def sellers(txt, pat, err):
    m = len(pat)
    n = len(txt)
    occ = []
    d = [ range(m+1), (m+1)*[0] ]
    if d[0][m] <= err:
        occ.append(0)
    prev = 0
    cur = 1
    for j in range(1,n+1):
        for i in range(1,m+1):
            d[cur][i] = min( d[prev][i-1] + phi(pat[i-1],txt[j-1]) , d[prev][i] + 1, d[cur][i-1] + 1 )
        #print(d[prev])
        if d[cur][m] <= err:
            occ.append(j-1)
        cur = (cur+1)%2
        prev = (prev+1)%2
    return occ

    

def amain():
    txt="abadac"
    pat="cada"
    err = 2
    occ = sellers(txt, pat, 2)
    print(occ)

def main() :
    filename = sys.argv[1]
    pat = sys.argv[2]
    txtfile  = open(filename, "r")
    err = int(sys.argv[3])
    count = 0
    for txt in txtfile:
        occ = sellers(txt, pat,err)
        if occ:
            print(txt)
            print(occ)
        count += 1 if occ else 0 #len(occ)
    txtfile.close()
    print("Total line with occurrences:",count)



if __name__ == "__main__":
    main()
