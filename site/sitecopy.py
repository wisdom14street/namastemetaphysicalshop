"""Namaste Metaphysical Shop (namastemetaphysicalshop.com): ritual, altar and practice supplies from the Namaste inventory,
organized by what you are setting up: an altar, a divination practice, sound, oils and herbs, spellwork. Copy written for this site only."""
import re, types
E = __import__('html').escape
ICON = 'pent'
FAM_LABEL, FAM_ALL, STYLE_LABEL, STYLE_ALL = 'Intention on the label', 'Any intention', 'Material', 'Any material'
NO_FAMILY = ()
QUIZ = None
NAV_AISLES = True
PRICE_OPTS = '<option value="0-10">Under $10</option><option value="0-25">Under $25</option><option value="0-50">Under $50</option><option value="50-99999">$50 and up</option>'
PRICE_BANDS = [('Under $12', 0, 12), ('$12 to $35', 12, 35), ('$35 and up', 35, 1e9)]
_T = {
 'pendulums': {'Pendulum', 'Pendulum Board', 'Dowsing Rod'},
 'divination': {'Rune Set', 'Scrying Mirror', 'Tarot Talisman'},
 'altar': {'Chalice Cup', 'Goblet', 'Offering Bowls', 'Diya', 'Mortar & Pestle', 'Bottles', 'Oil Burner'},
 'statues': {'Statue'},
 'sound': {'Brass Singing Bowl', 'Crystal Singing Bowl', 'Singing Bowl Cushion', 'Singing Bowl Mallet', 'Hand Bells', 'Chimes', 'Tuning Fork', 'Musical instruments', 'Instruments'},
 'oils': {'Essential Oils', 'Aroma Oil', 'Fragrance Oil'},
 'herbs': {'Herbs', 'Herb', 'Bath Salt'},
 'waters': {'Smudge Sprays Fine Mists', 'Cleansing Water', 'Spiritual Spray', 'Room Spray'},
 'symbols': {'Wall Hanging'},
 'kits': {'Spiritual Kit & Bundle', 'Energy Cleansing Kit'},
}
_T2 = {t: k for k, ts in _T.items() for t in ts}
SPELL_CANDLE = re.compile(r'spell|chime candle|mini (ritual )?candle|ritual candle|7 ?day|seven day|novena|soul ?sticks|magic mini|offering candle|altar candle', re.I)
def category(p):
    t, ty = p['title'], p.get('product_type', '') or ''
    if re.search(r'\bby [A-Z]|\bbook\b|deck\b|mug\b|compact .*mirror|mirror - assorted|flower essence|supplement|inhaler|soap', t, re.I): return None
    if ty in _T2:
        k = _T2[ty]
        if ty == 'Chimes' and not re.search(r'chime', t, re.I): return None
        return k
    if ty in ('Candle', 'Candles', 'Ritual Candle') and SPELL_CANDLE.search(t): return 'candles'
    if ty in ('Incense Holder', 'Incense Burner') and re.search(r'cauldron', t, re.I): return 'altar'
    if ty == 'Incense Burner' and re.search(r'charcoal', t, re.I): return 'smoke'
    if ty == 'Candle Holder' and re.search(r'chime|spell|altar', t, re.I): return 'candles'
    if ty in ('Resin Incense',) and not re.search(r'stick|cone|charcoal', t, re.I): return 'smoke'
    if ty == 'Incense Chips': return 'smoke'
    if ty in ('Sage', 'Smudging') and re.search(r'kit|abalone|shell|loose|feather|fan|broom|bowl', t, re.I): return 'smoke' if not re.search(r'broom', t, re.I) else 'altar'
    if ty == '' and re.search(r'cauldron|athame|altar (cloth|tile|bell|bowl|broom)|chalice|pentacle (plate|tile|altar)|besom|spell (jar|bottle|kit)|offering bowl|boline', t, re.I): return 'altar'
    return None
def assign(x): return x['base']
_I = [('Protection', r'protect|evil eye|hamsa|guard|shield|uncross|spell break|banish|black salt'), ('Love & attraction', r'\blove|attraction|heart|rose\b|romance|venus'),
      ('Money & luck', r'money|wealth|prosper|abundance|luck|jackpot|fortune|success|lakshmi|ganesh'), ('Cleansing', r'cleans|clear|purif|florida water|sage|smudg|uncross'),
      ('Peace & calm', r'peace|calm|tranquil|serenity|relax|lavender'), ('Intuition & dreams', r'intuition|psychic|third eye|dream|moon|divin|scry'),
      ('Chakras', r'chakra|root|sacral|solar plexus|throat|crown'), ('Grounding', r'ground|earth|root')]
def _slug(n): return re.sub(r'[^a-z0-9]+', '-', n.lower()).strip('-')
FAMILIES = [(_slug(n), n, rx) for n, rx in _I]
_M = [('Brass', r'brass'), ('Copper', r'copper'), ('Crystal & stone', r'crystal|quartz|amethyst|obsidian|jade|marble|soapstone|stone|onyx|carnelian|jasper|moonstone|selenite|rose quartz'),
      ('Wood', r'wood|bamboo'), ('Resin & polyresin', r'resin|polyresin|polystone'), ('Glass', r'glass'), ('Ceramic & clay', r'ceramic|clay|porcelain'), ('Iron & steel', r'iron|steel|metal'), ('Silver tone', r'silver'), ('Gold tone', r'gold')]
def style_of(t, b, base):
    if base in ('oils', 'herbs', 'waters', 'candles', 'smoke'): return ''
    for n, rx in _M:
        if re.search(rx, t, re.I): return n
    return ''
_BRANDS = [('suns-eye', "Sun's Eye", r"sun['\u2019]?s eye", ["Sun's Eye", 'SNSEY']), ('kates-magik', "Kate's Magik", r"kate'?s'? magik", ['Kates Magik']), ('fred-soll', "Fred Soll's", r'fred soll', ['fredsoll']),
           ('sonavi', 'Sonavi', r'sonavi', []), ('woodstock-chimes', 'Woodstock Chimes', r'woodstock', []), ('lo-scarabeo', 'Lo Scarabeo', r'lo scarabeo', ['Lo Scarabeo']),
           ('murray-lanman', 'Murray & Lanman', r'murray (&|and) lanman', []), ('wicked-good', 'Wicked Good', r'wicked good', []), ('crystal-earth-studio', 'Crystal Earth Studio', r'crystal earth studio', ['crystal Earth Studio'])]
_V = {v: k for k, _, _, vs in _BRANDS for v in vs}
def _brand_of(title, vendor=''):
    for k, _, rx, _ in _BRANDS:
        if re.search(rx, title, re.I): return k
    return _V.get(vendor or '', '')
BR = types.SimpleNamespace(NAME={k: n for k, n, _, _ in _BRANDS}, brand_of=_brand_of, FACTS={})

AISLES = {
 'altar':      ('Altar Tools & Vessels', 'Altar tools', 'altar-tools-vessels', 'Chalices, goblets, cauldrons, offering bowls, diyas, mortars and altar brooms: the working pieces of an altar.', '#8a4b2e'),
 'statues':    ('Deities & Altar Statues', 'Statues', 'deity-altar-statues', 'Figures to stand at the center of an altar: deities, Buddhas, angels, guardians and familiars.', '#6a5a2e'),
 'pendulums':  ('Pendulums & Boards', 'Pendulums', 'pendulums-boards', 'Crystal, brass and copper pendulums, pendulum boards and dowsing rods.', '#3b5a6a'),
 'divination': ('Runes, Scrying & Talismans', 'Divination tools', 'runes-scrying-talismans', 'Rune sets, obsidian scrying mirrors and tarot talismans.', '#4a3b6a'),
 'sound':      ('Bowls, Bells & Sound Tools', 'Sound', 'singing-bowls-bells-sound', 'Singing bowls and their cushions and mallets, altar bells, tuning forks, chimes and rainsticks.', '#9a7a1a'),
 'oils':       ('Ritual & Essential Oils', 'Oils', 'ritual-essential-oils', 'Single-note essential oils, aroma oils and intention-blend oils for dressing candles and tools.', '#2e6a4a'),
 'herbs':      ('Loose Herbs & Salts', 'Herbs & salts', 'loose-herbs-salts', 'Dried loose herbs and bath salts for sachets, jars and ritual baths.', '#5a7a2e'),
 'waters':     ('Ritual Waters & Mists', 'Waters & mists', 'ritual-waters-mists', 'Florida water, rose water, cleansing waters and smoke-free sprays.', '#2e5a7a'),
 'smoke':      ('Loose Resin, Bakhoor & Smudge Kits', 'For the censer', 'loose-resin-bakhoor-smudge-kits', 'Only the loose materials for a censer or shell: resin, bakhoor chips, abalone shells and ready smudge kits.', '#6a3b3b'),
 'candles':    ('Spellwork Candles', 'Spell candles', 'spellwork-candles', 'Small chime, mini ritual and spell candles meant to burn down in a single working.', '#9a3b5a'),
 'symbols':    ('Protective Symbols & Hangings', 'Symbols', 'protective-symbols-hangings', 'Hamsas, evil eyes and other symbols to hang by a door or above an altar.', '#3b6a8a'),
 'kits':       ('Ritual Kits', 'Kits', 'ritual-kits', 'Ready-made bundles that gather the pieces for one kind of practice.', '#7a4b6a'),
}
VISIT_EYEBROW = 'Want to hold it first?'
def STORE_DESC(S): return f'Ritual and altar supply shop with about {S.ABOUT_N:,} pieces: altar tools, statues, pendulums, runes, singing bowls, oils, herbs and spell candles, from Namaste Bookshop in Manhattan.'
REVIEW_TITLE = 'Set up your altar with us?'
REVIEW_TEXT = 'A short Google review helps other practitioners find the shop.'
LOGO_SVG = '<svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="15" fill="none" stroke="#c4622d" stroke-width="2"/><path d="M20 6l8.2 25.2L6.7 15.6h26.6L11.8 31.2z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>'
WORDMARK = 'Namaste <b>Metaphysical</b>'
SEARCH_PLACEHOLDER = 'Search supplies: pendulum, chalice, Florida water'
def FOOTER_EXPLORE(S):
    return [('Set up a first altar', '/guide/setting-up-an-altar/'), ('Using a pendulum', '/guide/how-to-use-a-pendulum/'), ('Caring for a singing bowl', '/guide/singing-bowl-care/'),
            ('By intention', '/by-intention/'), ('Supplies under $15', '/supplies-under-15/')]
FOOT_BLURB = 'Supplies for practice rather than decor: the tools, vessels, oils and herbs that go on an altar or into a ritual.'
HERO_BASES = ('altar', 'pendulums', 'sound', 'statues')
def HERO(S): return {'eyebrow': '', 'h1': '', 'lede': ''}
ORDER = ['altar', 'pendulums', 'sound', 'statues', 'divination', 'oils', 'herbs', 'waters', 'candles', 'smoke', 'symbols', 'kits']
def _pick(S, k, n=8): return [x for x in (S.by_rank if S.HAS_RANK else (lambda xs: xs))([x for x in S.leaders if x['aisle'] == k]) if not x['noimg']][:n]
def HOME_BODY(S):
    tiles = ''
    for k in ORDER:
        if k not in S.AISLE_KEYS: continue
        xs = _pick(S, k, 1)
        im = f'<img loading="lazy" src="{S.img(xs[0]["images"][0], 300)}" alt="" width="300" height="300">' if xs else ''
        tiles += f'<a class="drawer" href="/shop/{S.AISLES[k][2]}/" style="--c:{S.AISLES[k][4]}">{im}<span><b>{E(S.AISLES[k][0])}</b><small>{S.cat_count[k]} pieces</small></span></a>'
    head = (f'<section class="mhead"><div class="wrap"><h1>Ritual &amp; altar supplies</h1><p>{S.N:,} working tools from <a href="{S.SHOP}">Namaste Bookshop</a>, 2 W 14th St, NYC, sorted into the drawers you would reach for. '
            f'Ships from New York or pick up on 14th Street.</p></div></section>')
    rows = ''.join(S.section({'type': 'grid', 'title': S.AISLES[k][0], 'select': (lambda S_, k=k: _pick(S_, k)), 'href': f'/shop/{S.AISLES[k][2]}/', 'link': f'All {S.cat_count[k]}'}) for k in ORDER[:4] if k in S.AISLE_KEYS)
    rows2 = ''.join(S.section({'type': 'grid', 'title': S.AISLES[k][0], 'select': (lambda S_, k=k: _pick(S_, k)), 'href': f'/shop/{S.AISLES[k][2]}/', 'link': f'All {S.cat_count[k]}'}) for k in ORDER[4:8] if k in S.AISLE_KEYS)
    ints = ''.join(f'<a class="chip" href="/by-intention/{k}/">{E(n)} <small>{S.fam_count[k]}</small></a>' for k, n, _ in FAMILIES if S.fam_count[k] >= 4)
    guides = ''.join(f'<a class="chip" href="{u}">{E(n)}</a>' for n, u in FOOTER_EXPLORE(S)[:3])
    return (head + f'<section class="wrap"><div class="drawers">{tiles}</div></section>' + rows
            + (f'<section class="wrap"><div class="sechead"><h2>Shop by the intention on the label</h2><a href="/by-intention/">What this means &rarr;</a></div><div class="chips">{ints}</div></section>' if ints else '')
            + rows2 + f'<section class="wrap"><div class="sechead"><h2>Practice notes</h2></div><div class="chips">{guides}</div></section>'
            + f'<section class="wrap">{S.p2_badges()}</section>' + S.section({'type': 'visit'}) + S.section({'type': 'review'}))
HOME_SECTIONS = []
def HOME_TITLE(S): return 'Namaste Metaphysical Shop | Altar Tools, Pendulums, Ritual Oils & Spell Supplies'
def HOME_DESC(S): return f'{S.N:,} ritual and altar supplies: chalices, cauldrons, statues, pendulums, runes, singing bowls, ritual oils, loose herbs and spell candles. Ships from NYC or pick up at 2 W 14th St.'
def SHOP_TITLE(S): return 'All Ritual & Altar Supplies | Namaste Metaphysical Shop'
def SHOP_DESC(S): return f'Browse {S.N:,} metaphysical supplies by drawer, intention, material, maker and price, from {S.money(S.MIN_PRICE)}.'
SHOP_H1 = 'All supplies'
def SHOP_SUB(S): return f'{S.N:,} pieces. Filter by drawer, the intention on the label, material or price.'
def AISLE_TITLE(S, k): return f'{AISLES[k][0]} | Namaste Metaphysical Shop'
def AISLE_DESC(S, k): return f'{AISLES[k][3]} {S.cat_count[k]} in stock at Namaste Metaphysical Shop, NYC.'
def LANDINGS(S):
    L = []
    for k, n, _ in FAMILIES:
        c = S.fam_count[k]
        if c < 4: continue
        L.append({'path': f'/by-intention/{k}/', 'title': f'{n} Ritual Supplies | Namaste Metaphysical Shop', 'desc': f'{c} supplies whose names mention {n.lower()}: oils, waters, candles, tools and symbols.',
                  'h1': f'Supplies labeled for {n.lower()}', 'sub': f'{c} pieces whose product names point to {n.lower()}.', 'filter': {'fam': [k]},
                  'intro': '<p class="intro">Grouped by the words in each product name. These are traditions of practice, not promises of an outcome.</p>'})
    L.append({'path': '/supplies-under-15/', 'title': 'Ritual Supplies Under $15 | Namaste Metaphysical Shop', 'desc': 'Spell candles, small oils, herbs, waters and tools under $15.',
              'h1': 'Supplies under $15', 'sub': 'Small, useful pieces for a first working.', 'filter': {'maxp': 15}})
    return L
def brand_intro(S, k, st): return f'<p>{st["n"]} pieces from {E(S.BRAND_NAME[k])}, mostly {E(" and ".join(S.AISLES[a][0].lower() for a, _ in st["aisles"].most_common(2)))}, from {S.money(st["min"])}.</p>'
def brand_faq(S, k, st): return []
def BRAND_H1(S, k): return f'{S.BRAND_NAME[k]} at Namaste Metaphysical'
def BRAND_TITLE(S, k, st): return f'{S.BRAND_NAME[k]} | Namaste Metaphysical Shop'
def BRAND_DESC(S, k, st): return f'{S.BRAND_NAME[k]} at Namaste Metaphysical Shop: {st["n"]} pieces starting at {S.money(st["min"])}, mailed from New York or picked up in Manhattan.'
def BRANDS_TITLE(S): return 'Makers | Namaste Metaphysical Shop'
def BRANDS_DESC(S): return 'Named makers of the oils, waters, resins and tools we stock.'
BRANDS_H1 = 'Makers'
def BRANDS_LEAD(S, n): return f'{n} named makers. Most altar tools come from importers without a brand, so browsing by <a href="/shop/">drawer</a> is usually quicker.'
PAIR = {'altar': ['candles', 'oils'], 'statues': ['candles', 'altar'], 'pendulums': ['divination'], 'divination': ['pendulums'], 'sound': ['sound'], 'oils': ['candles', 'herbs'], 'herbs': ['oils', 'altar'],
        'waters': ['smoke', 'herbs'], 'smoke': ['altar', 'waters'], 'candles': ['oils', 'herbs'], 'symbols': ['waters'], 'kits': ['candles']}
CART_PAIR_TITLE = 'Often used together'
REL_BRAND = 'More from {brand}'
REL_SCENT = 'Also for {scent}'
REL_PAIR = 'Used alongside it'
REL_MORE = 'More {aisle}'
USE = {'altar': 'A working piece for the altar or ritual table.', 'statues': 'A figure to give an altar its focus.', 'pendulums': 'For yes/no questions, dowsing and board work.',
       'divination': 'A tool for casting, gazing or carrying a card\u2019s image with you.', 'sound': 'For sound in meditation, ritual openings and closings.',
       'oils': 'Used to scent a space, or dab onto candles and tools in candle magic. Essential oils are concentrated; dilute before skin contact and keep away from children and pets.',
       'herbs': 'Dried herb or salt for sachets, spell jars or a ritual bath. Not sold as food or medicine.', 'waters': 'A liquid alternative to smoke: sprinkle or mist a room, altar or doorway. Not for drinking.',
       'smoke': 'Loose material for burning on charcoal or in a shell. Burn in a heat-safe vessel with airflow and never leave it unattended.',
       'candles': 'Small candles for one sitting. Use a holder, keep away from drafts and anything flammable, and never leave a flame unattended.',
       'symbols': 'A symbol to hang or place; protective meanings come from folk tradition.', 'kits': 'A bundle that collects the pieces for one practice.'}
def describe(S, x):
    s = [f"{E(x['title'])}, from the {E(AISLES[x['aisle']][0].lower())} drawer.", USE.get(x['aisle'], '')]
    if x['family']: s.append(f"Its name points to {E(S.FAM_NAME[x['family']].lower())}; that comes from practice and folklore, not a promised result.")
    if x['style']: s.append(f"Material: {E(x['style'].lower())}, as named in the listing.")
    s.append('Mailed from New York, or collected at Namaste Bookshop on 14th Street; payment is taken on Shopify.')
    return [t for t in s if t]
def PRODUCT_DESC(S, x, v0): return f"{x['title']} for {S.money(v0['price'])}, in the {AISLES[x['aisle']][1].lower()} drawer of Namaste Metaphysical Shop. Delivered from New York or collected on 14th Street."
def FACTS_EXTRA(S, x, v0): return [('Material', E(x['style']))] if x['style'] else []
def ABOUT_DESC(S): return 'About Namaste Metaphysical Shop: ritual and altar supplies from the Namaste Bookshop inventory, run by Wealth Edge Ventures Inc.'
ABOUT_H1 = 'About Namaste Metaphysical Shop'
def ABOUT(S):
    return f'''<p class="lead">Namaste Metaphysical Shop is the supply cupboard: the tools and materials people use in practice, laid out by drawer rather than by gift idea.</p>
<p>About {S.ABOUT_N:,} pieces are listed: altar vessels and statues, pendulums and boards, runes and scrying mirrors, bowls and bells, oils, loose herbs, ritual waters and small spell candles. Incense and candles appear only in their ritual forms; Namaste runs separate incense and candle shops for the rest.</p>
<h2>Who runs it</h2><p>{S.LEGAL} The supplies come from the same stock as Namaste Bookshop, owned by the same company. Orders are paid for on Shopify through <a href="{S.SHOP}" rel="noopener">namastebookshop.com</a> and ship from New York City.</p>
<h2>A note on intentions</h2><p>Many products are named for an intention such as protection or money. We group them that way because that is how practitioners shop, but the meanings come from tradition. Nothing here is a medical product or a guarantee of a result.</p>
<h2>In person</h2><p>Come by Namaste Bookshop, {S.STORE_ADDR}, or call <a href="tel:{S.TEL}">{S.PHONE}</a>. Email <a href="mailto:info@namastebookshop.com">info@namastebookshop.com</a>.</p>{S.hours_html()}{S.visit_buttons()}'''
def FAQ_DESC(S): return 'Questions about Namaste Metaphysical Shop: shipping liquids and oils, pickup, safe use of candles and resin, and what the intention labels mean.'
FAQ_H1 = 'Supply shop questions'
def FAQ(S):
    return [('Do you ship oils and waters?', 'Yes, from New York City, through checkout on namastebookshop.com. Options and costs show before you pay.'),
            ('Is in-person pickup possible?', f'It is: select Pickup while paying and the order waits at {S.STORE_ADDR}.' + (f' Most are {S.READY.lower()}.' if S.READY else '')),
            ('Why is there so little incense here?', 'Namaste has dedicated incense shops. This site carries only loose resin, bakhoor and smudge kits for a censer or shell.'),
            ('Are the essential oils safe on skin?', 'Essential oils are concentrated. Dilute them in a carrier oil before skin contact, patch-test first, and keep them away from eyes, children and pets.'),
            ('What does "intention on the label" mean?', 'It is the purpose written in the product name, such as protection or love. It reflects tradition, not a promised effect.'),
            ('Do you carry tarot decks and books?', 'Not on this site; Namaste Bookshop carries them.')]
def GUIDES(S):
    ints = ''.join(f'<li><a href="/by-intention/{k}/">{E(n)}</a> <span class="small">{S.fam_count[k]} pieces</span></li>' for k, n, _ in FAMILIES if S.fam_count[k] >= 4)
    return [
     {'path': '/by-intention/', 'title': 'Supplies by Intention', 'desc': 'Ritual supplies grouped by the intention in their names: protection, love, money and luck, cleansing, calm, intuition and more.', 'h1': 'Shopping by intention',
      'html': f'<p class="lead">Many oils, waters, candles and symbols are named for a purpose. These groups follow those names.</p><ul class="dir">{ints}</ul><p class="small">Intentions describe tradition and practice. They are not medical or financial claims.</p>'},
     {'path': '/guide/setting-up-an-altar/', 'title': 'Setting Up a First Altar', 'desc': 'A practical way to set up a first altar: choose the surface, a focus, light, an offering vessel and something for each element, then keep it simple.', 'h1': 'Setting up a first altar',
      'html': '''<p class="lead">An altar is a surface you keep for practice. It can be a shelf, a windowsill or a small table, and it does not need to be elaborate.</p>
<h2>1. Choose the surface</h2><p>Pick a stable place where a flame is safe and the pieces will not be knocked. A cloth defines the space.</p>
<h2>2. Give it a focus</h2><p>Many altars center on a <a href="/shop/deity-altar-statues/">statue</a>, an image or a symbol that matters to you.</p>
<h2>3. Add light and an offering vessel</h2><p>A small <a href="/shop/spellwork-candles/">candle</a> in a holder and an <a href="/shop/altar-tools-vessels/">offering bowl or chalice</a> are the common basics.</p>
<h2>4. Represent the elements, if your tradition uses them</h2><p>Salt or a stone for earth, a feather or bell for air, a candle for fire, water in a bowl or chalice.</p>
<h2>5. Keep it tended</h2><p>Dust it, replace offerings, and clear away spent candles. A simple altar used often beats a crowded one used rarely.</p>'''},
     {'path': '/guide/how-to-use-a-pendulum/', 'title': 'How to Use a Pendulum', 'desc': 'Holding a pendulum, finding its yes and no, asking clear questions and using a pendulum board.', 'h1': 'Using a pendulum',
      'html': '''<p class="lead">A pendulum is a small weight on a chain. Practitioners use its swing to answer simple questions.</p>
<h2>Hold it still</h2><p>Pinch the chain a few inches above the weight, rest your elbow on a table and let the pendulum settle.</p>
<h2>Find its yes and no</h2><p>Ask a question you know the answer to, and note the movement: forward and back, side to side, or a circle. Repeat for "no".</p>
<h2>Ask clear, single questions</h2><p>Yes-or-no questions work best. Avoid asking the same thing again and again in hope of a different answer.</p>
<h2>Try a board</h2><p>A <a href="/shop/pendulums-boards/">pendulum board</a> adds letters, numbers or yes/no zones for more detailed sessions.</p>
<p class="small">Pendulum work is a divination practice, not a substitute for professional advice.</p>'''},
     {'path': '/guide/singing-bowl-care/', 'title': 'Playing and Caring for a Singing Bowl', 'desc': 'How to strike and rim a singing bowl, which mallet to use, and how to clean and store brass and crystal bowls.', 'h1': 'Playing and caring for a singing bowl',
      'html': '''<p class="lead">A bowl sounds best resting on a cushion, played with a little patience.</p>
<h2>Striking</h2><p>Tap the outer rim gently with the padded end of the mallet, then let the tone ring out.</p>
<h2>Rimming</h2><p>Press the mallet's wooden side against the outside of the rim and circle it slowly and evenly. Speed matters less than steady pressure.</p>
<h2>Brass bowls</h2><p>Wipe with a dry soft cloth after use. Fingerprints darken brass over time, which many owners like; polish only if you prefer a bright finish.</p>
<h2>Crystal bowls</h2><p>Frosted quartz bowls are fragile. Keep them on their ring, never stack them, and carry them with both hands.</p>
<p><a class="btn" href="/shop/singing-bowls-bells-sound/">Bowls, bells and mallets</a></p>'''},
    ]
NOT_FOUND = 'That drawer is empty'
def ICON_DRAW(d, s, th):
    import math
    w = max(2, int(1.8 * s)); cx, cy, r = 20*s, 20*s, 14*s
    d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=th['accent'], width=w)
    pts = [(cx + r*0.92*math.sin(math.radians(a)), cy - r*0.92*math.cos(math.radians(a))) for a in (0, 144, 288, 72, 216, 0)]
    d.line(pts, fill=th['paper'], width=w, joint='curve')
