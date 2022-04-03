

def gray_code(n):
    g = ['0', '1']
    if n <= 0:
        return []
    for i in range(n - 1):
        g1 = ['1' + i for i in g][::-1]
        g0 = ['0' + i for i in g]
        g = g0 + g1
    return g


def K_map(s1):
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
    t = []
    """if n == len(tab):
        p = zip(*tab)
        for i in range(len(tab[0])-n + 1):
            tout = True
            for j in range(n):
                if p[j-1] != p[j] or not all(p[j]):
                    tout = False
                    break
            if tout:
                test = False
                for a in range(i+n):
                    for b in range(n):
                        if comp[b][a] == 0:
                            comp[b][a] = 1
                            test = True
                if test:
                    a.append([i-n,0-n,i,n])
    else:"""
    p = [[any(table[i:n-i][j:n-j]) for j in range(len(table[i]))] for i in range(len(table))]
    print(p)
    for a in range(len(p)):
        for b in range(len(p[a])):
            if p[a][b] and not all(comp[a:n-a][b:n-b]):
                comp[a::n-a][b::n-b] = 1
                t.append([a-n, a, b-n, b])
    return t, comp


def recherche_ligne(n, table, comp):
    t = []
    p = [[all(table[i][j:n-j])for j in range(len(table[i]))] for i in range(len(table))]
    for a in range(len(p)):
        for b in range(len(p[a])):
            if p[a][b] and not all(comp[a][b:n-b]):
                comp[a][b:n-b] = 1
                t.append([a, a, b-n, b])
    return t, comp


def recherche_colonne(n, table, comp):
    t = []
    p = [[all(table[i:n-i][j]) for j in range(len(table[0]))] for i in range(len(table))]
    for a in range(len(p)):
        for b in range(len(p[a])):
            if p[a][b] and not all(comp[a:n-a][b]):
                comp[a:n-a][b] = 1
                t.append([a - n, a, b, b])
    return t, comp


def gray_tp_propositionnell(s1):
    s = ""
    newt = []
    m = K_map(s1)
    k = min(len(m), len(m[0]))
    passe_par = [[0 for _ in range(len(m[i]))] for i in range(len(m))]
    while k > 0:
        p1, passe_par = recherchebloc(k, m, passe_par)
        p2, passe_par = recherche_ligne(k, m, passe_par)
        p3, passe_par = recherche_colonne(k, m, passe_par)
        newt.append(p1)
        newt.append(p2)
        newt.append(p3)
        k //= 2

    for i in newt:
        if i[-1] == i[-2]:
            l = [m[a] + m[-1] for a in range(i[0], i[1])]
        elif i[0] == i[1]:
            l = [m[0] + m[i] for a in range(i[2], i[3])]
        else:
            c = [[m[a] + m[b] for a in range(i[0], [1])] for b in range(i[-2],i[-1])]
            l = [item for sublist in c for item in sublist]
        t = zip(l)
        newstr = [p[0] if p[:-1] == p[1:] else -1 for p in t]
        s += '('
        for i, j in enumerate(newstr):
            if j == 1:
                s += f'x{i}'
            elif j == 0:
                s += f'~x{i}'
            s = s + "&" if 1 in newstr[j:] or 0 in newstr[j:] else s
    return s
