"""
Elementary School Social Studies Generator (K–5)
Covers: Community & Citizenship, Maps & Geography, American Symbols & Holidays,
        US History Basics, World Communities, Government Basics
"""
import random
import json

def _q(topic, diff, question, choices, answer_idx, explanation, grade=2):
    return ('Social Studies', topic, diff, question, json.dumps(choices), answer_idx, explanation, grade)

def _shuffle_choices(correct, wrongs, rng):
    choices = list(rng.sample(wrongs, min(3, len(wrongs))))
    idx = rng.randint(0, min(3, len(choices)))
    choices.insert(idx, correct)
    return choices[:4], idx


def gen_community_citizenship(n=25, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What is a community?", "A group of people who live and work in the same area",
         ["A type of government", "A country", "A school building"],
         "Communities can be neighborhoods, towns, or cities where people share resources.", 'easy', 1),
        ("What does it mean to be a good citizen?",
         "Following rules, helping others, and being responsible",
         ["Doing whatever you want", "Ignoring rules", "Only helping yourself"],
         "Good citizens contribute positively to their community.", 'easy', 1),
        ("What is a community helper?", "Someone whose job helps people in the community",
         ["Someone who only works at school", "A family member", "A type of building"],
         "Firefighters, doctors, teachers, and police officers are community helpers.", 'easy', 1),
        ("Why are rules important?", "They keep people safe and treat everyone fairly",
         ["They are only for children", "They are not important", "They only exist at school"],
         "Rules create order and protect people's rights and safety.", 'easy', 1),
        ("What is a responsibility?", "Something you are supposed to do or take care of",
         ["A fun activity", "A type of reward", "Something you choose not to do"],
         "Responsibilities include chores at home, following rules at school, and helping others.", 'easy', 2),
        ("What is a right?", "Something you are allowed to do or have",
         ["Something you must do", "A type of punishment", "A rule at school only"],
         "Rights include freedom of speech, religion, and education.", 'medium', 3),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Community & Citizenship', diff, q_text, choices, idx,
                     f"Correct: {ans}.", grade))
    return qs


def gen_maps_geography_elem(n=30, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What is a map?", "A drawing that shows what a place looks like from above",
         ["A type of photograph", "A list of directions", "A story about a place"],
         "Maps are flat representations of places, showing features like roads, rivers, and cities.", 'easy', 1),
        ("What is a compass rose?", "A symbol on a map that shows directions (N, S, E, W)",
         ["A type of flower", "A legend on a map", "A scale on a map"],
         "The compass rose shows North, South, East, and West on a map.", 'easy', 1),
        ("What is a map legend (key)?",
         "A list explaining what symbols on a map mean",
         ["The title of a map", "The compass on a map", "A map scale"],
         "The legend tells you what colors and symbols represent on a map.", 'easy', 2),
        ("What is a continent?", "One of the seven large landmasses on Earth",
         ["A type of country", "An ocean", "A city"],
         "The 7 continents: Asia, Africa, North America, South America, Antarctica, Europe, Australia.", 'easy', 2),
        ("How many continents are there on Earth?", "7",
         ["5", "6", "8"],
         "The 7 continents are Asia, Africa, North America, South America, Antarctica, Europe, and Australia.", 'easy', 2),
        ("What are the four cardinal directions?", "North, South, East, West",
         ["Up, Down, Left, Right", "Near, Far, Above, Below", "Forward, Backward, Left, Right"],
         "Cardinal directions help us find locations on a map.", 'easy', 1),
        ("What is a globe?", "A round model of Earth",
         ["A flat map", "A type of clock", "A weather tool"],
         "A globe accurately shows Earth's shape, unlike flat maps which distort shapes and sizes.", 'easy', 1),
        ("What is the capital of the United States?", "Washington, D.C.",
         ["New York City", "Los Angeles", "Chicago"],
         "Washington, D.C. is the capital where the President lives and Congress meets.", 'easy', 2),
        ("What ocean is on the East Coast of the United States?",
         "Atlantic Ocean", ["Pacific Ocean", "Indian Ocean", "Arctic Ocean"],
         "The Atlantic Ocean borders the East Coast; the Pacific Ocean borders the West Coast.", 'easy', 3),
        ("What are the two largest states in the United States?",
         "Alaska and Texas",
         ["California and Florida", "Texas and California", "Alaska and Montana"],
         "Alaska is the largest state; Texas is the second largest.", 'medium', 4),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Maps & Geography', diff, q_text, choices, idx,
                     f"Correct: {ans}.", grade))
    return qs


def gen_american_symbols(n=25, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What do the stars on the American flag represent?",
         "The 50 states",
         ["The 13 original colonies", "The number of wars fought", "The states that won the Civil War"],
         "There are 50 stars — one for each state in the United States.", 'easy', 1),
        ("What do the stripes on the American flag represent?",
         "The 13 original colonies",
         ["The 50 states", "The number of presidents", "The years since independence"],
         "There are 13 stripes — one for each of the original 13 colonies.", 'easy', 2),
        ("What is the Statue of Liberty a symbol of?",
         "Freedom and democracy",
         ["Military strength", "Wealth", "Education"],
         "The Statue of Liberty was a gift from France and symbolizes freedom.", 'easy', 2),
        ("When is Independence Day celebrated?", "July 4th",
         ["July 14th", "September 4th", "December 4th"],
         "July 4, 1776 is when the Declaration of Independence was adopted.", 'easy', 2),
        ("What is the national anthem of the United States?",
         "The Star-Spangled Banner",
         ["America the Beautiful", "My Country 'Tis of Thee", "Yankee Doodle"],
         "The Star-Spangled Banner was written by Francis Scott Key during the War of 1812.", 'easy', 3),
        ("What is the Pledge of Allegiance?",
         "A promise of loyalty to the United States flag and country",
         ["A song about America", "A type of law", "A prayer"],
         "The Pledge is said facing the flag, with hand over heart.", 'easy', 2),
        ("Who was the first President of the United States?",
         "George Washington",
         ["Abraham Lincoln", "Thomas Jefferson", "Benjamin Franklin"],
         "George Washington served as the 1st President from 1789 to 1797.", 'easy', 2),
        ("What do we celebrate on Thanksgiving?",
         "Giving thanks and remembering the feast shared by Pilgrims and Wampanoag people",
         ["Independence from Britain", "The end of a war", "The birth of George Washington"],
         "Thanksgiving is celebrated on the fourth Thursday of November.", 'easy', 2),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('American Symbols & Holidays', diff, q_text, choices, idx,
                     f"Correct: {ans}.", grade))
    return qs


def gen_government_elem(n=20, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("Who is in charge of the United States?",
         "The President",
         ["The mayor", "The governor", "A king"],
         "The President leads the country's government from Washington, D.C.", 'easy', 2),
        ("What do we call the leader of a city?", "Mayor",
         ["President", "Governor", "Senator"],
         "Mayors lead city governments. Governors lead states. The President leads the nation.", 'easy', 2),
        ("What do we call the leader of a state?", "Governor",
         ["Mayor", "President", "Senator"],
         "Each of the 50 states has a governor elected by its citizens.", 'easy', 3),
        ("What is a vote?", "A way citizens choose their leaders or make decisions",
         ["A type of law", "A school activity", "A type of tax"],
         "Voting is a key right and responsibility in a democracy.", 'easy', 2),
        ("What is democracy?", "A system where people choose their leaders by voting",
         ["A country ruled by a king", "A type of religion", "A school subject"],
         "In a democracy, the government gets its power from the people.", 'medium', 3),
        ("What are the three branches of US government?",
         "Executive, Legislative, Judicial",
         ["President, Senate, Police", "Local, State, National",
          "Laws, Rules, Guidelines"],
         "The three branches balance power: Executive (enforces), Legislative (makes laws), Judicial (interprets).", 'medium', 5),
        ("What does Congress do?", "Makes the laws for the United States",
         ["Enforces the laws", "Interprets the laws", "Leads the military"],
         "Congress is the legislative branch — it is made up of the Senate and House of Representatives.", 'medium', 5),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Government Basics', diff, q_text, choices, idx,
                     f"Correct: {ans}.", grade))
    return qs


_TOPIC_GENERATORS = {
    'Community & Citizenship':      [(gen_community_citizenship, {})],
    'Maps & Geography':             [(gen_maps_geography_elem, {})],
    'American Symbols & Holidays':  [(gen_american_symbols, {})],
    'Government Basics':            [(gen_government_elem, {})],
}

_DIFF_WEIGHTS = {t: {'easy': [fn], 'medium': [fn], 'hard': [fn]}
                 for t, [(fn, _)] in _TOPIC_GENERATORS.items()}


def generate_for_topic(topic, difficulty='medium', count=10, seed=None):
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
    return [{'id': -(i+1), 'subject': row[0], 'topic': row[1], 'difficulty': row[2],
             'question': row[3], 'choices': json.loads(row[4]), 'answer': row[5],
             'explanation': row[6]} for i, row in enumerate(pool[:count])]


def generate_all(seed=42):
    r = random.Random(seed)
    all_qs = []
    for fns in _TOPIC_GENERATORS.values():
        for fn, kwargs in fns:
            all_qs.extend(fn(seed=r.randint(0, 999999), n=25))
    return all_qs
