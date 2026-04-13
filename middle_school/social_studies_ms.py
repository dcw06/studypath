"""
Middle School Social Studies Generator (Grades 6–8) — Fact Triplet Engine
Covers: Ancient Civilizations, Medieval History, World Geography,
        Early American History, Government Basics

Architecture: each topic has a _FACTS list (dicts with named fields) and a
_TEMPLATES list of (question_fmt, ans_key, dist_key, difficulty, grade).
The engine masks ans_key, formats the question from remaining fields, and
draws distractors from other facts' dist_key values — yielding
len(facts) × len(templates) unique question types per topic.
"""
import random
import json


def _q(topic, diff, question, choices, answer_idx, explanation, grade=7):
    return ('Social Studies', topic, diff, question, json.dumps(choices), answer_idx, explanation, grade)


def _shuffle_choices(correct, wrongs, rng):
    choices = list(rng.sample(wrongs, min(3, len(wrongs))))
    idx = rng.randint(0, min(3, len(choices)))
    choices.insert(idx, correct)
    return choices[:4], idx


def _fact_qs(facts, templates, topic, n, rng):
    """Core fact-triplet engine.

    templates: list of (question_fmt, ans_key, dist_key, difficulty, grade)
      - question_fmt: Python format string using {field} placeholders for all
        fact fields *except* ans_key (the answer field is masked out).
      - ans_key:   which field is the correct answer.
      - dist_key:  which field from *other* facts to use as distractors
                   (almost always same as ans_key).
      - difficulty, grade: metadata for the generated question.

    Returns n 8-tuple questions.
    """
    pairs = [(f, t) for f in facts for t in templates]
    qs = []
    for _ in range(n):
        fact, (tmpl, ans_key, dist_key, diff, grade) = rng.choice(pairs)
        answer = str(fact[ans_key])
        fmt_fields = {k: v for k, v in fact.items() if k != ans_key}
        q_text = tmpl.format(**fmt_fields)
        distractors = list(dict.fromkeys(
            str(f[dist_key]) for f in facts if str(f[dist_key]) != answer
        ))
        choices, idx = _shuffle_choices(answer, distractors, rng)
        qs.append(_q(topic, diff, q_text, choices, idx, f"Correct: {answer}.", grade))
    return qs


# ── Ancient Civilizations  (10 facts × 6 templates = 60 unique question types)

_ANCIENT_FACTS = [
    {'civ': 'Sumer (Mesopotamia)',
     'region': 'Tigris and Euphrates river valley',
     'achievement': 'cuneiform writing — the first writing system',
     'known_for': 'inventing writing and organizing the first city-states',
     'period': 'c. 4500–1900 BCE'},
    {'civ': 'Ancient Egypt',
     'region': 'Nile River valley in northeastern Africa',
     'achievement': 'pyramid construction and hieroglyphic writing',
     'known_for': 'pharaohs, pyramids, and mummification',
     'period': 'c. 3100–30 BCE'},
    {'civ': 'Ancient Greece',
     'region': 'Aegean peninsula and islands in southeastern Europe',
     'achievement': 'democracy and systematic philosophy',
     'known_for': 'democracy, the Olympic Games, and philosophy',
     'period': 'c. 800–146 BCE'},
    {'civ': 'Ancient Rome',
     'region': 'Italian peninsula and the Mediterranean world',
     'achievement': 'Roman law and engineering (roads and aqueducts)',
     'known_for': 'Roman law, roads, a vast empire, and a republican government',
     'period': 'c. 753 BCE–476 CE'},
    {'civ': 'Ancient China',
     'region': 'Yellow River and Yangtze River valleys in East Asia',
     'achievement': 'papermaking, silk production, and gunpowder',
     'known_for': 'the Great Wall, the Silk Road, and Confucianism',
     'period': 'c. 2100 BCE onward'},
    {'civ': 'Indus Valley civilization',
     'region': 'Indus River valley in South Asia (modern Pakistan and India)',
     'achievement': 'planned cities with grid layouts and underground sewage systems',
     'known_for': 'advanced urban planning and sanitation',
     'period': 'c. 3300–1300 BCE'},
    {'civ': 'Phoenicia',
     'region': 'eastern Mediterranean coast (modern Lebanon and Syria)',
     'achievement': 'phonetic alphabet — the ancestor of most modern alphabets',
     'known_for': 'the alphabet and Mediterranean sea trade',
     'period': 'c. 1500–300 BCE'},
    {'civ': 'Babylon',
     'region': 'Mesopotamia (modern Iraq)',
     'achievement': "Hammurabi's Code — one of the earliest written law codes",
     'known_for': "Hammurabi's Code and the legendary Hanging Gardens",
     'period': 'c. 1894–539 BCE'},
    {'civ': 'Ancient Persia',
     'region': 'Iranian plateau and surrounding regions',
     'achievement': 'Royal Road and an efficient imperial postal system',
     'known_for': 'the largest empire of the ancient world and religious tolerance',
     'period': 'c. 550–330 BCE'},
    {'civ': 'Maya',
     'region': 'Mesoamerica (Yucatán Peninsula and Central America)',
     'achievement': 'advanced calendar, hieroglyphic writing, and astronomical knowledge',
     'known_for': 'precise astronomy, mathematics, and monumental stone temples',
     'period': 'c. 2000 BCE–1500 CE'},
]

_ANCIENT_TEMPLATES = [
    ('Which ancient civilization was located in the {region}?',
     'civ', 'civ', 'easy', 6),
    ('Where was the {civ} civilization located?',
     'region', 'region', 'easy', 6),
    ('What was a major achievement of the {civ} civilization?',
     'achievement', 'achievement', 'medium', 7),
    ('What is the {civ} civilization best known for?',
     'known_for', 'known_for', 'medium', 7),
    ('Which ancient civilization is known for {known_for}?',
     'civ', 'civ', 'medium', 7),
    ('Approximately when did the {civ} civilization exist?',
     'period', 'period', 'hard', 8),
]


def gen_ancient_civilizations(n=35, seed=None):
    return _fact_qs(_ANCIENT_FACTS, _ANCIENT_TEMPLATES,
                    'Ancient Civilizations', n, random.Random(seed))


# ── Medieval History  (8 facts × 4 templates = 32 unique question types)

_MEDIEVAL_FACTS = [
    {'event': 'Feudalism',
     'period': 'c. 900–1300 CE',
     'location': 'medieval Europe',
     'what_was_it': 'a social and political system where lords granted land to vassals in exchange for military service',
     'significance': 'organized society and military power in the absence of strong central governments'},
    {'event': 'the Crusades',
     'period': '1095–1291 CE',
     'location': 'Europe and the Middle East',
     'what_was_it': 'a series of military campaigns by European Christians to capture the Holy Land (Jerusalem)',
     'significance': 'increased cultural exchange and trade between Europe and the Islamic world'},
    {'event': 'the Black Death',
     'period': '1347–1351 CE',
     'location': 'Europe and parts of Asia',
     'what_was_it': 'a devastating bubonic plague epidemic that killed approximately one-third of Europe\'s population',
     'significance': 'disrupted the feudal system, reduced the labor force, and reshaped European society and religion'},
    {'event': 'Magna Carta',
     'period': '1215 CE',
     'location': 'England',
     'what_was_it': 'a legal charter limiting the power of the English king and protecting the rights of nobles and freemen',
     'significance': 'one of the earliest limits on royal power and a foundation for constitutional government'},
    {'event': 'the Byzantine Empire',
     'period': '330–1453 CE',
     'location': 'Constantinople (modern Istanbul, Turkey)',
     'what_was_it': 'the eastern continuation of the Roman Empire after Rome fell in 476 CE',
     'significance': 'preserved Greek and Roman knowledge through the Middle Ages and influenced Eastern Europe'},
    {'event': 'the Norman Conquest',
     'period': '1066 CE',
     'location': 'England',
     'what_was_it': 'William of Normandy defeated King Harold at the Battle of Hastings and became King of England',
     'significance': 'blended Norman French and Anglo-Saxon cultures, shaping the English language and feudal law in England'},
    {'event': 'guilds',
     'period': 'c. 1000–1500 CE',
     'location': 'medieval European cities',
     'what_was_it': 'associations of craftsmen or merchants that regulated trade, set quality standards, and trained apprentices',
     'significance': 'controlled quality and pricing for skilled trades, strengthening the merchant middle class'},
    {'event': 'the Renaissance',
     'period': 'c. 1300–1600 CE',
     'location': 'Italy, then spreading throughout Europe',
     'what_was_it': 'a cultural movement emphasizing art, humanism, and a rebirth of classical Greek and Roman ideas',
     'significance': 'produced masterworks by Leonardo da Vinci and Michelangelo and laid the groundwork for the Scientific Revolution'},
]

_MEDIEVAL_TEMPLATES = [
    ('What was {event}?',
     'what_was_it', 'what_was_it', 'medium', 7),
    ('When did {event} occur?',
     'period', 'period', 'medium', 7),
    ('Where did {event} primarily take place?',
     'location', 'location', 'easy', 6),
    ('What was the historical significance of {event}?',
     'significance', 'significance', 'hard', 8),
]


def gen_medieval_history(n=30, seed=None):
    return _fact_qs(_MEDIEVAL_FACTS, _MEDIEVAL_TEMPLATES,
                    'Medieval History', n, random.Random(seed))


# ── World Geography  (10 facts × 4 templates = 40 unique question types)

_GEO_FACTS = [
    {'place': 'Nile River',
     'type': 'river',
     'continent': 'Africa',
     'country': 'Egypt and northeastern Africa',
     'notable_for': 'longest river in the world (~6,650 km)'},
    {'place': 'Amazon River',
     'type': 'river',
     'continent': 'South America',
     'country': 'Brazil and neighboring countries',
     'notable_for': 'largest river in the world by water volume'},
    {'place': 'Pacific Ocean',
     'type': 'ocean',
     'continent': 'between Asia/Australia and the Americas',
     'country': 'international waters',
     'notable_for': 'largest and deepest ocean on Earth'},
    {'place': 'Sahara Desert',
     'type': 'desert',
     'continent': 'Africa',
     'country': 'northern Africa (Algeria, Libya, Egypt, and others)',
     'notable_for': 'largest hot desert in the world (~9.2 million km²)'},
    {'place': 'Mount Everest',
     'type': 'mountain',
     'continent': 'Asia',
     'country': 'Nepal and China (Tibet)',
     'notable_for': 'tallest mountain in the world at 8,849 m above sea level'},
    {'place': 'Amazon Rainforest',
     'type': 'tropical rainforest',
     'continent': 'South America',
     'country': 'primarily Brazil',
     'notable_for': 'largest tropical rainforest on Earth and greatest biodiversity'},
    {'place': 'Ural Mountains',
     'type': 'mountain range',
     'continent': 'Europe/Asia border',
     'country': 'Russia',
     'notable_for': 'traditional geographic boundary between Europe and Asia'},
    {'place': 'Ganges River',
     'type': 'river',
     'continent': 'Asia',
     'country': 'India and Bangladesh',
     'notable_for': 'sacred river in Hinduism, central to Indian civilization'},
    {'place': 'Antarctica',
     'type': 'continent',
     'continent': 'Antarctica (South Pole)',
     'country': 'no permanent population; claimed by multiple nations',
     'notable_for': 'coldest and driest continent on Earth'},
    {'place': 'the Equator',
     'type': 'imaginary line at 0° latitude',
     'continent': 'crosses Africa, South America, and Asia',
     'country': 'passes through multiple countries in three continents',
     'notable_for': 'divides Earth into the Northern and Southern hemispheres'},
]

_GEO_TEMPLATES = [
    ('On which continent is the {place} located?',
     'continent', 'continent', 'easy', 6),
    ('In which country or region is the {place} found?',
     'country', 'country', 'medium', 7),
    ('What type of geographic feature is the {place}?',
     'type', 'type', 'medium', 7),
    ('What is the {place} most notable for?',
     'notable_for', 'notable_for', 'medium', 7),
]


def gen_world_geography(n=30, seed=None):
    return _fact_qs(_GEO_FACTS, _GEO_TEMPLATES,
                    'World Geography', n, random.Random(seed))


# ── Early American History  (10 facts × 4 templates = 40 unique question types)

_EARLY_AMER_FACTS = [
    {'event': 'First Americans arrive',
     'date': 'c. 15,000–20,000 years ago',
     'who': 'Indigenous peoples who migrated from Asia',
     'location': 'the Americas (via the Bering Land Bridge)',
     'significance': 'the first human habitation of North and South America'},
    {'event': "Columbus's voyage to the Americas",
     'date': '1492',
     'who': 'Christopher Columbus, funded by Spain',
     'location': 'the Caribbean (island of San Salvador)',
     'significance': 'initiated sustained European contact with the Americas'},
    {'event': 'the Columbian Exchange',
     'date': 'after 1492',
     'who': 'European settlers, Indigenous peoples, and Africans',
     'location': 'the Atlantic world',
     'significance': 'transferred plants, animals, diseases, and ideas between the Old World and New World'},
    {'event': 'founding of Jamestown',
     'date': '1607',
     'who': 'English settlers of the Virginia Company',
     'location': 'Virginia, North America',
     'significance': 'the first permanent English settlement in North America'},
    {'event': 'Mayflower Compact',
     'date': '1620',
     'who': 'Pilgrims (Separatist Puritans) aboard the Mayflower',
     'location': 'Plymouth, Massachusetts',
     'significance': 'one of the earliest examples of self-government by consent in the American colonies'},
    {'event': 'French and Indian War',
     'date': '1754–1763',
     'who': 'Britain vs. France and their Native American allies',
     'location': 'North America',
     'significance': "Britain won French territory but imposed new colonial taxes, fueling the American Revolution"},
    {'event': 'American Revolution begins',
     'date': '1775',
     'who': 'American colonists (Patriots) vs. British forces',
     'location': 'Lexington and Concord, Massachusetts',
     'significance': 'began the armed conflict for American independence from Britain'},
    {'event': 'Declaration of Independence',
     'date': 'July 4, 1776',
     'who': 'Continental Congress, drafted primarily by Thomas Jefferson',
     'location': 'Philadelphia, Pennsylvania',
     'significance': 'declared the 13 colonies independent from Britain and asserted natural rights'},
    {'event': 'US Constitution ratified',
     'date': '1788',
     'who': 'Founding Fathers and delegates from the states',
     'location': 'Philadelphia, Pennsylvania',
     'significance': 'established the framework for US government with three branches and checks and balances'},
    {'event': 'Louisiana Purchase',
     'date': '1803',
     'who': 'President Thomas Jefferson purchased the territory from France',
     'location': 'central North America',
     'significance': 'roughly doubled the size of the United States'},
]

_EARLY_AMER_TEMPLATES = [
    ('When did {event} occur?',
     'date', 'date', 'easy', 6),
    ('Who was involved in {event}?',
     'who', 'who', 'medium', 7),
    ('Where did {event} take place?',
     'location', 'location', 'medium', 7),
    ('What was the historical significance of {event}?',
     'significance', 'significance', 'hard', 8),
]


def gen_early_american_history(n=30, seed=None):
    return _fact_qs(_EARLY_AMER_FACTS, _EARLY_AMER_TEMPLATES,
                    'Early American History', n, random.Random(seed))


# ── Government Basics  (8 facts × 4 templates = 32 unique question types)

_GOV_FACTS = [
    {'concept': 'Legislative Branch (Congress)',
     'also_called': 'Congress',
     'function': 'makes the laws of the United States',
     'composed_of': 'the Senate and the House of Representatives',
     'example': 'Congress votes to pass a new tax law or the annual federal budget'},
    {'concept': 'Executive Branch',
     'also_called': 'the Presidency',
     'function': 'enforces and carries out the laws',
     'composed_of': 'the President, Vice President, and Cabinet',
     'example': 'the President signs a bill into law or vetoes it'},
    {'concept': 'Judicial Branch',
     'also_called': 'the Courts',
     'function': 'interprets the Constitution and federal laws',
     'composed_of': 'the Supreme Court and lower federal courts',
     'example': 'the Supreme Court rules that a law violates the Constitution'},
    {'concept': 'the US Constitution',
     'also_called': 'the supreme law of the land',
     'function': 'establishes the structure and limits of the US government',
     'composed_of': 'a Preamble, 7 articles, and 27 amendments',
     'example': 'defines the three branches of government and protects individual rights through amendments'},
    {'concept': 'the Bill of Rights',
     'also_called': 'the first 10 amendments to the Constitution',
     'function': 'protects individual freedoms from government overreach',
     'composed_of': 'the first 10 amendments, ratified in 1791',
     'example': 'the First Amendment protects freedom of speech, religion, and press'},
    {'concept': 'federalism',
     'also_called': 'shared sovereignty between national and state governments',
     'function': 'divides power between the national government and the individual states',
     'composed_of': 'the federal government and 50 state governments',
     'example': 'states set their own education standards; the federal government controls national defense'},
    {'concept': 'checks and balances',
     'also_called': 'the system of shared and limited powers',
     'function': 'prevents any one branch of government from having too much power',
     'composed_of': 'powers distributed and limited across all three branches',
     'example': 'the President vetoes a law; Congress can override the veto with a two-thirds majority'},
    {'concept': 'the Electoral College',
     'also_called': 'the presidential election system',
     'function': 'electors formally select the President and Vice President',
     'composed_of': '538 electors (270 electoral votes needed to win)',
     'example': 'a candidate wins all of a state\'s electoral votes by winning that state\'s popular vote'},
]

_GOV_TEMPLATES = [
    ('What does {concept} do in the US government?',
     'function', 'function', 'medium', 7),
    ('What is another name for {concept}?',
     'also_called', 'also_called', 'easy', 6),
    ('Who or what is {concept} composed of?',
     'composed_of', 'composed_of', 'medium', 7),
    ('Which of these is an example of {concept} in action?',
     'example', 'example', 'hard', 8),
]


def gen_government_basics(n=25, seed=None):
    return _fact_qs(_GOV_FACTS, _GOV_TEMPLATES,
                    'Government', n, random.Random(seed))


# ── Standard interface ───────────────────────────────────────────────────────

_TOPIC_GENERATORS = {
    'Ancient Civilizations':  [(gen_ancient_civilizations, {})],
    'Medieval History':       [(gen_medieval_history, {})],
    'World Geography':        [(gen_world_geography, {})],
    'Early American History': [(gen_early_american_history, {})],
    'Government':             [(gen_government_basics, {})],
}

_DIFF_WEIGHTS = {t: {'easy': [fn], 'medium': [fn], 'hard': [fn]}
                 for t, [(fn, _)] in _TOPIC_GENERATORS.items()}


def generate_for_topic(topic, difficulty='medium', count=10, seed=None):
    """Return a list of `count` question dicts for `topic`.

    Each dict has keys: id, subject, topic, difficulty, question,
    choices (list of 4 strings), answer (index of correct choice), explanation.
    """
    import random as _r
    rng = _r.Random(seed)
    fns = (_DIFF_WEIGHTS.get(topic, {}).get(difficulty)
           or [fn for fn, _ in _TOPIC_GENERATORS.get(topic, [])])
    if not fns:
        return []
    pool = []
    for fn in fns:
        pool.extend(fn(seed=rng.randint(0, 999999), n=max(count * 3, 30)))
    rng.shuffle(pool)
    return [{'id': -(i + 1), 'subject': row[0], 'topic': row[1], 'difficulty': row[2],
             'question': row[3], 'choices': json.loads(row[4]), 'answer': row[5],
             'explanation': row[6]} for i, row in enumerate(pool[:count])]


def generate_all(seed=42):
    """Return all questions as 8-tuples for database seeding."""
    r = random.Random(seed)
    all_qs = []
    for fns in _TOPIC_GENERATORS.values():
        for fn, kwargs in fns:
            all_qs.extend(fn(seed=r.randint(0, 999999), n=30))
    return all_qs
