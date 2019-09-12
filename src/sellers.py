

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

    

def main():
    x="abracadabra"
    y="acabradaabra"
    d = dist(x,y)
    print("d=",d)



if __name__ == "__main__":
    main()
