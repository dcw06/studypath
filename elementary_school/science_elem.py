"""
Elementary School Science Generator (K–5)
Covers: Living vs Non-Living, Basic Needs, Weather, 5 Senses,
        Animal Groups, Plant Parts, Life Cycles, States of Matter,
        Forces, Ecosystems, Earth Science, Scientific Method
"""
import random
import json

def _q(topic, diff, question, choices, answer_idx, explanation, grade=2):
    return ('Science', topic, diff, question, json.dumps(choices), answer_idx, explanation, grade)

def _shuffle_choices(correct, wrongs, rng):
    choices = list(rng.sample(wrongs, min(3, len(wrongs))))
    idx = rng.randint(0, min(3, len(choices)))
    choices.insert(idx, correct)
    return choices[:4], idx


def gen_living_nonliving(n=30, seed=None):
    r = random.Random(seed)
    items = [
        ("dog", "living", ["rock", "car", "cloud"]),
        ("tree", "living", ["chair", "water", "sand"]),
        ("rock", "non-living", ["bird", "fish", "flower"]),
        ("car", "non-living", ["cat", "worm", "grass"]),
        ("flower", "living", ["book", "lamp", "pencil"]),
        ("cloud", "non-living", ["rabbit", "mushroom", "oak tree"]),
        ("bacteria", "living", ["plastic", "metal", "glass"]),
        ("river", "non-living", ["frog", "duck", "algae"]),
        ("mushroom", "living", ["stone", "sand", "snow"]),
        ("pencil", "non-living", ["spider", "ant", "moss"]),
    ]
    qs = []
    for _ in range(n):
        item, category, wrongs_items = r.choice(items)
        q_text = f"Is a '{item}' living or non-living?"
        ans = category
        wrongs = ["living" if category == "non-living" else "non-living",
                  "both living and non-living", "it depends"]
        choices, idx = _shuffle_choices(ans, wrongs[:3], r)
        qs.append(_q('Living vs Non-Living', 'easy', q_text, choices, idx,
                     f"A {item} is {category}. Living things grow, respond, and reproduce.", 0))
    return qs


def gen_basic_needs(n=25, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What do plants need to make food?", "Sunlight", ["Darkness", "Salt", "Rocks"],
         "Plants use sunlight, water, and air to make food through photosynthesis.", 'easy', 1),
        ("Which basic need do all living things share?", "Water", ["Television", "Clothing", "Books"],
         "All living things need water to survive.", 'easy', 1),
        ("What gas do humans need to breathe?", "Oxygen", ["Carbon dioxide", "Nitrogen", "Helium"],
         "Humans breathe in oxygen and breathe out carbon dioxide.", 'easy', 1),
        ("What do plants use to make their own food?", "Sunlight, water, and air",
         ["Soil, rocks, and sand", "Rain, wind, and snow", "Insects and animals"],
         "Photosynthesis requires sunlight, water, and carbon dioxide from air.", 'medium', 2),
        ("Which is NOT a basic need of animals?", "Shelter from TV",
         ["Food", "Water", "Air"], "TV is not a basic need. Animals need food, water, air, and shelter.", 'easy', 1),
        ("Why do animals eat food?", "To get energy", ["To get bigger quickly", "To attract mates", "To make water"],
         "Food provides energy for living things to move, grow, and survive.", 'easy', 2),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, expl, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Basic Needs', diff, q_text, choices, idx, expl, grade))
    return qs


def gen_weather(n=30, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What tool measures temperature?", "Thermometer", ["Ruler", "Scale", "Compass"],
         "A thermometer measures how hot or cold it is.", 'easy', 1),
        ("What is precipitation?", "Water falling from clouds", ["Wind speed", "Air temperature", "Cloud color"],
         "Precipitation includes rain, snow, sleet, and hail — water falling from clouds.", 'medium', 3),
        ("Which type of cloud is flat and dark, often bringing rain?", "Stratus", ["Cumulus", "Cirrus", "Nimbus"],
         "Stratus clouds are low, flat, and gray — they often bring drizzle or rain.", 'hard', 4),
        ("What causes wind?", "Differences in air pressure", ["The moon pulling air", "Clouds moving", "Rain evaporating"],
         "Wind is caused by air moving from high-pressure areas to low-pressure areas.", 'hard', 5),
        ("What is the water cycle?", "The continuous movement of water through nature",
         ["Rainfall only", "Just evaporation", "Only ocean currents"],
         "The water cycle includes evaporation, condensation, precipitation, and collection.", 'medium', 4),
        ("What season comes after winter?", "Spring", ["Summer", "Fall", "Autumn"],
         "The seasons go: Winter → Spring → Summer → Fall.", 'easy', 1),
        ("What do we call a severe storm with thunder and lightning?", "Thunderstorm",
         ["Blizzard", "Hurricane", "Tornado"],
         "A thunderstorm has both thunder (sound) and lightning (electrical discharge).", 'medium', 3),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, expl, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Weather', diff, q_text, choices, idx, expl, grade))
    return qs


def gen_animal_groups(n=30, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("Which group does a dog belong to?", "Mammals", ["Birds", "Reptiles", "Amphibians"],
         "Dogs are mammals — they have fur, are warm-blooded, and nurse their young.", 'easy', 1),
        ("Which animal is a reptile?", "Lizard", ["Frog", "Eagle", "Salmon"],
         "Lizards are reptiles — cold-blooded with dry, scaly skin.", 'easy', 2),
        ("What makes mammals unique?", "They nurse young with milk",
         ["They lay eggs", "They have scales", "They breathe underwater"],
         "Mammals produce milk to feed their young.", 'medium', 2),
        ("Which is an amphibian?", "Frog", ["Snake", "Hawk", "Salmon"],
         "Frogs are amphibians — they live in water and on land and have moist skin.", 'medium', 2),
        ("How do birds stay warm?", "Feathers", ["Scales", "Fur", "Slime"],
         "Birds are covered in feathers which provide insulation and enable flight.", 'easy', 2),
        ("Which animal is a fish?", "Salmon", ["Whale", "Dolphin", "Penguin"],
         "Salmon are fish — they breathe through gills and live their whole lives in water.", 'medium', 3),
        ("What is a characteristic of insects?", "6 legs", ["4 legs", "8 legs", "10 legs"],
         "Insects always have exactly 6 legs and 3 body segments.", 'easy', 2),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, expl, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Animal Groups', diff, q_text, choices, idx, expl, grade))
    return qs


def gen_plant_parts(n=25, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What part of a plant absorbs water from the soil?", "Roots",
         ["Leaves", "Stem", "Flower"], "Roots anchor the plant and absorb water and minerals from soil.", 'easy', 1),
        ("What part of a plant makes food using sunlight?", "Leaves",
         ["Roots", "Stem", "Seeds"], "Leaves contain chlorophyll and carry out photosynthesis.", 'easy', 2),
        ("What is the function of the stem?", "Carries water to leaves",
         ["Makes seeds", "Absorbs sunlight", "Absorbs water from soil"],
         "The stem acts as a pipeline, transporting water and nutrients between roots and leaves.", 'medium', 3),
        ("What part of a flower becomes the fruit?", "The ovary",
         ["The petal", "The stem", "The roots"],
         "After fertilization, the ovary develops into a fruit containing seeds.", 'hard', 5),
        ("What do seeds need to germinate?", "Water, warmth, and oxygen",
         ["Sunlight, sand, and cold", "Soil, light, and salt", "Wind, ice, and nutrients"],
         "Seeds germinate (sprout) when they have enough water, warmth, and oxygen.", 'medium', 4),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, expl, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Plant Parts', diff, q_text, choices, idx, expl, grade))
    return qs


def gen_states_of_matter(n=30, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("Which state of matter has a definite shape?", "Solid",
         ["Liquid", "Gas", "Plasma"], "Solids have a fixed shape and volume.", 'easy', 2),
        ("What happens to water when it freezes?", "It becomes a solid",
         ["It becomes a gas", "It disappears", "It becomes heavier"],
         "Water (liquid) → ice (solid) when cooled below 0°C.", 'easy', 2),
        ("What is it called when a liquid becomes a gas?", "Evaporation",
         ["Condensation", "Freezing", "Melting"],
         "Evaporation is when liquid water turns into water vapor (gas).", 'medium', 3),
        ("What state of matter takes the shape of its container?", "Liquid",
         ["Solid", "Gas", "All of them"], "Liquids flow and take the shape of whatever holds them.", 'easy', 2),
        ("What is it called when steam (gas) turns back into water (liquid)?", "Condensation",
         ["Evaporation", "Freezing", "Melting"],
         "Condensation is gas → liquid. You see it on a cold glass.", 'medium', 4),
        ("Ice → water is an example of:", "Melting",
         ["Freezing", "Evaporation", "Condensation"],
         "When a solid warms up and becomes liquid, it melts.", 'easy', 3),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, expl, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('States of Matter', diff, q_text, choices, idx, expl, grade))
    return qs


def gen_forces_motion(n=25, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What is a force?", "A push or pull", ["A type of energy", "A living thing", "A type of matter"],
         "A force is any push or pull that can change an object's motion.", 'easy', 3),
        ("What force pulls objects toward the Earth?", "Gravity",
         ["Friction", "Magnetism", "Electricity"],
         "Gravity is the force that pulls objects toward the center of the Earth.", 'easy', 3),
        ("What force slows down a sliding book?", "Friction",
         ["Gravity", "Magnetism", "Wind"],
         "Friction is the force that resists motion when two surfaces rub together.", 'medium', 4),
        ("If you push a box harder, what happens?", "It moves faster or farther",
         ["It slows down", "Nothing changes", "It gets heavier"],
         "A stronger force causes greater acceleration or movement.", 'medium', 4),
        ("What simple machine makes it easier to lift heavy objects?", "Ramp (inclined plane)",
         ["Wheel", "Lever", "Pulley"],
         "Inclined planes (ramps) spread the effort over a longer distance, reducing needed force.", 'hard', 5),
        ("What happens to an object at rest if no force acts on it?", "It stays at rest",
         ["It starts moving", "It falls down", "It disappears"],
         "Newton's 1st Law: objects at rest stay at rest unless acted on by a force.", 'hard', 5),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, expl, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Forces & Motion', diff, q_text, choices, idx, expl, grade))
    return qs


_TOPIC_GENERATORS = {
    'Living vs Non-Living': [(gen_living_nonliving, {})],
    'Basic Needs':          [(gen_basic_needs, {})],
    'Weather':              [(gen_weather, {})],
    'Animal Groups':        [(gen_animal_groups, {})],
    'Plant Parts':          [(gen_plant_parts, {})],
    'States of Matter':     [(gen_states_of_matter, {})],
    'Forces & Motion':      [(gen_forces_motion, {})],
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
            all_qs.extend(fn(seed=r.randint(0, 999999), n=30))
    return all_qs
