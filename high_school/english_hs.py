"""
High School English Generator (Grades 9–12)
Covers: Literary Analysis, Rhetoric & Argumentation, Grammar & Style,
        Vocabulary, Reading Comprehension, AP English concepts
"""
import random
import json

def _q(topic, diff, question, choices, answer_idx, explanation, grade=10):
    return ('Language', topic, diff, question, json.dumps(choices), answer_idx, explanation, grade)

def _shuffle_choices(correct, wrongs, rng):
    choices = list(rng.sample(wrongs, min(3, len(wrongs))))
    idx = rng.randint(0, min(3, len(choices)))
    choices.insert(idx, correct)
    return choices[:4], idx


def gen_literary_analysis_hs(n=45, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What is the definition of 'tragic flaw' (hamartia) in Greek tragedy?",
         "A character's fatal weakness that leads to their downfall",
         ["A physical disability", "A character who dies", "A moral lesson"],
         "Hamartia (Aristotle): the flaw or error causing the hero's downfall — e.g., Macbeth's ambition.", 'medium', 10),
        ("What is an 'unreliable narrator'?",
         "A narrator whose credibility is compromised",
         ["A narrator who speaks in third person", "A narrator who is all-knowing",
          "A narrator who tells the story backwards"],
         "Unreliable narrators may be biased, delusional, or dishonest — e.g., in 'Gone Girl'.", 'medium', 10),
        ("What is the difference between denotation and connotation?",
         "Denotation is literal meaning; connotation is the associated feeling or implication",
         ["Denotation is emotional; connotation is dictionary meaning",
          "They are synonyms", "Denotation applies to poetry; connotation to prose"],
         "E.g., 'home' denotes a dwelling place but connotes comfort and family.", 'medium', 10),
        ("What is stream of consciousness?",
         "A narrative technique depicting a character's flowing thoughts",
         ["A type of external conflict", "First-person omniscient narration",
          "A plot device that skips time"],
         "Used by Woolf and Joyce — the narrative mirrors the unstructured flow of thought.", 'hard', 12),
        ("What is an allegory?",
         "A narrative where characters/events symbolize deeper moral or political meanings",
         ["A comparison using 'like' or 'as'", "A story told in reverse chronological order",
          "A poem with a strict rhyme scheme"],
         "Allegory: 'Animal Farm' represents Soviet communism; characters = political figures.", 'hard', 11),
        ("What is 'in medias res'?",
         "Starting the narrative in the middle of the action",
         ["Ending the story with a twist", "Narrating events in chronological order",
          "Using a flashback to start"],
         "In medias res (Latin: 'into the middle of things') — begins at a critical moment.", 'hard', 11),
        ("What is a motif?", "A recurring element that has symbolic significance",
         ["The main theme", "A character's defining trait", "The setting of the story"],
         "Motifs recur throughout a work to reinforce themes — e.g., light/dark in Romeo & Juliet.", 'medium', 10),
        ("What distinguishes a Shakespearean sonnet from a Petrarchan sonnet?",
         "Shakespearean: 3 quatrains + couplet (ABAB CDCD EFEF GG); Petrarchan: octave + sestet",
         ["Shakespearean sonnets have 16 lines", "They are structurally identical",
          "Petrarchan sonnets never rhyme"],
         "Both have 14 lines but differ in structure and turn (volta) placement.", 'hard', 12),
        ("What is catharsis in drama?",
         "Emotional purification or release felt by the audience",
         ["The conflict between two characters", "The climax of the play",
          "The protagonist's transformation"],
         "Aristotle: tragedy produces catharsis — purgation of pity and fear in the audience.", 'hard', 12),
        ("What is the purpose of a foil character?",
         "To highlight the protagonist's traits through contrast",
         ["To be the main villain", "To provide comic relief", "To narrate the story"],
         "Foils illuminate character by contrast: Laertes vs. Hamlet, Watson vs. Holmes.", 'medium', 10),
        ("What is an archetype?",
         "A universal character type or pattern found across cultures and literature",
         ["A villain in a story", "A type of narrator", "A figure of speech"],
         "Archetypes (hero, mentor, trickster) are universal patterns in myth and literature.", 'hard', 11),
        ("In literary criticism, what is the 'New Criticism' approach?",
         "Close reading of the text itself, ignoring author's biography or historical context",
         ["Analyzing literature through historical context", "Using psychology to analyze characters",
          "Reading texts through a feminist lens"],
         "New Criticism (mid-20th century) focuses on 'the text itself' — irony, ambiguity, tension.", 'hard', 12),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Literary Analysis', diff, q_text, choices, idx,
                     f"Correct: {ans}.", grade))
    return qs


def gen_rhetoric(n=35, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What is ethos in rhetoric?",
         "An appeal to the author's credibility or character",
         ["An appeal to emotion", "An appeal to logic/evidence", "An appeal to audience fear"],
         "Ethos = credibility. Pathos = emotion. Logos = logic/evidence (Aristotle's rhetorical appeals).", 'medium', 10),
        ("What is pathos?",
         "An appeal to the audience's emotions",
         ["An appeal to credibility", "An appeal to logic", "An appeal to authority"],
         "Pathos moves the audience emotionally to persuade them.", 'medium', 10),
        ("What is logos?",
         "An appeal to logic, reason, or evidence",
         ["An appeal to emotion", "An appeal to authority", "An appeal to tradition"],
         "Logos uses facts, data, and reasoned arguments.", 'medium', 10),
        ("What is an ad hominem fallacy?",
         "Attacking the person making an argument rather than the argument itself",
         ["Using emotional language", "Presenting false statistics",
          "Assuming something is true without evidence"],
         "Ad hominem attacks the arguer, not the argument — a logical fallacy.", 'hard', 11),
        ("What is a straw man argument?",
         "Misrepresenting someone's argument to make it easier to attack",
         ["Using a weak example to prove a point", "Appealing to popular opinion",
          "Citing unreliable sources"],
         "Straw man distorts the opponent's position, then attacks the distorted version.", 'hard', 11),
        ("What is anaphora?",
         "Repetition of a word or phrase at the beginning of successive clauses",
         ["Repetition of sounds at the end of words", "A question asked for effect",
          "An extreme exaggeration"],
         "MLK's 'I Have a Dream' uses anaphora: 'I have a dream that...' repeated.", 'hard', 11),
        ("What is a rhetorical question?",
         "A question asked for effect, not expecting an answer",
         ["A question that is unanswerable", "A question in an essay introduction",
          "A question with multiple answers"],
         "Rhetorical questions engage the audience and make a point without requiring response.", 'medium', 10),
        ("What is the difference between argument and persuasion?",
         "Argument relies on logic; persuasion can use emotion, appeals, or manipulation",
         ["They are identical", "Persuasion is always logical",
          "Argument uses emotion; persuasion uses logic"],
         "Arguments depend on sound reasoning; persuasion is broader and includes emotional appeals.", 'hard', 12),
        ("What does 'diction' refer to in writing?",
         "Word choice and style",
         ["Sentence length", "Punctuation use", "Paragraph structure"],
         "Diction = the specific words an author chooses, which affect tone and meaning.", 'medium', 10),
        ("What is syntax in writing?",
         "The arrangement and structure of sentences",
         ["Word choice", "The tone of the writing", "The use of figurative language"],
         "Syntax includes sentence length, word order, and clause structure.", 'medium', 11),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Rhetoric & Argumentation', diff, q_text, choices, idx,
                     f"Correct: {ans}.", grade))
    return qs


def gen_vocabulary_hs(n=50, seed=None):
    r = random.Random(seed)
    vocab = [
        ("abstruse", "difficult to understand; obscure", ["clear", "simple", "obvious"], 11),
        ("acrimony", "bitterness or ill feeling", ["kindness", "joy", "calmness"], 10),
        ("ameliorate", "to improve a bad situation", ["worsen", "ignore", "describe"], 11),
        ("anachronism", "something out of its proper historical time", ["modern thing", "historical fact", "future event"], 11),
        ("anomaly", "something that deviates from what is standard", ["norm", "average", "standard"], 10),
        ("apathy", "lack of interest or enthusiasm", ["passion", "energy", "concern"], 10),
        ("capricious", "given to sudden changes of mood", ["stable", "predictable", "calm"], 11),
        ("contentious", "causing or likely to cause an argument", ["peaceful", "agreeable", "clear"], 11),
        ("cynical", "believing people are motivated purely by self-interest", ["idealistic", "trusting", "naive"], 10),
        ("dearth", "a scarcity or lack of something", ["abundance", "excess", "wealth"], 11),
        ("disparate", "essentially different in kind; not able to be compared", ["similar", "equal", "related"], 12),
        ("equivocal", "open to more than one interpretation", ["clear", "unambiguous", "definite"], 12),
        ("esoteric", "intended for or likely understood by a small number of people", ["popular", "common", "obvious"], 12),
        ("fallacy", "a mistaken belief based on flawed reasoning", ["truth", "fact", "proof"], 10),
        ("garrulous", "excessively talkative", ["silent", "reserved", "concise"], 11),
        ("iconoclast", "a person who attacks cherished beliefs or institutions", ["conformist", "traditionalist", "follower"], 12),
        ("indefatigable", "persisting tirelessly", ["exhausted", "lazy", "weak"], 12),
        ("laconic", "using very few words; brief", ["verbose", "wordy", "lengthy"], 11),
        ("malleable", "easily influenced; able to be changed", ["rigid", "stubborn", "fixed"], 10),
        ("mercurial", "subject to sudden changes of mood", ["stable", "consistent", "predictable"], 11),
        ("nuance", "a subtle difference in meaning or expression", ["obvious contrast", "major difference", "clear distinction"], 11),
        ("obsequious", "excessively compliant or attentive", ["assertive", "defiant", "independent"], 12),
        ("pedantic", "overly concerned with minor details or rules", ["practical", "creative", "flexible"], 12),
        ("pragmatic", "dealing with things sensibly and practically", ["idealistic", "impractical", "abstract"], 10),
        ("rhetoric", "language designed to have a persuasive effect", ["factual reporting", "fictional narrative", "technical writing"], 10),
    ]
    qs = []
    for _ in range(n):
        word, definition, wrongs, grade = r.choice(vocab)
        qtype = r.choice(['define', 'identify'])
        if qtype == 'define':
            q_text = f"What does '{word}' mean?"
            ans = definition
            wrong_choices = r.sample(wrongs, min(3, len(wrongs)))
        else:
            q_text = f"Which word means '{definition}'?"
            ans = word
            other_words = [v[0] for v in vocab if v[0] != word and v[3] == grade]
            wrong_choices = r.sample(other_words, min(3, len(other_words))) if len(other_words) >= 3 else wrongs
        choices, idx = _shuffle_choices(ans, wrong_choices[:3], r)
        diff = 'medium' if grade <= 10 else 'hard'
        qs.append(_q('Vocabulary', diff, q_text, choices, idx,
                     f"'{word}' means: {definition}.", grade))
    return qs


def gen_grammar_style_hs(n=35, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("Which sentence correctly uses a colon?",
         "She needed three things: courage, strength, and determination.",
         ["She needed: courage, strength, and determination.",
          "She: needed courage, strength, and determination.",
          "She needed three things: Courage, Strength, and Determination."],
         "A colon follows a complete independent clause and introduces a list or explanation.", 'medium', 10),
        ("Which sentence has a dangling modifier?",
         "Walking down the street, the rain started to fall.",
         ["Walking down the street, she felt the rain start to fall.",
          "She felt the rain while walking down the street.",
          "The rain fell as she walked down the street."],
         "The modifier 'Walking down the street' doesn't logically connect to 'the rain'.", 'hard', 11),
        ("What is the subjunctive mood used for?",
         "Expressing hypothetical or contrary-to-fact situations",
         ["Expressing commands", "Describing past events",
          "Stating definite facts"],
         "Subjunctive: 'If I were you...' or 'I suggest that he be present.'", 'hard', 12),
        ("Which is correct: 'who' or 'whom' in: '___ did you call?'",
         "Whom", ["Who", "Whoever", "Whomever"],
         "'Whom' is the object form. 'You called whom?' → 'Whom did you call?'", 'hard', 11),
        ("What is passive voice and when should it be avoided?",
         "When the subject receives the action; avoided when active voice is clearer",
         ["When the subject performs the action; always avoid",
          "A form of past tense; never correct",
          "Used only in academic writing; always preferred"],
         "Passive: 'The ball was kicked.' Active: 'She kicked the ball.' Active is usually clearer.", 'medium', 10),
        ("Which sentence correctly uses 'effect' vs 'affect'?",
         "The medicine did not affect her symptoms, but the side effects were noticeable.",
         ["The medicine did not effect her symptoms, but the side affects were noticeable.",
          "The medicine did not affect her symptoms, but the side affects were noticeable.",
          "The medicine did not effect her symptoms, but the side effects were noticeable."],
         "'Affect' is usually a verb; 'effect' is usually a noun.", 'medium', 10),
        ("What is zeugma?",
         "Using one word to modify two others in different ways",
         ["Repetition of a word at the end of successive clauses",
          "A comparison using 'like' or 'as'",
          "An abrupt shift in speaker"],
         "Zeugma: 'She lost her keys and her temper.' One verb modifies two very different objects.", 'hard', 12),
        ("Which sentence demonstrates parallel structure?",
         "The report was accurate, thorough, and well-organized.",
         ["The report was accurate, very thorough, and showed good organization.",
          "The report: accurate, organized, and it was thorough.",
          "The report was accurate and thorough, plus showing organization."],
         "Parallel structure: all items in a list use the same grammatical form.", 'medium', 10),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Grammar & Style', diff, q_text, choices, idx,
                     f"Correct: {ans}.", grade))
    return qs


def gen_reading_comprehension_hs(n=30, seed=None):
    r = random.Random(seed)
    passages = [
        {
            "text": (
                "In his 1838 address to the Young Men's Lyceum of Springfield, Abraham Lincoln warned against "
                "mob rule, arguing that the greatest threat to American democracy was not foreign invasion "
                "but internal lawlessness. Lincoln contended that reverence for the law must become the "
                "'political religion' of the nation, binding citizens together across generations. He worried "
                "that ambitious men, unable to distinguish themselves within a stable republic, might seek "
                "fame by destroying rather than upholding its institutions."
            ),
            "questions": [
                ("According to Lincoln, what was the greatest threat to American democracy?",
                 "Internal lawlessness and mob rule",
                 ["Foreign invasion", "Economic inequality", "Weak military defense"],
                 "Lincoln explicitly contrasts the domestic threat of lawlessness with foreign attack.", 'medium', 11),
                ("What does Lincoln mean by 'political religion'?",
                 "A reverence for law that citizens hold as a deeply held civic value",
                 ["Mixing church and state", "A literal religious movement in politics",
                  "Religious laws governing civil society"],
                 "Lincoln uses religious language to convey the depth of commitment law should command.", 'hard', 12),
                ("What is Lincoln's concern about ambitious men?",
                 "They might undermine institutions to achieve fame they couldn't gain within the system",
                 ["They would leave America for other countries",
                  "They would become foreign spies",
                  "They would create new political parties"],
                 "Lincoln fears ambition that cannot be satisfied by ordinary achievement might turn destructive.", 'hard', 12),
            ]
        },
        {
            "text": (
                "The concept of cognitive dissonance, introduced by Leon Festinger in 1957, describes the "
                "mental discomfort people experience when they hold two conflicting beliefs or when their "
                "actions contradict their beliefs. To relieve this discomfort, people may change their beliefs, "
                "acquire new information that supports one view, or reduce the importance of the conflict. "
                "Advertisers and political campaigns have long exploited this tendency by framing choices "
                "in ways that create dissonance unless the consumer acts in the desired direction."
            ),
            "questions": [
                ("What causes cognitive dissonance?",
                 "Holding conflicting beliefs or acting against one's beliefs",
                 ["Forgetting important information", "Feeling too much emotion",
                  "Making a difficult but consistent decision"],
                 "Festinger defined it as the discomfort from inconsistent cognitions or behaviors.", 'medium', 10),
                ("Which of the following is NOT listed as a way to reduce cognitive dissonance?",
                 "Suppressing all emotions related to the conflict",
                 ["Changing one's beliefs", "Acquiring supporting information",
                  "Reducing the importance of the conflict"],
                 "The passage lists three strategies; suppressing emotions is not among them.", 'hard', 11),
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


_TOPIC_GENERATORS = {
    'Literary Analysis':        [(gen_literary_analysis_hs, {})],
    'Rhetoric & Argumentation': [(gen_rhetoric, {})],
    'Vocabulary':               [(gen_vocabulary_hs, {})],
    'Grammar & Style':          [(gen_grammar_style_hs, {})],
    'Reading Comprehension':    [(gen_reading_comprehension_hs, {})],
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
            all_qs.extend(fn(seed=r.randint(0, 999999), n=35))
    return all_qs
