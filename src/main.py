import json, os, sys, urllib.request, urllib.error, random
E = os.environ.get("MAKEFUN_ENV_URL") or sys.exit("no env")
NODES = 80000
T = "kkkkkkkkuuuuuuuummoqqommllmppmllkkkookkkljikkijllmmggmmlkkkkkkkkaceeeecacgkkkkgcekmnnmkeelnoonleeknoonkeelmnnmlecgkllkgcaceeeecagiiiiiigikkkkkkiiklmmlkiillmmlliikmmmmkiimmmmmmiilkkkkligiiiiiigkkkkkkkklmmmmmmljkkkkkkjjkkkkkkjjkkkkkkjjkkkkkkjjkkkkkkjkkkllkkkgiijjiigikkkkkkiikllllkijkllllkjkkllllkjilllllkiiklkkkkigiijjiigeccaacceeccaacceeccaacceeccaaccegeecceegiggggggiookkkkoooqmkkmqoaceggecaegikkigeeioqqoieeiqssqieeiqssqieeioqqoieeekkkkeeaeeeeeea"
PS = [[(ord(T[i * 64 + j]) - 107) * 5 for j in range(64)] for i in range(7)]
V = (0, 100, 320, 330, 500, 900, 0)
PASS = (0, 5, 10, 20, 35, 60, 100, 0)
SQS = [r * 16 + f for r in range(8) for f in range(8)]
KN = (31, 33, 14, 18, -31, -33, -14, -18)
KG = (1, -1, 16, -16, 15, 17, -15, -17)
BD = (15, 17, -15, -17)
RD = (1, -1, 16, -16)
_R = random.Random(20261113)
ZP = [[_R.getrandbits(64) for _ in range(128)] for _ in range(12)]
ZS = _R.getrandbits(64)
ZC = [_R.getrandbits(64) for _ in range(16)]
ZE = [_R.getrandbits(64) for _ in range(8)]
b = [0] * 128
D = 0
Y = 0
ep = -1
H = 0
Z = 0
wk = 4
bk = 116
st = []
TT = {}
KIL = [[0, 0] for _ in range(128)]
HIS = [0] * 32768
n = 0
TOT = 0
rep = set()


def W(path, body):
    req = urllib.request.Request(E + path, data=json.dumps(body).encode(),
                                 headers={"content-type": "application/json"})
    try:
        with urllib.request.urlopen(req) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"{path}: HTTP {e.code}")


def F(fen):
    global b, D, Y, ep, H, Z, wk, bk
    b = [0] * 128
    parts = fen.split()
    mp = {"P": 1, "N": 2, "B": 3, "R": 4, "Q": 5, "K": 6,
          "p": -1, "n": -2, "b": -3, "r": -4, "q": -5, "k": -6}
    for i, row in enumerate(parts[0].split("/")):
        f = 0
        for c in row:
            if c.isdigit():
                f += int(c)
            else:
                b[(7 - i) * 16 + f] = mp[c]
                f += 1
    D = 0 if parts[1] == "w" else 1
    Y = 0
    if len(parts) > 2:
        for c in parts[2]:
            Y |= {"K": 1, "Q": 2, "k": 4, "q": 8}.get(c, 0)
    ep = -1
    if len(parts) > 3 and parts[3] != "-":
        ep = (int(parts[3][1]) - 1) * 16 + (ord(parts[3][0]) - 97)
    H = int(parts[4]) if len(parts) > 4 else 0
    Z = 0
    for sq in SQS:
        p = b[sq]
        if p:
            Z ^= ZP[(p - 1) if p > 0 else (5 - p)][sq]
            if p == 6:
                wk = sq
            elif p == -6:
                bk = sq
    if D:
        Z ^= ZS
    Z ^= ZC[Y]
    if ep >= 0:
        Z ^= ZE[ep & 7]


def A(sq, by_white):
    if by_white:
        for t in (sq - 15, sq - 17):
            if t & 0x88 == 0 and b[t] == 1:
                return True
    else:
        for t in (sq + 15, sq + 17):
            if t & 0x88 == 0 and b[t] == -1:
                return True
    for d in KN:
        t = sq + d
        if t & 0x88 == 0 and b[t] == (2 if by_white else -2):
            return True
    for d in KG:
        t = sq + d
        if t & 0x88 == 0 and b[t] == (6 if by_white else -6):
            return True
    for d in BD:
        t = sq + d
        while t & 0x88 == 0:
            p = b[t]
            if p:
                if p == (3 if by_white else -3) or p == (5 if by_white else -5):
                    return True
                break
            t += d
    for d in RD:
        t = sq + d
        while t & 0x88 == 0:
            p = b[t]
            if p:
                if p == (4 if by_white else -4) or p == (5 if by_white else -5):
                    return True
                break
            t += d
    return False


def K(w):
    return wk if w else bk


def G(caps_only=False):
    ms = []
    w = D == 0
    for f in SQS:
        p = b[f]
        if p == 0 or (p > 0) != w:
            continue
        ap = abs(p)
        if ap == 1:
            d = 16 if w else -16
            t = f + d
            if b[t] == 0:
                if not caps_only:
                    r = t >> 4
                    if r == (7 if w else 0):
                        for pr in (5, 4, 3, 2):
                            ms.append(f | (t << 7) | (pr << 14))
                    else:
                        ms.append(f | (t << 7))
                        if (f >> 4) == (1 if w else 6):
                            t2 = f + 2 * d
                            if b[t2] == 0:
                                ms.append(f | (t2 << 7))
            for dt in (d - 1, d + 1):
                t = f + dt
                if t & 0x88:
                    continue
                q = b[t]
                if q and (q > 0) != w:
                    r = t >> 4
                    if r == (7 if w else 0):
                        for pr in (5, 4, 3, 2):
                            ms.append(f | (t << 7) | (pr << 14))
                    else:
                        ms.append(f | (t << 7))
                elif t == ep:
                    ms.append(f | (t << 7))
        elif ap in (2, 6):
            for d in (KN if ap == 2 else KG):
                t = f + d
                if t & 0x88:
                    continue
                q = b[t]
                if q == 0:
                    if not caps_only:
                        ms.append(f | (t << 7))
                elif (q > 0) != w:
                    ms.append(f | (t << 7))
        else:
            for d in (BD if ap == 3 else RD if ap == 4 else BD + RD):
                t = f + d
                while t & 0x88 == 0:
                    q = b[t]
                    if q == 0:
                        if not caps_only:
                            ms.append(f | (t << 7))
                    else:
                        if (q > 0) != w:
                            ms.append(f | (t << 7))
                        break
                    t += d
    if not caps_only:
        if w:
            if Y & 1 and b[5] == 0 and b[6] == 0 and b[4] == 6 and b[7] == 4 \
                    and not A(4, False) and not A(5, False) and not A(6, False):
                ms.append(4 | (6 << 7))
            if Y & 2 and b[3] == 0 and b[2] == 0 and b[1] == 0 and b[4] == 6 and b[0] == 4 \
                    and not A(4, False) and not A(3, False) and not A(2, False):
                ms.append(4 | (2 << 7))
        else:
            if Y & 4 and b[117] == 0 and b[118] == 0 and b[116] == -6 and b[119] == -4 \
                    and not A(116, True) and not A(117, True) and not A(118, True):
                ms.append(116 | (118 << 7))
            if Y & 8 and b[115] == 0 and b[114] == 0 and b[113] == 0 and b[116] == -6 and b[112] == -4 \
                    and not A(116, True) and not A(115, True) and not A(114, True):
                ms.append(116 | (114 << 7))
    return ms


def M(m):
    global D, Y, ep, H, Z, wk, bk
    f = m & 127
    t = (m >> 7) & 127
    pr = (m >> 14) & 7
    p = b[f]
    cap = b[t]
    epcap = -1
    if abs(p) == 1 and t == ep and cap == 0:
        epcap = t - 16 if D == 0 else t + 16
        cap = b[epcap]
    st.append((m, cap, epcap, Y, ep, H, Z))
    Z ^= ZP[(p - 1) if p > 0 else (5 - p)][f]
    if cap:
        Z ^= ZP[(cap - 1) if cap > 0 else (5 - cap)][epcap if epcap >= 0 else t]
    Z ^= ZC[Y]
    if ep >= 0:
        Z ^= ZE[ep & 7]
    np = pr * (1 if D == 0 else -1) if pr else p
    b[t] = np
    Z ^= ZP[(np - 1) if np > 0 else (5 - np)][t]
    b[f] = 0
    if epcap >= 0:
        b[epcap] = 0
    if abs(p) == 6:
        if D == 0:
            wk = t
        else:
            bk = t
    if abs(p) == 6 and abs(t - f) == 2:
        if t == 6:
            b[5] = b[7]; b[7] = 0
            Z ^= ZP[3][7] ^ ZP[3][5]
        elif t == 2:
            b[3] = b[0]; b[0] = 0
            Z ^= ZP[3][0] ^ ZP[3][3]
        elif t == 118:
            b[117] = b[119]; b[119] = 0
            Z ^= ZP[9][119] ^ ZP[9][117]
        elif t == 114:
            b[115] = b[112]; b[112] = 0
            Z ^= ZP[9][112] ^ ZP[9][115]
    if abs(p) == 6:
        Y &= 12 if D == 0 else 3
    if f == 0 or t == 0:
        Y &= ~2
    if f == 7 or t == 7:
        Y &= ~1
    if f == 112 or t == 112:
        Y &= ~8
    if f == 119 or t == 119:
        Y &= ~4
    Z ^= ZC[Y]
    ep = -1
    if abs(p) == 1 and abs(t - f) == 32:
        ep = (f + t) // 2
        Z ^= ZE[ep & 7]
    H = 0 if abs(p) == 1 or cap else H + 1
    D ^= 1
    Z ^= ZS


def U():
    global D, Y, ep, H, Z, wk, bk
    m, cap, epcap, Y, ep, H, Z = st.pop()
    f = m & 127
    t = (m >> 7) & 127
    pr = (m >> 14) & 7
    D ^= 1
    p = b[t]
    if abs(p) == 6:
        if D == 0:
            wk = f
        else:
            bk = f
    if abs(p) == 6 and abs(t - f) == 2:
        if t == 6:
            b[7] = b[5]; b[5] = 0
        elif t == 2:
            b[0] = b[3]; b[3] = 0
        elif t == 118:
            b[119] = b[117]; b[117] = 0
        elif t == 114:
            b[112] = b[115]; b[115] = 0
    b[f] = (1 if D == 0 else -1) if pr else p
    b[t] = 0
    if cap:
        b[epcap if epcap >= 0 else t] = cap


def e():
    s = 0
    wbp = bbp = 0
    wp = [0] * 8
    bp = [0] * 8
    phase = 0
    for sq in SQS:
        p = b[sq]
        if not p:
            continue
        ap = abs(p)
        r = sq >> 4
        f = sq & 7
        if p > 0:
            s += V[ap] + PS[ap - 1][(7 - r) * 8 + f]
            if ap == 3:
                wbp += 1
            elif ap == 1:
                wp[f] += 1
            else:
                phase += V[ap]
        else:
            s -= V[ap] + PS[ap - 1][r * 8 + f]
            if ap == 3:
                bbp += 1
            elif ap == 1:
                bp[f] += 1
            else:
                phase += V[ap]
    if wbp >= 2:
        s += 30
    if bbp >= 2:
        s -= 30
    for f in range(8):
        if wp[f] > 1:
            s -= 8 * (wp[f] - 1)
        if bp[f] > 1:
            s += 8 * (bp[f] - 1)
        if wp[f] and not (wp[f - 1] if f else 0) and not (wp[f + 1] if f < 7 else 0):
            s -= 12
        if bp[f] and not (bp[f - 1] if f else 0) and not (bp[f + 1] if f < 7 else 0):
            s += 12
    bmax = [-1] * 8
    wmin = [8] * 8
    for sq in SQS:
        p = b[sq]
        if abs(p) != 1:
            continue
        r = sq >> 4
        f = sq & 7
        if p > 0:
            if r < wmin[f]:
                wmin[f] = r
        elif r > bmax[f]:
            bmax[f] = r
    for sq in SQS:
        p = b[sq]
        if abs(p) != 1:
            continue
        r = sq >> 4
        f = sq & 7
        if p > 0:
            if all(bmax[ff] <= r for ff in (f - 1, f, f + 1) if 0 <= ff < 8):
                s += PASS[r]
        elif all(wmin[ff] >= r for ff in (f - 1, f, f + 1) if 0 <= ff < 8):
            s -= PASS[7 - r]
    if phase <= 1300:
        for sq in SQS:
            p = b[sq]
            if abs(p) == 6:
                r = sq >> 4
                f = sq & 7
                if p > 0:
                    s += PS[6][(7 - r) * 8 + f] - PS[5][(7 - r) * 8 + f]
                else:
                    s -= PS[6][r * 8 + f] - PS[5][r * 8 + f]
    return s if D == 0 else -s


def O(ms, tt_move, ply):
    def sc(m):
        if m == tt_move:
            return 1 << 28
        t = (m >> 7) & 127
        cap = b[t]
        if cap:
            return 1000000 + V[abs(cap)] * 16 - V[abs(b[m & 127])] // 16
        if m == KIL[ply][0]:
            return 900000
        if m == KIL[ply][1]:
            return 800000
        return HIS[(D << 14) | (m & 16383)]
    ms.sort(key=sc, reverse=True)
    return ms


class Abort(Exception):
    pass


def Q(alpha, beta, ply):
    global n
    n += 1
    if n > NODES:
        raise Abort
    stand = e()
    if stand >= beta:
        return beta
    if stand > alpha:
        alpha = stand
    c = A(K(D == 0), D == 1)
    ms = G(caps_only=not c)
    O(ms, 0, ply)
    for m in ms:
        M(m)
        try:
            if not A(K(D == 1), D == 0):
                sc = -Q(-beta, -alpha, ply + 1)
                if sc >= beta:
                    return beta
                if sc > alpha:
                    alpha = sc
        finally:
            U()
    return alpha


def S(alpha, beta, depth, ply):
    global n
    n += 1
    if n > NODES:
        raise Abort
    if H >= 100:
        return 0
    if Z in rep:
        return 0
    rep.add(Z)
    try:
        return R(alpha, beta, depth, ply)
    finally:
        rep.discard(Z)


def R(alpha, beta, depth, ply):
    c = A(K(D == 0), D == 1)
    if c:
        depth += 1
    if depth <= 0:
        return Q(alpha, beta, ply)
    a0 = alpha
    tt = TT.get(Z)
    tt_move = 0
    if tt and tt[0] >= depth:
        _, fl, val, mv = tt
        if fl == 0:
            return val
        if fl == 1 and val > alpha:
            alpha = val
        elif fl == 2 and val < beta:
            beta = val
        if alpha >= beta:
            return val
        tt_move = mv
    ms = G()
    O(ms, tt_move, ply)
    best = -1000000
    bestm = ms[0] if ms else 0
    found = False
    for m in ms:
        M(m)
        try:
            if A(K(D == 1), D == 0):
                continue
            found = True
            sc = -S(-beta, -alpha, depth - 1, ply + 1)
        finally:
            U()
        if sc > best:
            best = sc
            bestm = m
        if sc > alpha:
            alpha = sc
        if alpha >= beta:
            if not b[(m >> 7) & 127]:
                if KIL[ply][0] != m:
                    KIL[ply][1] = KIL[ply][0]
                    KIL[ply][0] = m
                HIS[(D << 14) | (m & 16383)] += depth * depth
            break
    if not found:
        return -100000 + ply if c else 0
    if best <= a0:
        fl = 2
    elif best >= beta:
        fl = 1
    else:
        fl = 0
    TT[Z] = (depth, fl, best, bestm)
    return best


def B():
    global n, TOT
    ms = []
    for m in G():
        M(m)
        if not A(K(D == 1), D == 0):
            ms.append(m)
        U()
    if not ms:
        return None
    if len(ms) == 1:
        return ms[0]
    bestm = ms[0]
    try:
        for d in range(1, 64):
            n = 0
            S(-1000000, 1000000, d, 0)
            TOT += n
            tt = TT.get(Z)
            if tt:
                bestm = tt[3]
    except Abort:
        TOT += n
    return bestm


def C(m):
    f = m & 127
    t = (m >> 7) & 127
    pr = (m >> 14) & 7
    s = "abcdefgh"[f & 7] + str((f >> 4) + 1) + "abcdefgh"[t & 7] + str((t >> 4) + 1)
    if pr:
        s += "nbrq"[pr - 2]
    return s


def main():
    while True:
        g = W("/game", {})
        if g["status"] == "done":
            break
        while g["status"] == "your_move":
            F(g["fen"])
            m = B()
            mv = C(m) if m is not None else None
            legal = g["legal_moves"]
            if mv not in legal:
                mv = legal[0]
            g = W("/move", {"game": g["game"], "move": mv})
        print(f"game {g['game']}: {g['outcome']} by {g['reason']}", file=sys.stderr)
    print(f"done: {g.get('wins')} won, {g.get('draws')} drawn, {g.get('losses')} lost; nodes {TOT}", file=sys.stderr)


if __name__ == "__main__":
    main()
