
def fsm(pat):
    n = len(pat)
    first_col = 128 * [0]
    first_col[ord(pat[0])] = 1
    n =len(pat)
    delta = [first_col]
    brd = 0
    for s in range(1,n):
        new_col = [delta[brd][i] for i in range(128)]
        new_col[ord(pat[s])] = s+1
        delta.append(new_col)
        brd = delta[brd][ord(pat[s])]
    return delta

def prefix_match(window, pat, ls):
    delta = fsm(pat)
    s = 0
    l = 0
    p = 0
    for i in range(len(window)):
        s = delta[s][ord(window[i])]
        if s > l  and i-s+1 < ls:
            l = s
            p = i-s+1
        if l==len(pat):
            break
    return (p,l)

# procurar maior prefixo de pat que ocorre em window
# antes da posicao ls
def prefix_match_bf(window, pat, ls):
    l = 0
    p = -1
    for i in range(ls):
        j = 0
        while j < len(pat) - 1 and window[i+j] == pat[j]:
            j += 1
        if j > l:
            l = j
            p = i
    return (p,l)


def lz77_encode(txt, la, ls):
    n = len(txt)
    txt = ls*"a" + txt
    i = ls
    code = []
    while i < n + ls :
        (p,l) = prefix_match(txt[i-ls: min(i+la, n+ls)], txt[i: min(i+la, n+ls)], ls)
        code.append((p,l,txt[i+l]))
        i += (l+1)
    return code


def lz77_decode(code, ls):
    txt = ls*"a"
    i = ls
    for (p,l,c) in code:
        for j in range(l):
            txt += txt[i-ls+p+j]
        txt += c
        i += (l+1)
    return txt[ls:]



def main():
    txt = "aababbabbabbc"
    ls = 4
    la = 4
    code = lz77_encode(txt,la, ls)
    decoded = lz77_decode(code, ls)
    print(code)
    print(decoded)
    assert decoded == txt


if __name__ == "__main__":
    main()
