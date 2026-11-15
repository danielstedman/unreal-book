# Extra sections for songs that already live in another category (e.g. Mountain King is
# Classical but also belongs under Halloween).  Applied after every song list is built.
from tunes import T
from specials import SPECIALS

ALSO = {
    'mountain-king': ['Halloween'], 'moonlight-sonata': ['Halloween'],
    'jingle-bells': ['Winter'], 'auld-lang-syne': ['Winter'], 'greensleeves': ['Winter'], 'gymnopedie-1': ['Winter'],
    'canon-in-d': ['Spring'], 'all-creatures': ['Spring'], 'brahms-lullaby': ['Spring'],
    'take-me-out': ['Summer'], 'daisy-bell': ['Summer'], 'silvery-moon': ['Summer'], 'the-entertainer': ['Summer'],
    'camptown-races': ['Summer'], 'oh-susanna': ['Summer'],
    'scarborough-fair': ['Autumn'], 'shenandoah': ['Autumn'], 'doxology': ['Autumn'], 'danny-boy': ['Autumn'],
}
for d in T + SPECIALS:
    for c in ALSO.get(d['id'], []):
        d.setdefault('also', [])
        if c not in d['also']:
            d['also'].append(c)
