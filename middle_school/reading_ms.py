"""
Middle School Reading & Language Arts Generator (Grades 6–8)
Covers: Reading Comprehension, Vocabulary, Grammar & Usage,
        Literary Analysis, Writing Skills, Figurative Language
"""
import random
import json

def _q(topic, diff, question, choices, answer_idx, explanation, grade=7):
    return ('Language', topic, diff, question, json.dumps(choices), answer_idx, explanation, grade)

def _shuffle_choices(correct, wrongs, rng):
    choices = list(rng.sample(wrongs, min(3, len(wrongs))))
    idx = rng.randint(0, min(3, len(choices)))
    choices.insert(idx, correct)
    return choices[:4], idx


def gen_vocabulary_ms(n=50, seed=None):
    r = random.Random(seed)
    vocab = [
        ("ambiguous", "having more than one possible meaning", ["clear", "simple", "obvious"], 6),
        ("benevolent", "kind and generous", ["cruel", "selfish", "harsh"], 6),
        ("circumvent", "find a way around an obstacle", ["face directly", "ignore", "destroy"], 7),
        ("diligent", "showing persistent effort", ["lazy", "careless", "hasty"], 6),
        ("eloquent", "fluent and persuasive in speech", ["silent", "mumbling", "confused"], 7),
        ("formidable", "inspiring fear or respect by being impressive", ["weak", "ordinary", "friendly"], 7),
        ("hypocrite", "someone who pretends to have virtues they lack", ["honest person", "brave person", "kind person"], 8),
        ("inevitable", "certain to happen; unavoidable", ["preventable", "unlikely", "optional"], 7),
        ("jurisdiction", "the authority to make legal decisions", ["ignorance", "confusion", "weakness"], 8),
        ("lethargic", "lacking energy; sluggish", ["energetic", "alert", "active"], 7),
        ("meticulous", "showing extreme care about details", ["careless", "hasty", "rough"], 8),
        ("nonchalant", "casually calm and relaxed", ["anxious", "excited", "nervous"], 8),
        ("ominous", "giving a warning of something bad", ["promising", "cheerful", "harmless"], 7),
        ("perseverance", "continuing despite difficulty", ["giving up", "laziness", "avoiding"], 6),
        ("scrutinize", "examine carefully and critically", ["ignore", "glance at", "overlook"], 8),
        ("tenacious", "holding firmly; not giving up", ["yielding", "weak", "indifferent"], 8),
        ("ubiquitous", "present everywhere", ["rare", "absent", "hidden"], 8),
        ("vehement", "showing strong feeling; forceful", ["mild", "calm", "indifferent"], 8),
        ("wary", "cautious about possible dangers", ["reckless", "trusting", "careless"], 6),
        ("zealous", "having great energy or enthusiasm", ["apathetic", "bored", "reluctant"], 7),
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
            wrong_choices = r.sample(other_words, min(3, len(other_words))) if len(other_words) >= 3 else wrongs
        choices, idx = _shuffle_choices(ans, wrong_choices[:3], r)
        diff = 'easy' if grade == 6 else ('medium' if grade == 7 else 'hard')
        qs.append(_q('Vocabulary', diff, q_text, choices, idx,
                     f"'{word}' means: {definition}.", grade))
    return qs


def gen_grammar_ms(n=50, seed=None):
    r = random.Random(seed)
    grammar_qs = [
        ("Which sentence uses a semicolon correctly?",
         "I love hiking; my sister prefers swimming.",
         ["I love hiking; but my sister prefers swimming.",
          "I love hiking, my sister; prefers swimming.",
          "I; love hiking my sister prefers swimming."],
         "A semicolon joins two independent clauses without a conjunction.", 7, 'medium'),
        ("Which sentence contains a misplaced modifier?",
         "Running down the street, the dog chased the boy.",
         ["The dog, running down the street, chased the boy.",
          "The dog chased the boy who was running down the street.",
          "Running fast, the boy was chased by the dog."],
         "In the incorrect sentence, 'Running down the street' seems to modify 'the dog' but should modify 'the boy'.", 8, 'hard'),
        ("Which sentence uses the correct form of 'lie' vs 'lay'?",
         "I will lie down after lunch.",
         ["I will lay down after lunch.",
          "I lied down yesterday.",
          "I laid myself down to rest."],
         "'Lie' means to recline (no object). 'Lay' requires a direct object.", 8, 'hard'),
        ("Which word is a subordinating conjunction?",
         "although",
         ["and", "but", "or"],
         "Subordinating conjunctions (although, because, since, while) begin dependent clauses.", 7, 'medium'),
        ("Which sentence is in active voice?",
         "The chef prepared a delicious meal.",
         ["A delicious meal was prepared by the chef.",
          "The meal was being prepared.",
          "The preparation of the meal was done."],
         "Active voice: subject performs the action. Passive voice: subject receives the action.", 7, 'medium'),
        ("What is the function of a dependent clause?",
         "It cannot stand alone as a complete sentence",
         ["It expresses a complete thought",
          "It has no verb",
          "It begins with a coordinating conjunction"],
         "A dependent clause has a subject and verb but begins with a subordinator, making it incomplete alone.", 7, 'medium'),
        ("Which sentence uses commas correctly with a nonrestrictive clause?",
         "My brother, who lives in Denver, is visiting next week.",
         ["My brother who lives in Denver, is visiting next week.",
          "My brother who lives in Denver is visiting next week.",
          "My, brother who lives in Denver is visiting, next week."],
         "Nonrestrictive clauses (extra info) are set off by commas on both sides.", 8, 'hard'),
        ("Which is an example of parallel structure?",
         "She likes hiking, swimming, and cycling.",
         ["She likes hiking, to swim, and goes cycling.",
          "She likes to hike, swimming, and the sport of cycling.",
          "Hiking, she swims, and cycling is what she likes."],
         "Parallel structure means all items in a list use the same grammatical form.", 8, 'hard'),
        ("What does the prefix 'inter-' mean?",
         "between or among",
         ["within", "against", "before"],
         "Inter- = between (international, interact, interconnect).", 6, 'easy'),
        ("What does the suffix '-ology' mean?",
         "the study of",
         ["the fear of", "the love of", "the practice of"],
         "-ology means the study of (biology, geology, psychology).", 6, 'easy'),
        ("Which sentence uses an appositive correctly?",
         "My teacher, Ms. Johnson, is very helpful.",
         ["My teacher Ms. Johnson is very helpful.",
          "Ms. Johnson my teacher is very helpful.",
          "My teacher is Ms. Johnson very helpful."],
         "An appositive renames the noun before it and is set off by commas.", 7, 'medium'),
        ("Which type of phrase is underlined: 'Running quickly, she caught the bus'?",
         "Participial phrase",
         ["Prepositional phrase", "Infinitive phrase", "Gerund phrase"],
         "A participial phrase begins with a participle (-ing or -ed form) and modifies a noun.", 8, 'hard'),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, expl, grade, diff = r.choice(grammar_qs)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Grammar', diff, q_text, choices, idx, expl, grade))
    return qs


def gen_literary_analysis(n=40, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What is the theme of a story?", "The central message or lesson",
         ["The setting of the story", "The main character's name", "The sequence of events"],
         "Theme is the underlying message or insight about life the author conveys.", 'medium', 6),
        ("What is the difference between plot and theme?",
         "Plot is what happens; theme is the message",
         ["They are the same thing", "Theme is what happens; plot is the message",
          "Plot is the setting; theme is the character"],
         "Plot = sequence of events. Theme = the deeper meaning or lesson.", 'medium', 7),
        ("Which point of view uses 'I' and 'we'?", "First person",
         ["Second person", "Third person limited", "Third person omniscient"],
         "First-person narration uses 'I' — the narrator is a character in the story.", 'easy', 6),
        ("What is 'dramatic irony'?",
         "When the audience knows something the characters don't",
         ["When a character says the opposite of what they mean",
          "When events turn out the opposite of what was expected",
          "When two characters disagree"],
         "Dramatic irony creates tension because readers know something characters don't.", 'hard', 8),
        ("What is the rising action of a story?",
         "Events building toward the climax",
         ["The highest point of tension", "The resolution of the conflict",
          "The opening scene"],
         "Rising action = complications that build tension leading up to the climax.", 'medium', 6),
        ("What is characterization?", "The way an author develops a character's personality",
         ["The physical setting of the story",
          "The sequence of plot events",
          "The conflict in the story"],
         "Characterization includes direct statements and indirect clues (dialogue, actions).", 'medium', 7),
        ("What does 'static character' mean?",
         "A character who does not change throughout the story",
         ["A character who is the hero",
          "A character who appears only once",
          "A character who changes dramatically"],
         "Static characters stay the same; dynamic characters grow or change.", 'medium', 7),
        ("What literary device is used in: 'The wind whispered through the trees'?",
         "Personification",
         ["Simile", "Metaphor", "Alliteration"],
         "Personification gives human qualities to non-human things. Wind can't actually whisper.", 'easy', 6),
        ("What is a simile?",
         "A comparison using 'like' or 'as'",
         ["A comparison without 'like' or 'as'",
          "Giving human traits to objects",
          "A word that imitates a sound"],
         "Simile: 'She is as brave as a lion.' Metaphor: 'She is a lion.'", 'easy', 6),
        ("What is the purpose of a foil character?",
         "To highlight the qualities of another character by contrast",
         ["To be the antagonist",
          "To provide comic relief",
          "To narrate the story"],
         "A foil contrasts with the protagonist, emphasizing their traits by comparison.", 'hard', 8),
        ("What is foreshadowing?",
         "Hints about what will happen later in the story",
         ["A flashback to earlier events",
          "When a character imagines the future",
          "The resolution of the conflict"],
         "Foreshadowing uses clues, symbols, or dialogue to hint at future events.", 'medium', 7),
        ("What is the external conflict type 'person vs. nature'?",
         "A character struggles against natural forces",
         ["A character struggles with their own feelings",
          "Two characters argue",
          "A character fights society's rules"],
         "Person vs. nature: surviving a storm, being stranded, fighting an animal.", 'medium', 6),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Literary Analysis', diff, q_text, choices, idx,
                     f"Correct: {ans}.", grade))
    return qs


def gen_reading_comprehension_ms(n=40, seed=None):
    r = random.Random(seed)
    passages = [
        {
            "text": (
                "The printing press, invented by Johannes Gutenberg around 1440, revolutionized the spread of "
                "information. Before its invention, books were copied by hand, making them rare and expensive. "
                "The press allowed books to be produced quickly and cheaply, making knowledge available to "
                "more people and fueling the Renaissance and Reformation."
            ),
            "questions": [
                ("What was the main problem with books before the printing press?",
                 "They were rare and expensive because they were copied by hand",
                 ["They were too large to carry", "They could only be read by priests",
                  "They were written in Latin"],
                 "The passage states books were 'rare and expensive' before the press.", 'easy', 6),
                ("How did the printing press contribute to the Renaissance?",
                 "By making knowledge available to more people",
                 ["By creating new artistic styles", "By replacing the church",
                  "By establishing universities"],
                 "The passage says it 'fuel[ed] the Renaissance' by spreading knowledge.", 'medium', 7),
                ("What can be inferred about literacy rates after the printing press?",
                 "More people likely learned to read as books became accessible",
                 ["Literacy decreased because books were confusing",
                  "Only wealthy people could read the new books",
                  "The church prevented people from reading"],
                 "If books became cheaper and more available, more people would have reason and access to learn to read.", 'hard', 8),
            ]
        },
        {
            "text": (
                "Wolves are apex predators that play a crucial role in maintaining healthy ecosystems. "
                "When wolves were reintroduced to Yellowstone National Park in 1995, they reduced the elk "
                "population and changed elk behavior. Elk stopped overgrazing riverbanks, allowing vegetation "
                "to recover, which stabilized rivers and increased biodiversity. This chain of events is called "
                "a trophic cascade."
            ),
            "questions": [
                ("What is a trophic cascade?",
                 "A chain of events caused by the addition or removal of a predator",
                 ["A flood caused by overgrazing", "A type of animal migration",
                  "The hunting behavior of wolves"],
                 "The passage defines it as the chain of events triggered by wolf reintroduction.", 'medium', 7),
                ("How did wolf reintroduction affect vegetation?",
                 "It allowed vegetation to recover by reducing elk overgrazing",
                 ["Wolves destroyed vegetation by digging", "Wolves ate the plants directly",
                  "Wolves prevented plants from spreading"],
                 "Wolves → fewer elk → less overgrazing → vegetation recovery.", 'medium', 6),
                ("What does 'apex predator' most likely mean?",
                 "A predator at the top of the food chain",
                 ["A predator that only hunts at night",
                  "A predator that lives near mountains",
                  "A predator that is also prey"],
                 "'Apex' means top or highest — apex predators have no natural predators.", 'hard', 8),
            ]
        },
    ]
    qs = []
    for _ in range(n):
        passage = r.choice(passages)
        q_text, ans, wrongs, diff, grade = r.choice(passage["questions"])
        full_q = f"Read the passage:\n\"{passage['text']}\"\n\n{q_text}"
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Reading Comprehension', diff, full_q, choices, idx,
                     f"Correct: {ans}.", grade))
    return qs


def gen_figurative_language(n=35, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("'The classroom was a zoo.' This is an example of:",
         "Metaphor", ["Simile", "Personification", "Hyperbole"],
         "A metaphor makes a direct comparison without 'like' or 'as'.", 'easy', 6),
        ("'I've told you a million times!' This is an example of:",
         "Hyperbole", ["Simile", "Metaphor", "Alliteration"],
         "Hyperbole is extreme exaggeration for emphasis.", 'easy', 6),
        ("'The thunder grumbled across the sky.' This is:",
         "Personification", ["Simile", "Metaphor", "Onomatopoeia"],
         "Thunder can't actually grumble — this gives it a human quality.", 'easy', 6),
        ("'Peter Piper picked a peck of pickled peppers.' This uses:",
         "Alliteration", ["Rhyme", "Onomatopoeia", "Assonance"],
         "Alliteration = repetition of the same consonant sound at the start of words.", 'medium', 7),
        ("'Buzz, crack, hiss.' These words are examples of:",
         "Onomatopoeia", ["Alliteration", "Hyperbole", "Imagery"],
         "Onomatopoeia = words that imitate sounds.", 'easy', 6),
        ("'Life is a journey.' What type of figurative language is this?",
         "Metaphor", ["Simile", "Hyperbole", "Alliteration"],
         "Direct comparison without 'like' or 'as' = metaphor.", 'easy', 6),
        ("'She is as cold as ice.' What type is this?",
         "Simile", ["Metaphor", "Personification", "Hyperbole"],
         "Simile = comparison using 'like' or 'as'.", 'easy', 6),
        ("What does 'break a leg' mean?",
         "Good luck", ["Literally break your leg", "Run away quickly", "Fall down"],
         "This is an idiom — a phrase whose meaning differs from its literal words.", 'medium', 7),
        ("An idiom is:", "A phrase whose meaning can't be understood from its literal words",
         ["A comparison using 'like' or 'as'",
          "Extreme exaggeration",
          "Repetition of consonant sounds"],
         "Idioms are cultural phrases with non-literal meanings.", 'medium', 7),
        ("'The sun smiled down on us.' This is:", "Personification",
         ["Metaphor", "Simile", "Hyperbole"],
         "The sun is given the human ability to smile.", 'easy', 6),
        ("'The stars danced in the night sky.' What device is used?",
         "Personification",
         ["Metaphor", "Simile", "Alliteration"],
         "Dancing is a human action attributed to the stars.", 'medium', 7),
        ("Which sentence uses a simile?",
         "Her smile was like sunshine.",
         ["Her smile was sunshine.", "She smiled all day long.", "The sunshine made her smile."],
         "Only 'like sunshine' is a comparison using 'like'.", 'easy', 6),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, expl, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Figurative Language', diff, q_text, choices, idx, expl, grade))
    return qs


def gen_writing_skills_ms(n=30, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What is the purpose of a thesis statement?",
         "To state the main argument of an essay",
         ["To summarize the conclusion", "To list all the evidence", "To introduce the characters"],
         "A thesis states the central claim that the rest of the essay supports.", 'medium', 7),
        ("Which sentence is the best thesis statement?",
         "Social media has both positive and negative effects on teenage mental health.",
         ["Social media is very popular.", "Many teenagers use social media.",
          "Social media was invented in the early 2000s."],
         "A thesis makes a specific, arguable claim — not just a fact.", 'hard', 8),
        ("What does 'cite evidence' mean in an essay?",
         "Support your claims with specific examples or quotes from the text",
         ["Write a longer paragraph", "Use fancy vocabulary", "Repeat your argument twice"],
         "Evidence grounds your argument in facts or textual support.", 'medium', 7),
        ("In argumentative writing, what is a 'counterclaim'?",
         "An opposing viewpoint that the writer then addresses",
         ["The writer's main argument", "A supporting detail", "The conclusion"],
         "Addressing a counterclaim shows the writer understands the full debate.", 'hard', 8),
        ("What is the difference between a fact and an opinion?",
         "A fact can be proven; an opinion is a personal belief",
         ["A fact is interesting; an opinion is boring",
          "A fact is short; an opinion is long",
          "There is no difference"],
         "Facts are verifiable. Opinions are subjective views.", 'easy', 6),
        ("Which transition word shows contrast?",
         "However", ["Furthermore", "Therefore", "In addition"],
         "'However' signals a contradiction or contrast. 'Furthermore/In addition' add information.", 'medium', 7),
        ("What is the purpose of a topic sentence?",
         "To introduce the main idea of a paragraph",
         ["To conclude the essay", "To provide evidence", "To introduce a new character"],
         "Topic sentences tell the reader what the paragraph will be about.", 'easy', 6),
        ("Which type of essay requires research and citations?",
         "Informational/expository essay",
         ["Personal narrative", "Descriptive essay", "Diary entry"],
         "Expository essays explain and inform using research and evidence.", 'medium', 7),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, expl, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Writing Skills', diff, q_text, choices, idx, expl, grade))
    return qs


_TOPIC_GENERATORS = {
    'Vocabulary':            [(gen_vocabulary_ms, {})],
    'Grammar':               [(gen_grammar_ms, {})],
    'Literary Analysis':     [(gen_literary_analysis, {})],
    'Reading Comprehension': [(gen_reading_comprehension_ms, {})],
    'Figurative Language':   [(gen_figurative_language, {})],
    'Writing Skills':        [(gen_writing_skills_ms, {})],
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
