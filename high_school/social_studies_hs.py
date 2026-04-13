"""
High School Social Studies Generator (Grades 9–12) — Fact Triplet Engine
Covers: US History, World History, Economics, Government & Civics

Architecture: each topic has a _FACTS list (dicts with named fields) and a
_TEMPLATES list of (question_fmt, ans_key, dist_key, difficulty, grade).
The engine masks ans_key, formats the question from remaining fields, and
draws distractors from other facts' dist_key values — yielding
len(facts) × len(templates) unique question types per topic.
"""
import random
import json


def _q(topic, diff, question, choices, answer_idx, explanation, grade=10):
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


# ── US History  (12 facts × 5 templates = 60 unique question types) ──────────

_US_HIST_FACTS = [
    {'event': 'Constitutional Convention',
     'date': '1787',
     'who': 'Founding Fathers including Madison, Hamilton, and Washington',
     'what_happened': 'delegates drafted the US Constitution to replace the ineffective Articles of Confederation',
     'significance': 'created the framework for US government with three branches still in use today'},
    {'event': 'Missouri Compromise',
     'date': '1820',
     'who': 'Congress, brokered by Henry Clay',
     'what_happened': 'admitted Missouri as a slave state and Maine as free; banned slavery north of 36°30\'N',
     'significance': 'temporarily eased tensions over slavery\'s expansion but did not resolve the underlying conflict'},
    {'event': 'Civil War',
     'date': '1861–1865',
     'who': 'Union (Northern states) vs. Confederacy (Southern states)',
     'what_happened': 'Southern states seceded over slavery; the Union fought to preserve the nation',
     'significance': 'ended slavery in the US and preserved the Union, though left deep racial and regional divisions'},
    {'event': 'Emancipation Proclamation',
     'date': '1863',
     'who': 'President Abraham Lincoln',
     'what_happened': 'declared enslaved people in Confederate states to be free',
     'significance': 'shifted the Civil War\'s stated purpose to ending slavery and prevented European support for the Confederacy'},
    {'event': 'Reconstruction',
     'date': '1865–1877',
     'who': 'federal government, formerly enslaved people, and Radical Republicans in Congress',
     'what_happened': 'the federal government tried to rebuild the South and integrate freed people as citizens',
     'significance': 'established the 13th, 14th, and 15th Amendments, but ended with Jim Crow laws taking hold'},
    {'event': 'World War I (US involvement)',
     'date': '1917–1918',
     'who': 'US joined the Allied Powers (Britain, France, Russia)',
     'what_happened': 'US entered WWI after German unrestricted submarine warfare and the Zimmermann Telegram',
     'significance': 'helped the Allies win; the US emerged as a major world power but retreated into isolationism'},
    {'event': 'the Great Depression',
     'date': '1929–1939',
     'who': 'entire US population, especially farmers, workers, and banks',
     'what_happened': 'the 1929 stock market crash triggered bank failures, massive unemployment, and global economic collapse',
     'significance': 'led to FDR\'s New Deal and permanently expanded the federal government\'s role in the economy'},
    {'event': 'the New Deal',
     'date': '1933–1939',
     'who': 'President Franklin D. Roosevelt and the Democratic-controlled Congress',
     'what_happened': 'a sweeping series of programs providing relief, economic recovery, and financial reform',
     'significance': 'created Social Security, the FDIC, and public works programs that still shape American life'},
    {'event': 'World War II (US involvement)',
     'date': '1941–1945',
     'who': 'US joined the Allies after Japan attacked Pearl Harbor on December 7, 1941',
     'what_happened': 'US fought on two fronts — Europe against Nazi Germany and the Pacific against Imperial Japan',
     'significance': 'US emerged as a global superpower; ended the Great Depression; set the stage for the Cold War'},
    {'event': 'Civil Rights Movement',
     'date': '1950s–1960s',
     'who': 'African Americans led by figures such as MLK, Rosa Parks, and John Lewis',
     'what_happened': 'nonviolent protests, marches, and legal challenges dismantled legal segregation in the South',
     'significance': 'led to the Civil Rights Act (1964) and Voting Rights Act (1965), ending legal segregation'},
    {'event': 'Cold War',
     'date': '1947–1991',
     'who': 'United States (capitalism) vs. Soviet Union (communism)',
     'what_happened': 'a geopolitical and ideological rivalry without direct war, fought through proxy conflicts and arms races',
     'significance': 'shaped US foreign policy for four decades; included the Korean War, Vietnam War, and Space Race'},
    {'event': 'September 11 attacks',
     'date': '2001',
     'who': 'Al-Qaeda terrorists hijacked four commercial airliners',
     'what_happened': 'planes struck the World Trade Center and Pentagon, killing nearly 3,000 people',
     'significance': 'launched the War on Terror, the invasion of Afghanistan, and reshaped US security and foreign policy'},
]

_US_HIST_TEMPLATES = [
    ('When did {event} take place?',
     'date', 'date', 'easy', 9),
    ('Who was involved in {event}?',
     'who', 'who', 'medium', 10),
    ('What happened during {event}?',
     'what_happened', 'what_happened', 'medium', 10),
    ('What was the historical significance of {event}?',
     'significance', 'significance', 'hard', 11),
    ('Which event is described as follows: "{what_happened}"?',
     'event', 'event', 'hard', 11),
]


def gen_us_history(n=40, seed=None):
    return _fact_qs(_US_HIST_FACTS, _US_HIST_TEMPLATES,
                    'US History', n, random.Random(seed))


# ── World History  (12 facts × 5 templates = 60 unique question types) ───────

_WORLD_HIST_FACTS = [
    {'event': 'French Revolution',
     'date': '1789–1799',
     'location': 'France',
     'what_happened': 'the French monarchy was overthrown and a republic established after a popular uprising against absolute rule',
     'significance': 'spread ideals of liberty, equality, and popular sovereignty; ended feudal privileges; influenced future revolutions'},
    {'event': 'Industrial Revolution',
     'date': '1760s–1840s',
     'location': 'Britain, then spreading to Europe and the Americas',
     'what_happened': 'economies shifted from agriculture to factory manufacturing driven by steam power and mechanization',
     'significance': 'transformed living standards, created the factory system, and sparked urbanization and labor movements'},
    {'event': 'Napoleonic Wars',
     'date': '1803–1815',
     'location': 'Europe',
     'what_happened': 'Napoleon Bonaparte conquered much of Europe before being defeated at Waterloo and exiled',
     'significance': 'spread French Revolutionary ideals across Europe; redrew borders; led to the Congress of Vienna'},
    {'event': 'Scramble for Africa (European imperialism)',
     'date': '1881–1914',
     'location': 'Africa',
     'what_happened': 'European powers rapidly divided and colonized nearly all of Africa, ignoring existing ethnic and political boundaries',
     'significance': 'exploited African resources and peoples; created arbitrary borders that contributed to modern conflicts'},
    {'event': 'World War I',
     'date': '1914–1918',
     'location': 'Europe and beyond',
     'what_happened': 'European alliance systems triggered a global war after the assassination of Archduke Franz Ferdinand in Sarajevo',
     'significance': 'killed over 20 million people; dissolved empires; created resentments that led directly to World War II'},
    {'event': 'Russian Revolution',
     'date': '1917',
     'location': 'Russia',
     'what_happened': 'Tsar Nicholas II was overthrown; Lenin\'s Bolsheviks seized power and established a communist government',
     'significance': 'created the Soviet Union and launched decades of communist influence and Cold War tensions worldwide'},
    {'event': 'Holocaust',
     'date': '1933–1945',
     'location': 'Nazi Germany and occupied Europe',
     'what_happened': 'the Nazi regime systematically murdered approximately 6 million Jews and millions of others in concentration camps',
     'significance': 'deadliest genocide in modern history; led to international human rights law and the founding of Israel'},
    {'event': 'World War II',
     'date': '1939–1945',
     'location': 'Europe, Pacific, Africa, and beyond',
     'what_happened': 'Nazi Germany, Fascist Italy, and Imperial Japan were defeated by the Allied Powers after a global conflict',
     'significance': 'deadliest war in history (~70–85 million deaths); led to the United Nations and the Cold War'},
    {'event': 'decolonization of Asia and Africa',
     'date': '1945–1975',
     'location': 'Asia and Africa',
     'what_happened': 'colonial peoples across Asia and Africa gained independence from European powers after World War II',
     'significance': 'created dozens of new nations and reshaped global politics, raising questions about development and self-determination'},
    {'event': 'Chinese Communist Revolution',
     'date': '1949',
     'location': 'China',
     'what_happened': 'Mao Zedong\'s Communist Party defeated the Nationalist government and established the People\'s Republic of China',
     'significance': 'made China a communist state; intensified Cold War tensions in Asia; affected millions through radical policies'},
    {'event': 'collapse of the Soviet Union',
     'date': '1991',
     'location': 'Soviet Union (Eastern Europe and Central Asia)',
     'what_happened': 'the USSR dissolved into 15 independent republics after economic stagnation and failed reforms under Gorbachev',
     'significance': 'ended the Cold War; expanded democracy and free markets in Eastern Europe; reshaped global geopolitics'},
    {'event': 'Rwandan Genocide',
     'date': '1994',
     'location': 'Rwanda, Africa',
     'what_happened': 'Hutu extremists systematically killed approximately 800,000 Tutsi and moderate Hutu within 100 days',
     'significance': 'exposed the international community\'s failure to prevent genocide and prompted debates on humanitarian intervention'},
]

_WORLD_HIST_TEMPLATES = [
    ('When did {event} occur?',
     'date', 'date', 'easy', 9),
    ('Where did {event} primarily take place?',
     'location', 'location', 'easy', 9),
    ('What happened during {event}?',
     'what_happened', 'what_happened', 'medium', 10),
    ('What was the historical significance of {event}?',
     'significance', 'significance', 'hard', 11),
    ('Which historical event is described as: "{what_happened}"?',
     'event', 'event', 'hard', 12),
]


def gen_world_history_hs(n=40, seed=None):
    return _fact_qs(_WORLD_HIST_FACTS, _WORLD_HIST_TEMPLATES,
                    'World History', n, random.Random(seed))


# ── Economics  (10 facts × 4 templates = 40 unique question types) ───────────

_ECON_FACTS = [
    {'term': 'GDP (Gross Domestic Product)',
     'definition': 'the total monetary value of all goods and services produced in a country in a given year',
     'example': 'the US GDP in 2023 was approximately $27 trillion, the largest in the world',
     'significance': 'the primary measure of a country\'s economic size and standard of living'},
    {'term': 'inflation',
     'definition': 'a general and sustained rise in the price level of goods and services over time',
     'example': 'if a basket of groceries that cost $100 last year costs $103 today, inflation is 3%',
     'significance': 'erodes purchasing power; the Federal Reserve targets approximately 2% annual inflation'},
    {'term': 'opportunity cost',
     'definition': 'the value of the next-best alternative foregone when making a choice',
     'example': 'choosing to attend college means forgoing four years of full-time employment income',
     'significance': 'central to economics — every choice involves a trade-off; drives rational decision-making'},
    {'term': 'supply and demand',
     'definition': 'the relationship between the quantity sellers offer and buyers want, which determines market price and quantity',
     'example': 'when a hurricane damages oil refineries, gasoline prices rise because supply drops while demand stays the same',
     'significance': 'the foundation of market economies; determines prices, output, and resource allocation'},
    {'term': 'comparative advantage',
     'definition': 'the ability to produce a good at a lower opportunity cost than others, justifying specialization and trade',
     'example': 'even if the US can produce both wheat and textiles more efficiently than Mexico, both countries benefit by specializing',
     'significance': 'explains why free trade increases total wealth even when one country is better at producing everything'},
    {'term': 'monetary policy',
     'definition': 'a central bank\'s control of interest rates and money supply to manage inflation and stabilize the economy',
     'example': 'the Federal Reserve raises interest rates to slow borrowing and cool down inflation',
     'significance': 'primary tool for managing economic cycles without requiring new legislation from Congress'},
    {'term': 'fiscal policy',
     'definition': 'a government\'s use of spending and taxation to influence economic activity',
     'example': 'Congress passes a stimulus package, increasing government spending to reduce unemployment during a recession',
     'significance': 'allows the government to directly stimulate or contract economic activity; controlled by elected officials'},
    {'term': 'monopoly',
     'definition': 'a market structure in which a single firm is the sole supplier of a product with no close substitutes',
     'example': 'a utility company with exclusive rights to provide electricity in a region',
     'significance': 'monopolies can charge above-market prices; antitrust laws such as the Sherman Act aim to prevent harmful monopolies'},
    {'term': 'progressive tax',
     'definition': 'a tax system in which the effective rate increases as the taxable amount (income) increases',
     'example': 'the US federal income tax charges someone earning $500,000 a higher percentage than someone earning $50,000',
     'significance': 'aims to reduce income inequality by requiring higher earners to contribute proportionally more'},
    {'term': 'market failure',
     'definition': 'a situation in which free markets fail to allocate resources efficiently, typically requiring government intervention',
     'example': 'a factory that pollutes a river creates a market failure because the firm does not pay the full cost of the harm it causes',
     'significance': 'justifies government roles in providing public goods, regulating externalities, and protecting consumers'},
]

_ECON_TEMPLATES = [
    ('What is {term}?',
     'definition', 'definition', 'medium', 10),
    ('Which economic term is defined as: "{definition}"?',
     'term', 'term', 'hard', 11),
    ('Which of these is an accurate example of {term}?',
     'example', 'example', 'medium', 10),
    ('Why is {term} important in economics?',
     'significance', 'significance', 'hard', 12),
]


def gen_economics_hs(n=35, seed=None):
    return _fact_qs(_ECON_FACTS, _ECON_TEMPLATES,
                    'Economics', n, random.Random(seed))


# ── Government & Civics  (10 facts × 4 templates = 40 unique question types) ─

_CIVICS_FACTS = [
    {'concept': 'judicial review',
     'definition': 'the power of courts to declare laws or government actions unconstitutional',
     'established_by': 'Marbury v. Madison (1803)',
     'significance': 'makes the judiciary a check on both legislative and executive power',
     'example': 'the Supreme Court strikes down a state law that discriminates based on race'},
    {'concept': 'First Amendment',
     'definition': 'protects freedom of speech, religion, press, peaceful assembly, and petition',
     'established_by': 'Bill of Rights (1791)',
     'significance': 'foundational protection of civil liberties; among the most litigated parts of the Constitution',
     'example': 'a citizen publicly criticizes the government and cannot be arrested for it'},
    {'concept': '14th Amendment',
     'definition': 'guarantees equal protection under the law, due process, and defines citizenship',
     'established_by': 'Reconstruction era (ratified 1868)',
     'significance': 'foundation for landmark civil rights cases; extended citizenship to formerly enslaved people',
     'example': 'Brown v. Board of Education used the 14th Amendment to strike down school segregation'},
    {'concept': 'separation of powers',
     'definition': 'the division of government authority among legislative, executive, and judicial branches',
     'established_by': 'US Constitution (1788)',
     'significance': 'prevents any single branch from dominating the government or becoming tyrannical',
     'example': 'Congress passes a law; the President signs it; the Supreme Court rules on its constitutionality'},
    {'concept': 'habeas corpus',
     'definition': 'the right to have a court determine whether your detention by the government is lawful',
     'established_by': 'English common law; incorporated into the US Constitution (Article I)',
     'significance': 'fundamental safeguard against indefinite imprisonment without charge or trial',
     'example': 'a prisoner petitions a federal court for release by arguing the government lacks legal grounds for detention'},
    {'concept': 'gerrymandering',
     'definition': 'manipulating electoral district boundaries to give an unfair advantage to a particular party or group',
     'established_by': 'named after Massachusetts Governor Elbridge Gerry, who signed a redistricting plan in 1812',
     'significance': 'can dilute minority votes or guarantee party safe seats, undermining fair representation',
     'example': 'a majority party draws a district in an unusual shape to pack opposition voters together and waste their votes'},
    {'concept': 'federalism',
     'definition': 'a system in which power is constitutionally divided between a national government and state governments',
     'established_by': 'US Constitution and 10th Amendment (1791)',
     'significance': 'allows states to govern themselves while maintaining a unified national framework',
     'example': 'states set their own speed limits and marriage laws; the federal government controls immigration and foreign policy'},
    {'concept': 'due process',
     'definition': 'the principle that the government must respect all legal rights owed to a person before depriving them of life, liberty, or property',
     'established_by': '5th Amendment (1791) and 14th Amendment (1868)',
     'significance': 'protects individuals from arbitrary government action and ensures fair legal proceedings',
     'example': 'a person accused of a crime must receive notice of charges and a fair trial before being punished'},
    {'concept': 'checks and balances',
     'definition': 'the system by which each branch of government can limit and oversee the powers of the other branches',
     'established_by': 'US Constitution (1788)',
     'significance': 'prevents tyranny by any single branch; forces cooperation and compromise across branches',
     'example': 'the President nominates Supreme Court justices; the Senate must confirm or reject those nominations'},
    {'concept': 'popular sovereignty',
     'definition': 'the principle that political authority rests with the people, who consent to be governed',
     'established_by': 'Declaration of Independence (1776) and US Constitution (1788)',
     'significance': 'foundation of democratic government — legitimacy flows from the citizens, not from kings or elites',
     'example': 'citizens vote in elections to choose their representatives in Congress and the White House'},
]

_CIVICS_TEMPLATES = [
    ('What is {concept}?',
     'definition', 'definition', 'medium', 10),
    ('Which legal principle or concept was established or named by {established_by}?',
     'concept', 'concept', 'hard', 11),
    ('Why is {concept} significant in American government?',
     'significance', 'significance', 'hard', 11),
    ('Which of these is an accurate example of {concept} in action?',
     'example', 'example', 'medium', 10),
]


def gen_government_civics(n=35, seed=None):
    return _fact_qs(_CIVICS_FACTS, _CIVICS_TEMPLATES,
                    'Government & Civics', n, random.Random(seed))


# ── Standard interface ───────────────────────────────────────────────────────

_TOPIC_GENERATORS = {
    'US History':          [(gen_us_history, {})],
    'World History':       [(gen_world_history_hs, {})],
    'Economics':           [(gen_economics_hs, {})],
    'Government & Civics': [(gen_government_civics, {})],
}

_DIFF_WEIGHTS = {t: {'easy': [fn], 'medium': [fn], 'hard': [fn]}
                 for t, [(fn, _)] in _TOPIC_GENERATORS.items()}


def generate_for_topic(topic, difficulty='medium', count=10, seed=None):
    """Return a list of `count` question dicts for `topic`.

    Each dict has keys: id, subject, topic, difficulty, question,
    choices (list of 4 strings), answer (index of correct choice), explanation.
    Both the question and the correct answer are always present.
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
            all_qs.extend(fn(seed=r.randint(0, 999999), n=35))
    return all_qs
