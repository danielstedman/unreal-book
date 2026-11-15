#!/usr/bin/env python3
"""Arrangement engine for Danny's Unreal Book.

Parses a small subset of ABC notation, transposes it with correct spelling,
generates left-hand accompaniment from chord symbols, and writes clean
two-voice (grand staff) ABC for abcjs.
"""
from fractions import Fraction as Fr
import re, copy

LET = 'CDEFGAB'
BASE = [0, 2, 4, 5, 7, 9, 11]
SHARPS = [3, 0, 4, 1, 5, 2, 6]
FLATS = [6, 2, 5, 1, 4, 0, 3]
MAJ = {'C': 0, 'G': 1, 'D': 2, 'A': 3, 'E': 4, 'B': 5, 'F#': 6, 'C#': 7,
       'F': -1, 'Bb': -2, 'Eb': -3, 'Ab': -4, 'Db': -5, 'Gb': -6, 'Cb': -7}
E8 = Fr(1, 8)


class P:
    __slots__ = ('l', 'a', 'o')

    def __init__(s, l, a, o):
        s.l, s.a, s.o = l, a, o

    @property
    def midi(s):
        return 12 * (s.o + 1) + BASE[s.l] + s.a

    def tr(s, dl, ds):
        o, l = divmod(s.o * 7 + s.l + dl, 7)
        a = s.midi + ds - (12 * (o + 1) + BASE[l])
        return P(l, a, o)

    def __repr__(s):
        return tname(s.l, s.a) + str(s.o)


def tname(l, a):
    return LET[l] + ('#' * a if a > 0 else 'b' * -a)


def parse_tone(s):
    """'Bb' -> (letter, acc)"""
    l = LET.index(s[0])
    a = s.count('#') - s.count('b')
    return l, a


def parse_key(k):
    minor = k.endswith('m')
    t = k[:-1] if minor else k
    l, a = parse_tone(t)
    return l, a, minor


def key_sig(k):
    l, a, minor = parse_key(k)
    if minor:
        p = P(l, a, 4).tr(2, 3)
        name = tname(p.l, p.a)
    else:
        name = tname(l, a)
    n = MAJ[name]
    sig = [0] * 7
    if n > 0:
        for x in SHARPS[:n]:
            sig[x] = 1
    else:
        for x in FLATS[:-n]:
            sig[x] = -1
    return sig


def interval(src, dst):
    l1, a1, _ = parse_key(src)
    l2, a2, _ = parse_key(dst)
    dl = (l2 - l1) % 7
    ds = (BASE[l2] + a2 - BASE[l1] - a1) % 12
    if dl == 0 and ds > 6:
        ds -= 12
    return dl, ds


class Ev:
    __slots__ = ('pitches', 'dur', 'wdur', 'tie', 'sym', 'tup', 'pre', 'lyr')

    def __init__(s, pitches, dur, tie=False, sym=None, tup=None, wdur=None):
        s.pitches, s.dur, s.tie, s.sym, s.tup = pitches, dur, tie, sym, tup
        s.wdur = dur if wdur is None else wdur
        s.pre = ''
        s.lyr = None


TOK = re.compile(r'''
 (?P<sym>"[^"]*")
|(?P<deco>![^!\s]*!)
|(?P<field>\[[A-Za-z]:[^\]]*\])
|(?P<bar>:\|\]|\|\]|\|\||\[\||\|:|:\||::|\|)
|(?P<ending>\[\d)
|(?P<tup>\(\d)
|(?P<chord>\[(?P<cn>[^\]]*)\](?P<cd>\d*/*\d*)(?P<ct>-?))
|(?P<note>(?P<acc>\^\^|\^|__|_|=)?(?P<let>[A-Ga-g])(?P<oct>[,']*)(?P<nd>\d*/*\d*)(?P<nt>-?))
|(?P<rest>[zx](?P<rd>\d*/*\d*))
|(?P<brk>[<>])
|(?P<ovl>&)
|(?P<grace>\{[^}]*\})
|(?P<skip>[()\s\\~.HLMOPSTuvy$\d-])
''', re.X)
NOTE = re.compile(r"(\^\^|\^|__|_|=)?([A-Ga-g])([,']*)")
ACC = {'^^': 2, '^': 1, '=': 0, '_': -1, '__': -2, None: None}
ACCS = {2: '^^', 1: '^', 0: '=', -1: '_', -2: '__'}


def pdur(s):
    m = re.match(r'(\d*)(/*)(\d*)$', s)
    n = int(m.group(1)) if m.group(1) else 1
    if m.group(3):
        d = int(m.group(3))
    else:
        d = 2 ** len(m.group(2))
    return Fr(n, d)


def parse(body, key, L=E8, scale=1, keep_text=False):
    """Return list of bars; each bar is a list of layers; each layer a list of Ev."""
    sig = key_sig(key)
    bars, layers, cur, state = [], [], [], {}
    sym = None
    pre = ['']
    tup = [0, None]
    pend_brk = None

    def mk(acc, let, octs):
        l = LET.index(let.upper())
        o = 4 if let.isupper() else 5
        o += octs.count("'") - octs.count(',')
        a = ACC[acc or None]
        if a is None:
            a = state.get((l, o), sig[l])
        else:
            state[(l, o)] = a
        return P(l, a, o)

    def add(pitches, d, tie):
        nonlocal sym, pend_brk
        w = d * L * scale
        real = w
        t = None
        if tup[0] > 0:
            real = w * Fr(2, 3)
            if tup[0] == 3:
                t = 3
            tup[0] -= 1
        e = Ev(pitches, real, tie, sym, t, w)
        e.pre, pre[0] = pre[0], ''
        sym = None
        if pend_brk:
            prev, kind = pend_brk
            if kind == '>':
                prev.dur = prev.wdur = prev.dur * Fr(3, 2)
                e.dur = e.wdur = e.dur / 2
            else:
                prev.dur = prev.wdur = prev.dur / 2
                e.dur = e.wdur = e.dur * Fr(3, 2)
            pend_brk = None
        cur.append(e)

    def endbar():
        nonlocal layers, cur, state
        if cur:
            layers.append(cur)
        if layers:
            bars.append(layers)
        layers, cur, state = [], [], {}

    pos = 0
    while pos < len(body):
        m = TOK.match(body, pos)
        if not m:
            raise ValueError('ABC parse error at: ' + body[pos:pos + 30])
        pos = m.end()
        k = m.lastgroup
        if m.group('sym'):
            sym = m.group('sym')[1:-1]
            if sym[:1] in '^_<>@':
                if keep_text:
                    pre[0] += '"%s"' % sym
                sym = None
        elif m.group('field'):
            if m.group('field').startswith('[K:clef'):
                pre[0] += m.group('field')
        elif m.group('bar'):
            endbar()
        elif m.group('tup'):
            if m.group('tup') != '(3':
                raise ValueError('only (3 tuplets supported')
            tup[0] = 3
        elif m.group('chord') is not None and m.group('chord'):
            ps = [mk(*x) for x in NOTE.findall(m.group('cn'))]
            cd = m.group('cd')
            if not cd:
                inner = re.search(r"[A-Ga-g][,']*(\d*/*\d*)", m.group('cn'))
                cd = inner.group(1) if inner else ''
            add(ps, pdur(cd), bool(m.group('ct')))
        elif m.group('note'):
            add([mk(m.group('acc'), m.group('let'), m.group('oct'))], pdur(m.group('nd')), bool(m.group('nt')))
        elif m.group('rest'):
            add([], pdur(m.group('rd')), False)
        elif m.group('brk'):
            pend_brk = (cur[-1], m.group('brk'))
        elif m.group('ovl'):
            layers.append(cur)
            cur = []
    endbar()
    return bars


def bdur(bar):
    return sum((e.dur for e in bar[0]), Fr(0))


def meter(M):
    a, b = M.split('/')
    a, b = int(a), int(b)
    blen = Fr(a, b)
    if b == 8 and a % 3 == 0:
        beam = Fr(3, 8)
    elif b == 2:
        beam = Fr(1, 2)
    else:
        beam = Fr(1, 4)
    return blen, beam


def check(bars, blen, label):
    """Every layer of every bar must fill the bar (first/last may be partial)."""
    errs = []
    for i, bar in enumerate(bars):
        for j, lay in enumerate(bar):
            d = sum((e.dur for e in lay), Fr(0))
            if d == blen:
                continue
            if j == 0 and i == 0 and d < blen:
                continue
            if j == 0 and i == len(bars) - 1 and d < blen:
                continue
            errs.append('%s: bar %d layer %d has %s, expected %s' % (label, i + 1, j, d, blen))
    return errs


def transpose(bars, dl, ds, octs=0):
    out = copy.deepcopy(bars)
    for bar in out:
        for lay in bar:
            for e in lay:
                e.pitches = [p.tr(dl, ds).tr(7 * octs, 12 * octs) for p in e.pitches]
                if e.sym:
                    e.sym = tr_chord(e.sym, dl, ds)
    return out


CH = re.compile(r'^([A-G][#b]?)([^/]*)(?:/([A-G][#b]?))?$')


def tr_tone(t, dl, ds):
    l, a = parse_tone(t)
    p = P(l, a, 4).tr(dl, ds)
    return tname(p.l, p.a)


def tr_chord(c, dl, ds):
    m = CH.match(c)
    if not m:
        return c
    s = tr_tone(m.group(1), dl, ds) + m.group(2)
    if m.group(3):
        s += '/' + tr_tone(m.group(3), dl, ds)
    return s


QUAL = [
    ('maj7', [(2, 4), (4, 7), (6, 11)]), ('m7b5', [(2, 3), (4, 6), (6, 10)]),
    ('dim7', [(2, 3), (4, 6), (6, 9)]), ('dim', [(2, 3), (4, 6)]),
    ('m7', [(2, 3), (4, 7), (6, 10)]), ('m6', [(2, 3), (4, 7), (5, 9)]),
    ('sus4', [(3, 5), (4, 7)]), ('sus', [(3, 5), (4, 7)]), ('aug', [(2, 4), (4, 8)]), ('+', [(2, 4), (4, 8)]),
    ('m', [(2, 3), (4, 7)]), ('7', [(2, 4), (4, 7), (6, 10)]), ('9', [(2, 4), (4, 7), (6, 10)]),
    ('6', [(2, 4), (4, 7), (5, 9)]), ('', [(2, 4), (4, 7)]),
    # chords without a third
    ('5', [(4, 7)]), ('sus2', [(1, 2), (4, 7)]), ('7sus4', [(3, 5), (4, 7), (6, 10)]), ('7sus', [(3, 5), (4, 7), (6, 10)]),
    ('11', [(3, 5), (4, 7), (6, 10)]),
    # colour chords, reduced to what the voicings use (3rd, 5th, one extra tone)
    ('add9', [(2, 4), (4, 7), (1, 2)]), ('add2', [(2, 4), (4, 7), (1, 2)]), ('madd9', [(2, 3), (4, 7), (1, 2)]),
    ('maj9', [(2, 4), (4, 7), (6, 11)]), ('m9', [(2, 3), (4, 7), (6, 10)]), ('m11', [(2, 3), (4, 7), (6, 10)]),
    ('13', [(2, 4), (4, 7), (6, 10)]), ('7b9', [(2, 4), (4, 7), (6, 10)]), ('7#9', [(2, 4), (4, 7), (6, 10)]),
    ('7#5', [(2, 4), (4, 8), (6, 10)]), ('aug7', [(2, 4), (4, 8), (6, 10)]), ('mmaj7', [(2, 3), (4, 7), (6, 11)]),
    ('m7b5', [(2, 3), (4, 6), (6, 10)]), ('6/9', [(2, 4), (4, 7), (5, 9)]),
]
NO_THIRD = ('5', 'sus2', 'sus4', 'sus', '7sus4', '7sus', '11')


def chord_tones(c):
    """-> (list of (letter, acc) tone classes root-first, bass tone class)"""
    m = CH.match(c)
    if not m:
        raise ValueError('bad chord ' + c)
    rl, ra = parse_tone(m.group(1))
    q = m.group(2)
    for name, ivs in QUAL:
        if q == name:
            break
    else:
        raise ValueError('unknown chord quality: ' + c)
    root = P(rl, ra, 4)
    tones = [(rl, ra)]
    for dl, ds in ivs:
        p = root.tr(dl, ds)
        tones.append((p.l, p.a))
    bass = parse_tone(m.group(3)) if m.group(3) else tones[0]
    return tones, bass


def place(tc, lo):
    """lowest pitch of tone class tc with midi >= lo"""
    for o in range(0, 8):
        p = P(tc[0], tc[1], o)
        if p.midi >= lo:
            return p


def ladder(c, lo, n=7):
    tones, bass = chord_tones(c)
    out = [place(bass, lo)]
    pcs = [(BASE[l] + a) % 12 for l, a in tones]
    bpc = (BASE[bass[0]] + bass[1]) % 12
    i = pcs.index(bpc) if bpc in pcs else -1
    while len(out) < n:
        i = (i + 1) % len(tones)
        out.append(place(tones[i], out[-1].midi + 1))
    return out


VALID = [Fr(1), Fr(3, 4), Fr(1, 2), Fr(3, 8), Fr(1, 4), Fr(3, 16), Fr(1, 8), Fr(3, 32), Fr(1, 16), Fr(1, 32)]


def split_dur(d):
    if d == Fr(3, 2):
        return [d]
    out = []
    while d > 0:
        for v in VALID:
            if v <= d:
                out.append(v)
                d -= v
                break
        else:
            raise ValueError('cannot split duration')
    return out


def held(pitches, d):
    parts = split_dur(d)
    evs = [Ev(list(pitches), x) for x in parts]
    if pitches:
        for e in evs[:-1]:
            e.tie = True
    return evs


def dur_str(w, L):
    r = w / L
    n, d = r.numerator, r.denominator
    if d == 1:
        return '' if n == 1 else str(n)
    if n == 1:
        return '/' if d == 2 else '/%d' % d
    return '%d/%d' % (n, d)


def pname(p, sig, state):
    cur = state.get((p.l, p.o), sig[p.l])
    s = ''
    if p.a != cur:
        s = ACCS[p.a]
        state[(p.l, p.o)] = p.a
    if p.o >= 5:
        return s + LET[p.l].lower() + "'" * (p.o - 5)
    return s + LET[p.l] + ',' * (4 - p.o)


def emit_bar(bar, sig, L, beam):
    outs = []
    state = {}
    for lay in bar:
        t = Fr(0)
        s = ''
        for e in lay:
            if t > 0 and (t % beam == 0 or e.tup):
                s += ' '
            if e.pre:
                s += e.pre
            if e.sym:
                s += '"%s"' % e.sym
            if e.tup:
                s += '(3'
            if not e.pitches:
                s += 'z'
            elif len(e.pitches) == 1:
                s += pname(e.pitches[0], sig, state)
            else:
                s += '[' + ''.join(pname(p, sig, state) for p in sorted(e.pitches, key=lambda p: p.midi)) + ']'
            s += dur_str(e.wdur, L)
            if e.tie:
                s += '-'
            t += e.dur
        outs.append(s)
    return ' & '.join(outs)


def emit(v1, v2, key, M, L, Q, per_line=4):
    sig = key_sig(key)
    blen, beam = meter(M)
    Ls = '%d/%d' % (L.numerator, L.denominator)
    head = ['X:1', 'M:' + M, 'L:' + Ls, 'Q:' + Q, '%%staves {1 2}', 'V:1 clef=treble', 'V:2 clef=bass', 'K:' + key]
    b1 = [emit_bar(b, sig, L, beam) for b in v1]
    b2 = [emit_bar(b, sig, L, beam) for b in v2]
    lines = []
    n = len(b1)
    for i in range(0, n, per_line):
        end = ' |]' if i + per_line >= n else ' |'
        lines.append('[V:1] ' + ' | '.join(b1[i:i + per_line]) + end)
        notes = [e for b in v1[i:i + per_line] for e in b[0] if e.pitches]
        if any(e.lyr for e in notes):
            out = ''
            for e in notes:
                tk = e.lyr or '*'
                out += tk if (not out or out.endswith('-')) else ' ' + tk
            lines.append('w: ' + out)
        lines.append('[V:2] ' + ' | '.join(b2[i:i + per_line]) + end)
    return '\n'.join(head + lines)


# ---------------------------------------------------------------- accompaniment

def chord_segments(bars, blen, chords):
    """chords: 'G|G . D7|...' one entry per full bar (pickup excluded).
    Returns per-bar list of (start, dur, chord). Also honours inline symbols."""
    pickup = bdur(bars[0]) < blen and len(bars) > 1
    segs = []
    last = None
    cb = [c.strip() for c in chords.strip().strip('|').split('|')] if chords else None
    full = len(bars) - (1 if pickup else 0)
    if cb is not None and len(cb) != full:
        raise ValueError('chord bars %d != melody bars %d' % (len(cb), full))
    for i, bar in enumerate(bars):
        d = bdur(bar)
        if cb is None:
            pts = []
            t = Fr(0)
            for e in bar[0]:
                if e.sym:
                    pts.append((t, e.sym))
                t += e.dur
        else:
            pts = []
            if not (pickup and i == 0):
                toks = cb[i - (1 if pickup else 0)].split()
                slot = blen / len(toks)
                for j, tk in enumerate(toks):
                    if tk != '.' and j * slot < d:
                        pts.append((j * slot, tk))
        if not pts or pts[0][0] > 0:
            pts.insert(0, (Fr(0), last))
        s = []
        for j, (t, c) in enumerate(pts):
            end = pts[j + 1][0] if j + 1 < len(pts) else d
            if end > t:
                s.append((t, end - t, c))
            last = c
        segs.append(s)
    return segs


def attach_syms(bars, segs):
    """Write chord symbols onto melody events (only when the chord changes)."""
    prev = None
    for bar, s in zip(bars, segs):
        for e in bar[0]:
            e.sym = None
        for (t, d, c) in s:
            if c is None or c == prev:
                prev = c if c else prev
                continue
            prev = c
            tt = Fr(0)
            for e in bar[0]:
                if tt >= t and tt < t + d:
                    if not e.sym:
                        e.sym = c
                    break
                tt += e.dur


def rh_min(bar):
    ms = [p.midi for lay in bar for e in lay for p in e.pitches]
    return min(ms) if ms else 127


def fit(lad, idxs, ceil):
    """pick ladder pitches for idxs, keeping everything <= ceil."""
    lad = list(lad)
    while lad[0].midi > ceil and lad[0].midi > 33:
        lad = [p.tr(-7, -12) for p in lad]
    out = []
    for i in idxs:
        p = lad[min(i, len(lad) - 1)]
        if p.midi > ceil:
            ok = [q for q in lad if q.midi <= ceil]
            p = ok[-1] if ok else lad[0]
        out.append(p)
    return out


FLOW = {1: [0], 2: [0, 2], 3: [0, 2, 3], 4: [0, 2, 3, 4], 5: [0, 2, 3, 4, 3], 6: [0, 2, 3, 4, 3, 2],
        7: [0, 2, 3, 4, 5, 4, 3], 8: [0, 2, 3, 4, 5, 4, 3, 2], 9: [0, 2, 3, 4, 3, 2, 3, 4, 3],
        12: [0, 2, 3, 4, 3, 2, 0, 2, 3, 4, 3, 2]}
OPEN = {0: 0, 1: 2, 2: 3, 3: 4}
FLOWC = {1: [0], 2: [0, 2], 3: [0, 1, 2], 4: [0, 1, 2, 1], 5: [0, 1, 2, 3, 2], 6: [0, 1, 2, 3, 2, 1],
         7: [0, 1, 2, 3, 2, 1, 2], 8: [0, 2, 1, 2, 0, 2, 1, 2], 9: [0, 1, 2, 3, 2, 1, 2, 3, 2],
         12: [0, 1, 2, 3, 2, 1, 0, 1, 2, 3, 2, 1]}


def _pc(tc):
    return (BASE[tc[0]] + tc[1]) % 12


def _clash(tc, mel):
    """True if tone class tc is a semitone from any melody pitch class."""
    p = _pc(tc)
    return any((p - m) % 12 in (1, 11) for m in mel)


def voicing(c, ceil, rich=False, mel=()):
    """Open, pianistic left-hand voicing (no arpeggio): bass + 5th/7th + 10th,
    with octave bass and a colour tone when rich.  Everything stays <= ceil."""
    tones, bass = chord_tones(c)
    q = CH.match(c).group(2)
    b = place(bass, 36)
    if b.midi > 45:
        b = b.tr(-7, -12)
    plain = q not in ('dim', 'dim7', 'aug', '+', 'm7b5', '7#5', 'aug7') and q not in NO_THIRD and len(tones) >= 3
    slash = _pc(bass) != _pc(tones[0])
    if not plain or slash:
        # chords with no third: keep the low voicing open (root, fifth, octave) rather than a low cluster
        lad = ladder(CH.match(c).group(1) + '5' if (q in NO_THIRD and not slash) else c, b.midi)
        ups = lad[1:4] if (rich or not slash) else lad[1:3]
    else:
        third, fifth = tones[1], tones[2]
        sev = tones[3] if len(tones) > 3 else None
        tcs = [sev, third] if sev else [fifth, third]
        if rich:
            if sev:
                tcs.append(fifth)                        # C2 Bb2 E3 G3
            elif q == 'm':
                tcs = [fifth, third]                     # A2 E3 G3 C4 (m7 colour)
                seventh = P(tones[0][0], tones[0][1], 4).tr(6, 10)
                st = (seventh.l, seventh.a)
                if not _clash(st, mel):
                    tcs = [fifth, st, third]
            elif q == '':
                sixth = P(tones[0][0], tones[0][1], 4).tr(5, 9)
                st = (sixth.l, sixth.a)
                if not _clash(st, mel):
                    tcs.append(st)                       # C2 G2 E3 A3 (6th colour)
        ups, cur = [], b.midi
        for tc in tcs:
            p = place(tc, cur + 1)
            ups.append(p)
            cur = p.midi
    ps = [b] + [p for p in ups if p.midi <= ceil]
    if rich and b.midi - 12 >= 28:
        ps.insert(0, b.tr(-7, -12))
    return list({p.midi: p for p in ps}.values())


def upper_chord(c, ceil, lo=48, n=3, cap=66):
    """Closed chord (3 notes, keeping 3rd and 7th) just under the melody."""
    tones, _ = chord_tones(c.split('/')[0])
    ceil = min(ceil, cap)
    pits = []
    for o in range(2, 7):
        for tc in tones:
            p = P(tc[0], tc[1], o)
            if lo <= p.midi <= ceil:
                pits.append(p)
    pits.sort(key=lambda p: p.midi)
    q = CH.match(c.split('/')[0]).group(2)
    need = (set() if q in NO_THIRD or len(tones) < 3 else {_pc(tones[1])}) | ({_pc(tones[3])} if len(tones) > 3 else set())
    for i in range(len(pits) - n, -1, -1):
        win = pits[i:i + n]
        if need <= {p.midi % 12 for p in win}:
            return win
    return pits[-n:] if len(pits) >= 2 else None


def lh_segment(pat, c, d, ceil, compound, first, mel=(), blen=Fr(1)):
    """-> list of Ev filling duration d for chord c."""
    n8 = d / E8
    tones, bass = chord_tones(c)
    plain = len(tones) >= 3 and CH.match(c).group(2) not in ('dim', 'dim7', 'aug', '+', 'm7b5')
    if pat in ('pad', 'padx'):
        ps = voicing(c, ceil, pat == 'padx', mel)
        strike = blen / 2 if blen in (Fr(1), Fr(3, 2)) else blen
        out, left = [], d
        while left > 0:
            ch = min(strike, left)
            out += held(ps, ch)
            left -= ch
        return out
    if n8.denominator != 1:
        pat = 'hold'
    n = int(n8) if n8.denominator == 1 else 0
    q = n // 2
    if pat == 'hold':
        lad = ladder(c, 41)
        ps = fit(lad, [0, 2] if (plain and d >= Fr(1, 2)) else [0], ceil)
        if ps[-1].midi == ps[0].midi:
            ps = ps[:1]
        return held(ps, d)
    if pat == 'end':
        lad = ladder(c, 36)
        ps = fit(lad, [0, 2, 3], ceil)
        ps = list({p.midi: p for p in ps}.values())
        return held(ps, d)
    if pat in ('flow', 'flowc'):
        lad = ladder(c, 36 if pat == 'flow' else 43)
        seq = (FLOW if pat == 'flow' else FLOWC).get(n)
        if seq is None:
            base = (FLOW if pat == 'flow' else FLOWC)[8]
            seq = [base[i % 8] for i in range(n)]
        if pat == 'flowc' and lad[0].midi < 48:
            seq = [OPEN[i] for i in seq]
        return [Ev([p], E8) for p in fit(lad, seq, ceil)]
    if pat == 'alberti':
        lad = ladder(c, 43)
        seq = [[0, 2, 1, 2][i % 4] for i in range(n)]
        if lad[0].midi < 48:
            seq = [[0, 3, 2, 3][i % 4] for i in range(n)]
        return [Ev([p], E8) for p in fit(lad, seq, ceil)]
    Q4 = Fr(1, 4)
    if n % 2:
        return lh_segment('flowc', c, d, ceil, compound, first)
    if pat == 'quarters':
        lad = ladder(c, 43)
        seq = [[0, 2, 3, 2][i % 4] for i in range(q)]
        return [Ev([p], Q4) for p in fit(lad, seq, ceil)]
    if pat in ('waltz', 'boom'):
        lad = ladder(c, 43)
        dy = fit(lad, [2, 4] if lad[0].midi < 48 else [1, 2], ceil)
        b = lad[0]
        if b.midi > ceil:
            b = b.tr(-7, -12)
        if dy[0].midi <= b.midi or dy[0].midi == dy[1].midi:
            dy = fit([p.tr(-7, -12) for p in lad[1:]] + lad[1:], [0, 1, 2, 3], ceil)[-2:]
        alt = lad[2].tr(-7, -12)
        if alt.midi < 36:
            alt = b
        uc = upper_chord(c, ceil, 48)
        if uc and uc[0].midi > b.midi + 4:
            dy = uc
        out = []
        for i in range(q):
            if pat == 'waltz':
                out.append(Ev([b], Q4) if i % 3 == 0 else Ev(list(dy), Q4))
            else:
                if i % 2 == 0:
                    out.append(Ev([b if i % 4 == 0 else alt], Q4))
                else:
                    out.append(Ev(list(dy), Q4))
        return out
    if pat in ('stride', 'waltzA'):
        lad = ladder(c, 36)
        b = lad[0]
        alt = place(tones[2] if plain else bass, 36)
        if alt.midi > 47:
            alt = alt.tr(-7, -12)
        if alt.midi < 31:
            alt = b
        up = ladder(c.split('/')[0], 50)
        tri = fit(up, [0, 1, 2], min(ceil, 64))
        tri = list({p.midi: p for p in tri if p.midi > b.midi + 4}.values())
        uc = upper_chord(c, min(ceil, 64), 50)
        if uc and uc[0].midi > b.midi + 4:
            tri = uc
        if not tri:
            tri = [b]
        out = []
        for i in range(q):
            if pat == 'waltzA':
                out.append(Ev([b], Q4) if i % 3 == 0 else Ev(list(tri), Q4))
            else:
                if i % 2 == 0:
                    out.append(Ev([b if i % 4 == 0 else alt], Q4))
                else:
                    out.append(Ev(list(tri), Q4))
        return out
    raise ValueError('unknown pattern ' + pat)


def make_lh(bars, segs, pat, blen, compound):
    out = []
    nb = len(bars)
    for i, (bar, s) in enumerate(zip(bars, segs)):
        ceil = min(rh_min(bar) - 1, 64)
        lay = []
        last = (i == nb - 1)
        for j, (t, d, c) in enumerate(s):
            if c is None:
                lay += held([], d)
            elif last and j == len(s) - 1 and pat != 'hold':
                lay += lh_segment('end', c, d, ceil, compound, True)
            else:
                mel, tt = set(), Fr(0)
                for e in bar[0]:
                    if tt < t + d and tt + e.dur > t:
                        mel |= {p.midi % 12 for p in e.pitches}
                    tt += e.dur
                lay += lh_segment(pat, c, d, ceil, compound, j == 0, mel, blen)
        out.append([lay])
    return out


def add_harmony(bars, segs, thresh=Fr(1, 4), mode='third'):
    """Advanced right hand: add chord tones under the longer melody notes."""
    prev = None
    nb = len(bars)
    for bi, (bar, s) in enumerate(zip(bars, segs)):
        t = Fr(0)
        evs = bar[0]
        for k, e in enumerate(evs):
            chord = None
            for (st, d, c) in s:
                if st <= t < st + d:
                    chord = c
            t += e.dur
            if not e.pitches:
                prev = None
                continue
            if prev is not None:      # continuation of a tie: copy the harmony
                e.pitches = [e.pitches[0]] + [P(p.l, p.a, p.o) for p in prev]
                prev = prev if e.tie else None
                continue
            add = []
            mel = e.pitches[0]
            if chord and e.dur >= thresh:
                tones, _ = chord_tones(chord)
                cands = []
                for tc in tones[:4]:
                    for o in range(2, 7):
                        cands.append(P(tc[0], tc[1], o))
                cands.sort(key=lambda p: -p.midi)
                if mode == 'oct':
                    lowp = mel.tr(-7, -12)
                    if lowp.midi >= 55:
                        add.append(lowp)
                else:
                    a1 = [p for p in cands if 3 <= mel.midi - p.midi <= 9 and p.midi >= 57]
                    if a1:
                        add.append(a1[0])
                        if mode == 'one':
                            a1 = []
                    if a1:
                        final = (bi == nb - 1 and k == len(evs) - 1) or (bi == nb - 2 and e.tie and k == len(evs) - 1)
                        if e.dur >= Fr(1, 2) or final:
                            a2 = [p for p in cands if p.midi <= a1[0].midi - 3 and mel.midi - p.midi <= 12 and p.midi >= 57]
                            if a2:
                                add.append(a2[0])
            e.pitches = [mel] + add
            prev = add if e.tie else None


def head_of(bar, d):
    out, t = [], Fr(0)
    for e in bar[0]:
        if t >= d:
            break
        e = copy.deepcopy(e)
        if t + e.dur > d:
            e.dur = e.wdur = d - t
            e.tie = False
        out.append(e)
        t += e.dur
    return [out]


def tail_of(bar, d, blen):
    out, t = [], Fr(0)
    start = bdur(bar) - d
    for e in bar[0]:
        if t >= start:
            out.append(copy.deepcopy(e))
        t += e.dur
    return [out]


def excerpt(bars, segs, blen, a, b):
    pickup = bdur(bars[0]) < blen and len(bars) > 1
    pd = bdur(bars[0]) if pickup else Fr(0)
    off = 1 if pickup else 0
    full = bars[off:]
    fs = segs[off:]
    sel = copy.deepcopy(full[a - 1:b])
    ss = copy.deepcopy(fs[a - 1:b])
    if pickup:
        if b < len(full):
            sel[-1] = head_of(sel[-1], blen - pd)
            ss[-1] = [(t, min(d, blen - pd - t), c) for (t, d, c) in ss[-1] if t < blen - pd]
        if a == 1:
            sel.insert(0, copy.deepcopy(bars[0]))
            ss.insert(0, copy.deepcopy(segs[0]))
        else:
            sel.insert(0, tail_of(full[a - 2], pd, blen))
            ss.insert(0, [(Fr(0), pd, None)])
    sel[-1][0][-1].tie = False
    if a > 1 and ss[0 if not pickup else 1][0][2] is None:
        pass
    return sel, ss


def span(bars):
    ms = [p.midi for bar in bars for lay in bar for e in lay for p in e.pitches]
    return min(ms), max(ms)


def best_shift(bars, src, dst, lo=60, hi=79):
    dl, ds = interval(src, dst)
    mn, mx = span(bars)
    best = None
    for o in (-1, 0, 1):
        a, b = mn + ds + 12 * o, mx + ds + 12 * o
        pen = max(0, lo - a) * 3 + max(0, b - hi) * 2 + abs(o) * 0.1 + abs(ds + 12 * o) * 0.01
        if best is None or pen < best[0]:
            best = (pen, o)
    return dl, ds, best[1], best[0]


EASY_MAJ = ['C', 'G', 'F', 'D']
EASY_MIN = ['Am', 'Em', 'Dm']
SIMPLER = {'Ab': 'G', 'Db': 'C', 'E': 'Eb', 'B': 'Bb', 'F#': 'F', 'Gb': 'G', 'Fm': 'Em', 'C#m': 'Dm', 'F#m': 'Em',
           'Bbm': 'Am', 'G#m': 'Am', 'Ebm': 'Em'}

PATS = {
    # style: {metre class: (easy, inter, adv)}.  Same key at every level; richer
    # voicings (not arpeggios) as the level goes up.
    'hymn': {'4': ('hold', 'pad', 'padx'), '3': ('hold', 'pad', 'padx'), 'c': ('hold', 'pad', 'padx')},
    'ballad': {'4': ('hold', 'pad', 'padx'), '3': ('hold', 'pad', 'padx'), 'c': ('hold', 'pad', 'padx')},
    'lively': {'4': ('hold', 'boom', 'stride'), '3': ('hold', 'waltz', 'waltzA'), 'c': ('hold', 'pad', 'padx')},
    'waltz': {'4': ('hold', 'boom', 'stride'), '3': ('hold', 'waltz', 'waltzA'), 'c': ('hold', 'pad', 'padx')},
}
LEVELS = ['easy', 'inter', 'adv']


def set_lyrics(bars, w, label='?'):
    """Attach one lyric token to each melody note (tied continuations are skipped; * = none)."""
    toks = w.split()
    notes, prev_tie = [], False
    for bar in bars:
        for e in bar[0]:
            if e.pitches:
                if not prev_tie:
                    notes.append(e)
                prev_tie = e.tie
            else:
                prev_tie = False
    if len(toks) != len(notes):
        raise ValueError('%s: %d lyric syllables for %d melody notes' % (label, len(toks), len(notes)))
    for e, tk in zip(notes, toks):
        e.lyr = None if tk == '*' else tk


def arrange(t, level):
    """t: tune dict.  Returns dict(abc=..., key=..., bars=..., bpm=...)."""
    M = t['M']
    blen, beam = meter(M)
    compound = beam == Fr(3, 8)
    cls = 'c' if compound else ('3' if blen == Fr(3, 4) else '4')
    L = t.get('L', E8)
    bars = parse(t['mel'], t['key'], L, t.get('scale', 1))
    errs = check(bars, blen, t['id'])
    if errs:
        raise ValueError('\n'.join(errs))
    if bdur(bars[0]) < blen and bdur(bars[0]) + bdur(bars[-1]) != blen:
        raise ValueError('%s: pickup + last bar != full bar' % t['id'])
    if t.get('w'):
        set_lyrics(bars, t['w'], t['id'])
    segs = chord_segments(bars, blen, t.get('chords'))
    opt = dict(t.get(level, {}))
    rng = opt.get('bars')
    if rng:
        bars, segs = excerpt(bars, segs, blen, rng[0], rng[1])
        if opt.get('cut'):
            pd = bdur(bars[0]) if bdur(bars[0]) < blen else Fr(0)
            cut = opt['cut']
            bars[-1] = head_of(bars[-1], cut)
            bars[-1][0][-1].tie = False
            if blen - pd - cut > 0:
                bars[-1][0] += held([], blen - pd - cut)
            segs[-1] = [(t, min(d, blen - pd - t), c) for (t, d, c) in segs[-1] if t < blen - pd]
    # One key for every level: the song's key, or a friendlier neighbour for awkward keys.
    dst = t.get('home') or SIMPLER.get(t['key'], t['key'])
    lo, hi = 60, 81
    dl, ds, o, pen = best_shift(bars, t['key'], dst, lo, hi)
    bars = transpose(bars, dl, ds, o)
    segs = [[(a, b, tr_chord(c, dl, ds) if c else None) for (a, b, c) in s] for s in segs]
    style = t.get('style', 'ballad')
    pat = opt.get('pat') or PATS[style][cls][LEVELS.index(level)]
    attach_syms(bars, segs)
    hm = opt.get('harm', t.get('harm', 'third'))
    if level == 'adv' and hm != 'none':
        add_harmony(bars, segs, mode=hm)
    elif level == 'inter' and hm != 'none':
        add_harmony(bars, segs, mode='one')
    lh = make_lh(bars, segs, pat, blen, compound)
    bpm = int(round(t.get('tempo', 90) * {'easy': 0.85, 'inter': 0.95, 'adv': 1.0}[level]))
    bpm = opt.get('tempo', bpm)
    unit = '3/8' if compound else ('1/2' if M.endswith('/2') else '1/4')
    abc = emit(bars, lh, dst, M, E8, '%s=%d' % (unit, bpm))
    nfull = len(bars) - (1 if bdur(bars[0]) < blen and len(bars) > 1 else 0)
    return dict(abc=abc, key=dst, bars=nfull, bpm=bpm)


def raw(spec):
    """Hand-written two-voice arrangement.  spec: M, L, K, Q, v1, v2 [, to]"""
    M = spec['M']
    blen, beam = meter(M)
    L = spec.get('L', E8)
    sc = spec.get('scale', 1)
    v1 = parse(spec['v1'], spec['K'], L, sc, True)
    v2 = parse(spec['v2'], spec['K'], L, sc, True)
    if spec.get('first_layer'):
        v1 = [[bar[0]] for bar in v1]
    if spec.get('thin1'):
        thin(v1, spec['thin1'])
    if spec.get('thin2'):
        thin(v2, spec['thin2'])
    errs = check(v1, blen, spec.get('id', '?') + ' RH') + check(v2, blen, spec.get('id', '?') + ' LH')
    if len(v1) != len(v2):
        errs.append('%s: RH has %d bars, LH has %d' % (spec.get('id', '?'), len(v1), len(v2)))
    else:
        for i, (a, b) in enumerate(zip(v1, v2)):
            if bdur(a) != bdur(b):
                errs.append('%s: bar %d RH %s vs LH %s' % (spec.get('id', '?'), i + 1, bdur(a), bdur(b)))
    if errs:
        raise ValueError('\n'.join(errs))
    key = spec['K']
    if spec.get('to'):
        dl, ds = interval(key, spec['to'])
        o = spec.get('oct', 0)
        v1 = transpose(v1, dl, ds, o)
        v2 = transpose(v2, dl, ds, o)
        key = spec['to']
    if 'beam' in spec:
        beam = spec['beam']
    sig = key_sig(key)
    abc = emit(v1, v2, key, M, spec.get('Lout', L), spec['Q'], spec.get('per_line', 4))
    nfull = len(v1) - (1 if bdur(v1[0]) < blen and len(v1) > 1 else 0)
    bpm = int(spec['Q'].split('=')[1])
    return dict(abc=abc, key=key, bars=nfull, bpm=bpm)


def thin(bars, how):
    """Reduce chords: 'top' keeps the highest note, 'bottom' the lowest, 'top2' the two highest."""
    for bar in bars:
        for lay in bar:
            for e in lay:
                if len(e.pitches) > 1:
                    ps = sorted(e.pitches, key=lambda p: p.midi)
                    if how in ('oct_hi', 'oct_lo'):
                        if len(ps) == 2 and ps[1].midi - ps[0].midi == 12:
                            e.pitches = ps[1:] if how == 'oct_hi' else ps[:1]
                    else:
                        e.pitches = ps[-1:] if how == 'top' else ps[:1] if how == 'bottom' else ps[-2:]


# Accompaniment patterns for chord charts, on an eighth-note grid for one bar.
# 'on' = strike, '-' = keep holding, 'z' = rest;  for the left hand 'lo' = bass octave, 'up' = the upper notes.
# These are generic comping figures written for this book, not transcriptions of any recording.
COMP_RH = {
    'ballad': {8: 'on - on on on - on on', 6: 'on - on on on on'},
    'rock': {8: 'z on z on z on z on'},
    'folk': {8: 'z z on on z z on on'},
    'waltz': {6: 'z z on - on on'},
    'compound': {6: 'on - on on - on', 12: 'on - on on - on on - on on - on'},
}
COMP_LH = {
    'ballad': {8: 'on - - - on - - -', 6: 'on - - - - -'},
    'rock': {8: 'lo - up - lo - up -'},
    'folk': {8: 'lo - up - lo - up -'},
    'waltz': {6: 'on - - - - -'},
    'compound': {6: 'on - - up - -', 12: 'on - - up - - on - - up - -'},
}


def _grid(cells, segs, notes_for, syms=False, anticipate=None):
    """cells: per-eighth actions for the bar.  segs: [(start8, len8, chord)].  -> list of Ev."""
    out = []
    n = len(cells)
    for (st, ln, c) in segs:
        i = st
        first = True
        while i < st + ln:
            act = cells[i]
            if i == st and act == '-':
                act = 'on'
            j = i + 1
            while j < st + ln and cells[j] == ('z' if act == 'z' else '-'):
                j += 1
            d = (j - i) * E8
            chord = c
            if anticipate and i == n - 1 and act != 'z':
                chord = anticipate
            evs = held([] if act == 'z' else notes_for(chord, act), d)
            if first and syms:
                evs[0].sym = c
            first = False
            out += evs
            i = j
    return out


def chart_levels(chart, bpm):
    """Chord chart -> Easy / Intermediate / Advanced accompaniment (chords only, never a melody)."""
    M = chart.get('M', '4/4')
    blen, beam = meter(M)
    n8 = int(blen / E8)
    compound = beam == Fr(3, 8)
    comp = 'compound' if compound else chart.get('comp', 'ballad')
    if blen == Fr(3, 4) and comp not in ('waltz',):
        comp = 'ballad'
    allbars = [bar for sec in chart['sections'] for bar in sec['bars']]
    key = chart.get('abckey', 'C')
    unit = '3/8' if compound else '1/4'

    def rh(c, act=None):
        return upper_chord(c, 72, lo=57, n=3, cap=72) or ladder(c.split('/')[0], 57)[:3]

    def bass(c):
        tones, b = chord_tones(c)
        p = place(b, 36)
        return p.tr(-7, -12) if p.midi > 45 else p

    def lh_pad(c, act=None):
        return voicing(c, 56, rich=False)

    def lh_rich(c, act='on'):
        v = sorted(voicing(c, 56, rich=True), key=lambda p: p.midi)
        if act == 'lo':
            return v[:2] if len(v) > 2 and v[1].midi - v[0].midi == 12 else v[:1]
        if act == 'up':
            up = v[2:] if len(v) > 2 and v[1].midi - v[0].midi == 12 else v[1:]
            return up or v
        return v

    half = n8 // 2 if n8 in (8, 12) else (3 if compound else n8)
    out = {}
    for level in LEVELS:
        v1, v2 = [], []
        for bi, bar in enumerate(allbars):
            if n8 % len(bar):
                raise ValueError('%s: a bar with %d chords does not divide a %s bar' % (chart['id'], len(bar), M))
            per = n8 // len(bar)
            segs = []
            for k, c in enumerate(bar):
                if segs and segs[-1][2] == c:
                    segs[-1][1] += per
                else:
                    segs.append([k * per, per, c])
            nxt = allbars[bi + 1][0] if bi + 1 < len(allbars) else None
            if level == 'easy':
                r = _grid(['on'] + ['-'] * (n8 - 1), segs, rh, True)
                l = _grid(['on'] + ['-'] * (n8 - 1), segs, lambda c, a: [bass(c)])
            elif level == 'inter':
                cells = [('on' if i % half == 0 else '-') for i in range(n8)]
                if blen == Fr(3, 4):
                    cells = ['on', '-', 'on', '-', '-', '-']
                r = _grid(cells, segs, rh, True)
                l = _grid(['on'] + ['-'] * (n8 - 1), segs, lh_pad)
            else:
                rc = COMP_RH[comp].get(n8) or COMP_RH['ballad'][n8]
                lc = COMP_LH[comp].get(n8) or COMP_LH['ballad'][n8]
                ant = nxt if (comp == 'ballad' and nxt and nxt != bar[-1]) else None
                r = _grid(rc.split(), segs, rh, True, ant)
                l = _grid(lc.split(), segs, lh_rich)
            v1.append([r])
            v2.append([l])
        abc = emit(v1, v2, key, M, E8, '%s=%d' % (unit, bpm))
        out[level] = dict(abc=abc, key=chart['key'], bars=len(v1), bpm=bpm)
    return out


def octs(body, down=True):
    """ABC string helper: double every note at the octave below (or above)."""
    def f(m):
        acc, let, marks, rest = m.group(1) or '', m.group(2), m.group(3), m.group(4)
        if down:
            if "'" in marks:
                other = let + marks[:-1]
            elif let.islower():
                other = let.upper()
            else:
                other = let + marks + ','
            return '[%s%s%s%s%s]%s' % (acc, other, acc, let, marks, rest)
        if ',' in marks:
            other = let + marks[:-1]
        elif let.isupper():
            other = let.lower()
        else:
            other = let + marks + "'"
        return '[%s%s%s%s%s]%s' % (acc, let, marks, acc, other, rest)
    return re.sub(r"(\^\^|\^|__|_|=)?([A-Ga-g])([,']*)(\d*/*\d*-?)", f, body)
