# Song data for Danny's Unreal Book.
#
# Every melody here is public domain (traditional, or published before 1929).
# The arrangements are original: the engine builds the accompaniment from the
# chord symbols, and the "special" pieces further down are written out by hand.
from fractions import Fraction as Fr
from tunes_hymnal import HYMNAL, HYMNAL_WORDS

T = []  # melody + chords tunes (three levels generated)


def tune(id, title, composer, cat, M, key, mel, chords, style='ballad', tempo=90, **kw):
    d = dict(id=id, title=title, composer=composer, cat=cat, M=M, key=key, mel=mel, chords=chords, style=style, tempo=tempo)
    d.update(kw)
    T.append(d)


def hymnal(id, title, composer, cat, chords, style='hymn', tempo=90, **kw):
    h = HYMNAL[id]
    if id in HYMNAL_WORDS and not kw.pop('nowords', False):
        kw.setdefault('w', HYMNAL_WORDS[id]['w'])
        kw.setdefault('verses', HYMNAL_WORDS[id]['verses'])
        kw.setdefault('wsrc', 'Words: public domain, as given in the Open Hymnal Project')
    tune(id, title, composer, cat, kw.pop('M', h['M']), kw.pop('key', h['key']), kw.pop('mel', h['mel']), chords, style, tempo, **kw)


# ------------------------------------------------------------------ Hymns
hymnal('amazing-grace', 'Amazing Grace', 'Traditional American melody (New Britain)', 'Hymns',
       'G|G|C|G|G|Em|D|D7|G|G|C|G|Em|G . D7|G|G', tempo=84)
hymnal('be-thou-my-vision', 'Be Thou My Vision', 'Traditional Irish melody (Slane)', 'Hymns',
       'Eb|Ab Eb .|Eb . Bb|Eb|Bb|Bb Eb .|Ab Eb .|Bb|Ab|Ab Eb .|Eb . Bb|Ab . Eb|Eb|Ab Eb .|Bb7 Eb .|Eb', tempo=96)
hymnal('abide-with-me', 'Abide with Me', 'William H. Monk, 1861 (Eventide)', 'Hymns',
       'Eb . . Bb|Eb|Ab Eb Bb7 .|Eb|Eb . Bb7 Eb|Ab Eb|Fm . Eb F7|Bb|Eb . . Bb|Eb|Bb7 . Ab Eb|Bb|Bb . Eb Ab|Eb Bb Cm Ab|Eb Bb7|Eb',
       tempo=72)
hymnal('what-a-friend', 'What a Friend We Have in Jesus', 'Charles C. Converse, 1868', 'Hymns',
       'F|Bb|F|C|F|Bb|F C7|F|C|F|Bb F|C|F|Bb|F C7|F', tempo=88)
hymnal('it-is-well', 'It Is Well with My Soul', 'Philip P. Bliss, 1876', 'Hymns',
       'Db|Db . Ab7 Db|Ab7|Db|Bbm|Eb7|Ab|Db|Eb7|Ab|Fm Bbm|Gb Db|Db Ab7|Db|Db|Ab|Ab7|Db|Gb|Db Ab7|Db', tempo=80,
       easy=dict(bars=(1, 14), cut=Fr(1, 2)), notes=dict(easy='Verse only'))
hymnal('holy-holy-holy', 'Holy, Holy, Holy', 'John B. Dykes, 1861 (Nicaea)', 'Hymns',
       'D|D|G|D|A|D A|A E7|A|D|D|G|D|D|G D|Em A7|D', tempo=96)
hymnal('come-thou-fount', 'Come, Thou Fount of Every Blessing', 'Traditional American melody (Nettleton)', 'Hymns',
       'Eb|Bb . Eb|Ab Eb .|Eb|Eb|Bb . Eb|Ab Eb .|Eb|Eb|Ab Eb .|Eb|Eb|Eb|Bb . Eb|Ab Eb .|Eb', tempo=100)
hymnal('great-is-thy-faithfulness', 'Great Is Thy Faithfulness', 'William M. Runyan, 1923', 'Hymns',
       'Eb|Ab|Bb7|Bb7 Eb .|Ab|Eb|F7|Bb|Bb7|Eb . Ab|Bb7 . Eb|Eb Bb .|Ab . Adim|Eb|Eb . Bb7|Eb|Bb|Eb|C7|Fm|Bb7|Eb . Ab|Bb . F7|Bb|Bb7|Eb . Ab|Bb7 . Eb|Eb Bb .|Ab . Adim|Eb|Eb Fm Bb7|Eb',
       tempo=88, easy=dict(bars=(1, 16)), notes=dict(easy='Verse only'))
hymnal('blessed-assurance', 'Blessed Assurance', 'Phoebe P. Knapp, 1873', 'Hymns',
       'D . G|D|D A E7|A|D . G|D|Em A7 .|D|D . G|D|G . A|A|D . G|D|Em A7 .|D', tempo=56,
       easy=dict(bars=(1, 8)), notes=dict(easy='Verse only'))
hymnal('rock-of-ages', 'Rock of Ages', 'Thomas Hastings, 1830 (Toplady)', 'Hymns',
       'Bb . Eb|Bb|Bb . F7|Bb|F7|Bb|F7|Bb|Bb . Eb|Bb|Bb . F7|Bb', tempo=80)
hymnal('nearer-my-god', 'Nearer, My God, to Thee', 'Lowell Mason, 1856 (Bethany)', 'Hymns',
       'G D7|C|G|D|G D7|C|G D7|G|G|G|G|G D|G D7|C|G D7|G', tempo=52)
hymnal('be-still-my-soul', 'Be Still, My Soul', 'Jean Sibelius, from Finlandia (1899)', 'Hymns',
       'Bb . . F|C7 F|C7 F . .|F|Bb . . F|C7 F|F|F|Bb . . F|F . C .|Gm|Gm . F C|F|Bb C7|F|F|Bb . . F|F . C .|Gm|Gm . F C|F|Bb C7|F|F',
       tempo=76)
hymnal('a-mighty-fortress', 'A Mighty Fortress Is Our God', 'Martin Luther, 1529 (Ein feste Burg)', 'Hymns',
       'D A|D G A D|A G D G|Em A7 D .|D A|D G A D|A G D G|Em A7 D .|D E7|A D A .|G A D A|Bm A G .|D G . D|G Em D .|A G D G|Em A7 D .',
       tempo=92)
hymnal('old-rugged-cross', 'The Old Rugged Cross', 'George Bennard, 1913', 'Hymns',
       'Bb|Eb|F7|Bb|Bb|Eb|F7|Bb|F7|Bb|Eb|Bb|Bb|Eb|Bb F7|Bb', tempo=54,
       easy=dict(bars=(1, 8)), notes=dict(easy='Verse only'))
hymnal('just-as-i-am', 'Just As I Am', 'William B. Bradbury, 1849 (Woodworth)', 'Hymns',
       'D|A7 D|D G|D|D|G|D|A7|D', tempo=50,
       mel='D/E/ | F2F A3/2G/F | E3/2F/G F2A | AEF G2B | B2A F2D/E/ | F2F A3/2G/F | B2B d3/2c/B | A2A A3/2G/F | E3 A3 | F3- F2 |]')
hymnal('crown-him', 'Crown Him with Many Crowns', 'George J. Elvey, 1868 (Diademata)', 'Hymns',
       'D|G|D . G D|A|D . G D|E7 . A .|A D E7 .|A|D . A D|G . . B7|E|A|D . G D|Em D|G D A7 .|D', tempo=100)
hymnal('all-creatures', 'All Creatures of Our God and King', 'Geistliche Kirchengesänge, 1623 (Lasst uns erfreuen)', 'Hymns',
       'D|A . D|D|A . D|G D .|G D .|D|A . D|D|A . D|A D .|A D .|G D .|G D .|A7|D', tempo=120)
tune('doxology', 'Doxology (Old Hundredth)', 'Genevan Psalter, 1551, attr. Louis Bourgeois', 'Hymns', '4/4', 'G',
     'G2 | G2 F2 E2 D2 | G2 A2 B2 B2 | B2 B2 A2 G2 | c2 B2 A2 G2 | A2 B2 A2 G2 | E2 F2 G2 d2 | B2 G2 A2 c2 | B2 A2 G2 |]',
     'G D Em G|C D G .|G . D Em|C G D G|D G D Em|C D G .|G Em D C|G D7 G .', 'hymn', 88)
tune('shall-we-gather', 'Shall We Gather at the River', 'Robert Lowry, 1864', 'Hymns', '4/4', 'D',
     'F2 F2 F3/2E/ F3/2G/ | A4 F4 | G2 G2 G3/2A/ G3/2F/ | E4 A4 | F2 F2 F3/2E/ F3/2G/ | A4 F2 FG | E2 EF G2 FE | D8 | '
     'B2 B2 d3/2c/ d3/2B/ | A4 F3F | G3/2F/ G3/2F/ G3/2F/ GE | F4 A4 | B3/2B/ B3/2B/ d3/2c/ d3/2B/ | A4 F2 F2 | E2 E3/2F/ G2 FE | D8 |]',
     'D|D|A7|A7|D|D|A7|D|G|D|A7|D|G|D|A7|D', 'hymn', 92, easy=dict(bars=(1, 8)), notes=dict(easy='Verse only'))

# ------------------------------------------------------------------ Christmas
hymnal('silent-night', 'Silent Night', 'Franz Xaver Gruber, 1818', 'Christmas',
       'Bb|Bb|F7|Bb|Eb|Bb|Eb|Bb|F7|Bb|Bb F7|Bb', 'ballad', 46)
hymnal('joy-to-the-world', 'Joy to the World', 'Lowell Mason, 1839 (Antioch)', 'Christmas',
       'D|D . . A7|D A7|D|G|A|D|D|D|D|D|D|D|A|A7|D . . G|D . . G|D A7|D', tempo=126)
hymnal('god-rest-ye', 'God Rest Ye Merry, Gentlemen', 'Traditional English carol', 'Christmas',
       'Em|Em D|Em Am|B7 . . Em|Em|Em D|Em Am|B7|Am G|G D|Em D|D . Em D|G . C G|G D Em B7|Em|D . Em D|G C G Em|G D Em B7|Em',
       tempo=116, key='Em')
hymnal('o-come-all-ye-faithful', 'O Come, All Ye Faithful', 'John Francis Wade, c. 1743 (Adeste Fideles)', 'Christmas',
       'G|D|G D G C|G . D G|Em . D A|D . . G|D . A7 .|D|G . D7 G|C G|D G Em D|D . . G|G D G D|G|G D G C|G . D G|C G D Em|D . G C|G . D7 .|G',
       tempo=104)
hymnal('hark-the-herald', 'Hark! The Herald Angels Sing', 'Felix Mendelssohn, 1840', 'Christmas',
       'F|F . . C|F C7|F C F .|F|F . . C|C|C G7 C .|F|Bb F . C|F|Bb F . C|Bb . . F|Gm D7 Gm .|C7 . F .|F C F .|Bb . . F|Gm D7 Gm .|C7 . F .|F C7 F .',
       tempo=108)
tune('jingle-bells', 'Jingle Bells', 'James Lord Pierpont, 1857', 'Christmas', '4/4', 'G',
     'D2 B2 A2 G2 | D6 DD | D2 B2 A2 G2 | E6 z2 | E2 c2 B2 A2 | F6 z2 | d2 d2 c2 A2 | B6 z2 | '
     'D2 B2 A2 G2 | D6 z2 | D2 B2 A2 G2 | E6 E2 | E2 c2 B2 A2 | d2 d2 d2 d2 | e2 d2 c2 A2 | G4 d4 | '
     'B2 B2 B4 | B2 B2 B4 | B2 d2 G3 A | B8 | c2 c2 c3 c | c2 B2 B2 BB | B2 A2 A2 B2 | A4 d4 | '
     'B2 B2 B4 | B2 B2 B4 | B2 d2 G3 A | B8 | c2 c2 c3 c | c2 B2 B2 BB | d2 d2 c2 A2 | G8 |]',
     'G|G|G|C|C|D7|D7|G|G|G|G|C|C|D7|D7|G D7|G|G|G|G|C|G|A7|D7|G|G|G|G|C|G|D7|G', 'lively', 132,
     easy=dict(bars=(17, 32)), notes=dict(easy='Chorus only'))
tune('deck-the-halls', 'Deck the Halls', 'Traditional Welsh melody (Nos Galan)', 'Christmas', '4/4', 'F',
     'c3 B A2 G2 | F2 G2 A2 F2 | GA BG A3 G | F2 E2 F4 | c3 B A2 G2 | F2 G2 A2 F2 | GA BG A3 G | F2 E2 F4 | '
     'G3 A B2 G2 | A3 B c2 G2 | A=B c2 de f2 | e2 d2 c4 | c3 B A2 G2 | F2 G2 A2 F2 | dd dd c3 B | A2 G2 F4 |]',
     'F|F|C7 F|F C7 F .|F|F|C7 F|F C7 F .|C7|F C|F G7|C G7 C .|F|F|Bb F|F C7 F .', 'lively', 112)
tune('carol-of-the-bells', 'Carol of the Bells', 'Mykola Leontovych, 1916 (Shchedryk)', 'Christmas', '3/4', 'Gm',
     'B2 AB G2 | B2 AB G2 | B2 AB G2 | B2 AB G2 | B2 AB G2 | B2 AB G2 | B2 AB G2 | B2 AB G2 | '
     'd2 cd B2 | d2 cd B2 | d2 cd B2 | d2 cd B2 | g2 gg fe | d2 dd cB | c2 cc dc | G2 GG G2 | '
     'D=E ^FG AB | cd c2 B2 | D=E ^FG AB | cd c2 B2 | B2 AB G2 | B2 AB G2 | B2 AB G2 | G6 |]',
     'Gm|Gm|Gm|Gm|Gm|Gm/F|Ebmaj7|Gm/D|Gm|Gm/F|Ebmaj7|Gm/D|Eb|Gm|Cm|Gm|D7|D7 . Gm|D7|D7 . Gm|Gm|Gm/F|Ebmaj7|Gm',
     'ballad', 150, badges=['Simplified'], inter=dict(pat='waltz'), easy=dict(tempo=110))

tune('o-holy-night', 'O Holy Night', 'Adolphe Adam, 1847 (Cantique de Noël)', 'Christmas', '6/8', 'D',
     'F3 F2F | A3- A2A | B2B G2B | d6 | A2A F2E | D3 F2G | A3 G2E | D6- | D4 z2 | '
     'F3 F2F | A3- A2A | B2B G2B | d6 | A2A ^G2F | c3 A2B | c3 d2c | F6- | F3 z2A | '
     'A3 B3 | E3 A3 | B2A d2F | B3 A2A | A3 B3 | E3 A3 | B2A d2F | A3- A2z | '
     'd6- | d2z c2B | c6- | c2z c3 | e6- | ez B B2B | d6- | d3 z2d | '
     'f6 | e3- e2A | d6- | d2z c2B | A6- | Az A B2A | A6- | A2z d3 | '
     'e6- | e2z A3 | f6- | f3 e3 | d3- d2z | c3 d2e | d6- | d4 z2 |]',
     'D|D|G|D|D A7|D|A7|D|D|D|D|G|D|F#m|F#m|C#7|F#m|F#m|A7|A7|D|G D|A7|A7|D|D|Bm|Bm|F#m|F#m|Em|Em|Bm|Bm|'
     'D|A7|D|G|D|A7|D|D|A|A7|D|D A7|D|A7|D|D', 'ballad', 46,
     easy=dict(bars=(1, 9)), inter=dict(bars=(1, 26)), notes=dict(easy='Opening phrase', inter='First half'))

# ------------------------------------------------------------------ Classical (melody + chords)
tune('ode-to-joy', 'Ode to Joy', 'Ludwig van Beethoven, Symphony No. 9 (1824)', 'Classical', '4/4', 'D',
     'F2 F2 G2 A2 | A2 G2 F2 E2 | D2 D2 E2 F2 | F3 E E4 | F2 F2 G2 A2 | A2 G2 F2 E2 | D2 D2 E2 F2 | E3 D D4 | '
     'E2 E2 F2 D2 | E2 FG F2 D2 | E2 FG F2 E2 | D2 E2 A,4 | F2 F2 G2 A2 | A2 G2 F2 E2 | D2 D2 E2 F2 | E3 D D4 |]',
     'D|A|D|D A|D|A|D|A7 D|A D|A D|A B7|Em A|D|A|D|A7 D', 'hymn', 108, badges=['Theme'])
tune('brahms-lullaby', 'Lullaby (Wiegenlied)', 'Johannes Brahms, Op. 49 No. 4 (1868)', 'Classical', '3/4', 'Eb',
     'GG | B3 G G2 | B2 z2 GB | e2 d3 c | c2 B2 FG | A2 F2 FG | A2 z2 FA | dc B2 d2 | e2 z2 EE | '
     'e4 cA | B4 GE | A2 B2 c2 | B4 EE | e4 cA | B4 GE | A2 G2 F2 | E4 |]',
     'Eb|Eb|Eb|Eb . Bb7|Bb7|Bb7|Bb7|Eb|Ab|Eb|Bb7|Eb|Ab|Eb|Bb7|Eb', 'ballad', 76, badges=['Melody arrangement'])

# ------------------------------------------------------------------ Traditional
tune('danny-boy', 'Danny Boy (Londonderry Air)', 'Traditional Irish melody', 'Traditional', '4/4', 'C',
     'B,CD | E3D EA GE | DC A,2 z CEF | G3A GE CE | D4 z B,CD | E3D EA GE | DC A,2 z B,CD | E3F ED CD | C4 z GAB | '
     'c3B BA GA | GE C2 z GAB | c3B BA GE | D4 z GGG | e3d dc Ac | GE C2 z B,CD | EA GE DC A,B, | C4 z |]',
     'C C7|F|C|G7|C C7|F|C G7|C|C F|C|C Am|D7 G7|C F|C|Am C Dm G7|C', 'ballad', 66, featured=True,
     easy=dict(key='C'), inter=dict(key='D'), adv=dict(key='Eb'))
tune('greensleeves', 'Greensleeves', 'Traditional English melody, 16th century', 'Traditional', '6/8', 'Am',
     'A | c2d e3/2^f/e | d2B G3/2A/B | c2A A3/2^G/A | B2^G E2A | c2d e3/2^f/e | d2B G3/2A/B | c3/2B/A ^G3/2^F/^G | A3 A3 | '
     'g3 g3/2^f/e | d2B G3/2A/B | c2A A3/2^G/A | B2^G E3 | g3 g3/2^f/e | d2B G3/2A/B | c3/2B/A ^G3/2^F/^G | A3- A2 |]',
     'Am|G|F|E|Am|G|Am E|Am|C|G|F|E|C|G|Am E|Am', 'ballad', 56)
tune('shenandoah', 'Shenandoah', 'Traditional American', 'Traditional', '4/4', 'C',
     'G,2 | C3C C2 DE | F2 A2 G3 c | B4 A2 GA | GE G4 G2 | A3A A2 EG | E2 D2 C2 CD | E4 C2 E2 | A2 G4 CD | E4 C2 D2 | C6 |]',
     'C|F C|Em F|C|F C|C G C G|C|F C|C G7|C', 'ballad', 72, easy=dict(key='F'), inter=dict(key='D'), adv=dict(key='Eb'))
tune('scarborough-fair', 'Scarborough Fair', 'Traditional English ballad', 'Traditional', '3/4', 'Em',
     'E4 E2 | B4 B2 | F3 G F2 | E6- | E2 B2 d2 | e4 d2 | B2 ^c2 A2 | B6- | B4 e2 | e4 e2 | d4 B2 | B2 A2 G2 | F2 D4- | D6 | '
     'E4 B2 | A4 G2 | F2 E2 D2 | E6- | E6 |]',
     'Em|Em|D|Em|Em|G|A|Em|Em|Em|G|G|D|D|Em|D|D|Em|Em', 'ballad', 108)
tune('when-the-saints', 'When the Saints Go Marching In', 'Traditional American', 'Traditional', '4/4', 'C',
     'z2 C2 E2 F2 | G8- | G2 C2 E2 F2 | G8- | G2 C2 E2 F2 | G4 E4 | C4 E4 | D8 | z2 E2 E2 D2 | C6 C2 | E4 G4 | G2 F6 | '
     'z4 E2 F2 | G4 E4 | C4 D4 | C8 |]',
     'C|C|C|C|C|C|C|G7|G7|C|C C7|C7 F . .|F|C|C G7|C', 'lively', 138)

# ------------------------------------------------------------------ Singalongs
tune('take-me-out', 'Take Me Out to the Ball Game', 'Albert Von Tilzer, 1908', 'Singalongs', '3/4', 'C',
     'C4 c2 | A2 G2 E2 | G6 | D6 | C4 c2 | A2 G2 E2 | G6- | G4 z2 | A2 ^G2 A2 | E2 F2 G2 | A4 F2 | D6 | A4 A2 | A2 B2 c2 | d2 B2 A2 | G2 E2 D2 | '
     'C4 c2 | A2 G2 E2 | G6 | D4 D2 | C4 D2 | E2 F2 G2 | A6- | A2 A2 B2 | c6 | c6 | c2 B2 A2 | G2 ^F2 G2 | A6 | B6 | c6- | c6 |]',
     'C|C|G7|G7|C|C|G7|G7|A7|A7|Dm|Dm|D7|D7|G7|G7|C|C|G7|G7|C|C7|F|F|C|C|Am|D7|D7|G7|C|C', 'waltz', 160,
     badges=['Chorus'])
tune('daisy-bell', 'Daisy Bell (Bicycle Built for Two)', 'Harry Dacre, 1892', 'Singalongs', '3/4', 'C',
     'g6 | e6 | c6 | G6 | A2 B2 c2 | A4 c2 | G6- | G4 z2 | d6 | g6 | e6 | c6 | A2 B2 c2 | d4 e2 | d6- | d4 e2 | '
     'f2 e2 d2 | g4 e2 | d2 c4- | c4 d2 | e4 c2 | A4 c2 | A2 G4- | G4 G2 | c4 e2 | d4 z2 | c4 e2 | d2 e2 f2 | g2 e2 c2 | d4 G2 | c6- | c6 |]',
     'C|C|C|C|F|F|C|C|G7|G7|C|Am|D7|D7|G7|G7|G7|C|G7 C .|C|C|F|F C .|C|C|G7|C|G7|C|G7|C|C', 'waltz', 152,
     badges=['Chorus'], easy=dict(key='F', oct=-1))
tune('let-me-call-you-sweetheart', 'Let Me Call You Sweetheart', 'Leo Friedman, 1910', 'Singalongs', '3/4', 'D',
     'F4 A2 | d4 e2 | f2 A4 | ^G4 A2 | B6 | B6 | B6- | B6 | c4 =c2 | ^c4 d2 | e2 c4 | B4 c2 | A6 | A6 | A6- | A2 _A2 G2 | '
     'F4 A2 | d4 e2 | f2 A4 | ^G4 A2 | B6 | B6 | e6- | e6 | e4 d2 | c4 d2 | f2 A4 | g4 f2 | B6 | c6 | d6- | d6 |]',
     'D|D|D|D|G|G|G|G|A7|A7|A7|A7|D|D|D|D|D|D|D|D|G|G|E7|E7|A7|A7|D|G|Em|A7|D|D', 'waltz', 138, badges=['Chorus'])
tune('silvery-moon', 'By the Light of the Silvery Moon', 'Gus Edwards, 1909', 'Singalongs', '4/4', 'A',
     'C2 D2 | E8 | z2 AB cB A2 | F8 | z2 B2 A2 F2 | G8 | z2 EF GF E2 | F4 C4 | E4 C2 D2 | E8 | z2 AB cB A2 | F8 | z2 B2 c2 d2 | '
     'c2 A2 B2 d2 | c2 AB cB A2 | c8 | z2 AB cA B2 | A8- | A2 z2 |]',
     'A|A|D|B7|E7|E7|D A|A|A|A|D|D|A E7|A|A|Bm7 E7|A|A', 'lively', 112, badges=['Chorus'], inter=dict(key='G'))
tune('oh-susanna', 'Oh! Susanna', 'Stephen Foster, 1848', 'Singalongs', '4/4', 'C',
     'CD | E2 G2 G3 A | G2 E2 C3 D | E2 E2 D2 C2 | D6 CD | E2 G2 G3 A | G2 E2 C3 D | E2 E2 D2 D2 | C6 z2 | '
     'F4 F4 | A2 A4 A2 | G2 G2 E2 C2 | D6 CD | E2 G2 G3 A | G2 E2 C3 D | E2 E2 D2 D2 | C6 |]',
     'C|C|C|G7|C|C|C G7|C|F|F|C|G7|C|C|C G7|C', 'lively', 126, inter=dict(key='D'), adv=dict(key='G'))
tune('camptown-races', 'Camptown Races', 'Stephen Foster, 1850', 'Singalongs', '4/4', 'C',
     'G2 | G2 G2 E2 G2 | A2 G2 E4 | E2 D6 | E2 D2 z2 G2 | G2 G2 E2 G2 | A2 G2 E4 | D4 E2 D2 | C6 z2 | '
     'C3 C E2 G2 | c8 | A3 A c2 A2 | G6 E2 | G2 G2 E2 G2 | A2 G2 E4 | D2 EF E2 DD | C6 |]',
     'C|C|G7|G7|C|C|G7|C|C|C|F|C|C|C|G7|C', 'lively', 132, inter=dict(key='D'), adv=dict(key='D'))
tune('old-folks-at-home', 'Old Folks at Home (Swanee River)', 'Stephen Foster, 1851', 'Singalongs', '4/4', 'C',
     'E4 DC ED | C2 c2 A c3 | G4 E2 C2 | D8 | E4 DC ED | C2 c2 A c3 | G2 E3/2C/ D2 D2 | C8 | '
     'B3 c d2 B2 | G3 A G2 c2 | c2 A2 F2 A2 | G8 | E4 DC ED | C2 c2 A c3 | G2 E3/2C/ D2 D2 | C8 |]',
     'C|C F|C|G7|C|C F|C G7|C|G|C|F|C G7|C|C F|C G7|C', 'ballad', 80, inter=dict(key='D'), adv=dict(key='D'))
tune('my-bonnie', 'My Bonnie Lies over the Ocean', 'Traditional Scottish', 'Singalongs', '3/4', 'G',
     'D2 | B2 A2 G2 | A2 G2 E2 | D2 B,4- | B,4 D2 | B2 A2 G2 | G2 F2 G2 | A6- | A4 D2 | B2 A2 G2 | A2 G2 E2 | D2 B,4- | B,4 D2 | '
     'E2 A2 G2 | F2 E2 F2 | G6- | G4 z2 | D6 | G6 | E6 | A6 | F2 F2 F2 | F2 E2 F2 | G4 A2 | B6 | D6 | G6 | E6 | A6 | F2 F2 F2 | F2 E2 F2 | G6- | G4 |]',
     'G|C|G|G|G|A7|D7|D7|G|C|G|G|C|D7|G|G|G|G|C|A7|D7|D7|G|G|G|G|C|A7|D7|D7|G|G', 'waltz', 144,
     easy=dict(bars=(1, 16)), notes=dict(easy='Verse only'))
tune('clementine', 'Oh My Darling, Clementine', 'Traditional American', 'Singalongs', '3/4', 'F',
     'F3/2F/ | F2 C2 A3/2A/ | A2 F2 F3/2A/ | c2 c2 B3/2A/ | G4 G3/2A/ | B2 B2 A3/2G/ | A2 F2 F3/2A/ | G2 C2 E3/2G/ | F4 F3/2F/ | '
     'F2 C2 A3/2A/ | A2 F2 F3/2A/ | c2 c2 B3/2A/ | G4 G3/2A/ | B2 B2 A3/2G/ | A2 F2 F3/2A/ | G2 C2 E3/2G/ | F4 |]',
     'F|F|F|C7|C7|F|C7|F|F|F|F|C7|C7|F|C7|F', 'waltz', 132, easy=dict(bars=(1, 8)), notes=dict(easy='Once through'))
tune('railroad', "I've Been Working on the Railroad", 'Traditional American', 'Singalongs', '4/4', 'G',
     'G3D G3/2D/ G3/2A/ | B4 G4 | c3c G2 A2 | B8 | G3D G3/2D/ G3/2A/ | B4 G2 B3/2B/ | B2 A2 A2 B2 | A8 | '
     'A3A ^G3/2A/ B3/2A/ | G4 D4 | c2 c3/2c/ G3/2G/ A3/2A/ | B8 | E3F G3/2F/ G3/2E/ | D4 G4 | B2 c2 B2 A2 | G8 | '
     'D3/2D/ D3/2D/ G4 | E3/2E/ E3/2E/ A4 | F3/2F/ F3/2F/ E2 F2 | G2 A2 B4 | D3/2D/ D3/2D/ G4 | E3/2E/ E3/2E/ A4 | F3/2F/ F3/2F/ E2 F2 | G8 |]',
     'G|G|C|G|G|G|A7|D7|D7|G|C|G|C|G|G D7|G|G|C|D7|G|G|C|D7|G', 'lively', 116,
     easy=dict(bars=(1, 16)), notes=dict(easy='First part'))
tune('coming-round-the-mountain', "She'll Be Coming 'Round the Mountain", 'Traditional American', 'Singalongs', '4/4', 'C',
     'GA | cc cc AG EG | c6 cd | ee ee gg ge | d6 gf | ee ee d c3 | cc cc f f3 | ee ee dd dd | c6 |]',
     'C|C|C|G7|C|F|C G7|C', 'lively', 100, easy=dict(key='F', oct=-1), inter=dict(key='G', oct=-1), adv=dict(key='G', oct=-1))
tune('auld-lang-syne', 'Auld Lang Syne', 'Traditional Scottish', 'Singalongs', '4/4', 'F',
     'C2 | F3F F2 A2 | G3F G2 A2 | F3F A2 c2 | d6 d2 | c3A A2 F2 | G3F G2 A2 | F3D D2 C2 | F6 d2 | '
     'c3A A2 F2 | G3F G2 d2 | c3A A2 c2 | d6 d2 | c3A A2 F2 | G3F G2 A2 | F3D D2 C2 | F6 |]',
     'F|C7|F|Bb|F|C7|Bb C7|F|F|C7|F|Bb|F|C7|Bb C7|F', 'ballad', 92)
