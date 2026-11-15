# Hand-written arrangements: piano pieces whose texture *is* the piece, the
# practice exercises, the original style studies, and the pop chord charts.
from fractions import Fraction as Fr
from engine import octs

S16 = Fr(1, 16)
SPECIALS = []


def special(id, title, composer, cat, levels, **kw):
    d = dict(id=id, title=title, composer=composer, cat=cat, levels=levels)
    d.update(kw)
    SPECIALS.append(d)


def J(*bars):
    return ' | '.join(bars)


# ============================================================ Fur Elise
FE = ['e^de B=dc', 'A2 z CEA', 'B2 z E^GB', 'c2 z Ee^d', 'e^de B=dc', 'A2 z CEA', 'B2 z EcB']
FL = ['z6', 'A,,E,A, z3', 'E,,E,^G, z3', 'A,,E,A, z3', 'z6', 'A,,E,A, z3', 'E,,E,^G, z3']
FE_EASY_L = ['z6', 'A,6', 'E,6', 'A,6', 'z6', 'A,6', 'E,6']
fe_mid_r = ['A2 z Bcd', 'e3 Gfe', 'd3 Fed', 'c3 Edc', 'B2 z Ee z', "z ee' z z ^d", 'e z z ^de^d']
fe_mid_l = ['A,,E,A, z3', 'C,G,C z3', 'G,,G,B, z3', 'A,,E,A, z3', 'E,,E,E z3', 'z6', 'z6']
special('fur-elise', 'Für Elise', 'Ludwig van Beethoven, WoO 59 (1810)', 'Classical', dict(
    easy=dict(M='3/8', L=S16, K='Am', Q='3/8=34', v1=J('e^d', *FE, 'A4'), v2=J('z2', *FE_EASY_L, 'A,4'),
              note='Opening theme, simplified left hand'),
    inter=dict(M='3/8', L=S16, K='Am', Q='3/8=40', v1=J('e^d', *FE, 'A2 z2 e^d', *FE, 'A4'),
               v2=J('z2', *FL, 'A,,E,A, z3', *FL, 'A,,E,A,2'), note='Opening theme as Beethoven wrote it'),
    adv=dict(M='3/8', L=S16, K='Am', Q='3/8=44', v1=J('e^d', *FE, *fe_mid_r, *FE, 'A4'),
             v2=J('z2', *FL, *fe_mid_l, *FL, 'A,,E,A,2'), note='Complete first section'),
), badges=['Excerpt'], note='The famous opening section only; the two contrasting episodes are not included.')

# ============================================================ Minuet in G (Petzold)
MR = ['d2 GABc', 'd2 G2 G2', 'e2 cdef', 'g2 G2 G2', 'c2 dcBA', 'B2 cBAG', 'F2 GABG', 'A6',
      'd2 GABc', 'd2 G2 G2', 'e2 cdef', 'g2 G2 G2', 'c2 dcBA', 'B2 cBAG', 'A2 BAGF', 'G6']
ML = ['[G,B,D]4 A,2', 'B,6', 'C6', 'B,6', 'A,6', 'G,6', 'D2 B,2 G,2', 'D2 D,C B,A,',
      'B,4 A,2', 'G,2 B,2 G,2', 'C6', 'B,2 CB, A,G,', 'A,4 F,2', 'G,4 B,2', 'C2 D2 D,2', 'G,4 G,,2']
ML_EASY = ['G,6', 'B,6', 'C6', 'B,6', 'A,6', 'G,6', 'D6', 'D6', 'B,6', 'G,6', 'C6', 'B,6', 'A,6', 'G,6', 'C4 D2', 'G,6']
MR2 = ['b2 gabg', 'a2 defd', 'g2 efgd', '^c2 B^cA2', 'AB ^cdef', 'g2 f2 e2', 'f2 A2 ^c2', 'd6',
       'd2 GFG2', 'e2 GFG2', 'd2 c2 B2', 'AG FGA2', 'DE FGAB', 'c2 B2 A2', 'Bd G2 F2', 'G6']
ML2 = ['G,6', 'F,6', 'E,2 G,2 E,2', 'A,4 A,,2', 'A,6', 'B,2 D2 ^C2', 'D2 F,2 A,2', 'D2 D,2 =C2',
       'B,2 D2 B,2', 'C2 E2 C2', 'B,2 A,2 G,2', 'D4 z2', 'D,4 F,2', 'E,2 G,2 F,2', 'G,2 B,,2 D,2', 'G,2 D,2 G,,2']
special('minuet-in-g', 'Minuet in G', 'Christian Petzold (from the Anna Magdalena Notebook, 1725)', 'Classical', dict(
    easy=dict(M='3/4', K='G', Q='1/4=92', v1=J(*MR), v2=J(*ML_EASY), note='First half, one bass note per bar'),
    inter=dict(M='3/4', K='G', Q='1/4=108', v1=J(*MR), v2=J(*ML), note='First half, both voices'),
    adv=dict(M='3/4', K='G', Q='1/4=120', v1=J(*(MR + MR2)), v2=J(*(ML + ML2)), note='Complete minuet'),
), note='Long credited to J. S. Bach; the composer is Christian Petzold.')

# ============================================================ Prelude in C (BWV 846)
PRE = ['C E G c e', 'C D A d f', 'B, D G d f', 'C E G c e', 'C E A e a', 'C D ^F A d', 'B, D G d g', 'B, C E G c',
       'A, C E G c', 'D, A, D ^F c', 'G, B, D G B', 'G, _B, E G ^c', 'F, A, D A d', 'F, _A, D F B', 'E, G, C G c',
       'E, F, A, C F', 'D, F, A, C F', 'G,, D, G, B, F', 'C, E, G, C E']


def pre_bars(idx):
    r, l = [], []
    for i in idx:
        a, b, c, d, e = PRE[i - 1].split()
        half_r = 'z2 %s%s %s%s%s%s' % (c, d, e, c, d, e)
        half_l = '%s%s3- %s4' % (a, b, b)
        r.append(half_r + ' ' + half_r)
        l.append(half_l + ' ' + half_l)
    return r, l


def pre_easy(idx):
    r, l = [], []
    for i in idx:
        a, b, c, d, e = PRE[i - 1].split()
        r.append('%s%s %s%s %s%s %s%s' % (c, d, e, d, c, d, e, d))
        l.append('[%s%s]8' % (a, b))
    return r, l


_r, _l = pre_easy([1, 2, 3, 4, 5, 6, 7, 3])
_ri, _li = pre_bars(list(range(1, 12)) + [18, 19])
_ra, _la = pre_bars(range(1, 20))
special('prelude-in-c', 'Prelude in C', 'J. S. Bach, BWV 846 (Well-Tempered Clavier, Book I)', 'Classical', dict(
    easy=dict(M='4/4', K='C', Q='1/4=72', v1=J(*_r, '[EGc]8'), v2=J(*_l, '[C,C]8'),
              note='Opening harmonies as gentle broken chords'),
    inter=dict(M='4/4', L=S16, K='C', Q='1/4=60', v1=J(*_ri, '[EGc]16'), v2=J(*_li, '[C,,C,]16'),
               note="Bach's figuration, bars 1–11 with a short close", per_line=2),
    adv=dict(M='4/4', L=S16, K='C', Q='1/4=66', v1=J(*_ra, '[EGc]16'), v2=J(*_la, '[C,,C,]16'),
             note="Bach's text, bars 1–19, then a closing chord", per_line=2),
), badges=['Excerpt'], note='The first 19 of 35 bars. Hold each pair of left-hand notes under the right-hand figure.')

# ============================================================ Moonlight Sonata, 1st movement
T1 = 'G,CE G,CE G,CE G,CE'
MOON_R = [T1, T1, 'A,CE A,CE A,=DF A,=DF', 'G,^B,F G,CE G,CD F,^B,D',
          T1 + ' & z9 G2G', 'G,DF G,DF G,DF G,DF & G6-G3 G2G', 'G,CE G,CE A,CF A,CF & G6 A6',
          'G,B,E G,B,E A,B,D A,B,D & G6 F3 B3', 'G,B,E G,B,E G,B,E G,B,E & E12']
MOON_L = ['[C,,C,]12', '[B,,,B,,]12', '[A,,,A,,]6 [F,,,F,,]6', '[G,,,G,,]6 [G,,,G,,]6', '[C,,C,]12',
          '[^B,,,^B,,]12', '[C,,C,]6 [F,,,F,,]6', '[B,,,B,,]6 [B,,,B,,]6', '[E,,E,]12']
special('moonlight-sonata', 'Moonlight Sonata (1st movement)', 'Ludwig van Beethoven, Op. 27 No. 2 (1801)', 'Classical', dict(
    easy=dict(M='12/8', K='C#m', Q='3/8=44', v1=J(*MOON_R), v2=J(*MOON_L), first_layer=True, thin2='bottom',
              note='The rolling triplets alone'),
    inter=dict(M='12/8', K='C#m', Q='3/8=48', v1=J(*MOON_R), v2=J(*MOON_L), thin2='bottom',
               note='Triplets and melody'),
    adv=dict(M='12/8', K='C#m', Q='3/8=52', v1=J(*MOON_R), v2=J(*MOON_L), note='Triplets, melody and left-hand octaves'),
), badges=['Excerpt', 'Simplified'],
    note='Bars 1–9. Written in 12/8 so the triplets read as plain eighth notes; the short melody note is lined up with the third triplet note.')

# ============================================================ Canon in D
CB = ['D,', 'A,,', 'B,,', 'F,,', 'G,,', 'D,', 'G,,', 'A,,']
C5 = ['A,', 'E,', 'F,', 'C,', 'D,', 'A,', 'D,', 'E,']
C8 = ['D', 'A,', 'B,', 'F,', 'G,', 'D', 'G,', 'A,']
C10 = ['F', 'C', 'D', 'A,', 'B,', 'F', 'B,', 'C']


def canon_l(kind, unit=1, low=''):
    out = []
    u = str(unit) if unit > 1 else ''
    for i in range(0, 8, 2):
        halves = []
        for j in (i, i + 1):
            if kind == 'half':
                halves.append('%s%d' % (C8[j], 4 * unit))
            elif kind == 'broken':
                halves.append(''.join(x + low + u for x in (CB[j], C5[j], C8[j], C5[j])))
            else:
                halves.append(''.join(x + low + u for x in (CB[j], C5[j], C8[j], C10[j])))
        out.append(' '.join(halves))
    return out


V1A = ['f4 e4', 'd4 c4', 'B4 A4', 'B4 c4']
V1T = ['[df]4 [ce]4', '[Bd]4 [Ac]4', '[GB]4 [FA]4', '[GB]4 [Ec]4']
V3 = ['d2 f2 a2 g2', 'f2 d2 f2 e2', 'd2 B2 d2 a2', 'g2 b2 a2 g2']
V4 = ['fafd eaec', 'dfdB cfcA', 'BdBG AdAF', 'BdBG ceag']
V5 = ['a2fg a2fg aABc defg', 'f2de f2FG ABAG AFGA', 'G2BA G2FE FEDE FGAB', 'G2BA B2cd ABcd efga']
x2 = lambda bars: [__import__('re').sub(r'(\d+)', lambda m: str(int(m.group(1)) * 2), b) for b in bars]
x2n = lambda bars: [__import__('re').sub(r"([A-Ga-g][,']*)(?!\d)", r'\g<1>2', b) for b in bars]
special('canon-in-d', 'Canon in D', 'Johann Pachelbel, c. 1680', 'Classical', dict(
    easy=dict(M='4/4', K='D', Q='1/4=60', v1=J(*(V1A + V3), 'f8'), v2=J(*(canon_l('half') * 2), 'D8'),
              note='The ground bass with two of the melodies'),
    inter=dict(M='4/4', K='D', Q='1/4=58', v1=J(*(V1A + V1T + V3 + V4), '[Adf]8'),
               v2=J(*(canon_l('half') + canon_l('broken') * 3), '[D,A,D]8'), note='Four variations over the ground bass'),
    adv=dict(M='4/4', L=S16, K='D', Q='1/4=56', v1=J(*(x2(V1T) + x2(V3) + x2n(V4) + V5), "[fad']16"),
             v2=J(*(canon_l('broken', 2, ',') + canon_l('wide', 2, ',') * 3), '[D,,D,]16'), per_line=2,
             note='Includes the well-known running sixteenth-note variation'),
), badges=['Simplified'],
    note="A solo-piano reduction: Pachelbel's bass line and a selection of the violin melodies. The eighth-note variation is the arranger's own.")

# ============================================================ Gymnopedie No. 1
GYM_M = ['z2 f2 a2', 'g2 f2 c2', 'B2 c2 d2', 'A6', 'F6-', 'F6-', 'F6-', 'F6']
GYM_L = lambda n, g, d: [(g if i % 2 == 0 else d) for i in range(n)]
special('gymnopedie-1', 'Gymnopédie No. 1', 'Erik Satie, 1888', 'Classical', dict(
    easy=dict(M='3/4', K='D', Q='1/4=66', v1=J('z6', 'z6', 'z6', 'z6', *GYM_M), v2=J(*GYM_L(12, 'G,6', 'D,6')),
              note='Melody over single bass notes'),
    inter=dict(M='3/4', K='D', Q='1/4=70', v1=J('z6', 'z6', 'z6', 'z6', *GYM_M),
               v2=J(*GYM_L(12, 'G,,2 [B,D]4', 'D,,2 [A,C]4')), note='Bass note, then a two-note chord'),
    adv=dict(M='3/4', K='D', Q='1/4=72', v1=J('z6', 'z6', 'z6', 'z6', *(GYM_M + GYM_M[:4]), 'F6-', 'F6'),
             v2=J(*GYM_L(18, 'G,,6 & z2 [B,DF]4', 'D,,6 & z2 [A,CF]4')), note="Satie's left hand: sustained bass with a chord on beat two"),
), badges=['Excerpt'], note='The opening statement of the melody (bars 1–16 of the original).')

# ============================================================ In the Hall of the Mountain King
KA = ['B,CDE FDF2', '^ECE2 =E=CE2', 'B,CDE FDFB', 'AFDF A4']
KB = ['FG^AB cAc2', 'd^Ad2 cAc2', 'FG^AB cAc2', 'd^Ad2 c4']
KLA = ['B,,2F,2 B,,2F,2', 'C,2^G,2 =C,2=G,2', 'B,,2F,2 B,,2F,2', 'D,2A,2 D,4']
KLB = ['F,,2C,2 F,,2C,2', 'F,,2C,2 F,,2C,2', 'F,,2C,2 F,,2C,2', 'F,,2C,2 F,,4']
KLA8 = ['[B,,,B,,]2F,2 [B,,,B,,]2F,2', '[C,,C,]2^G,2 [=C,,=C,]2=G,2', '[B,,,B,,]2F,2 [B,,,B,,]2F,2', '[D,,D,]2A,2 [D,,D,]4']
KA8 = [octs(b, False) for b in ['B,CDE FDF2', '^ECE2 =E=CE2', 'B,CDE FDFB', 'AFDF A4']]
special('mountain-king', 'In the Hall of the Mountain King', 'Edvard Grieg, Peer Gynt (1875)', 'Classical', dict(
    easy=dict(M='4/4', K='Bm', Q='1/4=92', v1=J(*(KA + KA)), v2=J(*(KLA + KLA)), note='The theme, twice'),
    inter=dict(M='4/4', K='Bm', Q='1/4=116', v1=J(*(KA + KA + KB + KB + KA + KA)), v2=J(*(KLA * 2 + KLB * 2 + KLA * 2)),
               note='Both strains of the theme'),
    adv=dict(M='4/4', K='Bm', Q='1/4=138', v1=J(*(KA + KA + KB + KB + KA8 + KA8)), v2=J(*(KLA * 2 + KLB * 2 + KLA8 * 2)),
             note='Ends with the theme in octaves'),
), badges=['Excerpt'], note='The main theme. A good one for Halloween: start slowly and let it speed up.')

# ============================================================ The Entertainer
E5, E6, E7 = 'Ec2E c2Ec-', 'c4- ccd^d', 'ecde- eBd2'
ENT_I_R = ['D^D', E5, E6, E7, 'c4- c2 D^D', E5, 'c4- c2 AG', '^FAce- edcA', 'd4- d2 D^D', E5, E6, E7, 'c4- c2 cd',
           'ecde- ecdc', 'ecde- ecdc', E7, 'c4- c2']
L5, L6, L7 = 'C,2 [E,G,]2 G,,2 [E,G,]2', 'F,,2 [A,C]2 E,,2 [G,C]2', 'G,,2 [E,G,]2 G,,2 [F,G,]2'
ENT_I_L = ['z2', L5, L6, L7, 'C,2 [E,G,]2 C,2 z2', L5, 'F,,2 [A,C]2 E,,2 _E,,2', 'D,,2 [^F,C]2 D,,2 [^F,C]2', 'G,,2 [F,B,]2 G,,2 z2',
           L5, L6, L7, 'C,2 [E,G,]2 C,2 z2', 'C,2 [E,G,]2 _B,,2 [E,G,]2', 'A,,2 [A,C]2 _A,,2 [_A,C]2', L7, 'C,2 [E,G,]2 C,2']
A6h = "c4- c" + octs("c'd'^d'")
A7h = octs("e'c'd'e'- e'bd'2")
ENT_A_R = ["d'e'c'a- abg2", 'decA- ABG2', 'DECA,- A,B,A,_A,', 'G,2 z2 [GBdg]2 D^D',
           E5, A6h, A7h, octs("c'4- c'2") + ' D^D', E5, 'c4- c2 ' + octs('ag'), octs("^fac'e'- e'd'c'a"), octs("d'4- d'2") + ' D^D',
           E5, A6h, A7h, octs("c'4- c'2 c'd'"), octs("e'c'd'e'- e'c'd'c'"), octs("e'c'd'e'- e'c'd'c'"), A7h, octs("c'6") + ' z2']
S5, S6, S7 = 'C,2 [E,G,C]2 G,,2 [E,G,_B,]2', 'F,,2 [A,CF]2 E,,2 [G,CE]2', 'G,,2 [G,CE]2 G,,2 [G,B,F]2'
ENT_A_L = ['z8', 'z8', 'D,E,C,A,,- A,,B,,A,,_A,,', 'G,,2 z2 [G,,G,]2 z2',
           S5, S6, S7, 'C,2 [G,CE]2 [G,CE]2 z2', S5, 'F,,2 [A,CF]2 E,,2 _E,,2', 'D,,2 [A,C^F]2 D,,2 [A,C^F]2', 'G,,2 [G,B,F]2 A,,2 B,,2',
           S5, S6, S7, 'C,2 [G,CE]2 [G,CE]2 z2', 'C,2 [G,CE]2 _B,,2 [G,CE]2', 'A,,2 [A,CF]2 _A,,2 [_A,CF]2', S7, 'C,2 [G,CE]2 [C,,C,]4']
ENT_E_R = ['D^D', E5, E6, E7, 'c4- c2 cd', 'ecde- ecdc', 'ecde- ecdc', E7, 'c4- c2']
ENT_E_L = ['z2', 'C,8', 'F,4 E,4', 'G,4 G,4', 'C,8', 'C,4 _B,,4', 'A,,4 _A,,4', 'G,,4 G,,4', 'C,6']
special('the-entertainer', 'The Entertainer', 'Scott Joplin, 1902', 'Ragtime', dict(
    easy=dict(M='4/4', L=S16, scale=2, Lout=Fr(1, 8), K='C', Q='1/4=112', v1=J(*ENT_E_R), v2=J(*ENT_E_L),
              note='The famous tune in 8 bars, written in easy-to-count eighth notes'),
    inter=dict(M='2/4', L=S16, K='C', Q='1/4=66', v1=J(*ENT_I_R), v2=J(*ENT_I_L), note='First strain with a light ragtime bass'),
    adv=dict(M='2/4', L=S16, K='C', Q='1/4=76', v1=J(*ENT_A_R), v2=J(*ENT_A_L), note='Introduction and first strain, octaves and stride bass'),
), badges=['Excerpt'], note="Joplin's melody for the introduction and first strain; the left hand is a new, simpler stride part. “Not fast.”")

# ============================================================ Maple Leaf Rag
MAP_R = ['z2', 'z A[Ee]A c[Ee]2G', '[Ee]GB[Ee]- [Ee]4', 'z A[Ee]A c[Ee]2G', '[Ee]GB[Ee]- [Ee]2 z[Ee]',
         'z A_c[_F_f] z[Ee] z[Ee]', 'z A_c[_F_f] z[Ee] z2', 'z8', "z A_ca z a_c'a'",
         "[aa']2[aa']2 [aa']2[aa'][aa']-", "[aa']e'f'c' e'[af']2[_fa]-", "[_fa]b[_f_c']a b[ec']2a", "[ec']a[eb]2 [ea]2 z[Aa]-",
         '[Aa]2[Aa]2 [Aa]2[Aa][Aa]-', '[Aa]e[Af]c e[Af]2[_FA]-', '[_FA]B[_F_c]A B[Ec]2A', '[Ec]A[EB]2 [EA]2']
MAP_L = ['[E,,E,]2', '[A,,A,]2[E,A,C]2 [E,A,C]2[=A,,=A,]2', '[B,,B,]2[E,G,D]2 [E,G,D]2[E,,E,]2',
         '[A,,A,]2[E,A,C]2 [E,A,C]2[=A,,=A,]2', '[B,,B,]2[E,G,D]2 [E,G,D]2[E,,E,]2',
         '[_F,,_F,]4 [E,,E,]2[E,,E,]2', '[_F,,_F,]4 [E,,E,]2 z2', 'A,,,A,,_C,A, A,,A,_CA', 'A,2 z2 A2 z2',
         '[K:clef=treble][=DFA=B]2[=DFA=B]2 [=DFA=B]2[=DFA=B]2', '[EAc]2[EAc]2 [EAc]2[EAc]2', '[_FA_c]2[_FA_c]2 [EAc]2[EAc]2', '[EAc]2[EGd]2 [Ac]2 z2',
         '[K:clef=bass][=D,F,A,=B,]2[=D,F,A,=B,]2 [=D,F,A,=B,]2[=D,F,A,=B,]2', '[E,A,C]2[E,A,C]2 [E,A,C]2[E,A,C]2',
         '[_F,A,_C]2[_F,A,_C]2 [E,A,C]2[E,A,C]2', '[E,A,C]2[E,G,D]2 [A,C]2']
MI = [0, 1, 2, 3, 4, 5, 6, 7, 8, 13, 14, 15, 16]
ME = [0, 1, 2, 3, 4, 13, 14, 15, 16]
MAP_L_I = [MAP_L[i] for i in MI]
MAP_L_I[9] = MAP_L_I[9].replace('[K:clef=bass]', '')
MAP_E_L = ['E,2', 'A,,4 E,4', 'E,,4 E,4', 'A,,4 E,4', 'E,,4 E,4', '=D,8', 'E,8', '_F,4 E,4', 'E,2 E,2 A,,2']
special('maple-leaf-rag', 'Maple Leaf Rag', 'Scott Joplin, 1899', 'Ragtime', dict(
    easy=dict(M='4/4', L=S16, scale=2, Lout=Fr(1, 8), K='Ab', Q='1/4=108', v1=J(*[MAP_R[i] for i in ME]), v2=J(*MAP_E_L),
              thin1='oct_hi', note='Opening and closing bars of the first strain, one bass note at a time'),
    inter=dict(M='2/4', L=S16, K='Ab', Q='1/4=66', v1=J(*[MAP_R[i] for i in MI]), v2=J(*MAP_L_I),
               thin1='oct_hi', thin2='oct_lo', note='First strain without the high middle phrase, octaves removed'),
    adv=dict(M='2/4', L=S16, K='Ab', Q='1/4=80', v1=J(*MAP_R), v2=J(*MAP_L), note="First strain as Joplin wrote it"),
), badges=['Excerpt'], note='The first strain (16 bars) of the rag. Tempo di marcia: steady, never rushed.')

# ============================================================ Practice exercises (original)
special('practice-triplets', 'Even Triplets', 'Practice exercise', 'Practice', dict(
    easy=dict(M='12/8', K='Am', to='C#m', oct=-1, Q='3/8=50', v1=J('EAc EAc EAc EAc', 'EAc EAc EAc EAc', 'FAc FAc FAc FAc', 'DFA DFA E^GB E^GB', 'EAc EAc [EAc]6'),
              v2=J('A,12', 'G,12', 'F,12', 'D,6 E,6', 'A,12'), note='Right hand stays in one place; left hand holds one note per bar'),
    inter=dict(M='12/8', K='Am', to='C#m', oct=-1, Q='3/8=50',
               v1=J('EAc EAc EAc EAc', 'EAc EAc EAc EAc', 'FAc FAc FAd FAd', 'E^Gd EAc EAB D^GB', 'EAc EAc [EAc]6'),
               v2=J('A,12', 'G,12', 'F,6 D,6', 'E,6 E,6', 'A,12'), note='Moving the chord shapes'),
    adv=dict(M='12/8', K='Am', to='C#m', oct=-1, Q='3/8=54',
             v1=J('EAc EAc EAc EAc & e12', 'EAc EAc EAc EAc & e9 e3', 'FAc FAc FAd FAd & f6 f6', 'E^Gd EAc EAB D^GB & e6 e3 d3', 'EAc EAc [EAc]6 & e12'),
             v2=J('[A,,A,]12', '[G,,G,]12', '[F,,F,]6 [D,,D,]6', '[E,,E,]6 [E,,E,]6', '[A,,A,]12'),
             note='Add a singing top note and left-hand octaves'),
), note='Preparation for the Moonlight Sonata: play the three notes perfectly evenly, quietly, without tension. Start around 50 BPM.')

special('practice-broken-chords', 'Ballad Broken Chords', 'Practice exercise', 'Practice', dict(
    easy=dict(M='4/4', K='C', Q='1/4=72', v1=J('"C"E4 G4', '"G"D4 G4', '"Am"E4 A4', '"F"c4 A4', '"C"G4 E4', '"G"D4 B,4', '"F"C4 F4', '"C"E8'),
              v2=J('C,2G,2 E,2G,2', 'G,,2D,2 B,,2D,2', 'A,,2E,2 C,2E,2', 'F,,2C,2 A,,2C,2', 'C,2G,2 E,2G,2', 'G,,2D,2 B,,2D,2', 'F,,2C,2 A,,2C,2', '[C,G,]8'),
              note='Left hand in quarter notes'),
    inter=dict(M='4/4', K='C', Q='1/4=76', v1=J('"C"E2 G2 c2 G2', '"G"D2 G2 B2 G2', '"Am"E2 A2 c2 A2', '"F"c2 A2 F2 A2', '"C"G2 E2 G2 c2', '"G"d2 B2 G2 D2', '"F"C2 F2 A2 G2', '"C"E8'),
               v2=J('C,G,E,G, C,G,E,G,', 'G,,D,B,,D, G,,D,B,,D,', 'A,,E,C,E, A,,E,C,E,', 'F,,C,A,,C, F,,C,A,,C,', 'C,G,E,G, C,G,E,G,', 'G,,D,B,,D, G,,D,B,,D,', 'F,,C,A,,C, F,,C,A,,C,', '[C,G,]8'),
               note='Left hand in flowing eighth notes'),
    adv=dict(M='4/4', K='C', Q='1/4=80', v1=J('"C"e3 d c2 G2', '"G"d3 c B2 G2', '"Am"c3 B A2 E2', '"F"A3 G F2 A2', '"C"G3 A c2 e2', '"G"d3 B G2 B2', '"F"A2 c2 "G7"B2 d2', '"C"[EGc]8'),
             v2=J('C,,G,,C,E, G,E,C,G,,', 'G,,,D,,G,,B,, D,B,,G,,D,,', 'A,,,E,,A,,C, E,C,A,,E,,', 'F,,,C,,F,,A,, C,A,,F,,C,,', 'C,,G,,C,E, G,E,C,G,,', 'G,,,D,,G,,B,, D,B,,G,,D,,', 'F,,,C,,F,,A,, G,,,D,,G,,B,,', '[C,,G,,C,]8'),
             note='Wide left-hand arpeggios (use the pedal)'),
), note='The left-hand pattern behind most piano ballads: C – G – Am – F. Keep the left hand soft and even; let the right hand sing.')

special('practice-descending-bass', 'Descending-Bass Chord Changes', 'Practice exercise', 'Practice', dict(
    easy=dict(M='4/4', K='C', Q='1/4=72', v1=J('"C"[EGc]8', '"G/B"[DGB]8', '"Am"[EAc]8', '"C/G"[EGc]8', '"F"[FAc]8', '"C/E"[EGc]8', '"G7"[DFB]8', '"C"[EGc]8'),
              v2=J('C,8', 'B,,8', 'A,,8', 'G,,8', 'F,,8', 'E,,8', 'G,,8', 'C,8'), note='Whole-note chords over a stepwise bass'),
    inter=dict(M='4/4', K='C', Q='1/4=80', v1=J('"C"[EGc]2 [EGc]2 [EGc]2 [EGc]2', '"G/B"[DGB]2 [DGB]2 [DGB]2 [DGB]2', '"Am"[EAc]2 [EAc]2 [EAc]2 [EAc]2', '"C/G"[EGc]2 [EGc]2 [EGc]2 [EGc]2',
                                              '"F"[FAc]2 [FAc]2 [FAc]2 [FAc]2', '"C/E"[EGc]2 [EGc]2 [EGc]2 [EGc]2', '"Dm7"[DFc]2 [DFc]2 "G7"[DFB]2 [DFB]2', '"C"[EGc]8'),
               v2=J('C,8', 'B,,8', 'A,,8', 'G,,8', 'F,,8', 'E,,8', 'D,4 G,,4', 'C,8'), note='Steady quarter-note chords'),
    adv=dict(M='4/4', K='C', Q='1/4=84', v1=J('"C"EGce gecG', '"G/B"DGBd gdBG', '"Am"EAce aecA', '"C/G"EGce gecG', '"F"FAcf afcA', '"C/E"EGce gecG', '"Dm7"DFAc "G7"dBGF', '"C"[EGc]8'),
             v2=J('[C,,C,]8', '[B,,,B,,]8', '[A,,,A,,]8', '[G,,,G,,]8', '[F,,,F,,]8', '[E,,,E,,]8', '[D,,D,]4 [G,,,G,,]4', '[C,,C,]8'),
             note='Right-hand arpeggios over left-hand octaves'),
), note='Smooth voice-leading over a bass that walks down the scale: the sound of countless pop ballads, without quoting any of them.')

FF = 'C2D2 E2F2', 'G2F2 E2D2'
special('practice-five-finger', 'Five-Finger Independence', 'Practice exercise', 'Practice', dict(
    easy=dict(M='4/4', K='C', Q='1/4=80', v1=J(FF[0], FF[1], 'C8', 'z8', 'z8', 'z8', FF[0], FF[1], 'C8'),
              v2=J('z8', 'z8', 'z8', 'C,2D,2 E,2F,2', 'G,2F,2 E,2D,2', 'C,8', 'C,2D,2 E,2F,2', 'G,2F,2 E,2D,2', 'C,8'),
              note='Right hand, left hand, then together'),
    inter=dict(M='4/4', K='C', Q='1/4=84', v1=J('CDEF GFED', 'CDEF GFED', 'C3D E3F', 'G3F E3D', 'CDEF GFED', 'CEDF EGFD', 'C8'),
               v2=J('C,D,E,F, G,F,E,D,', 'C,D,E,F, G,F,E,D,', 'C,3D, E,3F,', 'G,3F, E,3D,', 'G,F,E,D, C,D,E,F,', 'G,E,F,D, E,C,D,F,', 'C,8'),
               note='Eighth notes, a long-short rhythm, then contrary motion'),
    adv=dict(M='4/4', K='C', Q='1/4=92', v1=J('CEDF EGFD', 'CEDF EGFD', 'GABc dcBA', 'GBAc BdcA', 'DE^FG AGFE', 'D^FEG FAGE', '[CEG]8'),
             v2=J('G,E,F,D, E,C,D,F,', 'C,E,D,F, E,G,F,D,', 'G,,A,,B,,C, D,C,B,,A,,', 'D,B,,C,A,, B,,G,,A,,C,', 'D,E,^F,G, A,G,F,E,', 'A,^F,G,E, F,D,E,G,', '[C,G,]8'),
             note='Broken thirds in the C, G and D hand positions'),
), note='Each hand separately, then together. Vary the rhythm; never force — stop if anything hurts.')

# ============================================================ Style studies (original music)
STUDIES = []


def study(id, title, about, spec, note):
    STUDIES.append(dict(id=id, title=title, composer=about, cat='Style Studies', levels=dict(study=spec), note=note, kind='study',
                        badges=['Original exercise']))


study('study-gospel-ballad', 'Style study: gospel ballad piano', 'In the style of Elton John · original exercise',
      dict(M='4/4', K='C', Q='1/4=72',
           v1=J('"C"[EGc]3[EGc]- [EGc]2[EGc]2', '"F"[FAc]3[FAc]- [FAc]2[EGc]2', '"C"[EGc]3[Gce]- [Gce]2[Gcd]2', '"G/B"[GBd]3[GBd]- [GBd]2[GBd]2',
                '"Am"[EAc]3[EAc]- [EAc]2[EAc]2', '"F"[FAc]3[FAd]- [FAd]2[FAc]2', '"C/G"[EGc]4 "G7sus"[DGc]2 "G"[DGB]2', '"C"[EGc]8'),
           v2=J('[C,,C,]4 [C,,C,]2[E,,E,]2', '[F,,F,]4 [F,,F,]2[E,,E,]2', '[C,,C,]4 [C,,C,]2[C,,C,]2', '[B,,,B,,]4 [B,,,B,,]2[^G,,,^G,,]2',
                '[A,,,A,,]4 [A,,,A,,]2[G,,,G,,]2', '[F,,,F,,]4 [F,,,F,,]2[^F,,,^F,,]2', '[G,,,G,,]4 [G,,,G,,]4', '[C,,C,]8')),
      'Left-hand octaves with passing notes that lead into the next chord, and right-hand chords pushed just ahead of the beat. An original 8 bars; no song is quoted.')
study('study-descending-bass', 'Style study: descending-bass ballad', 'In the style of the Beatles · original exercise',
      dict(M='4/4', K='C', Q='1/4=76',
           v1=J('"C"[EGc]2[EGc]2 [EGc]2[EGc]2', '"C/B"[EGc]2[EGc]2 [EGd]2[EGc]2', '"Am"[EAc]2[EAc]2 [EAc]2[EAc]2', '"Am/G"[EAc]2[EAc]2 [EAB]2[EAc]2',
                '"F"[FAc]2[FAc]2 [FAd]2[FAc]2', '"C/E"[EGc]2[EGc]2 [EGc]2[EGB]2', '"Dm7"[DFA]2[DFc]2 "G7"[DFB]2[DFB]2', '"C"[EGc]8'),
           v2=J('C,8', 'B,,8', 'A,,8', 'G,,8', 'F,,8', 'E,,8', 'D,4 G,,4', 'C,8')),
      'Steady quarter-note chords in the right hand while the bass steps down the scale one note per bar (C – B – A – G – F – E). Original music.')
study('study-piano-waltz', 'Style study: piano-bar waltz', 'In the style of Billy Joel · original exercise',
      dict(M='3/4', K='C', Q='1/4=152',
           v1=J('"C"e4 dc', '"Em/B"B4 G2', '"Am"c4 BA', '"C/G"G6', '"F"A4 cA', '"C/E"G4 E2', '"Dm7"F2 A2 c2', '"G7"B4 d2', '"C"c6'),
           v2=J('C,2 [E,G,]2[E,G,]2', 'B,,2 [E,G,]2[E,G,]2', 'A,,2 [C,E,]2[C,E,]2', 'G,,2 [C,E,]2[C,E,]2', 'F,,2 [A,,C,]2[A,,C,]2',
                'E,,2 [G,,C,]2[G,,C,]2', 'D,2 [F,A,]2[F,A,]2', 'G,,2 [F,B,]2[F,B,]2', 'C,2 [E,G,]4')),
      'An oom-pah-pah left hand over a walking-down bass, with a simple tune on top. Original music.')
BOOG = lambda r, f, s: '[%s%s][%s%s] [%s%s][%s%s] [%s%s][%s%s] [%s%s][%s%s]' % (r, f, r, f, r, s, r, s, r, f, r, f, r, s, r, s)
BC, BF, BG = BOOG('C,', 'G,', 'A,'), BOOG('F,,', 'C,', 'D,'), BOOG('G,,', 'D,', 'E,')
RC, RC7, RF, RG = 'z2 [EGc]2 z [EGc] z2', 'z2 [EGc]2 z [EG_B] z2', 'z2 [FAc]2 z [FAc] z2', 'z2 [GBd]2 z [GBd] z2'
study('study-rock-and-roll', 'Style study: rock-and-roll piano', 'In the style of Bob Seger · original exercise',
      dict(M='4/4', K='C', Q='1/4=126',
           v1=J('"C"' + RC, RC, RC, '"C7"' + RC7, '"F"' + RF, RF, '"C"' + RC, RC, '"G"' + RG, '"F"' + RF, '"C"' + RC, '[EGc]8'),
           v2=J(BC, BC, BC, BC, BF, BF, BC, BC, BG, BF, BC, '[C,,C,]8')),
      'A 12-bar blues: the left hand rocks between the fifth and the sixth (the boogie pattern) while the right hand stabs chords off the beat. Original music.')
study('study-power-ballad', 'Style study: power-ballad chords', 'In the style of Foreigner · original exercise',
      dict(M='4/4', K='Am', Q='1/4=66',
           v1=J('"Am"[EAc]8', '"F"[FAc]6 [FAd]2', '"C"[EGc]8', '"G"[DGB]6 [DGc]2', '"Am"[EAc]4 [EAe]4', '"F"[FAc]4 [FAf]4', '"C"[EGc]4 [EGe]4', '"G"[DGB]8', '"Am"[EAc]8'),
           v2=J('A,,A,,A,,A,, A,,A,,A,,A,,', 'F,,F,,F,,F,, F,,F,,F,,F,,', 'C,C,C,C, C,C,C,C,', 'G,,G,,G,,G,, G,,G,,G,,G,,',
                'A,,A,,A,,A,, A,,A,,A,,A,,', 'F,,F,,F,,F,, F,,F,,F,,F,,', 'C,C,C,C, C,C,C,C,', 'G,,G,,G,,G,, G,,G,,G,,G,,', '[A,,,A,,]8')),
      'Long, sustained right-hand chords over a quietly pulsing bass note: let each chord ring. Original music.')
study('study-folk-strum', 'Style study: folk-song accompaniment', 'In the style of Pete Seeger and Woody Guthrie · original exercise',
      dict(M='4/4', K='G', Q='1/4=104',
           v1=J('"G"G2 B2 d2 B2', 'd4 B4', '"C"e2 e2 d2 c2', '"G"B6 z2', '"D7"A2 A2 B2 c2', 'd2 c2 A2 F2', '"G"G2 B2 d2 B2', 'G8'),
           v2=J('G,,2 [G,B,]2 D,2 [G,B,]2', 'G,,2 [G,B,]2 D,2 [G,B,]2', 'C,2 [E,G,]2 G,,2 [E,G,]2', 'G,,2 [G,B,]2 D,2 [G,B,]2',
                'D,2 [F,C]2 A,,2 [F,C]2', 'D,2 [F,C]2 A,,2 [F,C]2', 'G,,2 [G,B,]2 D,2 [G,B,]2', 'G,,2 [G,B,]2 G,,4')),
      'The piano version of a guitar strum: bass note, chord, other bass note, chord. Three chords and an original tune.')

# ============================================================ Pop requests: chord charts and the request list


def bars(s):
    return [b.split() for b in s.strip().strip('|').split('|')]


# Chord charts for the pop requests: chord names, section labels and bar structure only.
# No melody and no lyrics.  Each chart was checked against the chord pages listed above it
# (UG = ultimate-guitar.com, GT = guitartabs.cc, GTAB = guitaretab.com); where a page is written
# for guitar with a capo, the chords are given here at sounding pitch.  Bar lengths are the
# arranger's reading of those pages and may differ from a printed score.
# status: 'play' = Danny can play it, 'learn' = Danny wants to learn it.
CHARTS = [
    # https://tabs.ultimate-guitar.com/tab/the-beatles/let-it-be-chords-17427
    # https://www.guitartabs.cc/tabs/b/beatles/let_it_be_acoustic_crd.html
    dict(id='chart-let-it-be', title='Let It Be', artist='The Beatles', key='C major', abckey='C', feel='Slow gospel ballad, 4/4', bpm=72, sections=[
        ('Intro', 'C G|Am F|C G|F F C/E Dm7 C C C C'),
        ('Verse', 'C G|Am F|C G|F F C/E Dm7 C C C C|C G|Am F|C G|F F C/E Dm7 C C C C'),
        ('Chorus', 'Am G|F C|C G|F F C/E Dm7 C C C C')]),
    # https://tabs.ultimate-guitar.com/tab/the-beatles/yesterday-chords-17450
    # https://www.guitartabs.cc/tabs/b/beatles/yesterday_crd.html
    dict(id='chart-yesterday', title='Yesterday', artist='The Beatles', key='F major', abckey='F', feel='Gentle ballad, 4/4', bpm=96, sections=[
        ('Verse (7 bars)', 'F|Em7 A7|Dm Dm/C|Bb C7|F C/E|Dm7 G7|Bb F'), ('Bridge', 'Em7 A7|Dm Dm/C Bb Bb|Gm C7|F|Em7 A7|Dm Dm/C Bb Bb|Gm C7|F')]),
    # https://tabs.ultimate-guitar.com/tab/the-beatles/hey-jude-chords-1061739  (capo 3)
    # https://www.guitartabs.cc/tabs/b/beatles/hey_jude_crd_ver_5.html  (written in G)
    dict(id='chart-hey-jude', title='Hey Jude', artist='The Beatles', key='F major', abckey='F', feel='Broad ballad, 4/4', bpm=74, sections=[
        ('Verse', 'F|C|C7|F|Bb|F|C7|F'), ('Bridge', 'F7|Bb Bb/A|Gm Gm/F|C7/E C7|F'), ('Outro', 'F|Eb|Bb|F')]),
    # https://tabs.ultimate-guitar.com/tab/the-beatles/in-my-life-chords-17422  (capo 2)
    # https://www.guitartabs.cc/tabs/b/beatles/in_my_life_crd_ver_5.html
    dict(id='chart-in-my-life', title='In My Life', artist='The Beatles', key='A major', abckey='A', feel='Moderate, 4/4', bpm=104, sections=[
        ('Intro', 'A|E|A|E'), ('Verse', 'A E|F#m A7/G|D Dm|A|A E|F#m A7/G|D Dm|A'), ('Chorus', 'F#m|D|G|A|F#m|B7|Dm|A')]),
    # https://tabs.ultimate-guitar.com/tab/john-lennon/imagine-chords-9306
    # https://www.guitartabs.cc/tabs/l/lennon_john/imagine_crd.html  (partial)
    dict(id='chart-imagine', title='Imagine', artist='John Lennon', key='C major', abckey='C', feel='Slow piano ballad, 4/4', bpm=76, status='learn', sections=[
        ('Intro / Verse', 'C Cmaj7|F|C Cmaj7|F'), ('Bridge', 'F Am/E|Dm7 F/C|G|G7'), ('Chorus', 'F G|C Cmaj7 E E7|F G|C Cmaj7 E E7|F G|C')]),
    # https://tabs.ultimate-guitar.com/tab/elton-john/your-song-chords-29113  (capo 1)
    # https://www.guitartabs.cc/tabs/e/elton_john/your_song_crd_ver_5.html  (written in C)
    dict(id='chart-your-song', title='Your Song', artist='Elton John', key='E♭ major', abckey='Eb', feel='Flowing ballad, 4/4', bpm=66, status='play', sections=[
        ('Intro', 'Eb Ab/Eb|Bb/Eb Ab/Eb'),
        ('Verse', 'Eb Abmaj7|Bb/D Gm|Cm Cm/Bb|Cm/A Abmaj7|Eb Bb|G/B Cm|Eb Fm7|Ab Bb'),
        ('Chorus', 'Bb/D Cm|Fm7 Ab|Bb/D Cm|Fm7 Ab|Cm Cm/Bb|Cm/A Ab|Eb/G Fm7|Ab Bb')]),
    # https://tabs.ultimate-guitar.com/tab/billy-joel/piano-man-chords-1051336
    # https://www.guitartabs.cc/tabs/b/billy_joel/piano_man_crd.html  (partial)
    dict(id='chart-piano-man', title='Piano Man', artist='Billy Joel', key='C major', abckey='C', feel='Waltz, 3/4 (felt in one)', bpm=170, M='3/4', comp='waltz', sections=[
        ('Verse / Chorus', 'C|G/B|F/A|C/G|F|C/E|D7|G|C|G/B|F/A|C/G|F|G|C|C'), ('Interlude', 'Am|Am/G|D7/F#|F|Am|Am/G|D7/F#|G')]),
    # https://tabs.ultimate-guitar.com/tab/bob-seger/old-time-rock-and-roll-chords-331847  (capo 2)
    # https://www.guitartabs.cc/tabs/b/bob_seger/old_time_rock_and_roll_crd.html
    dict(id='chart-old-time-rock-and-roll', title='Old Time Rock and Roll', artist='Bob Seger', key='F♯ major (I – IV – V)', abckey='F#', feel='Driving rock and roll, 4/4', bpm=124, comp='rock', sections=[
        ('Verse / Chorus', 'F#|F#|B|B|C#|C#|F#|F#')]),
    # https://tabs.ultimate-guitar.com/tab/bob-seger-the-silver-bullet-band/turn-the-page-chords-2166139
    # https://www.guitartabs.cc/tabs/b/bob_seger/turn_the_page_crd.html
    dict(id='chart-turn-the-page', title='Turn the Page', artist='Bob Seger', key='E minor', abckey='Em', feel='Slow rock ballad, 4/4', bpm=70, sections=[
        ('Verse', 'Em|Em|D|D|A|A|Em|Em'), ('Chorus', 'D|Em|D|Em|D|A|C D|Em')]),
    # https://tabs.ultimate-guitar.com/tab/pete-seeger/where-have-all-the-flowers-gone-chords-1055880
    # https://www.guitaretab.com/p/pete-seeger/276967.html
    dict(id='chart-where-have-all-the-flowers-gone', title='Where Have All the Flowers Gone?', artist='Pete Seeger', key='A major', abckey='A', feel='Gentle folk, 4/4', bpm=100, comp='folk', sections=[
        ('Verse', 'A|F#m|D|E|A|F#m|Bm|E7|A|F#m|D|E|D|A|D E|A')]),
    # https://tabs.ultimate-guitar.com/tab/woody-guthrie/this-land-is-your-land-chords-1054304
    # https://www.guitartabs.cc/tabs/w/woody_guthrie/this_land_is_your_land_crd_ver_2.html
    dict(id='chart-this-land-is-your-land', title='This Land Is Your Land', artist='Woody Guthrie', key='D major', abckey='D', feel='Easy folk two-step, 4/4', bpm=112, comp='folk', sections=[
        ('Verse / Chorus', 'G|D|A7|D|G|D|A7|D')]),
    # https://tabs.ultimate-guitar.com/tab/the-beatles/the-long-and-winding-road-chords-525032  (capo 1)
    # https://www.guitartabs.cc/tabs/b/beatles/the_long_and_winding_road_crd.html
    dict(id='chart-the-long-and-winding-road', title='The Long and Winding Road', artist='The Beatles', key='E♭ major (starts on C minor)', abckey='Eb', feel='Slow ballad, 4/4', bpm=66, sections=[
        ('Verse', 'Cm|Ab/Bb|Eb Eb7|Ab|Gm Cm|Fm7 Bb7|Eb Eb7|Ab|Gm Cm|Fm7 Bb7|Eb'), ('Bridge', 'Eb Ab|Gm Fm7 Bb7 Bb7|Eb Ab|Gm Fm7 Bb7 Bb7')]),
    # https://tabs.ultimate-guitar.com/tab/elton-john/tiny-dancer-chords-900075
    # https://www.guitartabs.cc/tabs/e/elton_john/tiny_dancer_crd_ver_4.html
    # Danny's printed copy is in G (it opens G | C | G | C): the same pattern, a fourth lower.
    dict(id='chart-tiny-dancer', title='Tiny Dancer', artist='Elton John', key="C major (Danny's printed copy is in G: read C as G, F as C, G as D)", abckey='C', feel='Rolling piano ballad, 4/4', bpm=72, sections=[
        ('Intro', 'C F/C|C F/C'),
        ('Verse', 'C F/C|C F/C|C F/A|G/B G|C F/C|C F/C|C F/A|G|F Em7|Am7 D7/F#|Dm7 E7|Am G7|C F/C|C F/C|C G|F Em7 Dm7 Dm7'),
        ('Pre-chorus', 'Ab Bb|Gm Cm|Ab Bb|G/B G/D'),
        ('Chorus', 'F C/E|Dm C|F C/E|A7sus4|F C/E|Dm C|F C/E|A7sus4')]),
    # https://tabs.ultimate-guitar.com/tab/elton-john/rocket-man-chords-10744  (capo 3)
    # https://www.guitartabs.cc/tabs/e/elton_john/rocket_man_crd.html
    dict(id='chart-rocket-man', title='Rocket Man', artist='Elton John', key='B♭ major (verse starts on G minor)', abckey='Bb', feel='Spacious ballad, 4/4', bpm=70, sections=[
        ('Verse', 'Gm7|C9|Gm7|C9|Eb Bb/D|Cm Cm/Bb|F/A|F'), ('Chorus', 'Bb|Eb|Bb|Eb|Bb/D|C9|Eb|Bb Eb')]),
    # https://tabs.ultimate-guitar.com/tab/elton-john/candle-in-the-wind-chords-1086982  (capo 2)
    # https://www.guitartabs.cc/tabs/e/elton_john/candle_in_the_wind_crd.html
    dict(id='chart-candle-in-the-wind', title='Candle in the Wind', artist='Elton John', key='E major', abckey='E', feel='Gentle ballad, 4/4', bpm=84, sections=[
        ('Verse', 'E|E|A|A|E|E|A|A'), ('Chorus', 'B|B7|E|A|E|B|A|C#m|B|A|E')]),
    # https://tabs.ultimate-guitar.com/tab/elton-john/dont-let-the-sun-go-down-on-me-chords-1065058
    # https://www.guitaretab.com/e/elton-john/280545.html
    dict(id='chart-don-t-let-the-sun-go-down-on-me', title="Don't Let the Sun Go Down on Me", artist='Elton John', key='C major', abckey='C', feel='Slow, broad ballad, 4/4', bpm=68, sections=[
        ('Intro', 'C|C/Bb|F C|F'), ('Verse', 'G C/G G G|F|C F/C C C/E|F Bb/F F F|G C/G G G|G'),
        ('Chorus', 'C|C/Bb|F/A|D7/F#|C/G|F/G G|C|C/Bb|F/A|Dm C/E|F|C/G G')]),
    # https://tabs.ultimate-guitar.com/tab/bob-seger-the-silver-bullet-band/night-moves-chords-1765474  (capo 1)
    # https://www.guitartabs.cc/tabs/b/bob_seger/night_moves_crd.html  (written in G)
    dict(id='chart-night-moves', title='Night Moves', artist='Bob Seger', key='A♭ major', abckey='Ab', feel='Loose, strummed rock, 4/4', bpm=118, comp='folk', sections=[
        ('Intro / Verse', 'Ab Gb|Db Gb|Ab Gb|Db Gb'), ('Chorus', 'Db Eb|Fm Eb|Db|Db|Db Eb|Fm Eb|Db|Db|Ab Gb|Db Gb'),
        ('Bridge', 'Dbmaj7|Ab|Dbmaj7|Ab|Gb|Eb|Ab|Ab')]),
    # https://tabs.ultimate-guitar.com/tab/bob-seger-the-silver-bullet-band/against-the-wind-chords-1708124
    # https://www.guitartabs.cc/tabs/b/bob_seger/against_the_wind_crd.html
    dict(id='chart-against-the-wind', title='Against the Wind', artist='Bob Seger', key='G major', abckey='G', feel='Easy country rock, 4/4', bpm=108, comp='folk', sections=[
        ('Verse', 'G|G|Bm|Bm|C|G|D C|G|G|G|Bm|Bm|C|G|C|D'), ('Pre-chorus', 'Em D|G|Em C|G|Em D|C|C|D'), ('Chorus', 'G|Bm|C|G|C Bm|Am|C|G')]),
    # https://tabs.ultimate-guitar.com/tab/bob-seger-the-silver-bullet-band/weve-got-tonight-chords-1930509
    # https://www.guitaretab.com/b/bob-seger/289887.html  (written in G)
    dict(id='chart-we-ve-got-tonight', title="We've Got Tonight", artist='Bob Seger', key='B major', abckey='B', feel='Slow piano ballad, 4/4', bpm=70, sections=[
        ('Verse', 'B F#/A#|E F#|B F#/A#|E/G# F#|B/D# Emaj7|B F#'), ('Chorus', 'B Emaj7|E6 B|B/D# Emaj7|E6 B')]),
    # https://tabs.ultimate-guitar.com/tab/bob-seger-the-silver-bullet-band/still-the-same-chords-1691983
    # https://www.guitartabs.cc/tabs/b/bob_seger/still_the_same_crd_ver_2.html
    dict(id='chart-still-the-same', title='Still the Same', artist='Bob Seger', key='C major', abckey='C', feel='Steady mid-tempo, 4/4', bpm=112, sections=[
        ('Intro / Verse', 'Cmaj7 C|Cmaj7 C|Cadd9|Em G|Cmaj7 C|Cmaj7 C|Cadd9|Em G|F G|C|E7|Am|Dm|G'), ('Chorus', 'C|E|A|Dm G|C|E|A|Dm G')]),
    # Danny's printed lead sheet (F major: F5, Bbsus2, G5, F/A, Bb5, C5)
    # https://tabs.ultimate-guitar.com/tab/pat-benatar/we-belong-chords-713978  (capo 3)
    # https://www.guitartabs.cc/tabs/p/pat_benatar/we_belong_crd.html
    dict(id='chart-we-belong', title='We Belong', artist='Pat Benatar', key='F major', abckey='F', feel='Moderate, pulsing eighths, 4/4', bpm=132, sections=[
        ('Verse', 'F5|F5|Bbsus2|Bbsus2|F5|F5|Bbsus2|Bbsus2'), ('Pre-chorus', 'G5|G5|F/A|Bb5|G5|G5|C5|C5'),
        ('Chorus', 'F|Bb|C5|C5|F|Bb|C5|C5|F|Bb|C5|C5|F|Bb|C5|C5')]),
    # Danny's printed copy (E-flat minor: intro, the Abm7 section and the turn Cb Gb/Bb | Abm7 Gb | Cb/Db)
    # https://tabs.ultimate-guitar.com/tab/foreigner/i-want-to-know-what-love-is-chords-42854  (tuned a half step down)
    # https://www.guitartabs.cc/tabs/f/foreigner/i_want_to_know_what_love_is_crd.html  (partial, other key)
    dict(id='chart-i-want-to-know-what-love-is', title='I Want to Know What Love Is', artist='Foreigner', key='E♭ minor (chorus in G♭ major)', abckey='Ebm', feel='Power ballad, 4/4', bpm=76, sections=[
        ('Intro', 'Ebm'), ('Verse', 'Ebm Ebm Ebm Db|Gb|Cb|Ebm|Ebm Ebm Ebm Db|Gb|Cb|Ebm'),
        ('Pre-chorus', 'Abm7|Db/Ab Abm7|Db/Ab Abm7|Abm7|Cb Gb/Bb|Abm7 Gb|Cb/Db'),
        ('Chorus (one source)', 'Gb|Ebm Db|Abm|Ebm Db|Gb|Ebm Db|Abm|Ebm Db')]),
    # https://www.guitaretab.com/b/byrds/275602.html
    # https://www.guitartabs.cc/tabs/b/byrds/turn_turn_turn_crd.html  (written in C)
    dict(id='chart-turn-turn-turn', title='Turn! Turn! Turn!', artist='Pete Seeger (as recorded by The Byrds)', key='D major', abckey='D', feel='Bright folk rock, 4/4', bpm=124, comp='folk', sections=[
        ('Chorus', 'D G|F#m A|D G|F#m A|G F#m|Em A|D'), ('Verse', 'A|D|A|D|A|D|G F#m|Em A|D')]),
    # https://tabs.ultimate-guitar.com/tab/pete-seeger/we-shall-overcome-chords-1055577
    # https://www.guitaretab.com/p/pete-seeger/276987.html
    dict(id='chart-we-shall-overcome', title='We Shall Overcome', artist='Traditional / Pete Seeger', key='C major', abckey='C', feel='Slow and steady, 4/4', bpm=72, sections=[
        ('Verse', 'C F|C|C F|C|C F G Am|D G D G|C F|C|F G|Am|C F C G|C')]),
    # https://tabs.ultimate-guitar.com/tab/elton-john/goodbye-yellow-brick-road-chords-10735
    # https://www.guitartabs.cc/tabs/e/elton_john/goodbye_yellow_brick_road_crd.html
    dict(id='chart-goodbye-yellow-brick-road', title='Goodbye Yellow Brick Road', artist='Elton John', key='F major', abckey='F', feel='Slow, stately ballad, 4/4', bpm=62, status='learn', sections=[
        ('Intro', 'F C/E|Dm Dm/C|Bb C|F'),
        ('Verse', 'Gm C|F Bb|Eb C|F|Gm C|F Bb|Eb C|F|Db Eb|Ab Db|Bbm|C7'),
        ('Chorus', 'F A7|Bb F|D7 Gm|C F|Dm A|Bb Db|Db Eb|F C/E|Dm Dm/C|Bb C|Db Eb|Ab Db|Bbm C7|F')]),
    # https://tabs.ultimate-guitar.com/tab/misc-soundtrack/willy-wonka-and-the-chocolate-factory-pure-imagination-chords-1240149
    # https://www.guitaretab.com/w/willy-wonka/351254.html
    dict(id='chart-pure-imagination', title='Pure Imagination', artist='Leslie Bricusse and Anthony Newley, 1971', key='C major (as charted; not checked against the film key)', abckey='C', feel='Dreamy ballad, 4/4', bpm=70, sections=[
        ('Verse', 'Cmaj7|Dm7 G7|Cmaj7 Am7|Dm7 G7|Cmaj7|Dm9 G13|Cmaj7 Am7|Dm9 Db7#9|E'),
        ('Bridge', 'Fmaj7 Em7|Dm7 G7|Cmaj7 Dm7|D#dim Em7|F#m7b5 B7b9|Em|A7sus4 A7|Dm7 G7'),
        ('Last verse', 'Dm9 G13|Cmaj7 Am7|Dm9 G13|C6')]),
    # https://tabs.ultimate-guitar.com/tab/crowded-house/dont-dream-its-over-chords-92855  (capo 3)
    # https://www.guitaretab.com/c/crowded-house/358041.html  (written in G)
    dict(id='chart-don-t-dream-it-s-over', title="Don't Dream It's Over", artist='Crowded House', key='E♭ major', abckey='Eb', feel='Laid-back pop ballad, 4/4', bpm=82, status='learn', sections=[
        ('Intro', 'Ebsus2|Ebsus2'), ('Verse', 'Ebsus2|Cm|Ab|G|Ebsus2|Cm|Ab|G'), ('Chorus', 'Ab Bb|Eb Cm|Ab Bb|Eb Cm|Ab Bb|Eb Cm|Ab|Bb')]),
    # https://tabs.ultimate-guitar.com/tab/bob-dylan/i-shall-be-released-chords-1047043
    # https://www.guitartabs.cc/tabs/b/bob_dylan/i_shall_be_released_crd.html
    dict(id='chart-i-shall-be-released', title='I Shall Be Released', artist='Bob Dylan', key='A major', abckey='A', feel='Slow gospel-folk, 4/4', bpm=76, comp='folk', status='learn', sections=[
        ('Verse', 'A|Bm|C#m Bm|A|A|Bm|C#m Bm|A E7'), ('Chorus', 'A|Bm|C#m Bm|A|A|Bm|C#m Bm|A')]),
    # https://tabs.ultimate-guitar.com/tab/lou-reed/perfect-day-chords-96657  (capo 1)
    # https://www.guitartabs.cc/tabs/l/lou_reed/perfect_day_crd.html
    dict(id='chart-perfect-day', title='Perfect Day', artist='Lou Reed', key='B♭ minor (chorus in B♭ major)', abckey='Bbm', feel='Slow, gentle ballad, 4/4', bpm=72, status='play', sections=[
        ('Intro', 'F Bbm|F Bbm'), ('Verse', 'Bbm Eb|Ab Db|Gb Ebm|F|Bbm Eb|Ab Db|Gb Ebm|F'),
        ('Chorus', 'Bb Eb|Dm Eb|Bb F|Gm F Eb Eb|Bb Eb|Dm Eb|Bb F|Gm F Eb Eb')]),
    # https://tabs.ultimate-guitar.com/tab/r-e-m-/strange-currencies-chords-1094294
    # https://www.guitartabs.cc/tabs/r/rem/strange_currencies_crd.html  (agrees on verse and bridge; its chorus differs)
    dict(id='chart-strange-currencies', title='Strange Currencies', artist='R.E.M.', key='C major', abckey='C', feel='Slow 6/8 sway', bpm=56, M='6/8', status='learn', sections=[
        ('Intro / Verse', 'C|Fadd9|C|Fadd9|C|F|Dm|G'), ('Chorus (one source)', 'C G|F C|F|G|C G|F|C|Dm|G'), ('Bridge', 'Am|G|Am|G|Am|F|Dm|G')]),
    # https://tabs.ultimate-guitar.com/tab/louis-armstrong/what-a-wonderful-world-chords-955258  (capo 5)
    # https://www.guitartabs.cc/tabs/l/louis_armstrong/what_a_wonderful_world_crd.html
    dict(id='chart-what-a-wonderful-world', title='What a Wonderful World', artist='Bob Thiele and George David Weiss (Louis Armstrong recording)', key='F major', abckey='F', feel='Slow, warm ballad, 4/4', bpm=72, status='play', sections=[
        ('Intro', 'F Gm|F Gm'), ('Verse', 'F Am|Bb Am|Gm7 F|A7 Dm|Db|Gm7 C7|F|F'), ('Bridge', 'C7|F|C7|F|Dm C|Dm C|Dm F#dim7|Gm7 C7')]),
    # https://tabs.ultimate-guitar.com/tab/chicago/hard-to-say-im-sorry-chords-1423583
    # https://www.guitaretab.com/c/chicago/369970.html  (simpler chords, same outline)
    dict(id='chart-hard-to-say-i-m-sorry', title="Hard to Say I'm Sorry", artist='Chicago', key='E major', abckey='E', feel='Piano power ballad, 4/4', bpm=72, status='learn', sections=[
        ('Verse', 'E|G#m7|A|A B|C#m B|E|G#m7|A|A B|C#m B'), ('Pre-chorus', 'C#m F#m|Bsus4 B|E|C#m F#m|Bsus4 B'),
        ('Chorus', 'E|A B|G#|C#m|F#|B|E|A B|G#|C#m F#|Bsus4 B')]),
    # https://tabs.ultimate-guitar.com/tab/chicago/if-you-leave-me-now-chords-151311  (tuned a half step down)
    # https://www.guitartabs.cc/tabs/c/chicago/if_you_leave_me_now_crd.html  (same shapes, written in C)
    dict(id='chart-if-you-leave-me-now', title='If You Leave Me Now', artist='Chicago', key='B major', abckey='B', feel='Soft ballad, 4/4', bpm=96, status='learn', sections=[
        ('Verse', 'B|G#m|D#m|D#m|G#m C#|F#|B|B'), ('Chorus', 'Eadd9|Am|E|E|G#m E|F# B|A#m D#|Eadd9|Am|E|E|G#m E|F# B|D#m G#m|C#m Em')]),
    # https://tabs.ultimate-guitar.com/tab/neil-diamond/sweet-caroline-chords-1053578  (capo 2)
    # https://www.guitartabs.cc/tabs/n/neil_diamond/sweet_caroline_crd.html  (written in A)
    dict(id='chart-sweet-caroline', title='Sweet Caroline', artist='Neil Diamond', key='B major', abckey='B', feel='Mid-tempo singalong, 4/4', bpm=126, status='learn', sections=[
        ('Intro', 'F#7|F#7|F#7|F#7'), ('Verse', 'B|B|E|E|B|B|F#|F#'), ('Pre-chorus', 'B|B|G#m|G#m|F#|F#|E|F#'),
        ('Chorus', 'B|E|E|F#|B|E|E|F#|E D#m|C#m')]),
]
for c in CHARTS:
    c['sections'] = [dict(name=n, bars=bars(b)) for n, b in c['sections']]

# Still only requests: the chord pages found for this one are different arrangements that do not agree.
REQUESTS = [
    ('If I Had a Hammer', 'Pete Seeger'),
]
# Public-domain songs that were asked for but are not notated yet (melody not verified against a score).
PENDING = [
    ('In the Garden', 'C. Austin Miles, 1912', 'Hymns'), ('Softly and Tenderly', 'Will L. Thompson, 1880', 'Hymns'),
    ('Home on the Range', 'Traditional American', 'Singalongs'), ('Shine On, Harvest Moon', 'Nora Bayes and Jack Norworth, 1908', 'Singalongs'),
    ('In the Good Old Summertime', 'George Evans, 1902', 'Singalongs'), ('When Irish Eyes Are Smiling', 'Ernest R. Ball, 1912', 'Singalongs'),
    ('Down by the Old Mill Stream', 'Tell Taylor, 1908', 'Singalongs'), ("Alexander's Ragtime Band", 'Irving Berlin, 1911', 'Singalongs'),
]
