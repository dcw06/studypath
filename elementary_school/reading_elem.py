"""
Elementary School Reading & Language Arts Generator (K–5)
Covers: Phonics, Sight Words, Vocabulary, Grammar, Reading Comprehension,
        Sentence Structure, Capitalization & Punctuation
"""
import random
import json

def _q(topic, diff, question, choices, answer_idx, explanation, grade=2):
    return ('Language', topic, diff, question, json.dumps(choices), answer_idx, explanation, grade)

def _shuffle_choices(correct, wrongs, rng):
    choices = list(rng.sample(wrongs, min(3, len(wrongs))))
    idx = rng.randint(0, min(3, len(choices)))
    choices.insert(idx, correct)
    return choices[:4], idx


def gen_phonics(n=40, seed=None):
    """Letter sounds and CVC words (K–1)."""
    r = random.Random(seed)
    pairs = [
        ("cat", "c", ["b", "d", "p"]),
        ("dog", "d", ["b", "h", "f"]),
        ("hat", "h", ["b", "m", "s"]),
        ("pig", "p", ["b", "d", "t"]),
        ("sun", "s", ["b", "r", "m"]),
        ("run", "r", ["b", "d", "s"]),
        ("map", "m", ["n", "b", "t"]),
        ("big", "b", ["d", "p", "r"]),
        ("top", "t", ["b", "d", "p"]),
        ("fox", "f", ["b", "d", "s"]),
        ("net", "n", ["b", "m", "s"]),
        ("leg", "l", ["b", "d", "p"]),
        ("wig", "w", ["b", "d", "s"]),
        ("zip", "z", ["b", "d", "s"]),
        ("cup", "c", ["b", "d", "p"]),
    ]
    qs = []
    for _ in range(n):
        word, sound, wrong_sounds = r.choice(pairs)
        ans = sound
        wrongs = r.sample(wrong_sounds, min(3, len(wrong_sounds)))
        choices, idx = _shuffle_choices(ans, wrongs, r)
        qs.append(_q('Phonics', 'easy',
                     f"What sound does the word '{word}' begin with?",
                     choices, idx,
                     f"'{word}' starts with the letter '{sound}', which makes the /{sound}/ sound.", 0))
    return qs


def gen_sight_words(n=40, seed=None):
    """High-frequency sight word recognition (K–2)."""
    r = random.Random(seed)
    pools = [
        ("the", "Which word means 'the'?", ["a", "an", "is"]),
        ("and", "Complete: cat ___ dog", ["or", "but", "not"]),
        ("is", "Which word shows something exists?", ["are", "was", "be"]),
        ("in", "The cat is ___ the box.", ["on", "at", "by"]),
        ("you", "Who am I talking to? I am talking to ___.", ["me", "him", "her"]),
        ("that", "Look at ___ bird over there.", ["this", "those", "these"]),
        ("he", "A boy is called ___.", ["she", "they", "it"]),
        ("was", "Yesterday it ___ sunny.", ["is", "are", "be"]),
        ("for", "This gift is ___ you.", ["to", "at", "of"]),
        ("on", "The book is ___ the table.", ["in", "at", "by"]),
        ("are", "They ___ happy.", ["is", "was", "be"]),
        ("have", "I ___ two cats.", ["has", "had", "be"]),
        ("said", "She ___ hello.", ["told", "spoke", "yelled"]),
        ("with", "Come ___ me.", ["by", "at", "to"]),
        ("his", "That is ___ hat.", ["her", "my", "our"]),
    ]
    qs = []
    for _ in range(n):
        ans, q_text, wrongs = r.choice(pools)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Sight Words', 'easy', q_text, choices, idx,
                     f"The correct word is '{ans}'.", 1))
    return qs


def gen_vocabulary(n=50, seed=None):
    """Grade-appropriate vocabulary and word meaning (Grade 2–5)."""
    r = random.Random(seed)
    vocab = [
        ("enormous", "very big", ["tiny", "fast", "blue"], 2),
        ("brave", "not afraid", ["shy", "lazy", "sick"], 2),
        ("ancient", "very old", ["new", "fast", "small"], 3),
        ("fragile", "easily broken", ["strong", "heavy", "warm"], 3),
        ("transparent", "see-through", ["opaque", "heavy", "loud"], 4),
        ("migrate", "move from one place to another", ["stay", "shrink", "freeze"], 4),
        ("abundant", "more than enough", ["scarce", "tiny", "cold"], 4),
        ("compassion", "deep sympathy for others", ["anger", "speed", "height"], 5),
        ("persevere", "keep trying despite difficulty", ["quit", "ignore", "forget"], 5),
        ("predict", "guess what will happen", ["remember", "forget", "explain"], 3),
        ("summarize", "give the main points briefly", ["expand", "memorize", "ignore"], 4),
        ("evidence", "proof or facts", ["opinion", "feeling", "guess"], 4),
        ("conclusion", "final decision based on facts", ["beginning", "middle", "question"], 5),
        ("fiction", "a made-up story", ["fact", "history", "science"], 3),
        ("synonym", "a word with the same meaning", ["antonym", "homophone", "prefix"], 4),
        ("antonym", "a word with the opposite meaning", ["synonym", "rhyme", "prefix"], 4),
        ("noun", "a person, place, or thing", ["verb", "adjective", "adverb"], 2),
        ("verb", "an action word", ["noun", "adjective", "pronoun"], 2),
        ("adjective", "a word that describes a noun", ["verb", "noun", "adverb"], 3),
        ("metaphor", "saying something IS something else", ["simile", "rhyme", "alliteration"], 5),
    ]
    qs = []
    for _ in range(n):
        word, definition, wrongs, grade = r.choice(vocab)
        qtype = r.choice(['define', 'identify'])
        if qtype == 'define':
            q_text = f"What does the word '{word}' mean?"
            ans = definition
            wrong_choices = r.sample(wrongs, min(3, len(wrongs)))
        else:
            q_text = f"Which word means '{definition}'?"
            ans = word
            other_words = [v[0] for v in vocab if v[0] != word and v[3] == grade]
            wrong_choices = r.sample(other_words, min(3, len(other_words))) if other_words else wrongs
        choices, idx = _shuffle_choices(ans, wrong_choices[:3], r)
        qs.append(_q('Vocabulary', 'medium' if grade <= 3 else 'hard', q_text, choices, idx,
                     f"'{word}' means {definition}.", grade))
    return qs


def gen_grammar_basic(n=50, seed=None):
    """Parts of speech, punctuation, capitalization (Grade 1–5)."""
    r = random.Random(seed)
    qs = []
    grammar_qs = [
        # (question, answer, wrongs, explanation, grade, diff)
        ("Which word is a noun? 'The happy dog runs fast.'",
         "dog", ["happy", "runs", "fast"], "A noun is a person, place, or thing. 'Dog' is a thing.", 2, 'easy'),
        ("Which word is a verb? 'She quickly eats an apple.'",
         "eats", ["quickly", "she", "apple"], "A verb is an action word. 'Eats' is the action.", 2, 'easy'),
        ("Which sentence has correct capitalization?",
         "My name is Emma.", ["my name is emma.", "My name Is Emma.", "my Name is Emma."],
         "Sentences start with a capital letter, and names are capitalized.", 1, 'easy'),
        ("Which sentence has correct punctuation?",
         "Is that your dog?", ["Is that your dog.", "Is that your dog", "is that your dog?"],
         "Questions end with a question mark.", 2, 'easy'),
        ("What punctuation ends a statement?",
         "Period (.)", ["Question mark (?)", "Exclamation mark (!)", "Comma (,)"],
         "Statements (telling sentences) end with a period.", 1, 'easy'),
        ("Which word is an adjective? 'The small, brown fox jumped.'",
         "small", ["fox", "jumped", "the"], "An adjective describes a noun. 'Small' describes the fox.", 3, 'medium'),
        ("Which is the correct plural of 'child'?",
         "children", ["childs", "childes", "childrens"], "'Child' has an irregular plural: 'children'.", 3, 'medium'),
        ("Which sentence uses correct subject-verb agreement?",
         "The dogs run fast.", ["The dogs runs fast.", "The dogs running fast.", "The dogs is running."],
         "Plural subjects take plural verbs: 'dogs run' not 'dogs runs'.", 3, 'medium'),
        ("What is the past tense of 'run'?",
         "ran", ["runned", "running", "runs"], "'Run' is an irregular verb. Past tense is 'ran'.", 3, 'medium'),
        ("Which word is an adverb? 'She quietly read her book.'",
         "quietly", ["she", "read", "book"], "An adverb modifies a verb. 'Quietly' tells how she read.", 4, 'medium'),
        ("Which sentence uses a comma correctly?",
         "I have a cat, a dog, and a fish.",
         ["I have, a cat a dog and a fish.", "I have a cat a dog, and a fish.", "I have a cat a dog and, a fish."],
         "Commas separate items in a list.", 4, 'medium'),
        ("A pronoun replaces which part of speech?",
         "Noun", ["Verb", "Adjective", "Adverb"], "Pronouns (he, she, it, they) replace nouns.", 3, 'medium'),
        ("Which is a compound sentence?",
         "I like cats, and she likes dogs.",
         ["I like cats.", "Because I like cats.", "I like cats and dogs."],
         "A compound sentence joins two independent clauses with a conjunction.", 5, 'hard'),
        ("What is the main idea of a paragraph?",
         "The most important point the author is making",
         ["The first sentence", "The last sentence", "Every detail mentioned"],
         "The main idea is the central message — not just one detail.", 4, 'medium'),
        ("Which sentence uses an apostrophe correctly?",
         "That is Sara's book.", ["That is Saras' book.", "That is sara's book.", "That is Sara book."],
         "Use 's after a name to show possession.", 3, 'medium'),
    ]
    for _ in range(n):
        q_text, ans, wrongs, expl, grade, diff = r.choice(grammar_qs)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Grammar', diff, q_text, choices, idx, expl, grade))
    return qs


def gen_reading_comprehension_elem(n=40, seed=None):
    """Reading comprehension: main idea, inference, detail (Grade 2–5)."""
    r = random.Random(seed)
    passages = [
        {
            "text": "Bears are large mammals. They sleep through the winter in a process called hibernation. During hibernation, they do not eat or drink. Bears eat a lot of food in fall to prepare.",
            "questions": [
                ("What do bears do in winter?", "Hibernate", ["Migrate south", "Hunt for food", "Swim"], "The passage says bears sleep through winter — this is called hibernation.", 'easy', 3),
                ("Why do bears eat a lot in fall?", "To prepare for hibernation", ["Because fall food tastes better", "To share with other animals", "To grow taller"], "They eat a lot in fall to have energy stored for winter hibernation.", 'medium', 4),
            ]
        },
        {
            "text": "The water cycle has four steps: evaporation, condensation, precipitation, and collection. Water evaporates from oceans and lakes. It forms clouds. Then it falls as rain or snow.",
            "questions": [
                ("What is the first step of the water cycle?", "Evaporation", ["Condensation", "Precipitation", "Collection"], "The passage lists evaporation as the first step.", 'easy', 3),
                ("Where does evaporation happen?", "Oceans and lakes", ["Clouds", "Rain", "Mountains"], "The passage says 'Water evaporates from oceans and lakes.'", 'medium', 4),
            ]
        },
        {
            "text": "The library is a special place. You can borrow books for free. There are books about every topic you can imagine. You need a library card to borrow books.",
            "questions": [
                ("What do you need to borrow books?", "A library card", ["Money", "A teacher", "Your own book"], "The passage states you need a library card to borrow books.", 'easy', 2),
                ("What is the best title for this passage?", "All About the Library", ["How to Read Fast", "Types of Books", "Going to School"], "The whole passage is about what the library is and how it works.", 'medium', 3),
            ]
        },
    ]
    qs = []
    for _ in range(n):
        passage = r.choice(passages)
        q_text_full, ans, wrongs, expl, diff, grade = r.choice(passage["questions"])
        full_q = f"Read the passage:\n\"{passage['text']}\"\n\n{q_text_full}"
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Reading Comprehension', diff, full_q, choices, idx, expl, grade))
    return qs


_TOPIC_GENERATORS = {
    'Phonics':               [(gen_phonics, {})],
    'Sight Words':           [(gen_sight_words, {})],
    'Vocabulary':            [(gen_vocabulary, {})],
    'Grammar':               [(gen_grammar_basic, {})],
    'Reading Comprehension': [(gen_reading_comprehension_elem, {})],
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
            all_qs.extend(fn(seed=r.randint(0, 999999), n=40))
    return all_qs
