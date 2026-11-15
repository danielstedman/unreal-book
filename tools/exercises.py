# Practice exercises: finger strength and music reading.
# Hanon No. 1 is public domain (C.-L. Hanon, "The Virtuoso Pianist", 1873); everything else is original.
from fractions import Fraction as Fr
from specials import special, J, S16


# ------------------------------------------------------------ helpers
def nm(i):
    """C-major scale degree i (0 = middle C) -> ABC note."""
    l = 'CDEFGAB'[i % 7]
    o = 4 + i // 7
    if o >= 5:
        return l.lower() + "'" * (o - 5)
    return l + ',' * (4 - o)


def up(n):
    return [n, n + 2, n + 3, n + 4, n + 5, n + 4, n + 3, n + 2]


def down(n):
    return [n, n - 2, n - 3, n - 4, n - 5, n - 4, n - 3, n - 2]


def seq(degs, shift=0):
    return ''.join(nm(d + shift) for d in degs)


def mirror(rh):
    """RH five-finger C position -> LH mirror (same fingers): D->F, E->E, F->D, G->C, C->G."""
    m = {'C': 'G,', 'D': 'F,', 'E': 'E,', 'F': 'D,', 'G': 'C,'}
    return ''.join(m.get(ch, ch) for ch in rh)


# ------------------------------------------------------------ 1. Hanon No. 1
_ups7 = [up(n) for n in range(0, 7)]
_downs7 = [down(n) for n in range(11, 4, -1)]
_ups14 = [up(n) for n in range(0, 14)]
_downs14 = [down(n) for n in range(18, 4, -1)]

special('hanon-1', 'Hanon No. 1: Finger Strength', 'Charles-Louis Hanon, The Virtuoso Pianist (1873)', 'Practice', dict(
    easy=dict(M='4/4', K='C', Q='1/4=72',
              v1=J(*([seq(p) for p in _ups7[:4]] + ['z8'] * 4 + ['C8'])),
              v2=J(*(['z8'] * 4 + [seq(p, -7) for p in _ups7[:4]] + ['C,8'])),
              note='Hands separately: right hand climbs four steps, then the left hand'),
    inter=dict(M='4/4', K='C', Q='1/4=80',
               v1=J(*([seq(p) for p in _ups7 + _downs7] + ['C8'])),
               v2=J(*([seq(p, -7) for p in _ups7 + _downs7] + ['C,8'])),
               note='Hands together, one octave up and back; lift each finger high'),
    adv=dict(M='4/4', L=S16, K='C', Q='1/4=72',
             v1=J(*([seq(a) + ' ' + seq(b) for a, b in zip(_ups14[::2], _ups14[1::2])] +
                    [seq(a) + ' ' + seq(b) for a, b in zip(_downs14[::2], _downs14[1::2])] + ['C16'])),
             v2=J(*([seq(a, -7) + ' ' + seq(b, -7) for a, b in zip(_ups14[::2], _ups14[1::2])] +
                    [seq(a, -7) + ' ' + seq(b, -7) for a, b in zip(_downs14[::2], _downs14[1::2])] + ['C,16'])),
             note='Sixteenth notes over two octaves; raise the tempo only when every note is even'),
), badges=['Finger strength'], note='The classic finger workout. Keep the wrist loose and quiet; let the fingers do the work.')

# ------------------------------------------------------------ 2. Hold and Lift (independence)
_e = ['D2E2 D2E2', 'E2F2 E2F2', 'F2G2 F2G2', 'D2E2 F2G2']
_i = ['DEFE DEFE', 'EFGF EFGF', 'DFEG DFEG', 'GFED GFED']
_a = ['DFDF DGDG', 'FGFG DFDG', 'GFDF GFDF', 'DFGF DFGF']
special('hold-and-lift', 'Hold and Lift', 'Practice exercise', 'Practice', dict(
    easy=dict(M='4/4', K='C', Q='1/4=60',
              v1=J(*([b + ' & C8' for b in _e] + ['z8'] * 4 + ['[CEG]8'])),
              v2=J(*(['z8'] * 4 + [mirror(b) + ' & G,8' for b in _e] + ['[C,G,]8'])),
              note='Thumb holds its key down the whole bar while the other fingers play'),
    inter=dict(M='4/4', K='C', Q='1/4=72',
               v1=J(*([b + ' & C8' for b in _i] + ['[CEG]8'])),
               v2=J(*([mirror(b) + ' & G,8' for b in _i] + ['[C,G,]8'])),
               note='Hands together, thumbs held'),
    adv=dict(M='4/4', K='C', Q='1/4=80',
             v1=J(*([b + ' & [CE]8' for b in _a] + ['[CEG]8'])),
             v2=J(*([mirror(b) + ' & [E,G,]8' for b in _a] + ['[C,G,]8'])),
             note='Hold two fingers (1 and 3) while 2, 4 and 5 play'),
), badges=['Finger strength'], note='Builds independence: held fingers stay down and relaxed, moving fingers lift and drop cleanly.')

# ------------------------------------------------------------ 3. Trill Builders (fingers 3-4-5)
special('trill-builders', 'Trill Builders (Fingers 3, 4, 5)', 'Practice exercise', 'Practice', dict(
    easy=dict(M='4/4', K='C', Q='1/4=60',
              v1=J('EFEF EFEF', 'E8', 'FGFG FGFG', 'F8', 'DEDE EFEF', 'FGFG G4', 'EFGF EDCD', 'C8'),
              v2=J('C,8', 'C,8', 'C,8', 'C,8', 'C,8', 'G,,8', 'G,,8', 'C,8'),
              note='Right hand only: slow, even pairs'),
    inter=dict(M='4/4', L=S16, K='C', Q='1/4=56',
               v1=J('EFEF EFEF EFEF E4', 'FGFG FGFG FGFG F4', 'DEDE DEDE EFEF E4', 'FGFG FGFG G8',
                    'G16', 'G16', 'E16', 'C16'),
               v2=J('[C,G,]16', '[C,G,]16', '[C,G,]16', '[C,G,]16',
                    'E,D,E,D, E,D,E,D, E,D,E,D, E,4', 'D,C,D,C, D,C,D,C, D,C,D,C, D,4',
                    'F,E,F,E, F,E,F,E, E,D,E,D, D,4', 'D,C,D,C, D,C,D,C, C,8'),
               note='Right hand trills, then the left hand'),
    adv=dict(M='4/4', L=S16, K='C', Q='1/4=66',
             v1=J('EFEF EFEF FGFG FGFG', 'DEDE DEDE EFEF EFEF', 'GFGF GFGF FEFE FEFE', 'DCDC DCDC EDED EDED',
                  'FGFG EFEF DEDE CDCD', 'C16'),
             v2=J('E,D,E,D, E,D,E,D, D,C,D,C, D,C,D,C,', 'F,E,F,E, F,E,F,E, E,D,E,D, E,D,E,D,',
                  'C,D,C,D, C,D,C,D, D,E,D,E, D,E,D,E,', 'G,F,G,F, G,F,G,F, F,E,F,E, F,E,F,E,',
                  'D,C,D,C, E,D,E,D, F,E,F,E, G,F,G,F,', 'C,16'),
             note='Hands together in sixteenths'),
), badges=['Finger strength'], note='Strengthens the weaker outer fingers. Keep the hand arched; stop if anything aches.')

# ------------------------------------------------------------ 4. Landmark notes
special('reading-landmarks', 'Reading: Landmark Notes', 'Practice exercise', 'Practice', dict(
    easy=dict(M='4/4', K='C', Q='1/4=72',
              v1=J('C2 D2 E2 D2', 'C2 E2 G2 E2', 'G2 A2 G2 F2', 'E2 D2 C4', 'G2 F2 E2 F2', 'G2 c2 G4', 'E2 G2 F2 D2', 'C8'),
              v2=J('C,8', 'C,8', 'F,8', 'G,8', 'C,8', 'E,8', 'F,4 G,4', 'C,8'),
              note='Steps out from Middle C, Treble G and Bass C'),
    inter=dict(M='4/4', K='C', Q='1/4=76',
               v1=J('c2 G2 E2 C2', 'D2 F2 A2 c2', 'B2 G2 D2 G2', 'c4 C4', 'e2 c2 A2 F2', 'G2 B2 d2 g2', 'f2 d2 B2 G2', 'c8'),
               v2=J('C,2 E,2 G,2 E,2', 'F,2 A,2 F,2 C,2', 'G,,2 B,,2 D,2 G,2', 'C,4 C,,4', 'A,,2 C,2 E,2 A,2',
                    'G,,2 D,2 G,2 B,2', 'G,,2 B,,2 D,2 F,2', 'C,8'),
               note='Skips (line to line, space to space)'),
    adv=dict(M='4/4', K='C', Q='1/4=84',
             v1=J('C2 E2 G2 c2', "e2 g2 c'4", 'b2 g2 d2 B2', 'c4 G4', 'A,2 C2 F2 A2', 'c2 f2 a2 f2', 'd2 B2 G2 D2', 'C8'),
             v2=J('C,,2 G,,2 C,2 E,2', 'G,2 C2 E4', 'G,,8', 'C,4 E,4', 'F,,2 C,2 F,2 A,2', 'F,,8', 'G,,2 D,2 G,2 B,2', 'C,,8'),
             note='Leaps and ledger lines above and below both staves'),
), badges=['Reading'], note='Find the landmark notes first (Middle C, Treble G, Bass F, High C), then read by step and skip.')

# ------------------------------------------------------------ 5. Rhythm
special('reading-rhythm', 'Reading: Rhythm', 'Practice exercise', 'Practice', dict(
    easy=dict(M='4/4', K='C', Q='1/4=72',
              v1=J('C2 C2 C4', 'C2 C2 C2 C2', 'C4 C4', 'C8', 'E2 E2 E4', 'E2 z2 E2 z2', 'D4 D4', 'C8'),
              v2=J('C,8', 'C,8', 'C,8', 'C,8', 'C,8', 'C,8', 'G,,8', 'C,8'),
              note='Quarter, half and whole notes; count “1 2 3 4” aloud'),
    inter=dict(M='4/4', K='C', Q='1/4=80',
               v1=J('C2 CC C2 CC', 'C3C C2 C2', 'E2 EE E4', 'E3E E2 z2', 'G2 G2 GG G2', 'G3G G4', 'E2 D2 C3C', 'C8'),
               v2=J('C,2 C,2 C,2 C,2', 'C,2 C,2 C,2 C,2', 'C,2 C,2 C,2 C,2', 'C,2 C,2 C,2 C,2',
                    'C,2 C,2 C,2 C,2', 'C,2 C,2 C,2 C,2', 'G,,2 G,,2 G,,2 G,,2', 'C,8'),
               note='Eighth notes and dotted rhythms over a steady left hand; count “1 & 2 &”'),
    adv=dict(M='4/4', K='C', Q='1/4=88',
             v1=J('C2 (3CCC C2 C2', 'C C2 C C2 C2', 'z C2 C C2 C2', '(3EEE (3EEE E4', 'E3E z E3', 'G C2 G C2 G2', 'E3 D3 C2', 'C8'),
             v2=J('C,2 G,,2 C,2 G,,2', 'C,2 G,,2 C,2 G,,2', 'C,2 G,,2 C,2 G,,2', 'C,2 G,,2 C,2 G,,2',
                  'C,2 G,,2 C,2 G,,2', 'C,2 G,,2 C,2 G,,2', 'G,,2 D,2 G,,2 D,2', 'C,8'),
             note='Triplets and syncopation against a steady bass'),
), badges=['Reading'], note='One note per hand, so all your attention goes to the rhythm.')

# ------------------------------------------------------------ 6. Intervals
special('reading-intervals', 'Reading: Intervals', 'Practice exercise', 'Practice', dict(
    easy=dict(M='4/4', K='C', Q='1/4=66',
              v1=J('C2 D2 C2 E2', 'C2 F2 C2 G2', 'G2 F2 G2 E2', 'G2 D2 G2 C2', '[CD]4 [CE]4', '[CF]4 [CG]4', '[CE]4 [DF]4', '[CEG]8'),
              v2=J('C,8', 'C,8', 'G,,8', 'G,,8', 'C,8', 'C,8', 'G,,8', 'C,8'),
              note='2nds, 3rds, 4ths and 5ths, first one note at a time, then together'),
    inter=dict(M='4/4', K='C', Q='1/4=72',
               v1=J('C2 A2 C2 c2', 'D2 B2 D2 d2', 'E2 c2 E2 e2', '[Ec]4 [Cc]4', '[CA]4 [DB]4', '[Ec]4 [Fd]4', '[Ge]4 [Gg]4', '[Cc]8'),
               v2=J('[C,E,]8', '[B,,D,]8', '[C,E,]8', '[A,,C,]8', '[F,,A,,]8', '[C,E,]8', '[G,,B,,]8', '[C,,C,]8'),
               note='6ths and octaves in the right hand, 3rds in the left'),
    adv=dict(M='4/4', K='C', Q='1/4=80',
             v1=J('[CE]2 [DF]2 [EG]2 [FA]2', '[GB]2 [Ac]2 [Bd]2 [ce]2', '[ce]2 [Ac]2 [FA]2 [DF]2', '[CE]4 [B,D]4',
                  '[CA]2 [DB]2 [Ec]2 [Fd]2', '[Ge]4 [^Fd]4', '[Gd]2 [Fd]2 [Ec]2 [DB]2', '[Ec]8'),
             v2=J('[C,G,]4 [D,A,]4', '[E,B,]4 [F,C]4', '[A,,E,]4 [F,,C,]4', '[C,G,]4 [G,,D,]4',
                  '[A,,E,]4 [G,,D,]4', '[C,G,]4 [D,A,]4', '[G,,D,]4 [G,,D,]4', '[C,G,]8'),
             note='Moving 3rds and 6ths over open 5ths'),
), badges=['Reading'], note='Read the distance between notes instead of naming every note: a 3rd is line-to-line or space-to-space.')

# ------------------------------------------------------------ 7. Bass clef
special('reading-bass-clef', 'Reading: Bass Clef', 'Practice exercise', 'Practice', dict(
    easy=dict(M='4/4', K='C', Q='1/4=66',
              v1=J('G8', 'G8', 'F8', 'F8', 'G8', 'G8', 'F8', 'E8'),
              v2=J('C,2 D,2 E,2 F,2', 'G,4 G,4', 'A,2 G,2 F,2 E,2', 'D,8', 'G,2 F,2 E,2 D,2', 'C,4 E,4', 'D,2 E,2 D,2 B,,2', 'C,8'),
              note='The tune is in the left hand; the right hand just holds'),
    inter=dict(M='4/4', K='C', Q='1/4=72',
               v1=J('[EG]8', '[DG]8', '[CE]8', '[DF]8', '[DG]8', '[EG]8', '[FA]4 [DG]4', '[EG]8'),
               v2=J('C,2 E,2 G,2 C2', 'B,2 G,2 D,2 G,,2', 'A,,2 C,2 E,2 A,2', 'F,3 E, D,4', 'G,,2 B,,2 D,2 G,2',
                    'C2 G,2 E,2 C,2', 'F,2 A,2 G,2 B,,2', 'C,8'),
               note='Skips across the whole bass staff'),
    adv=dict(M='4/4', K='C', Q='1/4=80',
             v1=J('[EGc]8', '[DGB]8', '[EGc]8', '[FAc]8', '[DGB]8', '[EGc]8', '[FAc]4 [DFB]4', '[EGc]8'),
             v2=J('C,D,E,F, G,A,B,C', 'DCB,A, G,F,E,D,', 'C,E,G,C EC G,E,', 'F,A,CF A,F,C,A,,', 'G,,B,,D,G, B,G,D,B,,',
                  'C,E,G,E, C,G,,E,,G,,', 'F,,A,,C,F, G,,B,,D,F,', 'C,,8'),
             note='Running eighths, including ledger lines above the bass staff'),
), badges=['Reading'], note='Bass clef landmarks: F is the line between the two dots; Bass C is in the second space.')

# ------------------------------------------------------------ 8. Key signatures (key changes on purpose)
special('reading-key-signatures', 'Reading: Key Signatures', 'Practice exercise', 'Practice', dict(
    easy=dict(M='4/4', K='G', Q='1/4=72',
              v1=J('G2 A2 B2 c2', 'd4 B4', 'c2 A2 F2 A2', 'G8', 'B2 A2 G2 F2', 'E2 F2 G4', 'A2 F2 D2 F2', 'G8'),
              v2=J('G,8', 'G,8', 'D,8', 'G,8', 'G,8', 'E,8', 'D,8', 'G,8'),
              note='G major: every F is F-sharp'),
    inter=dict(M='4/4', K='F', Q='1/4=76',
               v1=J('F2 G2 A2 B2', 'c4 A4', 'B2 G2 E2 G2', 'F8', 'A2 c2 f2 c2', 'd2 B2 G2 E2', 'F2 A2 G2 E2', 'F8'),
               v2=J('[F,,C,]8', '[F,,C,]8', '[C,G,]8', '[F,,C,]8', '[F,,C,]8', '[B,,F,]8', '[C,G,]8', '[F,,C,]8'),
               note='F major: every B is B-flat'),
    adv=dict(M='4/4', K='D', Q='1/4=84',
             v1=J('D2 F2 A2 d2', 'c2 e2 A4', 'B2 ^G2 E2 G2', 'A3B =c2 B2', 'F2 A2 d2 f2', 'e2 d2 B2 ^G2', 'A2 B2 c2 e2', 'd8'),
             v2=J('[D,A,]8', '[A,,E,]8', '[E,B,]8', '[A,,E,]8', '[D,A,]8', '[E,B,]8', '[A,,G,]8', '[D,A,]8'),
             note='D major (F-sharp and C-sharp) plus accidentals that last to the end of the bar'),
), badges=['Reading'], note='Each level is in a different key on purpose: the point is reading the key signature.')
