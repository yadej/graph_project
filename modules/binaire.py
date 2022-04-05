def gray_code(n):
    '''

    input: n (int)
    output: g (list of char)
    returns n bits gray code in a list of char
    '''
    g = ['0', '1']
    if n <= 0:
        return []
    for i in range(n - 1):
        g1 = ['1' + i for i in g][::-1]
        g0 = ['0' + i for i in g]
        g = g0 + g1
    return g


def K_map(s1):
    '''
    input: s1 (string)
    output: t (2D vector)
    returns the Karnaugh table associated with the bit string.
    '''
    w = len(s1) - 1 if len(s1) > 5 else len(s1)
    a = len(s1)
    k = 0
    while w > 0:
        w = w // 2
        k += 1
    s1 = s1 + '0' * (2 ** k - a)
    if k % 2 == 1:
        t1 = gray_code(k // 2 + 1)
        t2 = gray_code(k // 2)
    else:
        t1 = gray_code(k // 2)
        t2 = gray_code(k // 2)
    k1 = len(t1)
    k2 = len(t2)
    t = [[0 for _ in range(k2)] for _ in range(k1)]

    for i in range(k1):
        for j in range(k2):
            p = int(t1[i] + t2[j], 2)
            if s1[p] == '1':
                t[i][j] = 1
            else:
                t[i][j] = 0
    return t


def recherchebloc(n, table, comp):
    '''
    inputs: n (int), table (list), comp: (list)
    outputs: t (list), comp (list)
    '''
    t = []
    p = [[all(table[i:n+i-1][x][j:n+j-1] for x in range(n))
         for j in range(len(table[i])-n+1)] for i in range(len(table)-n+1)]
    print(p)
    for a in range(len(p)-n+1):
        for b in range(len(p[a])-n+1):
            if p[a][b] and not all(comp[a:n+a-1][x][b:n+b-1] for x in range(n)):
                for x in range(n):
                    comp[a:n-a][x][b:n-b] = [1 for _ in range(n)]
                t.append([a, a+n, b, b+n])
    return t, comp


def recherche_ligne(n, table, comp):
    '''
    inputs: n (int), table (list), comp (list),
    outputs: t (list), comp (list)
    '''
    t = []
    p = [[all(table[i][j:n+j]) for j in range(len(table[i])-n+1)] for i in range(len(table))]
    for a in range(len(p)):
        for b in range(len(p[a])-n):
            if p[a][b] and not all(comp[a][b:n+b]):
                comp[a][b:n+b] = [1 for _ in range(n)]
                t.append([a, a, b, b+n])
    return t, comp


def recherche_colonne(n, table, comp):
    '''
    inputs: n (int), table (list), comp (list)
    outputs: t (list), comp (list)
    '''
    t = []
    p = [[all(table[i:n+i][x][j] for x in range(n)) for j in range(len(table[0]))] for i in range(len(table)-n+1)]
    print("d")
    print(p)
    print(len(p)-n)
    for a in range(len(p)-n):
        for b in range(len(p[a])):
            print("c")
            print(comp[a:n+a][0:n][b])
            if p[a][b] and not all(comp[a:n+a][0:n][b]):
                for x in range(n):
                    comp[a:n+a][x][b] = 1
                t.append([a, a + n-1, b, b])
    return t, comp


def gray_tp_propositionnell(s1):
    '''
    input: s1 (string)
    output: s (string)
    '''
    s = ""
    newt = []
    m = K_map(s1)
    k = min(len(m), len(m[0]))
    passe_par = [[0 for _ in range(len(m[i]))] for i in range(len(m))]
    while k > 1:
        p1, passe_par = recherchebloc(k//2, m, passe_par)
        p2, passe_par = recherche_ligne(k, m, passe_par)
        p3, passe_par = recherche_colonne(k, m, passe_par)
        if p1:
            newt.append(p1)
        if p2:
            newt.append(p2)
        if p3:
            newt.append(p3)
        k //= 2
    print(newt)
    print("a")
    print(passe_par)
    newt = [x for i in newt for x in i]
    print(newt)
    for i in newt:
        if i[-1] == i[-2]:
            l = [m[a] + m[-1] for a in range(i[0], i[1])]
        elif i[0] == i[1]:
            l = [m[0] + m[a] for a in range(i[2], i[3])]
        else:
            c = [[m[a] + m[b] for a in range(i[0], i[1])] for b in range(i[-2],i[-1])]
            l = [item for sublist in c for item in sublist]
        t = zip(l)
        print(list(t))
        newstr = [p[0] if p[:-1] == p[1:] else -1 for p in t]
        s += '('
        print("b")
        print(newstr)
        for a in newstr:
            for w, j in enumerate(a):
                if j == 1:
                    s += f'x{w}'
                elif j == 0:
                    s += f'~x{w}'
                s = s + "&"
            s = s[:-1]
        s += ')|'
    s = s[:-1]
    return s
