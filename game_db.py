"""
Game database — SQLite-backed storage for users, questions, sessions, leaderboard.
"""

import sqlite3
import os
import json
from datetime import date
import math_gen

DB_PATH = os.getenv('GAME_DB', 'game.db')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    with get_db() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS players (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            email       TEXT    UNIQUE NOT NULL,
            username    TEXT    UNIQUE,
            avatar      TEXT    DEFAULT '🎮',
            role        TEXT    DEFAULT 'student',
            xp          INTEGER DEFAULT 0,
            level       INTEGER DEFAULT 1,
            streak      INTEGER DEFAULT 0,
            last_login  TEXT,
            created_at  TEXT    DEFAULT (date('now'))
        );

        CREATE TABLE IF NOT EXISTS questions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            subject     TEXT NOT NULL,
            topic       TEXT NOT NULL,
            difficulty  TEXT NOT NULL DEFAULT 'medium',
            question    TEXT NOT NULL,
            choices     TEXT NOT NULL,  -- JSON array of 4 choices
            answer      INTEGER NOT NULL,  -- index of correct choice (0-3)
            explanation TEXT,
            grade       INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS game_sessions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id   INTEGER NOT NULL,
            mode        TEXT NOT NULL,
            subject     TEXT,
            topic       TEXT,
            difficulty  TEXT,
            score       INTEGER DEFAULT 0,
            total       INTEGER DEFAULT 0,
            xp_earned   INTEGER DEFAULT 0,
            time_taken  INTEGER DEFAULT 0,  -- seconds
            answers     TEXT,  -- JSON array
            completed   INTEGER DEFAULT 0,
            created_at  TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (player_id) REFERENCES players(id)
        );

        CREATE TABLE IF NOT EXISTS achievements (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id   INTEGER NOT NULL,
            badge       TEXT NOT NULL,
            earned_at   TEXT DEFAULT (date('now')),
            FOREIGN KEY (player_id) REFERENCES players(id)
        );

        CREATE TABLE IF NOT EXISTS daily_challenges (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            challenge_date TEXT UNIQUE NOT NULL,
            subject     TEXT,
            topic       TEXT,
            question_ids TEXT  -- JSON array
        );
        """)
        _seed_questions(db)


COLLEGE_MATH_TOPICS = {'Calculus', 'Linear Algebra', 'Statistics', 'Differential Equations', 'Probability'}
NEW_SUBJECTS = {'Computer Science', 'Economics', 'Psychology'}

# ── Subject metadata (icon + accent color) ─────────────────────────────────────
SUBJECT_META = {
    'Math':                 {'icon': '➕', 'color': '#6366f1'},
    'Science':              {'icon': '🔬', 'color': '#10b981'},
    'Language':             {'icon': '📝', 'color': '#f59e0b'},
    'History':              {'icon': '🏛️', 'color': '#ef4444'},
    'Computer Science':     {'icon': '💻', 'color': '#06b6d4'},
    'Economics':            {'icon': '📊', 'color': '#84cc16'},
    'Psychology':           {'icon': '🧠', 'color': '#a855f7'},
}


EXTRA_LANG_TOPICS = {'Grammar', 'Vocabulary', 'Literature', 'Writing', 'Reading Comprehension'}
EXTRA_HIST_TOPICS = {'Ancient Civilizations', 'World Wars', 'American History', 'Modern History', 'Geography'}


def _seed_questions(db):
    existing_subjects = {r[0] for r in db.execute(
        "SELECT DISTINCT subject FROM questions"
    ).fetchall()}
    existing_math_topics = {r[0] for r in db.execute(
        "SELECT DISTINCT topic FROM questions WHERE subject='Math'"
    ).fetchall()}
    existing_lang_topics = {r[0] for r in db.execute(
        "SELECT DISTINCT topic FROM questions WHERE subject='Language'"
    ).fetchall()}
    existing_hist_topics = {r[0] for r in db.execute(
        "SELECT DISTINCT topic FROM questions WHERE subject='History'"
    ).fetchall()}
    existing_sci_count = db.execute(
        "SELECT COUNT(*) FROM questions WHERE subject='Science'"
    ).fetchone()[0]

    to_add = []
    if not existing_subjects:
        to_add.extend(_base_questions())

    if not COLLEGE_MATH_TOPICS.issubset(existing_math_topics):
        to_add.extend(_college_math_questions())

    for subj in NEW_SUBJECTS:
        if subj not in existing_subjects:
            if subj == 'Computer Science':
                to_add.extend(_cs_questions())
            elif subj == 'Economics':
                to_add.extend(_econ_questions())
            elif subj == 'Psychology':
                to_add.extend(_psych_questions())

    if not EXTRA_LANG_TOPICS.issubset(existing_lang_topics):
        to_add.extend(_language_extra_questions())
    if not EXTRA_HIST_TOPICS.issubset(existing_hist_topics):
        to_add.extend(_history_extra_questions())
    if existing_sci_count < 40:
        to_add.extend(_science_extra_questions())

    existing_math_count = db.execute("SELECT COUNT(*) FROM questions WHERE subject='Math'").fetchone()[0]
    if existing_math_count < 200:
        to_add.extend(_math_expanded_questions())

    # Procedural math generation — adds ~1,770 questions from math_gen.py
    total_math_count = db.execute(
        "SELECT COUNT(*) FROM questions WHERE subject='Math'"
    ).fetchone()[0]
    if total_math_count < 2000:
        to_add.extend(math_gen.generate_all())

    if to_add:
        db.executemany(
            "INSERT INTO questions (subject, topic, difficulty, question, choices, answer, explanation, grade) "
            "VALUES (?,?,?,?,?,?,?,?)",
            to_add
        )


def _base_questions():
    return [
        # Math — Arithmetic
        ('Math', 'Arithmetic', 'easy', 'What is 7 × 8?',
         '["48", "54", "56", "64"]', 2, 'Seven times eight equals 56.', 5),
        ('Math', 'Arithmetic', 'easy', 'What is 144 ÷ 12?',
         '["10", "11", "12", "13"]', 2, '144 divided by 12 is 12.', 5),
        ('Math', 'Arithmetic', 'medium', 'What is 15% of 200?',
         '["20", "25", "30", "35"]', 2, '15% of 200 = 0.15 × 200 = 30.', 6),
        ('Math', 'Arithmetic', 'medium', 'What is the value of 2⁸?',
         '["128", "256", "512", "64"]', 1, '2⁸ = 256.', 7),
        ('Math', 'Arithmetic', 'hard', 'If a train travels at 80 km/h for 2.5 hours, how far does it travel?',
         '["160 km", "180 km", "200 km", "220 km"]', 2, 'Distance = speed × time = 80 × 2.5 = 200 km.', 8),

        # Math — Algebra
        ('Math', 'Algebra', 'easy', 'Solve for x: 2x + 4 = 12',
         '["2", "3", "4", "5"]', 2, '2x = 8, x = 4.', 7),
        ('Math', 'Algebra', 'medium', 'What is the slope of the line y = 3x - 5?',
         '["−5", "3", "5", "−3"]', 1, 'In y = mx + b, the slope m = 3.', 8),
        ('Math', 'Algebra', 'hard', 'Solve x² - 5x + 6 = 0',
         '["x=1,x=6", "x=2,x=3", "x=−2,x=−3", "x=1,x=−6"]', 1,
         'Factor: (x−2)(x−3) = 0, so x = 2 or x = 3.', 9),

        # Science — Biology
        ('Science', 'Biology', 'easy', 'What is the powerhouse of the cell?',
         '["Nucleus", "Ribosome", "Mitochondria", "Vacuole"]', 2,
         'Mitochondria produce ATP energy for the cell.', 6),
        ('Science', 'Biology', 'easy', 'How many chromosomes does a normal human cell have?',
         '["23", "44", "46", "48"]', 2, 'Humans have 46 chromosomes (23 pairs).', 6),
        ('Science', 'Biology', 'medium', 'What process do plants use to make food?',
         '["Respiration", "Photosynthesis", "Fermentation", "Digestion"]', 1,
         'Plants convert sunlight, CO₂ and water into glucose via photosynthesis.', 7),
        ('Science', 'Biology', 'hard', 'What is the role of mRNA in protein synthesis?',
         '["Stores genetic info", "Carries amino acids", "Carries genetic code to ribosome", "Forms the ribosome"]', 2,
         'mRNA transcribes the DNA code and brings it to the ribosome for translation.', 10),

        # Science — Physics
        ('Science', 'Physics', 'easy', 'What is the unit of force?',
         '["Watt", "Joule", "Newton", "Pascal"]', 2, 'Force is measured in Newtons (N).', 6),
        ('Science', 'Physics', 'medium', 'According to Newton\'s second law, F = ?',
         '["m + a", "m × a", "m ÷ a", "m − a"]', 1, 'F = ma (Force = mass × acceleration).', 7),
        ('Science', 'Physics', 'hard', 'What is the speed of light in a vacuum?',
         '["3 × 10⁶ m/s", "3 × 10⁸ m/s", "3 × 10¹⁰ m/s", "3 × 10⁴ m/s"]', 1,
         'Speed of light c ≈ 3 × 10⁸ m/s.', 9),

        # Science — Chemistry
        ('Science', 'Chemistry', 'easy', 'What is the chemical symbol for water?',
         '["WA", "H₂O", "HO₂", "W"]', 1, 'Water is H₂O — two hydrogen atoms and one oxygen atom.', 5),
        ('Science', 'Chemistry', 'medium', 'What is the atomic number of Carbon?',
         '["4", "5", "6", "7"]', 2, 'Carbon has 6 protons, so its atomic number is 6.', 7),
        ('Science', 'Chemistry', 'hard', 'What type of bond involves the sharing of electron pairs?',
         '["Ionic bond", "Covalent bond", "Metallic bond", "Hydrogen bond"]', 1,
         'Covalent bonds form when atoms share electron pairs.', 9),

        # Language — Grammar
        ('Language', 'Grammar', 'easy', 'Which sentence is grammatically correct?',
         '["She go to school.", "She goes to school.", "She going to school.", "She goed to school."]', 1,
         '"She goes" uses the correct third-person singular present tense.', 5),
        ('Language', 'Grammar', 'medium', 'What is the past tense of "run"?',
         '["Runned", "Runs", "Ran", "Running"]', 2, '"Run" is an irregular verb; past tense is "ran".', 6),
        ('Language', 'Grammar', 'hard', 'Identify the subjunctive mood: which sentence is correct?',
         '["If I was you, I would leave.", "If I were you, I would leave.", "If I am you, I would leave.", "If I be you, I would leave."]', 1,
         'The subjunctive mood uses "were" for hypothetical statements: "If I were you".', 9),

        # Language — Vocabulary
        ('Language', 'Vocabulary', 'easy', 'What does "benevolent" mean?',
         '["Evil", "Kind and generous", "Angry", "Lazy"]', 1,
         'Benevolent means well-meaning and kind.', 6),
        ('Language', 'Vocabulary', 'medium', 'What is a synonym for "ephemeral"?',
         '["Permanent", "Transient", "Massive", "Ancient"]', 1,
         'Ephemeral means lasting for a very short time — synonymous with "transient".', 8),

        # History — World History
        ('History', 'World History', 'easy', 'In what year did World War II end?',
         '["1943", "1944", "1945", "1946"]', 2, 'World War II ended in 1945 with Germany\'s surrender in May and Japan\'s in September.', 6),
        ('History', 'World History', 'medium', 'Who was the first person to walk on the Moon?',
         '["Buzz Aldrin", "Yuri Gagarin", "Neil Armstrong", "John Glenn"]', 2,
         'Neil Armstrong became the first person to walk on the Moon on July 20, 1969.', 7),
        ('History', 'World History', 'hard', 'The Treaty of Westphalia (1648) ended which war?',
         '["The Hundred Years War", "The Thirty Years War", "The Seven Years War", "The Napoleonic Wars"]', 1,
         'The Peace of Westphalia ended the Thirty Years War and the Eighty Years War.', 10),

        # History — Geography
        ('History', 'Geography', 'easy', 'What is the capital of France?',
         '["Berlin", "Madrid", "Paris", "Rome"]', 2, 'Paris is the capital city of France.', 5),
        ('History', 'Geography', 'medium', 'Which is the longest river in the world?',
         '["Amazon", "Nile", "Yangtze", "Mississippi"]', 1,
         'The Nile River in Africa is considered the longest river at about 6,650 km.', 6),
        ('History', 'Geography', 'hard', 'Which country has the most time zones?',
         '["Russia", "USA", "China", "France"]', 3,
         'France (including overseas territories) spans 12 time zones, the most of any country.', 9),
    ]


def _college_math_questions():
    return [
        # ── Calculus ──────────────────────────────────────────────────────────
        ('Math', 'Calculus', 'easy',
         'What is the derivative of f(x) = x³?',
         '["x²", "3x²", "3x³", "x⁴/4"]', 1,
         'd/dx [xⁿ] = nxⁿ⁻¹, so d/dx [x³] = 3x².', 12),

        ('Math', 'Calculus', 'easy',
         'What is ∫ 2x dx?',
         '["x² + C", "2x² + C", "x + C", "2 + C"]', 0,
         '∫ 2x dx = x² + C using the power rule for integration.', 12),

        ('Math', 'Calculus', 'medium',
         'What is the derivative of f(x) = sin(x)?',
         '["−sin(x)", "cos(x)", "−cos(x)", "tan(x)"]', 1,
         'd/dx [sin(x)] = cos(x).', 13),

        ('Math', 'Calculus', 'medium',
         'Evaluate lim(x→0) [sin(x)/x].',
         '["0", "∞", "1", "undefined"]', 2,
         'This is a standard limit: lim(x→0) sin(x)/x = 1.', 13),

        ('Math', 'Calculus', 'medium',
         'What is the integral ∫ eˣ dx?',
         '["eˣ + C", "xeˣ + C", "eˣ/x + C", "e^(x+1) + C"]', 0,
         'The exponential function eˣ is its own antiderivative: ∫ eˣ dx = eˣ + C.', 13),

        ('Math', 'Calculus', 'hard',
         'Using the chain rule, find d/dx [sin(x²)].',
         '["cos(x²)", "2x·cos(x²)", "2cos(x²)", "sin(2x)"]', 1,
         'd/dx [sin(u)] = cos(u)·u\', where u = x², so u\' = 2x. Result: 2x·cos(x²).', 14),

        ('Math', 'Calculus', 'hard',
         'What is ∫₀¹ x² dx?',
         '["1/4", "1/3", "1/2", "1"]', 1,
         '∫ x² dx = x³/3 + C. Evaluated from 0 to 1: (1/3) − 0 = 1/3.', 14),

        ('Math', 'Calculus', 'hard',
         'Which rule is used to differentiate a product f(x)·g(x)?',
         '["Chain rule", "Quotient rule", "Product rule", "Power rule"]', 2,
         'Product rule: d/dx [f·g] = f\'·g + f·g\'.', 13),

        # ── Linear Algebra ────────────────────────────────────────────────────
        ('Math', 'Linear Algebra', 'easy',
         'What is the determinant of the 2×2 matrix [[3,1],[2,4]]?',
         '["10", "11", "12", "14"]', 0,
         'det([[a,b],[c,d]]) = ad − bc = (3)(4) − (1)(2) = 12 − 2 = 10.', 13),

        ('Math', 'Linear Algebra', 'easy',
         'What is the result of multiplying matrix [[1,0],[0,1]] by any matrix A?',
         '["0", "A transposed", "A", "A inverse"]', 2,
         '[[1,0],[0,1]] is the identity matrix I; I·A = A for any compatible matrix A.', 12),

        ('Math', 'Linear Algebra', 'medium',
         'A system of linear equations has no solution. What does this mean geometrically for two lines?',
         '["They are identical", "They intersect at one point", "They are parallel", "They are perpendicular"]', 2,
         'Parallel lines never intersect, giving no solution (inconsistent system).', 13),

        ('Math', 'Linear Algebra', 'medium',
         'What is the rank of the matrix [[1,2],[2,4]]?',
         '["0", "1", "2", "4"]', 1,
         'Row 2 is 2× row 1, so they are linearly dependent. Only 1 independent row → rank = 1.', 14),

        ('Math', 'Linear Algebra', 'medium',
         'What is the dot product of vectors u = [1, 2, 3] and v = [4, 5, 6]?',
         '["12", "22", "32", "56"]', 2,
         'u·v = 1×4 + 2×5 + 3×6 = 4 + 10 + 18 = 32.', 13),

        ('Math', 'Linear Algebra', 'hard',
         'If a matrix A has eigenvalue λ and eigenvector v, which equation holds?',
         '["Av = v + λ", "Av = λv", "Av = λ + v", "A + λ = v"]', 1,
         'By definition of eigenvalue/eigenvector: Av = λv.', 14),

        ('Math', 'Linear Algebra', 'hard',
         'What does it mean for a square matrix to be singular?',
         '["Its determinant is 1", "It has no transpose", "Its determinant is 0", "All entries are equal"]', 2,
         'A singular matrix has determinant 0 and is therefore not invertible.', 14),

        # ── Statistics ────────────────────────────────────────────────────────
        ('Math', 'Statistics', 'easy',
         'What is the mean of the data set {4, 8, 6, 5, 3, 2, 8, 9, 2, 5}?',
         '["5", "5.2", "5.5", "6"]', 1,
         'Sum = 52, n = 10. Mean = 52/10 = 5.2.', 12),

        ('Math', 'Statistics', 'easy',
         'What measure of central tendency is least affected by extreme outliers?',
         '["Mean", "Mode", "Median", "Range"]', 2,
         'The median (middle value) is resistant to outliers unlike the mean.', 12),

        ('Math', 'Statistics', 'medium',
         'In a normal distribution, approximately what percentage of data falls within one standard deviation of the mean?',
         '["50%", "68%", "95%", "99.7%"]', 1,
         'The empirical rule: ~68% within ±1σ, ~95% within ±2σ, ~99.7% within ±3σ.', 13),

        ('Math', 'Statistics', 'medium',
         'What does a p-value less than 0.05 typically indicate?',
         '["Accept the null hypothesis", "Strong practical significance", "Statistically significant result", "Large sample size"]', 2,
         'p < 0.05 means there is less than 5% probability of the observed result under the null hypothesis — conventionally considered statistically significant.', 14),

        ('Math', 'Statistics', 'medium',
         'What is the variance of the data set {2, 4, 4, 4, 5, 5, 7, 9}?',
         '["2", "4", "4.5", "5"]', 1,
         'Mean = 5. Variance = mean of squared deviations = (9+1+1+1+0+0+4+16)/8 = 32/8 = 4.', 14),

        ('Math', 'Statistics', 'hard',
         'Which test is appropriate for comparing means of two independent groups when population variance is unknown?',
         '["Chi-square test", "ANOVA", "Two-sample t-test", "Z-test"]', 2,
         'The two-sample t-test (Welch\'s or equal-variance) is used when population variances are unknown and comparing two independent group means.', 15),

        ('Math', 'Statistics', 'hard',
         'What does a correlation coefficient of −0.9 indicate?',
         '["Weak positive relationship", "No relationship", "Strong positive relationship", "Strong negative relationship"]', 3,
         'r = −0.9 is close to −1, indicating a strong negative linear relationship.', 13),

        # ── Probability ───────────────────────────────────────────────────────
        ('Math', 'Probability', 'easy',
         'A fair coin is flipped twice. What is the probability of getting two heads?',
         '["1/4", "1/2", "1/3", "3/4"]', 0,
         'P(H)×P(H) = (1/2)×(1/2) = 1/4. The events are independent.', 12),

        ('Math', 'Probability', 'easy',
         'A standard die is rolled. What is the probability of rolling a number greater than 4?',
         '["1/6", "1/3", "1/2", "2/3"]', 1,
         'Numbers greater than 4 are {5, 6}. P = 2/6 = 1/3.', 12),

        ('Math', 'Probability', 'medium',
         'What is the probability of drawing a king from a standard 52-card deck?',
         '["1/13", "1/26", "4/52", "1/52"]', 0,
         'There are 4 kings in 52 cards: P = 4/52 = 1/13.', 12),

        ('Math', 'Probability', 'medium',
         'If P(A) = 0.4 and P(B) = 0.3 and A and B are independent, what is P(A ∩ B)?',
         '["0.7", "0.12", "0.1", "0.58"]', 1,
         'For independent events: P(A ∩ B) = P(A) × P(B) = 0.4 × 0.3 = 0.12.', 13),

        ('Math', 'Probability', 'hard',
         'A bag has 5 red and 3 blue balls. Two balls are drawn without replacement. What is the probability both are red?',
         '["5/16", "25/64", "5/14", "10/56"]', 2,
         'P(R₁) = 5/8. P(R₂|R₁) = 4/7. P(both red) = (5/8)×(4/7) = 20/56 = 5/14.', 14),

        ('Math', 'Probability', 'hard',
         'Using Bayes\' theorem: P(A|B) = ?',
         '["P(B|A)·P(B) / P(A)", "P(A)·P(B) / P(B|A)", "P(B|A)·P(A) / P(B)", "P(A|B)·P(A) / P(B)"]', 2,
         'Bayes\' theorem: P(A|B) = P(B|A)·P(A) / P(B).', 15),

        # ── Differential Equations ────────────────────────────────────────────
        ('Math', 'Differential Equations', 'medium',
         'What is the general solution to the ODE dy/dx = y?',
         '["y = x + C", "y = Ceˣ", "y = Ce⁻ˣ", "y = Cx"]', 1,
         'dy/y = dx → ln|y| = x + C₀ → y = Ceˣ, where C = e^C₀.', 14),

        ('Math', 'Differential Equations', 'medium',
         'What is the order of the ODE d²y/dx² + 3(dy/dx) + 2y = 0?',
         '["0", "1", "2", "3"]', 2,
         'The order is determined by the highest derivative present — d²y/dx² makes this a 2nd-order ODE.', 13),

        ('Math', 'Differential Equations', 'hard',
         'The characteristic equation for y″ − 5y′ + 6y = 0 has roots r₁ and r₂. What are they?',
         '["r = 2, r = 3", "r = −2, r = −3", "r = 1, r = 6", "r = 5, r = 1"]', 0,
         'Characteristic equation: r² − 5r + 6 = 0 → (r−2)(r−3) = 0 → r = 2, r = 3.', 15),

        ('Math', 'Differential Equations', 'hard',
         'What technique is used to solve a first-order linear ODE of the form dy/dx + P(x)y = Q(x)?',
         '["Separation of variables", "Integrating factor", "Euler\'s method", "Laplace transform"]', 1,
         'Multiply both sides by the integrating factor μ(x) = e^∫P(x)dx to make the left side an exact derivative.', 15),
    ]


def _cs_questions():
    return [
        # ── Programming Basics ────────────────────────────────────────────────
        ('Computer Science', 'Programming', 'easy',
         'What does the keyword "return" do in a function?',
         '["Ends the program", "Sends a value back to the caller", "Declares a variable", "Loops through code"]', 1,
         'return exits the function and optionally passes a value back to the calling code.', 9),
        ('Computer Science', 'Programming', 'easy',
         'What is the output of: print(2 ** 3) in Python?',
         '["6", "8", "9", "23"]', 1,
         '** is the exponentiation operator. 2³ = 8.', 9),
        ('Computer Science', 'Programming', 'medium',
         'What is the difference between a compiled language and an interpreted language?',
         '["Compiled code runs faster always", "Compiled code is translated to machine code before execution; interpreted code is translated line by line at runtime", "They are the same", "Interpreted code is always faster"]', 1,
         'Compiled languages (C, C++) translate source to machine code upfront. Interpreted languages (Python, JS) translate and execute line-by-line.', 11),
        ('Computer Science', 'Programming', 'medium',
         'What is recursion in programming?',
         '["A loop that iterates N times", "A function that calls itself", "A variable that stores a function", "A type of array"]', 1,
         'Recursion is when a function calls itself (with a base case to stop), breaking a problem into smaller sub-problems.', 11),
        ('Computer Science', 'Programming', 'hard',
         'What is the time complexity of binary search?',
         '["O(n)", "O(n²)", "O(log n)", "O(1)"]', 2,
         'Binary search halves the search space each step → O(log n) time complexity.', 12),

        # ── Data Structures ───────────────────────────────────────────────────
        ('Computer Science', 'Data Structures', 'easy',
         'Which data structure operates on a First-In First-Out (FIFO) principle?',
         '["Stack", "Queue", "Tree", "Graph"]', 1,
         'A queue processes elements in the order they arrive — first in, first out.', 10),
        ('Computer Science', 'Data Structures', 'easy',
         'What is the top of a stack?',
         '["The first element inserted", "The last element inserted", "The middle element", "A random element"]', 1,
         'A stack is Last-In First-Out (LIFO). The most recently pushed element is at the top.', 10),
        ('Computer Science', 'Data Structures', 'medium',
         'What is the worst-case time complexity for searching in an unsorted array?',
         '["O(1)", "O(log n)", "O(n)", "O(n²)"]', 2,
         'In the worst case you must check every element: O(n) linear time.', 11),
        ('Computer Science', 'Data Structures', 'medium',
         'Which data structure uses nodes with pointers to the next node?',
         '["Array", "Linked List", "Stack (only)", "Hash Table"]', 1,
         'A linked list stores data in nodes, each containing a value and a pointer to the next node.', 11),
        ('Computer Science', 'Data Structures', 'hard',
         'What is the average-case time complexity for lookup in a hash table?',
         '["O(n)", "O(log n)", "O(n²)", "O(1)"]', 3,
         'With a good hash function and low load factor, hash table lookups are O(1) on average.', 12),

        # ── Algorithms ────────────────────────────────────────────────────────
        ('Computer Science', 'Algorithms', 'easy',
         'Which sorting algorithm works by repeatedly swapping adjacent elements that are in the wrong order?',
         '["Merge Sort", "Quick Sort", "Bubble Sort", "Heap Sort"]', 2,
         'Bubble sort compares adjacent pairs and swaps them if needed, "bubbling" large values to the end.', 10),
        ('Computer Science', 'Algorithms', 'medium',
         'What is the divide-and-conquer approach?',
         '["Solve the whole problem at once", "Break into smaller sub-problems, solve each, combine results", "Use iteration instead of recursion", "Prioritize the hardest sub-problem first"]', 1,
         'Divide and conquer splits a problem into sub-problems, solves them independently, then combines. Examples: merge sort, quicksort.', 12),
        ('Computer Science', 'Algorithms', 'medium',
         'What does Big-O notation describe?',
         '["Exact runtime of an algorithm", "The best-case performance", "Upper bound on time/space growth relative to input size", "Memory usage only"]', 2,
         'Big-O gives an asymptotic upper bound describing how an algorithm\'s resource use scales with input size n.', 12),
        ('Computer Science', 'Algorithms', 'hard',
         'Which algorithm finds the shortest path in a weighted graph with non-negative edge weights?',
         '["Breadth-First Search", "Depth-First Search", "Dijkstra\'s Algorithm", "Bellman-Ford"]', 2,
         'Dijkstra\'s algorithm uses a priority queue to greedily expand the shortest known path and works on graphs with non-negative weights.', 14),

        # ── Databases ─────────────────────────────────────────────────────────
        ('Computer Science', 'Databases', 'easy',
         'What does SQL stand for?',
         '["Structured Query Language", "Simple Question Language", "System Query Logic", "Sequential Queue List"]', 0,
         'SQL (Structured Query Language) is the standard language for managing relational databases.', 10),
        ('Computer Science', 'Databases', 'medium',
         'What is a primary key in a relational database?',
         '["A key that encrypts data", "A column (or set) that uniquely identifies each row", "The first column in a table", "A foreign reference to another table"]', 1,
         'A primary key uniquely identifies each record in a table. It must be unique and not null.', 11),
        ('Computer Science', 'Databases', 'medium',
         'What does a JOIN clause do in SQL?',
         '["Deletes duplicate rows", "Combines rows from two or more tables based on a related column", "Creates a new table", "Sorts query results"]', 1,
         'JOIN combines records from multiple tables where the join condition matches (e.g., matching foreign key to primary key).', 12),
        ('Computer Science', 'Databases', 'hard',
         'What is database normalization?',
         '["Encrypting all database fields", "Organizing data to reduce redundancy and improve integrity", "Converting a database to NoSQL", "Indexing all columns"]', 1,
         'Normalization organizes tables to minimize data redundancy and dependency (1NF, 2NF, 3NF, etc.).', 13),

        # ── Networking ────────────────────────────────────────────────────────
        ('Computer Science', 'Networking', 'easy',
         'What does IP stand for in networking?',
         '["Internet Protocol", "Internal Process", "Input Port", "Integrated Packet"]', 0,
         'IP (Internet Protocol) is the set of rules governing data packets sent over the internet.', 9),
        ('Computer Science', 'Networking', 'medium',
         'What is the purpose of DNS?',
         '["Assigns IP addresses dynamically", "Translates domain names to IP addresses", "Encrypts web traffic", "Routes packets between networks"]', 1,
         'DNS (Domain Name System) maps human-readable domain names (e.g., google.com) to IP addresses.', 11),
        ('Computer Science', 'Networking', 'hard',
         'Which OSI layer is responsible for end-to-end communication and error recovery?',
         '["Network layer", "Transport layer", "Session layer", "Data link layer"]', 1,
         'The Transport layer (Layer 4) handles end-to-end communication, flow control, and reliability (TCP/UDP).', 13),

        # ── Cybersecurity ─────────────────────────────────────────────────────
        ('Computer Science', 'Cybersecurity', 'easy',
         'What is phishing?',
         '["A type of computer virus", "A fraudulent attempt to steal sensitive info by disguising as a trustworthy entity", "A network scanning tool", "Encrypted communication"]', 1,
         'Phishing tricks users into revealing credentials or clicking malicious links by impersonating legitimate sources.', 10),
        ('Computer Science', 'Cybersecurity', 'medium',
         'What does HTTPS provide over HTTP?',
         '["Faster loading", "Compressed data", "Encrypted and authenticated communication", "Larger bandwidth"]', 2,
         'HTTPS uses TLS/SSL to encrypt data in transit and authenticate the server, protecting against eavesdropping.', 11),
        ('Computer Science', 'Cybersecurity', 'hard',
         'What is a SQL injection attack?',
         '["Overloading a database server", "Injecting malicious SQL code into an input to manipulate the database", "Stealing database backups", "Cracking password hashes"]', 1,
         'SQL injection inserts malicious SQL into input fields to manipulate queries — e.g., bypassing authentication or exfiltrating data.', 13),
    ]


def _econ_questions():
    return [
        # ── Microeconomics ────────────────────────────────────────────────────
        ('Economics', 'Microeconomics', 'easy',
         'What is the law of demand?',
         '["As price rises, quantity demanded rises", "As price rises, quantity demanded falls", "Demand is always constant", "Supply determines demand"]', 1,
         'The law of demand states that, all else equal, higher prices lead to lower quantity demanded.', 9),
        ('Economics', 'Microeconomics', 'easy',
         'What is opportunity cost?',
         '["The monetary cost of a good", "The next best alternative forgone when a choice is made", "The total cost of production", "Government taxes on goods"]', 1,
         'Opportunity cost is the value of the best alternative you give up by making a decision.', 10),
        ('Economics', 'Microeconomics', 'medium',
         'What happens to price when supply increases and demand stays constant?',
         '["Price rises", "Price stays the same", "Price falls", "Quantity falls"]', 2,
         'More supply with the same demand creates a surplus, pushing prices down until equilibrium is restored.', 11),
        ('Economics', 'Microeconomics', 'medium',
         'What is a monopoly?',
         '["Two companies controlling a market", "A market with many small sellers", "A single seller dominating the market with no close substitutes", "Government-owned businesses"]', 2,
         'A monopoly exists when one firm is the sole producer of a product with no close substitutes, giving it significant pricing power.', 11),
        ('Economics', 'Microeconomics', 'medium',
         'What is price elasticity of demand?',
         '["How fast prices change over time", "A measure of how responsive quantity demanded is to a price change", "The relationship between supply and production cost", "Fixed pricing in competitive markets"]', 1,
         'Price elasticity of demand = % change in quantity demanded / % change in price. Values > 1 are elastic (responsive); < 1 are inelastic.', 12),
        ('Economics', 'Microeconomics', 'hard',
         'At the profit-maximizing output for a competitive firm, which condition holds?',
         '["Price = Average Total Cost", "Marginal Revenue = Marginal Cost", "Total Revenue is maximized", "Price = Average Variable Cost"]', 1,
         'Firms maximize profit where MR = MC (marginal revenue equals marginal cost).', 13),

        # ── Macroeconomics ────────────────────────────────────────────────────
        ('Economics', 'Macroeconomics', 'easy',
         'What does GDP stand for?',
         '["General Domestic Product", "Gross Domestic Product", "Government Debt Policy", "Global Development Plan"]', 1,
         'GDP (Gross Domestic Product) is the total monetary value of all goods and services produced in a country in a given period.', 9),
        ('Economics', 'Macroeconomics', 'easy',
         'What is inflation?',
         '["A decrease in the money supply", "A general rise in prices over time reducing purchasing power", "An increase in unemployment", "Government spending increase"]', 1,
         'Inflation is the rate at which the general price level rises, eroding the purchasing power of money.', 9),
        ('Economics', 'Macroeconomics', 'medium',
         'What is the role of the Federal Reserve in the U.S. economy?',
         '["Collects federal taxes", "Manages the national debt", "Sets monetary policy and regulates the money supply", "Creates the federal budget"]', 2,
         'The Federal Reserve (Fed) is the U.S. central bank. It controls monetary policy — setting interest rates and regulating money supply — to pursue price stability and employment.', 12),
        ('Economics', 'Macroeconomics', 'medium',
         'What is fiscal policy?',
         '["Central bank interest rate decisions", "Government spending and taxation decisions", "Trade tariff negotiations", "Corporate pricing strategies"]', 1,
         'Fiscal policy refers to government decisions about spending and taxation used to influence the economy.', 12),
        ('Economics', 'Macroeconomics', 'hard',
         'According to the Phillips Curve (short run), what is the typical tradeoff?',
         '["Higher inflation → lower GDP", "Lower unemployment → higher inflation", "Higher taxes → lower inflation", "More spending → lower interest rates"]', 1,
         'The short-run Phillips Curve suggests an inverse relationship between unemployment and inflation: lower unemployment tends to correlate with higher inflation.', 14),

        # ── Personal Finance ──────────────────────────────────────────────────
        ('Economics', 'Personal Finance', 'easy',
         'What is compound interest?',
         '["Interest earned only on the original principal", "Interest earned on both the principal and previously accumulated interest", "A fixed monthly fee charged by banks", "Government bonds interest"]', 1,
         'Compound interest earns interest on the principal AND on previously earned interest, accelerating growth over time.', 9),
        ('Economics', 'Personal Finance', 'medium',
         'What is a credit score used for?',
         '["Tracking your income", "Measuring your investment returns", "Assessing your creditworthiness for loans", "Calculating your taxes"]', 2,
         'A credit score (e.g., FICO) reflects your history of repaying debt and is used by lenders to assess default risk.', 10),
        ('Economics', 'Personal Finance', 'medium',
         'What is diversification in investing?',
         '["Putting all money in one stock", "Spreading investments across different assets to reduce risk", "Only investing in bonds", "Timing the market"]', 1,
         'Diversification reduces risk by spreading investments across various assets so that losses in one area can be offset by gains in another.', 11),
    ]


def _psych_questions():
    return [
        # ── Intro Psychology ──────────────────────────────────────────────────
        ('Psychology', 'Intro Psychology', 'easy',
         'Who is known as the "father of psychoanalysis"?',
         '["Carl Jung", "B.F. Skinner", "Sigmund Freud", "William James"]', 2,
         'Sigmund Freud developed psychoanalysis, emphasizing the unconscious mind, id/ego/superego, and defense mechanisms.', 9),
        ('Psychology', 'Intro Psychology', 'easy',
         'What is psychology?',
         '["The study of brain anatomy", "The scientific study of behavior and mental processes", "The philosophy of the mind", "The study of social systems"]', 1,
         'Psychology is the scientific discipline that studies behavior and mental processes, including perception, cognition, emotion, and development.', 9),
        ('Psychology', 'Intro Psychology', 'medium',
         'What is the difference between classical and operant conditioning?',
         '["They are the same thing", "Classical pairs stimuli; operant uses consequences (rewards/punishments)", "Classical uses rewards; operant uses neutral stimuli", "Operant is only for animals"]', 1,
         'Classical conditioning (Pavlov) pairs a neutral stimulus with an unconditioned one. Operant conditioning (Skinner) shapes behavior through reinforcement and punishment.', 11),
        ('Psychology', 'Intro Psychology', 'medium',
         'What is confirmation bias?',
         '["Forgetting information that contradicts beliefs", "Remembering only positive events", "Tendency to search for and interpret information that confirms existing beliefs", "Changing beliefs when proven wrong"]', 2,
         'Confirmation bias is the cognitive tendency to favor information that confirms pre-existing beliefs and ignore contradictory evidence.', 11),
        ('Psychology', 'Intro Psychology', 'hard',
         'According to Maslow\'s hierarchy of needs, which need must be met before self-actualization?',
         '["Esteem needs", "Love/belonging needs", "Safety needs", "Physiological needs"]', 0,
         'Maslow\'s hierarchy (bottom to top): Physiological → Safety → Love/Belonging → Esteem → Self-Actualization. Esteem needs come just before self-actualization.', 13),

        # ── Cognitive Psychology ──────────────────────────────────────────────
        ('Psychology', 'Cognitive Psychology', 'easy',
         'What is long-term memory?',
         '["Memory lasting only a few seconds", "The ability to store and retrieve information over extended periods", "Only memories from childhood", "Working memory capacity"]', 1,
         'Long-term memory stores information for extended periods — from hours to a lifetime — and has a very large capacity.', 10),
        ('Psychology', 'Cognitive Psychology', 'medium',
         'What is working memory?',
         '["Memory of past traumas", "The brain\'s short-term system for temporarily holding and manipulating information", "Muscle memory", "Procedural memory for skills"]', 1,
         'Working memory is the limited-capacity system that temporarily holds and processes information needed for tasks like reasoning and comprehension.', 12),
        ('Psychology', 'Cognitive Psychology', 'medium',
         'What is cognitive dissonance?',
         '["Learning two conflicting skills", "Mental discomfort from holding contradictory beliefs or behaviors", "Short-term memory failure", "Social anxiety disorder"]', 1,
         'Cognitive dissonance (Festinger) is the discomfort felt when holding two conflicting beliefs or when behavior contradicts a belief, often motivating attitude change.', 12),
        ('Psychology', 'Cognitive Psychology', 'hard',
         'In schema theory, what is "accommodation"?',
         '["Fitting new info into existing schemas", "Changing existing schemas to fit new information", "Forgetting old schemas", "Creating an entirely new memory system"]', 1,
         'Piaget\'s accommodation means modifying or creating new schemas when new information cannot fit existing ones. The opposite is assimilation (fitting new info into old schemas).', 13),

        # ── Developmental Psychology ──────────────────────────────────────────
        ('Psychology', 'Developmental Psychology', 'easy',
         'Which theorist proposed the stages of cognitive development in children?',
         '["Sigmund Freud", "Erik Erikson", "Jean Piaget", "Lev Vygotsky"]', 2,
         'Jean Piaget described four stages of cognitive development: Sensorimotor, Preoperational, Concrete Operational, and Formal Operational.', 10),
        ('Psychology', 'Developmental Psychology', 'medium',
         'What is the "strange situation" experiment used to measure?',
         '["Children\'s reaction to strangers", "Quality of infant attachment to caregivers", "Object permanence", "Language development milestones"]', 1,
         'Mary Ainsworth\'s Strange Situation measures infant attachment style (secure, anxious, avoidant) by observing reactions to separation from and reunion with a caregiver.', 12),
        ('Psychology', 'Developmental Psychology', 'hard',
         'What is Vygotsky\'s "Zone of Proximal Development" (ZPD)?',
         '["The age range of optimal learning", "Tasks a child can do alone", "The gap between what a learner can do alone vs. with guidance", "Cognitive skills developed after age 12"]', 2,
         'The ZPD is the range of tasks a learner cannot yet do alone but can accomplish with skilled guidance — the sweet spot for learning (Vygotsky).', 14),
    ]


def _math_expanded_questions():
    return [
        # ── Algebra ──────────────────────────────────────────────────────────
        ('Math', 'Algebra', 'easy',
         'Solve for x: 5x - 10 = 20',
         '["x = 2", "x = 4", "x = 6", "x = 30"]', 2,
         '5x = 30, so x = 6.', 7),
        ('Math', 'Algebra', 'easy',
         'What is the y-intercept of y = 4x + 7?',
         '["4", "7", "-7", "0"]', 1,
         'In y = mx + b, the y-intercept is b = 7.', 7),
        ('Math', 'Algebra', 'easy',
         'Simplify: 3(x + 4) - 2x',
         '["x + 12", "x + 4", "5x + 12", "x + 7"]', 0,
         '3x + 12 - 2x = x + 12.', 7),
        ('Math', 'Algebra', 'easy',
         'Which of the following is the factored form of x^2 - 9?',
         '["(x-3)^2", "(x+3)(x-3)", "(x+9)(x-1)", "(x-9)(x+1)"]', 1,
         'x^2 - 9 is a difference of squares: (x+3)(x-3).', 7),
        ('Math', 'Algebra', 'easy',
         'Solve the inequality: 2x + 1 > 7',
         '["x > 3", "x > 4", "x > 6", "x < 3"]', 0,
         '2x > 6, so x > 3.', 7),
        ('Math', 'Algebra', 'easy',
         'What is the domain of f(x) = sqrt(x - 3)?',
         '["x > 3", "x >= 3", "x >= 0", "All real numbers"]', 1,
         'The radicand must be non-negative: x - 3 >= 0, so x >= 3.', 8),
        ('Math', 'Algebra', 'easy',
         'Evaluate: f(3) for f(x) = 2x^2 - x + 1',
         '["16", "18", "10", "14"]', 0,
         'f(3) = 2(9) - 3 + 1 = 18 - 3 + 1 = 16.', 7),
        ('Math', 'Algebra', 'easy',
         'What is the sum of the roots of x^2 - 5x + 6 = 0?',
         '["5", "6", "-5", "1"]', 0,
         'By Vieta\'s formulas, sum of roots = -b/a = 5.', 8),
        ('Math', 'Algebra', 'easy',
         'Simplify: (x^3)(x^4)',
         '["x^7", "x^12", "x^1", "2x^7"]', 0,
         'When multiplying powers with the same base, add exponents: x^(3+4) = x^7.', 7),
        ('Math', 'Algebra', 'easy',
         'What is the multiplicative inverse of 5?',
         '["5", "-5", "1/5", "0"]', 2,
         'The multiplicative inverse (reciprocal) of 5 is 1/5, since 5 * (1/5) = 1.', 6),
        ('Math', 'Algebra', 'medium',
         'Solve: x^2 - 7x + 12 = 0',
         '["x = 3 or x = 4", "x = -3 or x = -4", "x = 2 or x = 6", "x = 1 or x = 12"]', 0,
         'Factor: (x-3)(x-4) = 0, giving x = 3 or x = 4.', 9),
        ('Math', 'Algebra', 'medium',
         'Use the quadratic formula to solve 2x^2 + 3x - 2 = 0',
         '["x = 1/2 or x = -2", "x = 2 or x = -1/2", "x = -1 or x = 2", "x = 1 or x = -1"]', 0,
         'Discriminant = 9 + 16 = 25. x = (-3 +/- 5)/4, giving x = 1/2 or x = -2.', 10),
        ('Math', 'Algebra', 'medium',
         'Solve the system: 2x + y = 7 and x - y = 2',
         '["x=3, y=1", "x=2, y=3", "x=1, y=5", "x=4, y=-1"]', 0,
         'Add the equations: 3x = 9, x = 3. Substituting: y = 7 - 6 = 1.', 9),
        ('Math', 'Algebra', 'medium',
         'What is the solution set of |2x - 3| = 7?',
         '["x = 5 or x = -2", "x = 5 or x = 2", "x = -5 or x = 2", "x = 5"]', 0,
         'Solve 2x-3=7 (x=5) and 2x-3=-7 (x=-2). Both satisfy the original equation.', 9),
        ('Math', 'Algebra', 'medium',
         'Simplify: (2x^2 y^3)^3',
         '["8x^6 y^9", "6x^5 y^6", "8x^5 y^6", "2x^6 y^9"]', 0,
         '(2)^3 = 8, (x^2)^3 = x^6, (y^3)^3 = y^9, giving 8x^6 y^9.', 9),
        ('Math', 'Algebra', 'medium',
         'Factor completely: 6x^2 - 7x - 3',
         '["(2x - 3)(3x + 1)", "(3x + 1)(2x - 3)", "(6x + 1)(x - 3)", "(2x+1)(3x-3)"]', 0,
         'Factor: (2x - 3)(3x + 1) = 6x^2 + 2x - 9x - 3 = 6x^2 - 7x - 3. Correct.', 10),
        ('Math', 'Algebra', 'medium',
         'Simplify the rational expression: (x^2 - 4)/(x^2 - x - 2)',
         '["(x+2)/(x+1)", "(x-2)/(x-1)", "(x+2)/(x-1)", "(x-2)/(x+1)"]', 0,
         'Numerator: (x+2)(x-2). Denominator: (x-2)(x+1). Cancel (x-2): (x+2)/(x+1).', 10),
        ('Math', 'Algebra', 'medium',
         'Solve for x: log_2(x) = 5',
         '["x = 10", "x = 25", "x = 32", "x = 64"]', 2,
         'log_2(x) = 5 means 2^5 = x = 32.', 9),
        ('Math', 'Algebra', 'medium',
         'What is the common ratio of the geometric sequence 3, 6, 12, 24, ...?',
         '["2", "3", "6", "1/2"]', 0,
         'Each term is multiplied by 2: 6/3 = 12/6 = 24/12 = 2.', 8),
        ('Math', 'Algebra', 'medium',
         'What is (3 + 4i)(2 - i) where i = sqrt(-1)?',
         '["6 - 4i", "10 + 5i", "2 + 4i", "6 + 4i"]', 1,
         '(3+4i)(2-i) = 6 - 3i + 8i - 4i^2 = 6 + 5i + 4 = 10 + 5i.', 11),
        ('Math', 'Algebra', 'medium',
         'Find (f∘g)(x) if f(x) = 2x + 1 and g(x) = x^2',
         '["2x^2 + 1", "4x^2 + 1", "(2x+1)^2", "2x + x^2"]', 0,
         'f(g(x)) = f(x^2) = 2(x^2) + 1 = 2x^2 + 1.', 10),
        ('Math', 'Algebra', 'medium',
         'What is the sum of the first 10 terms of the arithmetic sequence 2, 5, 8, 11, ...?',
         '["155", "120", "110", "145"]', 0,
         'S_n = n/2*(2a + (n-1)d) = 10/2*(4 + 27) = 5*31 = 155.', 10),
        ('Math', 'Algebra', 'medium',
         'Simplify: ln(e^5)',
         '["5", "e^5", "5e", "1/5"]', 0,
         'ln and e are inverse functions, so ln(e^5) = 5.', 8),
        ('Math', 'Algebra', 'medium',
         'Solve for x: 3^(2x) = 81',
         '["x = 2", "x = 3", "x = 4", "x = 1"]', 0,
         '81 = 3^4, so 3^(2x) = 3^4 means 2x = 4, x = 2.', 9),
        ('Math', 'Algebra', 'medium',
         'What is the product of the roots of 3x^2 - 12x + 9 = 0?',
         '["3", "4", "9", "12"]', 0,
         'By Vieta\'s, product of roots = c/a = 9/3 = 3.', 9),
        ('Math', 'Algebra', 'hard',
         'Solve the system: x^2 + y^2 = 25 and y = x + 1',
         '["(3,4) and (-4,-3)", "(3,4) and (4,3)", "(0,5) and (4,5)", "(-3,-4) and (4,3)"]', 0,
         'Substitute y = x+1 into x^2+y^2=25: x^2+(x+1)^2=25, 2x^2+2x-24=0, x^2+x-12=0, (x+4)(x-3)=0. x=3,y=4 and x=-4,y=-3.', 12),
        ('Math', 'Algebra', 'hard',
         'Simplify: (x^2 - 5x + 6)/(x^2 - 9) * (x + 3)/(x - 2)',
         '["(x-3)/(x+3)", "(x-2)/(x+3)", "1", "(x+3)/(x-3)"]', 2,
         'Factor: (x-2)(x-3)/((x-3)(x+3)) * (x+3)/(x-2) = 1 after all cancellations.', 11),
        ('Math', 'Algebra', 'hard',
         'Solve: 2^(x+1) - 2^x = 16',
         '["x = 4", "x = 3", "x = 5", "x = 2"]', 0,
         '2^(x+1) - 2^x = 2*2^x - 2^x = 2^x = 16 = 2^4, so x = 4.', 11),
        ('Math', 'Algebra', 'hard',
         'What is the inverse function of f(x) = (2x - 3)/(x + 1)?',
         '["f^-1(x) = (x+3)/(2-x)", "f^-1(x) = (x-3)/(2-x)", "f^-1(x) = (x+3)/(x-2)", "f^-1(x) = (2x+3)/(1-x)"]', 0,
         'Set y=(2x-3)/(x+1), swap x and y: x(y+1)=2y-3, xy-2y=-3-x, y(x-2)=-(x+3), y=(x+3)/(2-x).', 12),
        ('Math', 'Algebra', 'hard',
         'Find all real roots of x^4 - 5x^2 + 4 = 0',
         '["x = ±1, x = ±2", "x = ±1, x = ±4", "x = ±2, x = ±4", "x = ±1"]', 0,
         'Let u = x^2: u^2 - 5u + 4 = 0, (u-1)(u-4)=0. u=1 gives x=±1; u=4 gives x=±2.', 12),
        ('Math', 'Algebra', 'hard',
         'The sum of an infinite geometric series is 12 and the first term is 4. What is the common ratio?',
         '["2/3", "1/2", "1/3", "3/4"]', 0,
         'S = a/(1-r): 12 = 4/(1-r), 1-r = 1/3, r = 2/3.', 12),
        ('Math', 'Algebra', 'hard',
         'If log_b(2) = 0.3010 and log_b(3) = 0.4771, what is log_b(12)?',
         '["1.0791", "0.7781", "1.1761", "0.8451"]', 0,
         'log_b(12) = log_b(4*3) = 2*log_b(2) + log_b(3) = 0.602 + 0.4771 = 1.0791.', 11),
        ('Math', 'Algebra', 'hard',
         'Solve: |3x + 1| > 8',
         '["x > 7/3 or x < -3", "x > 3 or x < -3", "x > 7/3 or x < -7/3", "-3 < x < 7/3"]', 0,
         '|3x+1|>8 means 3x+1>8 (x>7/3) or 3x+1<-8 (x<-3).', 11),
        ('Math', 'Algebra', 'hard',
         'Find the partial fraction decomposition of 5x/((x-1)(x+2))',
         '["5/3 * 1/(x-1) + 10/3 * 1/(x+2)", "1/(x-1) + 4/(x+2)", "5/(x-1) - 5/(x+2)", "2/(x-1) + 3/(x+2)"]', 0,
         'Set 5x = A(x+2)+B(x-1). x=1: 5=3A, A=5/3. x=-2: -10=-3B, B=10/3. Result: 5/(3(x-1)) + 10/(3(x+2)).', 12),
        ('Math', 'Algebra', 'hard',
         'What are the complex roots of x^2 + 4x + 13 = 0?',
         '["x = -2 ± 3i", "x = 2 ± 3i", "x = -4 ± 3i", "x = -2 ± 9i"]', 0,
         'Discriminant = 16 - 52 = -36. x = (-4 ± 6i)/2 = -2 ± 3i.', 11),
        ('Math', 'Algebra', 'hard',
         'Simplify: (1 + i)^8 where i = sqrt(-1)',
         '["16", "-16", "16i", "-16i"]', 0,
         '(1+i)^2 = 2i. (2i)^2 = -4. (-4)^2 = 16.', 12),
        ('Math', 'Algebra', 'hard',
         'Find the number of terms in the expansion of (a+b)^10 that are distinct',
         '["11", "10", "20", "100"]', 0,
         'The binomial expansion (a+b)^n has n+1 terms. For n=10, there are 11 terms.', 10),
        ('Math', 'Algebra', 'medium',
         'What is the vertex of the parabola y = 2(x - 3)^2 + 5?',
         '["(3, 5)", "(-3, 5)", "(3, -5)", "(-3, -5)"]', 0,
         'Vertex form y = a(x-h)^2 + k has vertex (h, k) = (3, 5).', 9),
        ('Math', 'Algebra', 'medium',
         'What is the remainder when 2x^3 - 3x^2 + x - 5 is divided by (x - 2)?',
         '["1", "-3", "3", "-1"]', 0,
         'By the Remainder Theorem, substitute x=2: 2(8) - 3(4) + 2 - 5 = 16 - 12 + 2 - 5 = 1.', 10),
        ('Math', 'Algebra', 'easy',
         'What is the slope of a horizontal line?',
         '["undefined", "1", "0", "-1"]', 2,
         'A horizontal line has zero rise over any run, so slope = 0.', 6),
        ('Math', 'Algebra', 'easy',
         'Which of the following is NOT a polynomial?',
         '["3x^2 + 2x - 1", "x^(1/2) + 1", "5x^3", "7"]', 1,
         'Polynomials require non-negative integer exponents. x^(1/2) is not a polynomial.', 7),
        ('Math', 'Algebra', 'medium',
         'If f(x) = x^2 - 3 and g(x) = 2x + 1, find g(f(x))',
         '["2x^2 - 5", "2x^2 - 3", "4x^2 + 4x - 2", "2x^2 - 2"]', 0,
         'g(f(x)) = 2(x^2-3) + 1 = 2x^2 - 6 + 1 = 2x^2 - 5.', 10),
        ('Math', 'Algebra', 'hard',
         'For the polynomial p(x) = x^3 - 6x^2 + 11x - 6, verify x=1 is a root and factor completely.',
         '["(x-1)(x-2)(x-3)", "(x+1)(x-2)(x-3)", "(x-1)^2(x-4)", "(x-1)(x^2-5x+6)"]', 0,
         'p(1) = 1-6+11-6 = 0. Divide by (x-1): x^2-5x+6 = (x-2)(x-3). Full factoring: (x-1)(x-2)(x-3).', 12),
        ('Math', 'Algebra', 'medium',
         'Solve: (x+2)/(x-1) = 3',
         '["x = 5/2", "x = 2", "x = 7/2", "x = 3/2"]', 0,
         'Cross-multiply: x+2 = 3(x-1) = 3x-3. 5 = 2x, x = 5/2.', 9),
        ('Math', 'Algebra', 'medium',
         'Expand: (x + 3)^3',
         '["x^3 + 9x^2 + 27x + 27", "x^3 + 6x^2 + 9x + 27", "x^3 + 27", "x^3 + 3x^2 + 3x + 27"]', 0,
         '(x+3)^3 = x^3 + 3(3)x^2 + 3(9)x + 27 = x^3 + 9x^2 + 27x + 27.', 10),
        ('Math', 'Algebra', 'hard',
         'What is the sum of an infinite geometric series with a=8 and r=1/4?',
         '["32/3", "10", "32", "8/3"]', 0,
         'S = a/(1-r) = 8/(1-1/4) = 8/(3/4) = 32/3.', 11),
        ('Math', 'Algebra', 'medium',
         'Factor: 12x^2 - 27',
         '["3(2x-3)(2x+3)", "3(4x^2-9)", "(4x-9)(3x+3)", "12(x^2-9/4)"]', 0,
         '12x^2 - 27 = 3(4x^2 - 9) = 3(2x-3)(2x+3).', 9),
        ('Math', 'Algebra', 'easy',
         'What is the axis of symmetry for y = x^2 - 6x + 5?',
         '["x = 3", "x = -3", "x = 5", "x = 6"]', 0,
         'Axis of symmetry: x = -b/(2a) = -(-6)/(2*1) = 3.', 8),
        ('Math', 'Algebra', 'medium',
         'Solve: 4^x = 8',
         '["x = 3/2", "x = 2", "x = 1/2", "x = 2/3"]', 0,
         '4^x = 2^(2x) and 8 = 2^3. So 2x = 3, x = 3/2.', 10),
        ('Math', 'Algebra', 'hard',
         'Find the inverse of f(x) = e^(2x-1)',
         '["f^-1(x) = (ln(x)+1)/2", "f^-1(x) = ln(x+1)/2", "f^-1(x) = (ln(x)-1)/2", "f^-1(x) = ln(x/2)+1"]', 0,
         'y = e^(2x-1), swap: x = e^(2y-1), ln(x) = 2y-1, y = (ln(x)+1)/2.', 11),
        ('Math', 'Algebra', 'medium',
         'What does the discriminant b^2 - 4ac < 0 tell us about the roots?',
         '["Two equal real roots", "Two distinct real roots", "Two complex (non-real) roots", "One real and one complex root"]', 2,
         'A negative discriminant means the square root is imaginary, giving two complex conjugate roots.', 9),

        # ── Arithmetic ───────────────────────────────────────────────────────
        ('Math', 'Arithmetic', 'easy',
         'What is 3/4 + 1/6?',
         '["9/12", "11/12", "4/10", "5/9"]', 1,
         'LCD = 12. 9/12 + 2/12 = 11/12.', 6),
        ('Math', 'Arithmetic', 'easy',
         'Convert 0.375 to a fraction in simplest form.',
         '["3/8", "3/7", "37/100", "1/3"]', 0,
         '0.375 = 375/1000 = 3/8.', 6),
        ('Math', 'Arithmetic', 'easy',
         'What is 40% of 150?',
         '["50", "60", "55", "70"]', 1,
         '0.40 * 150 = 60.', 6),
        ('Math', 'Arithmetic', 'easy',
         'Evaluate: 5 + 3 * 4 - 2^2',
         '["48", "13", "52", "24"]', 1,
         'PEMDAS: 2^2=4, 3*4=12, then 5+12-4=13.', 6),
        ('Math', 'Arithmetic', 'easy',
         'What is the GCF of 36 and 48?',
         '["6", "8", "12", "4"]', 2,
         'Factors of 36: 1,2,3,4,6,9,12,18,36. Factors of 48: 1,2,3,4,6,8,12,16,24,48. GCF = 12.', 6),
        ('Math', 'Arithmetic', 'easy',
         'What is the LCM of 4 and 6?',
         '["8", "10", "12", "24"]', 2,
         'LCM(4,6) = 12 since 12 is the smallest number divisible by both 4 and 6.', 6),
        ('Math', 'Arithmetic', 'easy',
         'Which of the following is a prime number?',
         '["51", "57", "59", "55"]', 2,
         '59 is prime. 51=3*17, 55=5*11, 57=3*19.', 6),
        ('Math', 'Arithmetic', 'easy',
         'What is 2.5 * 10^3 in standard notation?',
         '["250", "2500", "25000", "0.0025"]', 1,
         '2.5 * 10^3 = 2500.', 6),
        ('Math', 'Arithmetic', 'easy',
         'Simplify: (-3) * (-4) * 2',
         '["24", "-24", "12", "-12"]', 0,
         '(-3)*(-4) = 12, then 12*2 = 24.', 6),
        ('Math', 'Arithmetic', 'easy',
         'A ratio of 3:5 means that for every 3 parts of A there are 5 parts of B. If A = 12, what is B?',
         '["15", "18", "20", "25"]', 2,
         '3/5 = 12/B, B = 12*5/3 = 20.', 7),
        ('Math', 'Arithmetic', 'medium',
         'What is the prime factorization of 360?',
         '["2^3 * 3^2 * 5", "2^2 * 3^2 * 5^2", "2^3 * 3 * 5^2", "2^3 * 3^2 * 5^2"]', 0,
         '360 = 8 * 45 = 2^3 * 3^2 * 5.', 8),
        ('Math', 'Arithmetic', 'medium',
         'Express 0.00045 in scientific notation.',
         '["4.5 * 10^-4", "4.5 * 10^4", "45 * 10^-5", "0.45 * 10^-3"]', 0,
         '0.00045 = 4.5 * 10^-4.', 7),
        ('Math', 'Arithmetic', 'medium',
         'A car travels 150 miles on 6 gallons of gas. How many miles per gallon does it get?',
         '["20", "25", "30", "15"]', 1,
         '150/6 = 25 miles per gallon.', 7),
        ('Math', 'Arithmetic', 'medium',
         'What percentage is 45 out of 180?',
         '["20%", "25%", "30%", "15%"]', 1,
         '45/180 = 1/4 = 25%.', 7),
        ('Math', 'Arithmetic', 'medium',
         'Evaluate: (2^3 + 4) / (3^2 - 5)',
         '["3", "2", "6", "1"]', 0,
         '(8 + 4) / (9 - 5) = 12/4 = 3.', 7),
        ('Math', 'Arithmetic', 'medium',
         'Convert 3 hours 45 minutes to minutes.',
         '["215", "225", "235", "245"]', 1,
         '3 * 60 + 45 = 180 + 45 = 225 minutes.', 6),
        ('Math', 'Arithmetic', 'medium',
         'What is the reciprocal of 7/11?',
         '["7/11", "11/7", "1/77", "77"]', 1,
         'The reciprocal of 7/11 is 11/7.', 6),
        ('Math', 'Arithmetic', 'medium',
         'Simplify: 5/6 ÷ 2/3',
         '["5/4", "10/18", "5/9", "15/12"]', 0,
         '5/6 ÷ 2/3 = 5/6 * 3/2 = 15/12 = 5/4.', 7),
        ('Math', 'Arithmetic', 'medium',
         'How many meters are in 2.5 kilometers?',
         '["25", "250", "2500", "25000"]', 2,
         '1 kilometer = 1000 meters, so 2.5 km = 2500 meters.', 6),
        ('Math', 'Arithmetic', 'medium',
         'What is 7! (7 factorial)?',
         '["720", "5040", "40320", "2520"]', 1,
         '7! = 7*6*5*4*3*2*1 = 5040.', 8),
        ('Math', 'Arithmetic', 'hard',
         'A number is divisible by 9 if and only if the sum of its digits is divisible by 9. Is 738,594 divisible by 9?',
         '["Yes, digit sum = 36", "No, digit sum = 36", "Yes, digit sum = 27", "No, digit sum = 30"]', 0,
         '7+3+8+5+9+4 = 36. 36/9 = 4. Yes, divisible by 9.', 9),
        ('Math', 'Arithmetic', 'hard',
         'What is 1.2 * 10^5 / (3 * 10^2) in scientific notation?',
         '["4 * 10^2", "4 * 10^3", "0.4 * 10^3", "4 * 10^-2"]', 0,
         '1.2/3 = 0.4, 10^5/10^2 = 10^3. 0.4 * 10^3 = 4 * 10^2.', 9),
        ('Math', 'Arithmetic', 'hard',
         'Find the number of positive integers less than 100 that are divisible by neither 3 nor 5.',
         '["53", "47", "51", "57"]', 0,
         'By inclusion-exclusion: 100 - 33 - 20 + 6 = 53. Subtract 1 for 100 itself if we want < 100: count up to 99 gives 33+19-6 = 46 divisible by 3 or 5, so 99-46 = 53.', 11),
        ('Math', 'Arithmetic', 'hard',
         'If x:y = 3:4 and y:z = 6:7, what is x:z?',
         '["9:14", "3:7", "18:28", "9:7"]', 0,
         'x:y = 3:4, y:z = 6:7. Scale: x:y:z = 18:24:28 = 9:12:14. So x:z = 9:14.', 11),
        ('Math', 'Arithmetic', 'hard',
         'What is the sum of all prime factors of 2520?',
         '["12", "14", "17", "10"]', 2,
         '2520 = 2^3 * 3^2 * 5 * 7. Distinct prime factors: 2,3,5,7. Sum = 2+3+5+7 = 17.', 10),
        ('Math', 'Arithmetic', 'medium',
         'What is the value of (-2)^5?',
         '["-32", "32", "-10", "10"]', 0,
         '(-2)^5 = -32 (odd power of negative number is negative).', 7),
        ('Math', 'Arithmetic', 'medium',
         'If a shirt costs $48 after a 20% discount, what was the original price?',
         '["$56", "$58", "$60", "$64"]', 2,
         '0.80 * original = 48, original = 48/0.80 = $60.', 8),
        ('Math', 'Arithmetic', 'easy',
         'What is the absolute value of -7.5?',
         '["-7.5", "7.5", "0", "-1"]', 1,
         'The absolute value is the distance from zero, so |-7.5| = 7.5.', 5),
        ('Math', 'Arithmetic', 'medium',
         'What is the least common multiple of 12, 15, and 20?',
         '["60", "30", "120", "180"]', 0,
         'LCM(12,15)=60, LCM(60,20)=60. LCM = 60.', 8),
        ('Math', 'Arithmetic', 'hard',
         'A population increases by 10% each year. After 3 years, what is the total percentage increase?',
         '["30%", "33.1%", "30.3%", "33.3%"]', 1,
         '1.10^3 = 1.331, so the total percentage increase is 33.1%.', 10),
        ('Math', 'Arithmetic', 'medium',
         'Convert 5/8 to a decimal.',
         '["0.575", "0.625", "0.65", "0.6"]', 1,
         '5 ÷ 8 = 0.625.', 6),
        ('Math', 'Arithmetic', 'medium',
         'What is 3.75 as a fraction in lowest terms?',
         '["375/100", "15/4", "7/2", "15/3"]', 1,
         '3.75 = 375/100 = 15/4.', 7),
        ('Math', 'Arithmetic', 'easy',
         'What is the result of -15 + 23 - 7?',
         '["1", "-1", "0", "31"]', 0,
         '-15 + 23 = 8; 8 - 7 = 1.', 5),
        ('Math', 'Arithmetic', 'medium',
         'In how many ways can you arrange the letters in "CAT"?',
         '["3", "6", "9", "12"]', 1,
         '3 letters can be arranged in 3! = 6 ways.', 8),
        ('Math', 'Arithmetic', 'hard',
         'What is the HCF of 196 and 294?',
         '["49", "98", "14", "42"]', 1,
         '196 = 2^2 * 7^2, 294 = 2 * 3 * 7^2. HCF = 2 * 7^2 = 98.', 10),
        ('Math', 'Arithmetic', 'medium',
         'Evaluate: (16)^(3/4)',
         '["4", "8", "12", "6"]', 1,
         '16^(3/4) = (16^(1/4))^3 = 2^3 = 8.', 9),
        ('Math', 'Arithmetic', 'medium',
         'A recipe calls for 2.5 cups of flour. If you want to make 1.5 times the recipe, how many cups do you need?',
         '["3.5", "3.75", "4", "4.5"]', 1,
         '2.5 * 1.5 = 3.75 cups.', 7),

        # ── Calculus ─────────────────────────────────────────────────────────
        ('Math', 'Calculus', 'easy',
         'What is lim(x->2) of (x^2 - 4)/(x - 2)?',
         '["0", "2", "4", "undefined"]', 2,
         'Factor: (x^2-4)/(x-2) = (x+2)(x-2)/(x-2) = x+2. As x->2, the limit is 4.', 10),
        ('Math', 'Calculus', 'easy',
         'What is the derivative of f(x) = 5x^3?',
         '["5x^2", "15x^2", "15x^3", "3x^2"]', 1,
         'Power rule: d/dx(5x^3) = 5 * 3 * x^(3-1) = 15x^2.', 10),
        ('Math', 'Calculus', 'easy',
         'What is the integral of 6x^2 dx?',
         '["3x^2 + C", "2x^3 + C", "6x^3 + C", "12x + C"]', 1,
         'integral of 6x^2 = 6*x^3/3 + C = 2x^3 + C.', 10),
        ('Math', 'Calculus', 'easy',
         'What is the derivative of sin(x)?',
         '["cos(x)", "-cos(x)", "-sin(x)", "tan(x)"]', 0,
         'd/dx(sin x) = cos x.', 9),
        ('Math', 'Calculus', 'easy',
         'What is the derivative of e^x?',
         '["x*e^(x-1)", "e^x", "e^(x-1)", "ln(x)*e^x"]', 1,
         'e^x is its own derivative: d/dx(e^x) = e^x.', 9),
        ('Math', 'Calculus', 'easy',
         'Evaluate the definite integral from 0 to 1 of 3x^2 dx.',
         '["0", "1", "3", "1/3"]', 1,
         'Antiderivative is x^3. Evaluating from 0 to 1: 1^3 - 0^3 = 1.', 10),
        ('Math', 'Calculus', 'medium',
         'Find d/dx of (x^2 * sin(x)) using the product rule.',
         '["2x*sin(x) + x^2*cos(x)", "2x*cos(x)", "x^2*cos(x)", "2x*sin(x)"]', 0,
         'Product rule: f\'g + fg\' = 2x*sin(x) + x^2*cos(x).', 11),
        ('Math', 'Calculus', 'medium',
         'Find d/dx of (x^2 + 1)^5 using the chain rule.',
         '["5(x^2+1)^4", "10x(x^2+1)^4", "5x(x^2+1)^4", "10(x^2+1)^4"]', 1,
         'Chain rule: 5(x^2+1)^4 * 2x = 10x(x^2+1)^4.', 11),
        ('Math', 'Calculus', 'medium',
         'Find d/dx of (sin x)/(x) using the quotient rule.',
         '["(x*cos(x) - sin(x))/x^2", "(cos(x) + sin(x))/x^2", "cos(x)/x", "(x*cos(x) + sin(x))/x^2"]', 0,
         'Quotient rule: (x*cos(x) - sin(x)*1)/x^2 = (x*cos(x) - sin(x))/x^2.', 11),
        ('Math', 'Calculus', 'medium',
         'What is lim(x->0) of sin(x)/x?',
         '["0", "1", "infinity", "pi"]', 1,
         'This is a standard limit: lim(x->0) sin(x)/x = 1.', 10),
        ('Math', 'Calculus', 'medium',
         'What is the second derivative of f(x) = x^4 - 3x^2?',
         '["12x^2 - 6", "4x^3 - 6x", "x^3 - 6x", "12x^2 - 3"]', 0,
         'f\'(x) = 4x^3 - 6x. f\'\'(x) = 12x^2 - 6.', 11),
        ('Math', 'Calculus', 'medium',
         'Find the critical points of f(x) = x^3 - 3x + 2.',
         '["x = 1 and x = -1", "x = 0", "x = 3 and x = -3", "x = 1"]', 0,
         'f\'(x) = 3x^2 - 3 = 0 gives x^2 = 1, so x = 1 and x = -1.', 11),
        ('Math', 'Calculus', 'medium',
         'Evaluate: integral of (1/x) dx',
         '["x + C", "ln|x| + C", "1/x^2 + C", "-1/x^2 + C"]', 1,
         'integral of 1/x = ln|x| + C.', 10),
        ('Math', 'Calculus', 'medium',
         'What is the integral of cos(x) dx?',
         '["sin(x) + C", "-sin(x) + C", "cos(x) + C", "-cos(x) + C"]', 0,
         'integral of cos(x) = sin(x) + C.', 9),
        ('Math', 'Calculus', 'medium',
         'Using substitution, evaluate the integral of 2x*(x^2+1)^3 dx.',
         '["(x^2+1)^4/2 + C", "(x^2+1)^4/4 + C", "2(x^2+1)^4 + C", "(x^2+1)^4 + C"]', 1,
         'Let u = x^2+1, du = 2x dx. Integral becomes u^3 du = u^4/4 + C = (x^2+1)^4/4 + C.', 11),
        ('Math', 'Calculus', 'medium',
         'What does it mean for a function to be continuous at a point x = c?',
         '["f(c) exists and f\'(c) exists", "The limit as x->c equals f(c) and f(c) is defined", "f is differentiable at c", "f(c) = 0"]', 1,
         'Continuity at c requires: f(c) is defined, lim(x->c) f(x) exists, and they are equal.', 10),
        ('Math', 'Calculus', 'medium',
         'What is the area between y = x^2 and y = x from x = 0 to x = 1?',
         '["1/3", "1/6", "1/2", "1"]', 1,
         'Area = integral from 0 to 1 of (x - x^2) dx = [x^2/2 - x^3/3] from 0 to 1 = 1/2 - 1/3 = 1/6.', 12),
        ('Math', 'Calculus', 'hard',
         'Use L\'Hopital\'s rule to evaluate lim(x->0) (e^x - 1)/x.',
         '["0", "1", "infinity", "e"]', 1,
         'L\'Hopital: differentiate top and bottom. lim(x->0) e^x / 1 = e^0 = 1.', 12),
        ('Math', 'Calculus', 'hard',
         'Evaluate the integral of x*e^x dx using integration by parts.',
         '["e^x(x+1) + C", "e^x(x-1) + C", "x*e^x + C", "e^x/x + C"]', 1,
         'Let u=x, dv=e^x dx. Then du=dx, v=e^x. IBP: x*e^x - integral of e^x dx = x*e^x - e^x + C = e^x(x-1) + C.', 12),
        ('Math', 'Calculus', 'hard',
         'Find the volume of the solid generated by rotating y = sqrt(x) from x=0 to x=4 around the x-axis.',
         '["8*pi", "16*pi", "4*pi", "2*pi"]', 0,
         'V = pi * integral from 0 to 4 of (sqrt(x))^2 dx = pi * integral of x dx = pi * [x^2/2] from 0 to 4 = pi*8 = 8*pi.', 13),
        ('Math', 'Calculus', 'hard',
         'What is the Taylor series of e^x centered at x=0?',
         '["sum(x^n/n!, n=0 to inf)", "sum((-1)^n*x^n/n!, n=0 to inf)", "sum(x^n/(2n)!, n=0 to inf)", "sum(x^(2n)/n!, n=0 to inf)"]', 0,
         'The Maclaurin (Taylor at 0) series for e^x = sum from n=0 to inf of x^n/n! = 1+x+x^2/2!+x^3/3!+...', 13),
        ('Math', 'Calculus', 'hard',
         'Find the arc length of y = x^(3/2) from x=0 to x=4.',
         '["(8/27)(10*sqrt(10) - 1)", "8", "(8/27)*10*sqrt(10)", "4*sqrt(17)"]', 0,
         'Arc length = integral of sqrt(1+(dy/dx)^2) dx. dy/dx = 3*sqrt(x)/2. 1+(3sqrt(x)/2)^2 = 1+9x/4. Evaluate from 0 to 4.', 13),
        ('Math', 'Calculus', 'hard',
         'Evaluate the improper integral of e^(-x) from 0 to infinity.',
         '["0", "1", "infinity", "1/e"]', 1,
         'integral from 0 to inf of e^(-x) dx = [-e^(-x)] from 0 to inf = 0 - (-1) = 1.', 12),
        ('Math', 'Calculus', 'hard',
         'What is the Maclaurin series of sin(x)?',
         '["x - x^3/3! + x^5/5! - ...", "1 - x^2/2! + x^4/4! - ...", "x + x^3/3! + x^5/5! + ...", "1 + x + x^2/2! + ..."]', 0,
         'sin(x) = x - x^3/3! + x^5/5! - ... = sum from n=0 to inf of (-1)^n * x^(2n+1)/(2n+1)!.', 12),
        ('Math', 'Calculus', 'hard',
         'Use implicit differentiation to find dy/dx for x^2 + y^2 = 25.',
         '["dy/dx = -x/y", "dy/dx = x/y", "dy/dx = -y/x", "dy/dx = 2x/2y"]', 0,
         'Differentiate both sides: 2x + 2y(dy/dx) = 0. Solving: dy/dx = -x/y.', 11),
        ('Math', 'Calculus', 'hard',
         'A ladder 10 ft long leans against a wall. If the bottom slides away at 2 ft/s, how fast is the top sliding down when the bottom is 6 ft from the wall?',
         '["1.5 ft/s", "2 ft/s", "3/2 ft/s", "3 ft/s"]', 0,
         'x^2+y^2=100. 2x(dx/dt)+2y(dy/dt)=0. When x=6, y=8. 2(6)(2)+2(8)(dy/dt)=0. dy/dt = -24/16 = -3/2. Speed = 3/2 ft/s.', 13),
        ('Math', 'Calculus', 'medium',
         'What is the derivative of ln(x^2 + 1)?',
         '["1/(x^2+1)", "2x/(x^2+1)", "x/(x^2+1)", "2/(x^2+1)"]', 1,
         'Chain rule: d/dx(ln(u)) = (1/u)*u\'. Here u = x^2+1, u\' = 2x. Result: 2x/(x^2+1).', 11),
        ('Math', 'Calculus', 'medium',
         'Find the local minimum of f(x) = x^2 - 4x + 5.',
         '["x = 2, f(2) = 1", "x = 2, f(2) = 5", "x = 4, f(4) = 5", "x = 0, f(0) = 5"]', 0,
         'f\'(x) = 2x-4 = 0 at x=2. f(2) = 4-8+5 = 1. f\'\'(x)=2>0, so x=2 is a local minimum.', 11),
        ('Math', 'Calculus', 'medium',
         'Evaluate the definite integral from 1 to 3 of (2x+1) dx.',
         '["10", "8", "12", "6"]', 0,
         '[x^2+x] from 1 to 3 = (9+3)-(1+1) = 12-2 = 10.', 10),
        ('Math', 'Calculus', 'hard',
         'What is the radius of convergence of the power series sum(n=0 to inf) of x^n/2^n?',
         '["R = 1", "R = 2", "R = 1/2", "R = infinity"]', 1,
         'Ratio test: |a_(n+1)/a_n| = |x/2| < 1 requires |x| < 2. So R = 2.', 12),
        ('Math', 'Calculus', 'medium',
         'If f(x) = x^2 - 4, on which interval is f increasing?',
         '["(-infinity, 0)", "(0, infinity)", "(-2, 2)", "(-infinity, 2)"]', 1,
         'f\'(x) = 2x > 0 when x > 0. So f is increasing on (0, infinity).', 10),
        ('Math', 'Calculus', 'hard',
         'Evaluate: integral of sin^2(x) dx',
         '["x/2 - sin(2x)/4 + C", "x/2 + sin(2x)/4 + C", "-cos(2x)/2 + C", "sin(2x)/2 + C"]', 0,
         'Use identity sin^2(x) = (1-cos(2x))/2. Integral = x/2 - sin(2x)/4 + C.', 12),
        ('Math', 'Calculus', 'medium',
         'What is the Fundamental Theorem of Calculus (Part 1)?',
         '["If F is an antiderivative of f, then the definite integral of f from a to b is F(b)-F(a)", "Every continuous function has an antiderivative", "d/dx of integral from a to x of f(t)dt = f(x)", "The integral of a constant is a constant"]', 2,
         'FTC Part 1: If F(x) = integral from a to x of f(t)dt, then F\'(x) = f(x). Part 2 relates definite integrals to antiderivatives.', 12),
        ('Math', 'Calculus', 'medium',
         'Find the inflection point of f(x) = x^3 - 3x^2 + 2.',
         '["x = 1", "x = 2", "x = 0", "x = -1"]', 0,
         'f\'\'(x) = 6x - 6 = 0 at x = 1. Check sign change: f\'\'(x) changes from negative to positive at x=1.', 11),

        # ── Differential Equations ────────────────────────────────────────────
        ('Math', 'Differential Equations', 'easy',
         'What is a separable differential equation?',
         '["One that can be written as dy/dx = f(x)g(y)", "One with constant coefficients", "One where y\'\'=0", "An equation with no solution"]', 0,
         'A separable ODE can be written as dy/dx = f(x)g(y), allowing separation and integration of each side.', 10),
        ('Math', 'Differential Equations', 'easy',
         'Solve dy/dx = y, y(0) = 1.',
         '["y = e^(-x)", "y = e^x", "y = x", "y = x^2"]', 1,
         'Separate: dy/y = dx. Integrate: ln|y| = x + C. With y(0)=1: C=0, so y = e^x.', 10),
        ('Math', 'Differential Equations', 'easy',
         'What order is the ODE d^2y/dx^2 + 3y = 0?',
         '["First order", "Second order", "Third order", "Zero order"]', 1,
         'The order is the highest derivative present. Here the highest is d^2y/dx^2, so it is second order.', 9),
        ('Math', 'Differential Equations', 'easy',
         'What is the integrating factor for dy/dx + P(x)y = Q(x)?',
         '["e^(integral of P dx)", "P(x)", "e^(P(x))", "1/Q(x)"]', 0,
         'For a linear first-order ODE dy/dx + P(x)y = Q(x), the integrating factor is mu = e^(integral of P dx).', 10),
        ('Math', 'Differential Equations', 'medium',
         'Solve dy/dx = x/y with y(0) = 3.',
         '["y^2 = x^2 + 9", "y = x + 3", "y = sqrt(x^2+9)", "y^2 = x + 9"]', 2,
         'Separate: y dy = x dx. Integrate: y^2/2 = x^2/2 + C. y(0)=3: 9/2=C. y^2 = x^2+9, y = sqrt(x^2+9).', 11),
        ('Math', 'Differential Equations', 'medium',
         'Find the general solution of y\' + 2y = 6.',
         '["y = 3 + Ce^(-2x)", "y = 3 + Ce^(2x)", "y = Ce^(-2x)", "y = 6x + Ce^(-2x)"]', 0,
         'Integrating factor: e^(2x). d/dx(e^(2x)y) = 6e^(2x). y = 3 + Ce^(-2x).', 11),
        ('Math', 'Differential Equations', 'medium',
         'What is the characteristic equation for y\'\' - 4y\' + 3y = 0?',
         '["r^2 - 4r + 3 = 0", "r^2 + 4r - 3 = 0", "r^2 - 4r - 3 = 0", "r - 4 + 3 = 0"]', 0,
         'Substitute y = e^(rx): r^2 - 4r + 3 = 0, which gives (r-1)(r-3) = 0, r = 1 or r = 3.', 11),
        ('Math', 'Differential Equations', 'medium',
         'Solve y\'\' - 4y\' + 3y = 0.',
         '["y = C1*e^x + C2*e^(3x)", "y = C1*e^(-x) + C2*e^(-3x)", "y = C1 + C2*e^(3x)", "y = (C1+C2*x)*e^(3x)"]', 0,
         'Characteristic equation: (r-1)(r-3)=0, roots r=1 and r=3. General solution: y = C1*e^x + C2*e^(3x).', 11),
        ('Math', 'Differential Equations', 'medium',
         'What is the form of a particular solution for y\'\' + y = 3x using undetermined coefficients?',
         '["y_p = Ax + B", "y_p = Ax^2 + Bx", "y_p = A*sin(x) + B*cos(x)", "y_p = Ae^x + B"]', 0,
         'For a polynomial forcing function 3x (degree 1), the particular solution guess is y_p = Ax + B.', 11),
        ('Math', 'Differential Equations', 'medium',
         'What does it mean for a differential equation to be exact?',
         '["M dx + N dy = 0 where dM/dy = dN/dx", "The solution can be found by separation", "The ODE has only constant coefficients", "The solution is unique"]', 0,
         'An ODE M dx + N dy = 0 is exact if dM/dy = dN/dx, meaning there exists F with dF/dx=M and dF/dy=N.', 12),
        ('Math', 'Differential Equations', 'hard',
         'Solve the Bernoulli equation dy/dx + y = y^2.',
         '["y = 1/(1 - Ce^x)", "y = Ce^x/(1+Ce^x)", "y = e^x/(C + e^x)", "y = 1/(Ce^(-x) - 1)"]', 2,
         'Let v = y^(1-2) = 1/y. Then dv/dx = -v + 1, linear. Solution v = 1 + Ce^(-x), so y = 1/v = e^x/(e^x + C).', 13),
        ('Math', 'Differential Equations', 'hard',
         'Find the Laplace transform of f(t) = e^(at).',
         '["1/(s-a) for s>a", "1/(s+a)", "a/(s^2+a^2)", "s/(s^2-a^2)"]', 0,
         'L{e^(at)} = integral from 0 to inf of e^(at)*e^(-st) dt = 1/(s-a), valid for s > a.', 12),
        ('Math', 'Differential Equations', 'hard',
         'What is the Laplace transform of sin(bt)?',
         '["b/(s^2+b^2)", "s/(s^2+b^2)", "b/(s^2-b^2)", "1/(s^2+b^2)"]', 0,
         'L{sin(bt)} = b/(s^2 + b^2).', 12),
        ('Math', 'Differential Equations', 'hard',
         'Solve y\'\' + 4y = 0 with y(0) = 1 and y\'(0) = 2.',
         '["y = cos(2x) + sin(2x)", "y = cos(2x) + 2*sin(2x)", "y = 2*cos(2x) + sin(2x)", "y = e^(2x) + e^(-2x)"]', 0,
         'Characteristic roots: r^2+4=0, r=±2i. General solution: y = C1*cos(2x)+C2*sin(2x). y(0)=1: C1=1. y\'(0)=2: 2*C2=2, C2=1.', 12),
        ('Math', 'Differential Equations', 'hard',
         'For y\'\' + 2y\' + y = 0, what type of damping occurs and what is the general solution?',
         '["Critically damped; y=(C1+C2*x)*e^(-x)", "Overdamped; y=C1*e^(-x)+C2*e^(-2x)", "Underdamped; y=e^(-x)(C1*cos(x)+C2*sin(x))", "Undamped; y=C1+C2*x"]', 0,
         'Characteristic: (r+1)^2=0, repeated root r=-1. Critically damped. General solution: y=(C1+C2*x)*e^(-x).', 13),
        ('Math', 'Differential Equations', 'medium',
         'Using variation of parameters, what is the formula for a particular solution y_p of y\'\'+P(x)y\'+Q(x)y=g(x)?',
         '["y_p = -y1*int(y2*g/W)dx + y2*int(y1*g/W)dx", "y_p = y1*int(y2*g)dx - y2*int(y1*g)dx", "y_p = (1/W)*int(g*dx)", "y_p = g(x)/(P+Q)"]', 0,
         'Variation of parameters gives y_p = -y1*(integral of y2*g/W dx) + y2*(integral of y1*g/W dx), where W is the Wronskian.', 13),
        ('Math', 'Differential Equations', 'medium',
         'Solve dy/dx = (y/x) + 1 using the substitution v = y/x.',
         '["y = x*(ln|x| + C)", "y = x*ln|x| + C", "y = x^2 + Cx", "y = C*x + x*ln|x|"]', 0,
         'Let y=vx: v + x*dv/dx = v + 1. x*dv/dx = 1. dv = dx/x. v = ln|x|+C. y = x*(ln|x|+C).', 12),
        ('Math', 'Differential Equations', 'hard',
         'What is the inverse Laplace transform of 1/(s^2+4)?',
         '["sin(2t)/2", "cos(2t)", "sin(2t)", "e^(-2t)"]', 0,
         'L^-1{b/(s^2+b^2)} = sin(bt). Here b=2: L^-1{2/(s^2+4)} = sin(2t). So L^-1{1/(s^2+4)} = sin(2t)/2.', 12),
        ('Math', 'Differential Equations', 'hard',
         'Use Euler\'s method with h=0.1 to approximate y(0.1) for dy/dx = x + y, y(0) = 1.',
         '["1.1", "1.2", "1.15", "1.05"]', 0,
         'y(0.1) ≈ y(0) + h*f(0,1) = 1 + 0.1*(0+1) = 1 + 0.1 = 1.1.', 11),
        ('Math', 'Differential Equations', 'medium',
         'What is the general solution of dy/dx = ky (exponential growth/decay)?',
         '["y = C*e^(kx)", "y = kx + C", "y = C*x^k", "y = ln(kx) + C"]', 0,
         'Separating: dy/y = k dx, integrate: ln|y| = kx + C0, so y = C*e^(kx).', 10),
        ('Math', 'Differential Equations', 'hard',
         'Solve the system: x\' = 2x + y, y\' = x + 2y.',
         '["x=C1*e^(3t)+C2*e^t; y=C1*e^(3t)-C2*e^t", "x=C1*e^(3t); y=C2*e^t", "x=(C1+C2)*e^(3t); y=(C1-C2)*e^t", "x=e^(2t)(C1+C2*t); y=e^(2t)(C1-C2*t)"]', 0,
         'Matrix [[2,1],[1,2]] has eigenvalues 3 and 1, eigenvectors (1,1) and (1,-1). Solution as stated.', 13),
        ('Math', 'Differential Equations', 'medium',
         'What is the criterion for an ODE M dx + N dy = 0 to be exact?',
         '["dM/dy = dN/dx", "dM/dx = dN/dy", "M = N", "M*N = constant"]', 0,
         'An equation M dx + N dy = 0 is exact when the mixed partial derivatives are equal: dM/dy = dN/dx.', 11),
        ('Math', 'Differential Equations', 'hard',
         'Find the particular solution of y\'\' - y\' = e^x using undetermined coefficients.',
         '["y_p = x*e^x", "y_p = x^2*e^x/2", "y_p = e^x", "y_p = x*e^x/2"]', 0,
         'Since e^x solves the homogeneous (r=1 is a root of r^2-r=0), multiply by x: y_p = Ax*e^x. Substituting gives A=1.', 13),
        ('Math', 'Differential Equations', 'medium',
         'What type of ODE is xy\' + y = x^2?',
         '["Separable", "Linear first-order", "Bernoulli", "Exact"]', 1,
         'Rewrite as y\' + (1/x)y = x. This is a linear first-order ODE with P(x)=1/x and Q(x)=x.', 10),
        ('Math', 'Differential Equations', 'easy',
         'What is the equilibrium solution of dy/dt = 3y - 6?',
         '["y = 1", "y = 2", "y = 3", "y = 6"]', 1,
         'Equilibrium solutions occur when dy/dt = 0: 3y - 6 = 0, y = 2.', 9),
        ('Math', 'Differential Equations', 'medium',
         'Solve the initial value problem dy/dx = 2x, y(0) = 5.',
         '["y = x^2 + 5", "y = 2x + 5", "y = x^2 - 5", "y = 2x^2 + 5"]', 0,
         'Integrate: y = x^2 + C. Apply y(0)=5: C=5. So y = x^2 + 5.', 9),

        # ── Linear Algebra ────────────────────────────────────────────────────
        ('Math', 'Linear Algebra', 'easy',
         'What is the dot product of vectors (1, 2, 3) and (4, 5, 6)?',
         '["30", "32", "28", "32"]', 1,
         '1*4 + 2*5 + 3*6 = 4 + 10 + 18 = 32.', 9),
        ('Math', 'Linear Algebra', 'easy',
         'What is the magnitude of vector (3, 4)?',
         '["5", "7", "sqrt(7)", "25"]', 0,
         '|v| = sqrt(3^2 + 4^2) = sqrt(9+16) = sqrt(25) = 5.', 8),
        ('Math', 'Linear Algebra', 'easy',
         'What is the result of adding matrices [[1,2],[3,4]] and [[5,6],[7,8]]?',
         '["[[6,8],[10,12]]", "[[5,12],[21,32]]", "[[6,8],[10,8]]", "[[4,4],[4,4]]"]', 0,
         'Matrix addition is element-wise: (1+5)=6, (2+6)=8, (3+7)=10, (4+8)=12.', 8),
        ('Math', 'Linear Algebra', 'easy',
         'What is the determinant of [[3, 1],[2, 4]]?',
         '["10", "12", "8", "14"]', 0,
         'det = 3*4 - 1*2 = 12 - 2 = 10.', 8),
        ('Math', 'Linear Algebra', 'easy',
         'What is the transpose of the matrix [[1,2,3],[4,5,6]]?',
         '["[[1,4],[2,5],[3,6]]", "[[1,2],[3,4],[5,6]]", "[[6,5,4],[3,2,1]]", "[[3,2,1],[6,5,4]]"]', 0,
         'Transposing swaps rows and columns. Row 1 (1,2,3) becomes column 1.', 8),
        ('Math', 'Linear Algebra', 'easy',
         'Two vectors are orthogonal if their dot product is:',
         '["1", "-1", "0", "undefined"]', 2,
         'Vectors are orthogonal (perpendicular) when their dot product equals 0.', 8),
        ('Math', 'Linear Algebra', 'medium',
         'Find the determinant of the 3x3 matrix [[1,2,3],[4,5,6],[7,8,9]].',
         '["0", "6", "-6", "3"]', 0,
         'Using cofactor expansion: 1(45-48) - 2(36-42) + 3(32-35) = -3+12-9 = 0. (Rows are linearly dependent.)' , 11),
        ('Math', 'Linear Algebra', 'medium',
         'What are the eigenvalues of [[3,1],[0,2]]?',
         '["3 and 2", "3 and -2", "1 and 2", "0 and 2"]', 0,
         'For an upper triangular matrix, eigenvalues are the diagonal entries: 3 and 2.', 10),
        ('Math', 'Linear Algebra', 'medium',
         'What is the inverse of the matrix [[2,1],[5,3]]?',
         '["[[3,-1],[-5,2]]", "[[-3,1],[5,-2]]", "[[3,1],[5,2]]", "[[1/2,1],[5,1/3]]"]', 0,
         'det = 2*3 - 1*5 = 1. Inverse = (1/det)*[[d,-b],[-c,a]] = [[3,-1],[-5,2]].', 11),
        ('Math', 'Linear Algebra', 'medium',
         'What is the rank of the matrix [[1,2,3],[4,5,6],[7,8,9]]?',
         '["1", "2", "3", "0"]', 1,
         'Row reduce: the third row becomes all zeros (rows are linearly dependent). Rank = 2 (two non-zero rows).', 11),
        ('Math', 'Linear Algebra', 'medium',
         'Find the cross product of vectors (1, 0, 0) and (0, 1, 0).',
         '["(0, 0, 1)", "(1, 1, 0)", "(0, 0, -1)", "(0, 1, 1)"]', 0,
         'i x j = k, so (1,0,0) x (0,1,0) = (0,0,1).', 10),
        ('Math', 'Linear Algebra', 'medium',
         'Which of the following sets of vectors forms a basis for R^2?',
         '["{ (1,2), (2,4) }", "{ (1,0), (0,1) }", "{ (1,1), (1,1) }", "{ (0,0), (1,0) }"]', 1,
         'A basis requires linearly independent vectors that span R^2. {(1,0),(0,1)} is the standard basis.', 10),
        ('Math', 'Linear Algebra', 'medium',
         'What is the null space of a matrix A?',
         '["The set of all vectors x such that Ax = 0", "The zero matrix", "The set of all solutions to Ax = b", "The column space"]', 0,
         'The null space (kernel) of A is the set of all vectors x such that Ax = 0.', 11),
        ('Math', 'Linear Algebra', 'medium',
         'What is the dimension of the column space of [[1,0,1],[0,1,1],[1,1,2]]?',
         '["1", "2", "3", "0"]', 1,
         'Row reduce: the third row is the sum of rows 1 and 2, so rank = 2. Dimension of column space = rank = 2.', 11),
        ('Math', 'Linear Algebra', 'hard',
         'Find the eigenvalues of [[4,1],[2,3]].',
         '["lambda = 5 and lambda = 2", "lambda = 4 and lambda = 3", "lambda = 2 and lambda = 5", "lambda = 1 and lambda = 6"]', 0,
         'det(A - lambdaI) = (4-lambda)(3-lambda) - 2 = lambda^2 - 7*lambda + 10 = 0. Roots: lambda = 5 and lambda = 2.', 12),
        ('Math', 'Linear Algebra', 'hard',
         'When is a matrix diagonalizable?',
         '["When it has n linearly independent eigenvectors for an n×n matrix", "When it is symmetric", "When all eigenvalues are positive", "When the determinant is non-zero"]', 0,
         'An n×n matrix is diagonalizable if and only if it has n linearly independent eigenvectors (equivalently, if each eigenvalue\'s geometric multiplicity equals its algebraic multiplicity).', 12),
        ('Math', 'Linear Algebra', 'hard',
         'What does the Gram-Schmidt process produce?',
         '["An orthonormal basis from a set of linearly independent vectors", "Eigenvalues of a matrix", "The inverse of a matrix", "The row echelon form"]', 0,
         'The Gram-Schmidt process takes a set of linearly independent vectors and produces an orthonormal basis through successive orthogonalization.', 12),
        ('Math', 'Linear Algebra', 'hard',
         'What is the characteristic polynomial of [[2,0],[1,3]]?',
         '["lambda^2 - 5*lambda + 6", "lambda^2 + 5*lambda + 6", "lambda^2 - 5*lambda - 6", "lambda^2 - 6*lambda + 5"]', 0,
         'det(A-lambdaI) = (2-lambda)(3-lambda) - 0*1 = lambda^2 - 5*lambda + 6.', 12),
        ('Math', 'Linear Algebra', 'hard',
         'Use Cramer\'s rule to solve: 2x + y = 5, x + 3y = 10.',
         '["x=1, y=3", "x=2, y=3", "x=3, y=2", "x=1, y=2"]', 0,
         'D = 2*3 - 1*1 = 5. Dx = 5*3 - 1*10 = 5. Dy = 2*10 - 5*1 = 15. x = Dx/D = 1, y = Dy/D = 3.', 12),
        ('Math', 'Linear Algebra', 'hard',
         'What is a linear transformation T: R^n -> R^m?',
         '["A function satisfying T(u+v)=T(u)+T(v) and T(cu)=cT(u)", "Any function from R^n to R^m", "A function where T(0)=0 only", "A bijective function between vector spaces"]', 0,
         'A linear transformation satisfies additivity T(u+v)=T(u)+T(v) and scalar multiplication T(cu)=cT(u).', 11),
        ('Math', 'Linear Algebra', 'medium',
         'What is the trace of a matrix?',
         '["Sum of all elements", "Sum of diagonal elements", "Product of diagonal elements", "Determinant of the matrix"]', 1,
         'The trace of a square matrix is the sum of its diagonal elements.', 9),
        ('Math', 'Linear Algebra', 'medium',
         'What does it mean for vectors v1, v2, ..., vk to be linearly independent?',
         '["c1*v1 + c2*v2 + ... + ck*vk = 0 implies all ci = 0", "They are all unit vectors", "They are all perpendicular", "Their sum is zero"]', 0,
         'Vectors are linearly independent if the only solution to the zero linear combination is all scalar coefficients being zero.', 10),
        ('Math', 'Linear Algebra', 'medium',
         'What is the dimension of the null space of a 3x5 matrix with rank 2?',
         '["2", "3", "1", "5"]', 1,
         'By the rank-nullity theorem: dim(null space) = number of columns - rank = 5 - 2 = 3.', 11),
        ('Math', 'Linear Algebra', 'medium',
         'What is a symmetric matrix?',
         '["A matrix equal to its own transpose: A = A^T", "A matrix with all positive entries", "A diagonal matrix", "A matrix whose rows are equal to its columns"]', 0,
         'A symmetric matrix satisfies A = A^T, meaning element a_ij = a_ji for all i, j.', 9),
        ('Math', 'Linear Algebra', 'hard',
         'For a 4x4 matrix A, if det(A) = -3, what is det(2A)?',
         '["-48", "-12", "16*(-3) = -48", "-6"]', 0,
         'det(cA) = c^n * det(A) for n×n matrix. det(2A) = 2^4 * (-3) = 16 * (-3) = -48.', 12),
        ('Math', 'Linear Algebra', 'medium',
         'What is an orthogonal matrix?',
         '["A matrix A where A^T * A = I", "A matrix with all zero off-diagonal entries", "A matrix whose columns are unit vectors", "A symmetric positive definite matrix"]', 0,
         'An orthogonal matrix Q has the property Q^T * Q = I, meaning Q^(-1) = Q^T. Its columns form an orthonormal basis.', 11),
        ('Math', 'Linear Algebra', 'easy',
         'What is the identity matrix of size 2x2?',
         '["[[1,0],[0,1]]", "[[0,1],[1,0]]", "[[1,1],[1,1]]", "[[0,0],[0,0]]"]', 0,
         'The identity matrix I has 1\'s on the diagonal and 0\'s elsewhere.', 7),
        ('Math', 'Linear Algebra', 'hard',
         'If lambda is an eigenvalue of A with eigenvector v, what is the eigenvalue of A^2?',
         '["lambda^2", "2*lambda", "lambda + 1", "lambda/2"]', 0,
         'A^2 * v = A * (A*v) = A * (lambda*v) = lambda * (A*v) = lambda * lambda * v = lambda^2 * v.', 11),
        ('Math', 'Linear Algebra', 'hard',
         'What is the relationship between the rank and nullity of an m×n matrix?',
         '["rank + nullity = n", "rank + nullity = m", "rank = nullity", "rank * nullity = m*n"]', 0,
         'The Rank-Nullity Theorem: for an m×n matrix, rank(A) + nullity(A) = n (the number of columns).', 11),

        # ── Probability ───────────────────────────────────────────────────────
        ('Math', 'Probability', 'easy',
         'A fair coin is flipped. What is the probability of getting heads?',
         '["1/4", "1/3", "1/2", "2/3"]', 2,
         'A fair coin has two equally likely outcomes. P(heads) = 1/2.', 6),
        ('Math', 'Probability', 'easy',
         'A single die is rolled. What is the probability of rolling a number greater than 4?',
         '["1/3", "1/2", "1/6", "2/3"]', 0,
         'Numbers greater than 4 are 5 and 6. P = 2/6 = 1/3.', 6),
        ('Math', 'Probability', 'easy',
         'What is the complement rule?',
         '["P(A) + P(B) = 1", "P(A) + P(A\') = 1", "P(A) * P(B) = 1", "P(A | B) = 1"]', 1,
         'The complement rule states P(A) + P(A\') = 1, where A\' is the complement of event A.', 7),
        ('Math', 'Probability', 'easy',
         'How many ways can 3 books be arranged on a shelf?',
         '["3", "6", "9", "12"]', 1,
         '3! = 3*2*1 = 6 ways.', 7),
        ('Math', 'Probability', 'easy',
         'How many ways can you choose 2 items from 5 items (order doesn\'t matter)?',
         '["10", "20", "5", "25"]', 0,
         'C(5,2) = 5!/(2!3!) = 10.', 8),
        ('Math', 'Probability', 'easy',
         'What is the probability of rolling a 6 on a fair die?',
         '["1/5", "1/6", "1/3", "2/6"]', 1,
         'There is 1 favorable outcome out of 6 equally likely outcomes. P = 1/6.', 6),
        ('Math', 'Probability', 'easy',
         'What is the sample space when flipping a coin twice?',
         '["HH, HT, TH, TT", "H, T", "HH, TT", "HT, TH"]', 0,
         'The sample space contains all possible outcomes: {HH, HT, TH, TT}.', 7),
        ('Math', 'Probability', 'easy',
         'Two events A and B are mutually exclusive. What is P(A or B)?',
         '["P(A) * P(B)", "P(A) + P(B)", "P(A) + P(B) - P(A and B)", "P(A) / P(B)"]', 1,
         'For mutually exclusive events, P(A and B) = 0, so P(A or B) = P(A) + P(B).', 7),
        ('Math', 'Probability', 'medium',
         'A bag has 3 red, 4 blue, and 5 green balls. What is the probability of drawing a red ball?',
         '["1/4", "3/12", "1/3", "5/12"]', 1,
         'Total balls = 12. P(red) = 3/12 = 1/4. Note: 3/12 = 1/4.', 8),
        ('Math', 'Probability', 'medium',
         'What is P(A and B) if A and B are independent with P(A) = 0.4 and P(B) = 0.5?',
         '["0.9", "0.2", "0.1", "0.02"]', 1,
         'For independent events: P(A and B) = P(A) * P(B) = 0.4 * 0.5 = 0.2.', 9),
        ('Math', 'Probability', 'medium',
         'What is P(B | A) if P(A and B) = 0.12 and P(A) = 0.4?',
         '["0.3", "0.048", "0.52", "0.25"]', 0,
         'P(B|A) = P(A and B) / P(A) = 0.12 / 0.4 = 0.3.', 9),
        ('Math', 'Probability', 'medium',
         'In the binomial distribution with n=10 and p=0.5, what is the expected value?',
         '["10", "5", "2.5", "0.5"]', 1,
         'E(X) = np = 10 * 0.5 = 5.', 9),
        ('Math', 'Probability', 'medium',
         'What is the variance of a binomial distribution with n=20 and p=0.3?',
         '["6", "4.2", "14", "1.2"]', 1,
         'Var(X) = np(1-p) = 20 * 0.3 * 0.7 = 4.2.', 10),
        ('Math', 'Probability', 'medium',
         'In a Poisson distribution with mean lambda = 3, what is P(X = 0)?',
         '["e^(-3)", "3*e^(-3)", "1/3", "3/e^3"]', 0,
         'P(X=0) = e^(-lambda)*lambda^0/0! = e^(-3).', 11),
        ('Math', 'Probability', 'medium',
         'What is P(A or B) when P(A)=0.4, P(B)=0.3, and P(A and B)=0.1?',
         '["0.7", "0.6", "0.12", "1.0"]', 1,
         'P(A or B) = P(A) + P(B) - P(A and B) = 0.4 + 0.3 - 0.1 = 0.6.', 9),
        ('Math', 'Probability', 'medium',
         'How many permutations are there of choosing 3 items from 7 (order matters)?',
         '["35", "210", "21", "120"]', 1,
         'P(7,3) = 7!/(7-3)! = 7*6*5 = 210.', 9),
        ('Math', 'Probability', 'medium',
         'A geometric distribution models the number of trials until the first success. If p=0.25, what is E(X)?',
         '["4", "0.25", "0.75", "2.5"]', 0,
         'For a geometric distribution, E(X) = 1/p = 1/0.25 = 4.', 10),
        ('Math', 'Probability', 'hard',
         'Apply Bayes\' theorem: P(D) = 0.01, P(+ | D) = 0.99, P(+ | no D) = 0.05. Find P(D | +).',
         '["0.167", "0.01", "0.99", "0.25"]', 0,
         'P(+) = 0.99*0.01 + 0.05*0.99 = 0.0099 + 0.0495 = 0.0594. P(D|+) = 0.0099/0.0594 ≈ 0.167.', 12),
        ('Math', 'Probability', 'hard',
         'What is the standard deviation of a binomial distribution with n=100 and p=0.4?',
         '["4.899", "4", "40", "2.4"]', 0,
         'Var = np(1-p) = 100*0.4*0.6 = 24. SD = sqrt(24) ≈ 4.899.', 11),
        ('Math', 'Probability', 'hard',
         'If X and Y are independent random variables, what is Var(X + Y)?',
         '["Var(X) * Var(Y)", "Var(X) + Var(Y)", "Var(X) - Var(Y)", "sqrt(Var(X)^2 + Var(Y)^2)"]', 1,
         'For independent random variables, the variance of the sum equals the sum of the variances: Var(X+Y) = Var(X) + Var(Y).', 11),
        ('Math', 'Probability', 'hard',
         'What does the Law of Large Numbers state?',
         '["Sample mean converges to population mean as n increases", "All samples are equally likely", "The probability of any event converges to 1", "Sample standard deviation equals population standard deviation"]', 0,
         'The Law of Large Numbers states that as sample size n increases, the sample mean converges in probability to the population mean.', 11),
        ('Math', 'Probability', 'hard',
         'What does the Central Limit Theorem state?',
         '["All populations are normally distributed", "Sample means are approximately normally distributed for large n, regardless of population distribution", "The mean equals the median for all distributions", "Variance equals the square of the mean"]', 1,
         'The CLT states that the sampling distribution of the sample mean approaches a normal distribution as sample size increases, regardless of the population\'s distribution.', 12),
        ('Math', 'Probability', 'hard',
         'A card is drawn from a standard deck. Given that it is red, what is the probability it is a heart?',
         '["1/4", "1/2", "1/13", "13/52"]', 1,
         'P(heart | red) = P(heart and red)/P(red) = (13/52)/(26/52) = 13/26 = 1/2.', 11),
        ('Math', 'Probability', 'medium',
         'What is the expected value of a random variable X with P(X=1)=0.3, P(X=2)=0.5, P(X=3)=0.2?',
         '["2", "1.9", "1.8", "2.1"]', 1,
         'E(X) = 1*0.3 + 2*0.5 + 3*0.2 = 0.3 + 1.0 + 0.6 = 1.9.', 9),
        ('Math', 'Probability', 'hard',
         'In a normal distribution, approximately what percentage of data falls within 2 standard deviations of the mean?',
         '["68%", "90%", "95%", "99.7%"]', 2,
         'The empirical rule: about 68% within 1 SD, 95% within 2 SDs, and 99.7% within 3 SDs.', 11),
        ('Math', 'Probability', 'medium',
         'What is the formula for combinations C(n, k)?',
         '["n! / k!", "n! / (k! * (n-k)!)", "n! / (n-k)!", "k! / (n-k)!"]', 1,
         'C(n,k) = n! / (k! * (n-k)!). It counts ways to choose k items from n without order.', 9),
        ('Math', 'Probability', 'medium',
         'Two dice are rolled. What is the probability the sum equals 7?',
         '["1/6", "5/36", "7/36", "1/12"]', 0,
         'Pairs summing to 7: (1,6),(2,5),(3,4),(4,3),(5,2),(6,1) = 6 pairs. P = 6/36 = 1/6.', 10),
        ('Math', 'Probability', 'hard',
         'A factory has 3 machines producing 20%, 30%, and 50% of output. Defect rates are 1%, 2%, 3%. If a randomly selected item is defective, what is the probability it came from machine 3?',
         '["0.652", "0.5", "0.3", "0.75"]', 0,
         'P(defect) = 0.2*0.01+0.3*0.02+0.5*0.03 = 0.002+0.006+0.015=0.023. P(M3|defect) = 0.015/0.023 ≈ 0.652.', 13),
        ('Math', 'Probability', 'medium',
         'What is the probability that at least one head appears in 3 coin flips?',
         '["1/8", "3/8", "7/8", "1/2"]', 2,
         'P(at least one head) = 1 - P(no heads) = 1 - (1/2)^3 = 1 - 1/8 = 7/8.', 9),

        # ── Statistics ────────────────────────────────────────────────────────
        ('Math', 'Statistics', 'easy',
         'What is the mean of the data set {4, 7, 9, 11, 14}?',
         '["8", "9", "10", "11"]', 1,
         'Mean = (4+7+9+11+14)/5 = 45/5 = 9.', 7),
        ('Math', 'Statistics', 'easy',
         'What is the median of {3, 5, 7, 9, 11}?',
         '["5", "7", "9", "6"]', 1,
         'The median is the middle value when data is sorted. For 5 values, it is the 3rd: 7.', 7),
        ('Math', 'Statistics', 'easy',
         'What is the mode of {2, 3, 3, 5, 7, 7, 7}?',
         '["3", "5", "7", "2"]', 2,
         'The mode is the most frequent value. 7 appears 3 times, more than any other.', 6),
        ('Math', 'Statistics', 'easy',
         'What is the range of the data set {5, 12, 3, 18, 7}?',
         '["9", "13", "15", "10"]', 2,
         'Range = max - min = 18 - 3 = 15.', 6),
        ('Math', 'Statistics', 'easy',
         'A z-score of 0 means the data point is:',
         '["One standard deviation above the mean", "Equal to the mean", "At the minimum", "Two standard deviations below the mean"]', 1,
         'A z-score of 0 indicates the data point equals the mean (zero standard deviations away).', 8),
        ('Math', 'Statistics', 'easy',
         'What does a larger standard deviation indicate?',
         '["Data is more spread out from the mean", "Data is closer to the mean", "The mean is larger", "The sample size is larger"]', 0,
         'Standard deviation measures spread. A larger standard deviation means data points are more dispersed around the mean.', 7),
        ('Math', 'Statistics', 'easy',
         'Which measure of central tendency is most affected by outliers?',
         '["Median", "Mode", "Mean", "Range"]', 2,
         'The mean is most affected by outliers because it uses the actual values of all data points.', 8),
        ('Math', 'Statistics', 'easy',
         'What is the sample variance of {2, 4, 6}?',
         '["2", "4", "8", "16"]', 1,
         'Mean = 4. Deviations squared: 4, 0, 4. Sample variance = (4+0+4)/(3-1) = 8/2 = 4.', 8),
        ('Math', 'Statistics', 'medium',
         'What is the z-score for a data point of 75 if the mean is 65 and standard deviation is 5?',
         '["1", "2", "3", "0.5"]', 1,
         'z = (x - mu) / sigma = (75 - 65) / 5 = 10/5 = 2.', 9),
        ('Math', 'Statistics', 'medium',
         'What is the 50th percentile also known as?',
         '["Mean", "Mode", "Median", "Standard deviation"]', 2,
         'The 50th percentile is the median — the middle value that divides the distribution in half.', 8),
        ('Math', 'Statistics', 'medium',
         'In hypothesis testing, what is a Type I error?',
         '["Failing to reject a false null hypothesis", "Rejecting a true null hypothesis", "Using the wrong test statistic", "Setting alpha too low"]', 1,
         'A Type I error is a false positive: rejecting the null hypothesis when it is actually true. Its probability is the significance level alpha.', 10),
        ('Math', 'Statistics', 'medium',
         'What does a p-value represent?',
         '["The probability that H0 is true", "The probability of observing results as extreme as the data, assuming H0 is true", "The probability of a Type II error", "The critical value"]', 1,
         'The p-value is the probability of obtaining a test statistic at least as extreme as the observed one, given that the null hypothesis is true.', 11),
        ('Math', 'Statistics', 'medium',
         'A 95% confidence interval means:',
         '["We are 95% sure the true parameter is in this interval", "95% of all data points fall in this interval", "If we repeated the sampling many times, 95% of such intervals would contain the true parameter", "The p-value is 0.95"]', 2,
         'A 95% CI means that if we construct such intervals repeatedly, approximately 95% of them will contain the true population parameter.', 11),
        ('Math', 'Statistics', 'medium',
         'When is a t-test used instead of a z-test?',
         '["When the sample size is large (n>30)", "When the population standard deviation is unknown and sample size is small", "When data is not normally distributed", "When comparing more than two groups"]', 1,
         'A t-test is appropriate when the population standard deviation is unknown and/or sample size is small, requiring estimation of variability from the sample.', 11),
        ('Math', 'Statistics', 'medium',
         'What does correlation coefficient r = 0 indicate?',
         '["Perfect positive linear relationship", "Perfect negative linear relationship", "No linear relationship", "The variables are equal"]', 2,
         'A correlation coefficient of 0 indicates no linear relationship between the two variables.', 9),
        ('Math', 'Statistics', 'medium',
         'What is the relationship between variance and standard deviation?',
         '["Variance = SD / mean", "SD = sqrt(Variance)", "Variance = SD + mean", "SD = Variance^2"]', 1,
         'Standard deviation is the square root of variance. Equivalently, variance = SD^2.', 8),
        ('Math', 'Statistics', 'medium',
         'In a normal distribution, what percentage of values fall within 1 standard deviation of the mean?',
         '["50%", "68%", "95%", "99.7%"]', 1,
         'The empirical rule (68-95-99.7 rule): approximately 68% of values fall within ±1 SD.', 10),
        ('Math', 'Statistics', 'hard',
         'What is the purpose of an ANOVA test?',
         '["Comparing the means of exactly two groups", "Comparing the means of three or more groups", "Testing whether a single mean equals a hypothesized value", "Testing for correlation"]', 1,
         'ANOVA (Analysis of Variance) tests whether the means of three or more groups are statistically significantly different from each other.', 11),
        ('Math', 'Statistics', 'hard',
         'What is the null hypothesis for a chi-square test of independence?',
         '["The two variables are dependent", "The two variables are independent", "The variances of two groups are equal", "The means of two groups are equal"]', 1,
         'The null hypothesis for a chi-square test of independence is that the two categorical variables are independent (no association).', 11),
        ('Math', 'Statistics', 'hard',
         'In simple linear regression y = b0 + b1*x, what does b1 represent?',
         '["The y-intercept", "The slope — change in y for a one-unit change in x", "The correlation coefficient", "The standard error"]', 1,
         'b1 is the slope of the regression line: it represents the expected change in y for each one-unit increase in x.', 11),
        ('Math', 'Statistics', 'hard',
         'What is the formula for the sample standard deviation?',
         '["sqrt(sum((xi - x_bar)^2) / n)", "sqrt(sum((xi - x_bar)^2) / (n-1))", "sum(|xi - x_bar|) / n", "sqrt(sum(xi^2) / n)"]', 1,
         'The sample standard deviation uses n-1 in the denominator (Bessel\'s correction) to give an unbiased estimate of population variance.', 11),
        ('Math', 'Statistics', 'hard',
         'A researcher computes a t-statistic of 2.45 with df=20. If the critical value is 2.09 (alpha=0.05, two-tailed), what is the conclusion?',
         '["Fail to reject H0", "Reject H0", "The test is inconclusive", "The p-value is exactly 0.05"]', 1,
         'Since |t| = 2.45 > critical value 2.09, we reject the null hypothesis at the 0.05 significance level.', 12),
        ('Math', 'Statistics', 'hard',
         'What is the interquartile range (IQR) and how is it used in box plots?',
         '["IQR = Q3 - Q1; outliers are beyond Q1 - 1.5*IQR or Q3 + 1.5*IQR", "IQR = Q2 - Q1; outliers beyond 2*IQR", "IQR = max - min; it is the range", "IQR = mean - SD"]', 0,
         'IQR = Q3 - Q1 (middle 50% of data). Outliers are defined as values below Q1-1.5*IQR or above Q3+1.5*IQR.', 11),
        ('Math', 'Statistics', 'hard',
         'What is the difference between a Type I and Type II error?',
         '["Type I: false positive (reject true H0); Type II: false negative (fail to reject false H0)", "Type I: false negative; Type II: false positive", "Type I: wrong mean; Type II: wrong variance", "Type I occurs in t-tests; Type II in z-tests"]', 0,
         'Type I error = false positive (rejecting a true null hypothesis), probability = alpha. Type II error = false negative (failing to reject a false null hypothesis), probability = beta.', 12),
        ('Math', 'Statistics', 'medium',
         'What does a correlation coefficient of r = 0.9 indicate?',
         '["Weak positive relationship", "No relationship", "Strong positive linear relationship", "Negative relationship"]', 2,
         'r = 0.9 is close to 1, indicating a strong positive linear relationship between the two variables.', 9),
        ('Math', 'Statistics', 'medium',
         'In a left-skewed distribution, how do the mean, median, and mode relate?',
         '["mean > median > mode", "mean < median < mode", "mean = median = mode", "mode < mean < median"]', 1,
         'In a left-skewed (negatively skewed) distribution, the mean is pulled to the left by the tail, giving mean < median < mode.', 11),
        ('Math', 'Statistics', 'hard',
         'What is the Central Limit Theorem\'s condition for approximating normality?',
         '["n > 10", "n >= 30 is a common rule of thumb", "Population must be normal", "Standard deviation must be > 1"]', 1,
         'The CLT guarantees approximately normal sampling distribution of the mean; n >= 30 is a common practical rule of thumb, though exact requirements depend on population skewness.', 11),
        ('Math', 'Statistics', 'medium',
         'What is sampling bias?',
         '["Random variation in samples", "Systematic error where some members of a population are more likely to be sampled", "Using too large a sample size", "Having a non-normal distribution"]', 1,
         'Sampling bias occurs when the sampling method causes some members of the population to be systematically over- or under-represented.', 10),
        ('Math', 'Statistics', 'hard',
         'What is the least squares method in linear regression?',
         '["Minimizing the sum of residuals", "Minimizing the sum of squared residuals", "Maximizing the correlation coefficient", "Minimizing the absolute value of residuals"]', 1,
         'The ordinary least squares (OLS) method finds the regression line that minimizes the sum of squared differences between observed and predicted y-values.', 12),
        ('Math', 'Statistics', 'medium',
         'What is a hypothesis test\'s power?',
         '["P(Type I error)", "1 - P(Type II error)", "P(rejecting H0 when H0 is true)", "The significance level alpha"]', 1,
         'Power = 1 - beta = 1 - P(Type II error) = probability of correctly rejecting a false null hypothesis.', 11),
        ('Math', 'Statistics', 'medium',
         'What is the coefficient of variation (CV)?',
         '["mean/SD", "SD/mean * 100%", "SD^2/mean", "(mean-median)/SD"]', 1,
         'The CV = (SD/mean)*100% is a standardized measure of dispersion that allows comparison across data sets with different units or magnitudes.', 10),
        ('Math', 'Statistics', 'hard',
         'When is a chi-square goodness-of-fit test used?',
         '["To test if observed categorical frequencies match expected frequencies", "To test if two quantitative variables are correlated", "To compare means of two groups", "To test normality only"]', 0,
         'The chi-square goodness-of-fit test determines whether observed categorical data frequencies differ significantly from theoretically expected frequencies.', 11),
        ('Math', 'Statistics', 'medium',
         'Which graphical display summarizes data using five-number summary?',
         '["Histogram", "Box plot", "Scatter plot", "Bar chart"]', 1,
         'A box plot displays the minimum, Q1, median (Q2), Q3, and maximum — the five-number summary.', 8),
        ('Math', 'Statistics', 'hard',
         'What is the effect of increasing the confidence level from 95% to 99% on a confidence interval?',
         '["The interval becomes narrower", "The interval becomes wider", "The interval stays the same", "The sample size decreases"]', 1,
         'A higher confidence level requires a wider interval to capture the true parameter with greater certainty.', 11),
    ]


def _language_extra_questions():
    return [
        # ── Grammar ──────────────────────────────────────────────────────────
        ('Language', 'Grammar', 'easy',
         'Which of the following is a proper noun?',
         '["city", "Paris", "happiness", "run"]', 1,
         'A proper noun names a specific person, place, or thing and is always capitalized. "Paris" is a specific city.', 8),
        ('Language', 'Grammar', 'easy',
         'Which sentence uses correct subject-verb agreement?',
         '["The dogs runs fast.", "The dog run fast.", "The dogs run fast.", "The dog running fast."]', 2,
         'A plural subject ("dogs") requires a plural verb ("run"). Singular subject ("dog") requires "runs".', 8),
        ('Language', 'Grammar', 'medium',
         'Which of the following is a subordinating conjunction?',
         '["although", "and", "but", "or"]', 0,
         '"Although" introduces a dependent clause, making it a subordinating conjunction. "And", "but", and "or" are coordinating conjunctions.', 10),
        ('Language', 'Grammar', 'medium',
         'What is a dangling modifier?',
         '["A misplaced comma", "A modifier that does not clearly modify the intended word", "A verb with no subject", "An adjective that comes after the noun"]', 1,
         'A dangling modifier is a word or phrase that does not clearly and logically connect to the word it is supposed to modify, creating ambiguity.', 10),
        ('Language', 'Grammar', 'medium',
         'Which punctuation mark is used to join two independent clauses without a conjunction?',
         '["Comma", "Semicolon", "Colon", "Dash"]', 1,
         'A semicolon connects two related independent clauses. Using only a comma creates a comma splice.', 10),
        ('Language', 'Grammar', 'hard',
         'In the sentence "Running through the park, the flowers looked beautiful," what is the grammatical error?',
         '["Wrong verb tense", "Dangling participle — it implies the flowers were running", "Missing comma", "Incorrect pronoun"]', 1,
         'The participial phrase "Running through the park" should modify the subject, but "the flowers" cannot run — it is a dangling participle.', 12),
        ('Language', 'Grammar', 'hard',
         'What is the function of an appositive phrase?',
         '["To express action", "To rename or describe the noun directly beside it", "To show time relationship", "To connect two clauses"]', 1,
         'An appositive phrase sits beside a noun and renames or further identifies it, e.g., "My brother, a doctor, works nights."', 12),
        ('Language', 'Grammar', 'medium',
         'Which sentence correctly uses a comma with a coordinating conjunction?',
         '["I wanted to go, but it rained.", "I wanted to go but, it rained.", "I wanted, to go but it rained.", "I wanted to go but it, rained."]', 0,
         'When a coordinating conjunction (FANBOYS) joins two independent clauses, a comma is placed before the conjunction.', 10),

        # ── Vocabulary ───────────────────────────────────────────────────────
        ('Language', 'Vocabulary', 'easy',
         'What does the prefix "anti-" mean?',
         '["Before", "Against", "After", "With"]', 1,
         'The prefix "anti-" means "against" or "opposed to," as in "antibiotic" (against bacteria) or "antisocial."', 8),
        ('Language', 'Vocabulary', 'medium',
         'What does "ubiquitous" mean?',
         '["Rare and unusual", "Present or found everywhere", "Hidden from view", "Loud and disruptive"]', 1,
         '"Ubiquitous" describes something that seems to appear everywhere at once. From Latin "ubique" meaning "everywhere."', 10),
        ('Language', 'Vocabulary', 'medium',
         'What does the root word "bene-" mean?',
         '["Bad", "Good or well", "Two", "Against"]', 1,
         'The Latin root "bene-" means "good" or "well," seen in words like "beneficial," "benevolent," and "benefit."', 10),
        ('Language', 'Vocabulary', 'medium',
         'Which word means "to make worse or more severe"?',
         '["Ameliorate", "Mitigate", "Exacerbate", "Alleviate"]', 2,
         '"Exacerbate" means to make a bad situation worse. "Ameliorate," "mitigate," and "alleviate" all mean to make something better or less severe.', 10),
        ('Language', 'Vocabulary', 'hard',
         'What does "equivocate" mean?',
         '["To speak clearly and directly", "To use ambiguous language to avoid commitment", "To argue loudly", "To agree enthusiastically"]', 1,
         '"Equivocate" means to use vague or ambiguous language, often to avoid making a definitive statement or to mislead.', 12),
        ('Language', 'Vocabulary', 'hard',
         'Which of the following best defines "sanguine"?',
         '["Pessimistic", "Bloodthirsty", "Optimistic and positive", "Pale and weak"]', 2,
         '"Sanguine" means optimistic, especially in a difficult situation. It derives from the Latin for "blood," linked to the old theory of sanguine temperament.', 12),
        ('Language', 'Vocabulary', 'medium',
         'What does the suffix "-logy" indicate?',
         '["Fear of", "Lover of", "The study of", "Without"]', 2,
         'The suffix "-logy" comes from the Greek "logos" meaning word/reason, and indicates the study of a subject, as in "biology" or "psychology."', 10),
        ('Language', 'Vocabulary', 'hard',
         'Which word is a synonym for "taciturn"?',
         '["Verbose", "Reserved", "Gregarious", "Eloquent"]', 1,
         '"Taciturn" describes a person who is habitually silent or reserved in speech. Its synonym is "reserved." "Verbose" and "eloquent" mean the opposite.', 12),

        # ── Literature ───────────────────────────────────────────────────────
        ('Language', 'Literature', 'easy',
         'What literary device gives human qualities to non-human things?',
         '["Simile", "Metaphor", "Personification", "Alliteration"]', 2,
         'Personification attributes human characteristics to animals, objects, or abstract ideas, e.g., "The wind whispered through the trees."', 8),
        ('Language', 'Literature', 'easy',
         'Which Shakespeare play features the characters Romeo and Juliet?',
         '["Hamlet", "A Midsummer Night\'s Dream", "Romeo and Juliet", "Othello"]', 2,
         '"Romeo and Juliet" (c. 1594–96) is one of Shakespeare\'s most famous tragedies, depicting two young star-crossed lovers from feuding families.', 8),
        ('Language', 'Literature', 'medium',
         'What is dramatic irony?',
         '["When the audience knows something the characters do not", "When a character says the opposite of what they mean", "An unexpected twist at the end", "Exaggeration for comic effect"]', 0,
         'Dramatic irony occurs when the audience has knowledge that the characters in the story lack, creating tension or humor.', 10),
        ('Language', 'Literature', 'medium',
         'Who wrote "To Kill a Mockingbird"?',
         '["Ernest Hemingway", "Harper Lee", "John Steinbeck", "F. Scott Fitzgerald"]', 1,
         'Harper Lee published "To Kill a Mockingbird" in 1960. It won the Pulitzer Prize in 1961 and explores racial injustice in the American South.', 10),
        ('Language', 'Literature', 'medium',
         'What is the term for the main conflict or turning point in a story?',
         '["Exposition", "Rising action", "Climax", "Denouement"]', 2,
         'The climax is the moment of highest tension and is the turning point of the narrative, after which events move toward resolution.', 10),
        ('Language', 'Literature', 'hard',
         'What poetic device is used in "Peter Piper picked a peck of pickled peppers"?',
         '["Assonance", "Alliteration", "Onomatopoeia", "Consonance"]', 1,
         'Alliteration is the repetition of the same initial consonant sound in closely connected words. Here the "p" sound repeats throughout.', 12),
        ('Language', 'Literature', 'hard',
         'In which Shakespeare play does the character Iago manipulate the protagonist into jealously murdering his wife?',
         '["Macbeth", "King Lear", "Othello", "Hamlet"]', 2,
         'In "Othello," the villain Iago manipulates Othello into believing his wife Desdemona is unfaithful, leading Othello to kill her in a jealous rage.', 13),
        ('Language', 'Literature', 'hard',
         'What is a Petrarchan sonnet\'s rhyme scheme in the octave (first 8 lines)?',
         '["ABAB CDCD", "ABBA ABBA", "ABAB ABAB", "AABB CCDD"]', 1,
         'The Petrarchan (Italian) sonnet has an octave rhyming ABBA ABBA and a sestet with various schemes (CDECDE, CDCCDC, etc.), presenting a problem then a resolution.', 14),

        # ── Writing ──────────────────────────────────────────────────────────
        ('Language', 'Writing', 'easy',
         'What is the purpose of a thesis statement in an essay?',
         '["To summarize the entire essay in detail", "To present the central argument or main point", "To list all supporting evidence", "To introduce the topic with a question"]', 1,
         'A thesis statement presents the central claim or argument of an essay, typically in one or two sentences at the end of the introduction.', 8),
        ('Language', 'Writing', 'medium',
         'Which type of essay attempts to persuade the reader to adopt a particular viewpoint?',
         '["Narrative", "Descriptive", "Expository", "Argumentative"]', 3,
         'An argumentative essay takes a position and supports it with evidence and reasoning to convince the reader, unlike expository (explains) or narrative (tells a story) essays.', 10),
        ('Language', 'Writing', 'medium',
         'What is the main purpose of a topic sentence in a paragraph?',
         '["To provide supporting evidence", "To conclude the paragraph\'s argument", "To introduce the main idea of the paragraph", "To transition to the next paragraph"]', 2,
         'A topic sentence states the main idea of a paragraph and guides the reader, signaling what the paragraph will discuss.', 10),
        ('Language', 'Writing', 'medium',
         'What does "coherence" mean in the context of essay writing?',
         '["Using many big words", "Ideas flowing logically and smoothly throughout", "Having a long conclusion", "Including many quotations"]', 1,
         'Coherence means the essay\'s ideas are logically connected and flow smoothly, so the reader can follow the argument easily.', 10),
        ('Language', 'Writing', 'hard',
         'What is the difference between a primary source and a secondary source?',
         '["Primary sources are more reliable", "Primary sources are original materials; secondary sources analyze or interpret primary sources", "Secondary sources are always books", "Primary sources are only used in science"]', 1,
         'Primary sources are original documents (diaries, raw data, speeches). Secondary sources interpret or analyze primary sources (textbooks, literary criticism).', 12),
        ('Language', 'Writing', 'hard',
         'In MLA format, how should a direct quotation of more than four lines be formatted?',
         '["In quotation marks, inline", "As a block quotation, indented 1 inch, no quotation marks", "In italics", "In a footnote"]', 1,
         'MLA style requires prose quotations longer than four lines to appear as a block quotation, indented one inch from the left margin, with no additional quotation marks.', 13),

        # ── Reading Comprehension ─────────────────────────────────────────────
        ('Language', 'Reading Comprehension', 'easy',
         'What is the "main idea" of a passage?',
         '["The first sentence of the passage", "The most important point the author is making", "A supporting detail", "The conclusion paragraph only"]', 1,
         'The main idea is the central point or message the author communicates throughout the passage, supported by details and examples.', 8),
        ('Language', 'Reading Comprehension', 'medium',
         'When you make an inference while reading, you are:',
         '["Summarizing every sentence", "Drawing a conclusion based on evidence and reasoning, not directly stated", "Copying the author\'s exact words", "Identifying every vocabulary word"]', 1,
         'An inference is a logical conclusion drawn from evidence in the text combined with prior knowledge, going beyond what is explicitly stated.', 10),
        ('Language', 'Reading Comprehension', 'medium',
         'What does the "tone" of a passage refer to?',
         '["The subject matter", "The author\'s attitude or feeling toward the subject", "The length of the passage", "The use of dialogue"]', 1,
         'Tone reflects the author\'s attitude (e.g., humorous, serious, sarcastic, melancholic) and is conveyed through word choice and style.', 10),
        ('Language', 'Reading Comprehension', 'hard',
         'A passage describes increasing global temperatures, rising sea levels, and declining biodiversity. What is the most likely implied conclusion?',
         '["Weather patterns are improving", "Climate change poses significant environmental risks", "Oceans are becoming less salty", "Biodiversity is unrelated to temperature"]', 1,
         'Combining the evidence of rising temperatures, sea levels, and biodiversity loss supports the implied conclusion that climate change presents serious environmental dangers.', 12),
        ('Language', 'Reading Comprehension', 'hard',
         'If a narrator describes events only from their own limited perspective and may not be fully reliable, they are called a:',
         '["Omniscient narrator", "Third-person objective narrator", "Unreliable narrator", "Authorial narrator"]', 2,
         'An unreliable narrator is one whose account may be biased, mistaken, or deliberately misleading, requiring readers to read between the lines.', 13),
    ]


def _history_extra_questions():
    return [
        # ── Ancient Civilizations ─────────────────────────────────────────────
        ('History', 'Ancient Civilizations', 'easy',
         'Which river is most closely associated with ancient Egyptian civilization?',
         '["Tigris", "Euphrates", "Nile", "Amazon"]', 2,
         'The Nile River provided fertile land and water for irrigation, making it the lifeblood of ancient Egyptian civilization.', 8),
        ('History', 'Ancient Civilizations', 'easy',
         'What structure did ancient Egyptians build to serve as tombs for their pharaohs?',
         '["Ziggurats", "Pyramids", "Colosseum", "Parthenon"]', 1,
         'The ancient Egyptians built pyramids as monumental royal tombs. The Great Pyramid of Giza is one of the Seven Wonders of the Ancient World.', 8),
        ('History', 'Ancient Civilizations', 'medium',
         'What was the name of the ancient Greek city-state famous for its warrior culture and military training?',
         '["Athens", "Corinth", "Sparta", "Thebes"]', 2,
         'Sparta was a militaristic city-state where boys began rigorous military training (agoge) at age 7 and society was organized around warfare.', 10),
        ('History', 'Ancient Civilizations', 'medium',
         'Which Mesopotamian civilization is credited with creating one of the earliest known law codes?',
         '["Sumerians", "Babylonians under Hammurabi", "Assyrians", "Persians"]', 1,
         'Hammurabi of Babylon created the Code of Hammurabi (c. 1754 BC), one of the earliest and most complete written legal codes in history.', 10),
        ('History', 'Ancient Civilizations', 'medium',
         'The Roman Republic officially became the Roman Empire under which leader?',
         '["Julius Caesar", "Augustus (Octavian)", "Marcus Aurelius", "Constantine"]', 1,
         'Augustus (Octavian), Julius Caesar\'s adopted son, became the first Roman Emperor in 27 BC after defeating Mark Antony and Cleopatra.', 11),
        ('History', 'Ancient Civilizations', 'hard',
         'What was the significance of the Battle of Marathon (490 BC)?',
         '["Athens conquered Persia", "Athens defeated a Persian invasion force, preserving Greek independence", "Sparta defeated Athens", "Greece united under Alexander"]', 1,
         'At Marathon, Athenian forces defeated the invading Persian army under Darius I, halting the first Persian invasion of Greece and boosting Athenian prestige.', 13),
        ('History', 'Ancient Civilizations', 'hard',
         'Which ancient wonder was located in Alexandria, Egypt?',
         '["The Hanging Gardens", "The Colossus of Rhodes", "The Great Lighthouse", "The Temple of Artemis"]', 2,
         'The Lighthouse of Alexandria (Pharos of Alexandria) was one of the Seven Wonders, guiding ships into the harbor of this major ancient city.', 13),

        # ── World Wars ────────────────────────────────────────────────────────
        ('History', 'World Wars', 'easy',
         'In which year did World War I begin?',
         '["1912", "1914", "1916", "1918"]', 1,
         'WWI began in 1914 following the assassination of Archduke Franz Ferdinand of Austria-Hungary on June 28.', 8),
        ('History', 'World Wars', 'easy',
         'What was the name of the military operation for the Allied invasion of Normandy on June 6, 1944?',
         '["Operation Barbarossa", "Operation Market Garden", "D-Day / Operation Overlord", "Operation Torch"]', 2,
         'Operation Overlord (commonly called D-Day) was the largest seaborne invasion in history, with Allied forces landing on five beaches in Normandy, France.', 8),
        ('History', 'World Wars', 'medium',
         'Which alliance system was a major cause of World War I escalating from a regional conflict to a world war?',
         '["The League of Nations", "Interlocking mutual defense alliances (Triple Alliance / Triple Entente)", "The UN Security Council", "The Marshall Plan"]', 1,
         'Europe\'s interlocking alliances meant that when Austria-Hungary declared war on Serbia, it triggered obligations that drew Germany, Russia, France, and Britain into the conflict.', 11),
        ('History', 'World Wars', 'medium',
         'What was the Holocaust?',
         '["A WWI battle in France", "The Nazi genocide of approximately 6 million Jews and millions of others", "The firebombing of German cities", "Stalin\'s purges in the USSR"]', 1,
         'The Holocaust was the state-sponsored systematic persecution and murder of six million Jews and millions of others (Roma, disabled people, political prisoners) by the Nazi regime during WWII.', 11),
        ('History', 'World Wars', 'medium',
         'Which event directly prompted the United States to enter World War II?',
         '["The invasion of Poland", "The Battle of Britain", "The Japanese attack on Pearl Harbor", "The fall of France"]', 2,
         'Japan\'s surprise attack on the US naval base at Pearl Harbor, Hawaii, on December 7, 1941 ("a date which will live in infamy") led the US to declare war.', 11),
        ('History', 'World Wars', 'hard',
         'What was the Schlieffen Plan?',
         '["Germany\'s plan to invade Russia first", "Germany\'s plan to quickly defeat France via Belgium then fight Russia", "The Allied plan for D-Day", "Austria-Hungary\'s mobilization strategy"]', 1,
         'The Schlieffen Plan was Germany\'s pre-WWI strategy to avoid a two-front war by rapidly defeating France through a sweep through Belgium, then turning east to face Russia.', 13),
        ('History', 'World Wars', 'hard',
         'What was the significance of the Battle of Stalingrad (1942–43)?',
         '["Germany captured the Soviet capital", "It was the turning point of WWII on the Eastern Front — Germany suffered a massive defeat", "The Soviets surrendered to Germany", "It opened the second front in France"]', 1,
         'Stalingrad was a brutal urban battle ending with the surrender of Germany\'s 6th Army. It marked the turning point on the Eastern Front and the beginning of Germany\'s retreat.', 14),
        ('History', 'World Wars', 'hard',
         'What treaty officially ended World War I, imposing heavy penalties on Germany?',
         '["Treaty of Paris", "Treaty of Utrecht", "Treaty of Versailles", "Treaty of Brest-Litovsk"]', 2,
         'The Treaty of Versailles (1919) formally ended WWI, requiring Germany to accept full blame (War Guilt Clause), pay reparations, and reduce its military.', 13),
        ('History', 'World Wars', 'medium',
         'What does "Blitzkrieg" mean, and which nation pioneered it?',
         '["Lightning war — pioneered by Germany", "Total war — pioneered by Britain", "Trench warfare — pioneered by France", "Naval blockade — pioneered by USA"]', 0,
         'Blitzkrieg ("lightning war") was a German tactic combining fast-moving armor, motorized infantry, and air support to overwhelm defenses before they could react.', 11),

        # ── American History ──────────────────────────────────────────────────
        ('History', 'American History', 'easy',
         'In which year did the United States declare independence from Britain?',
         '["1765", "1776", "1783", "1789"]', 1,
         'The Declaration of Independence was adopted on July 4, 1776, formally announcing the thirteen colonies\' separation from Britain.', 8),
        ('History', 'American History', 'easy',
         'Who was the first President of the United States?',
         '["John Adams", "Thomas Jefferson", "Benjamin Franklin", "George Washington"]', 3,
         'George Washington was unanimously elected as the first President of the United States, serving from 1789 to 1797.', 8),
        ('History', 'American History', 'medium',
         'What was the primary cause of the American Civil War (1861–1865)?',
         '["Disagreements over tariff policy only", "Slavery and its expansion into new territories", "A dispute over foreign policy with Britain", "Disagreement over the national bank"]', 1,
         'While multiple factors contributed, the central cause of the Civil War was the institution of slavery and the conflict over its expansion into new western territories.', 11),
        ('History', 'American History', 'medium',
         'What did the Emancipation Proclamation (1863) do?',
         '["Freed all slaves in the United States immediately", "Declared freedom for enslaved people in Confederate states in rebellion", "Granted women the right to vote", "Abolished the slave trade internationally"]', 1,
         'President Lincoln\'s Emancipation Proclamation declared that all enslaved persons in Confederate states in rebellion were "forever free," though it did not immediately free those in border states.', 11),
        ('History', 'American History', 'medium',
         'What was the significance of the Supreme Court\'s Brown v. Board of Education (1954) ruling?',
         '["It upheld school segregation", "It declared racial segregation in public schools unconstitutional", "It established affirmative action", "It gave voting rights to African Americans"]', 1,
         'Brown v. Board of Education overturned Plessy v. Ferguson\'s "separate but equal" doctrine, ruling that racial segregation in public schools violated the 14th Amendment.', 12),
        ('History', 'American History', 'hard',
         'What was the Boston Massacre (1770)?',
         '["A colonial tax rebellion", "British soldiers killing five colonists during a confrontation, fueling anti-British sentiment", "The burning of Boston by British troops", "A naval battle in Boston Harbor"]', 1,
         'British soldiers fired into a crowd of colonists in Boston, killing five men. The event was used as propaganda by Patriots to increase colonial opposition to British rule.', 13),
        ('History', 'American History', 'hard',
         'What was the significance of the Civil Rights Act of 1964?',
         '["It gave African Americans voting rights", "It outlawed discrimination based on race, color, religion, sex, or national origin", "It desegregated the military", "It created the NAACP"]', 1,
         'The Civil Rights Act of 1964 banned discrimination in employment and public accommodations, and prohibited unequal voter registration requirements, a landmark in the civil rights movement.', 13),
        ('History', 'American History', 'hard',
         'What was the significance of the Battle of Gettysburg (July 1–3, 1863)?',
         '["The Confederacy captured Washington D.C.", "It was the Union victory that ended the Confederacy\'s last major northern invasion", "General Lee surrendered here", "The first major battle of the Civil War"]', 1,
         'Gettysburg was the bloodiest battle of the Civil War and the decisive defeat of Lee\'s Army of Northern Virginia during its invasion of the North, a major turning point for the Union.', 14),

        # ── Modern History ────────────────────────────────────────────────────
        ('History', 'Modern History', 'easy',
         'What were the two superpowers in the Cold War?',
         '["USA and China", "USA and USSR", "UK and USSR", "USA and Germany"]', 1,
         'The Cold War (1947–1991) was a geopolitical tension between the United States and the Soviet Union (USSR), representing capitalism vs. communism.', 8),
        ('History', 'Modern History', 'medium',
         'What event symbolized the end of the Cold War division of Europe?',
         '["The Cuban Missile Crisis", "The formation of NATO", "The fall of the Berlin Wall in 1989", "The Korean War armistice"]', 2,
         'The fall of the Berlin Wall on November 9, 1989 symbolized the collapse of the Iron Curtain and led to German reunification and the eventual dissolution of the USSR.', 11),
        ('History', 'Modern History', 'medium',
         'In what year did the Soviet Union officially dissolve?',
         '["1989", "1990", "1991", "1993"]', 2,
         'The USSR officially dissolved on December 25, 1991, when Mikhail Gorbachev resigned and the Soviet flag was lowered for the last time over the Kremlin.', 11),
        ('History', 'Modern History', 'medium',
         'What happened on September 11, 2001?',
         '["A major earthquake struck New York", "Al-Qaeda terrorists hijacked planes and attacked the World Trade Center and Pentagon", "The US invaded Iraq", "The Oklahoma City bombing"]', 1,
         'On 9/11, Al-Qaeda terrorists hijacked four commercial aircraft, crashing two into the World Trade Center, one into the Pentagon, and one in Pennsylvania, killing nearly 3,000 people.', 11),
        ('History', 'Modern History', 'hard',
         'What was the Marshall Plan?',
         '["The US military strategy in Vietnam", "A US economic aid program to rebuild Western Europe after WWII", "NATO\'s defense budget plan", "The Soviet five-year economic plan"]', 1,
         'The Marshall Plan (1948) was a US program providing over $12 billion to rebuild Western European economies after WWII, aiming to prevent the spread of communism.', 13),
        ('History', 'Modern History', 'hard',
         'What was the Cuban Missile Crisis (1962)?',
         '["Cuba\'s invasion of the USA", "A 13-day nuclear standoff after the USSR placed missiles in Cuba", "The Bay of Pigs invasion", "Castro\'s rise to power"]', 1,
         'When the US discovered Soviet nuclear missiles in Cuba, a 13-day standoff between Kennedy and Khrushchev brought the world to the brink of nuclear war before a diplomatic resolution.', 14),

        # ── Geography ────────────────────────────────────────────────────────
        ('History', 'Geography', 'easy',
         'What is the capital of France?',
         '["Berlin", "London", "Madrid", "Paris"]', 3,
         'Paris is the capital and largest city of France, located in northern France along the Seine River.', 7),
        ('History', 'Geography', 'easy',
         'Which is the longest river in the world?',
         '["Amazon", "Nile", "Yangtze", "Mississippi"]', 1,
         'The Nile River in Africa, at approximately 6,650 km (4,130 miles), is generally recognized as the world\'s longest river.', 7),
        ('History', 'Geography', 'medium',
         'On which continent is the Amazon Rainforest primarily located?',
         '["Africa", "Asia", "South America", "Australia"]', 2,
         'The Amazon Rainforest spans nine countries, primarily Brazil, and is located in South America. It is the world\'s largest tropical rainforest.', 9),
        ('History', 'Geography', 'medium',
         'How many continents are there on Earth?',
         '["5", "6", "7", "8"]', 2,
         'The seven continents are Africa, Antarctica, Asia, Australia/Oceania, Europe, North America, and South America.', 9),
        ('History', 'Geography', 'medium',
         'What is the highest mountain in the world?',
         '["K2", "Kangchenjunga", "Mount Everest", "Mont Blanc"]', 2,
         'Mount Everest in the Himalayas on the Nepal-China border stands at 8,849 m (29,032 ft), the highest point on Earth above sea level.', 9),
        ('History', 'Geography', 'hard',
         'Which tectonic plates are responsible for the formation of the Himalayan mountain range?',
         '["Pacific Plate and North American Plate", "African Plate and Eurasian Plate", "Indian Plate and Eurasian Plate", "Arabian Plate and African Plate"]', 2,
         'The Himalayas formed from the collision of the Indian Plate and the Eurasian Plate, a process that began around 50 million years ago and continues today.', 13),
    ]


def _science_extra_questions():
    return [
        # ── Biology ───────────────────────────────────────────────────────────
        ('Science', 'Biology', 'easy',
         'What is the basic structural and functional unit of all living organisms?',
         '["Atom", "Cell", "Organ", "Tissue"]', 1,
         'The cell is the basic unit of life, as established by cell theory. All living things are made of one or more cells.', 8),
        ('Science', 'Biology', 'easy',
         'What process do plants use to convert sunlight into food?',
         '["Cellular respiration", "Photosynthesis", "Fermentation", "Transpiration"]', 1,
         'Photosynthesis is the process by which plants, algae, and some bacteria convert light energy, water, and CO₂ into glucose and oxygen.', 8),
        ('Science', 'Biology', 'easy',
         'What molecule carries genetic information in most living organisms?',
         '["RNA", "ATP", "DNA", "Protein"]', 2,
         'DNA (deoxyribonucleic acid) stores and transmits hereditary information. RNA helps express that information in the form of proteins.', 8),
        ('Science', 'Biology', 'medium',
         'What is mitosis?',
         '["Cell division producing gametes with half the chromosomes", "Cell division producing two genetically identical daughter cells", "DNA replication only", "Protein synthesis"]', 1,
         'Mitosis is the type of cell division that produces two genetically identical daughter cells with the same number of chromosomes as the parent cell, used for growth and repair.', 10),
        ('Science', 'Biology', 'medium',
         'According to Darwin\'s theory, what is natural selection?',
         '["Random mutation with no direction", "Organisms with favorable traits survive and reproduce more successfully", "The strongest animal always wins", "Organisms adapt by choice"]', 1,
         'Natural selection is the process whereby organisms with traits better suited to their environment tend to survive and reproduce more, passing those traits to offspring.', 10),
        ('Science', 'Biology', 'medium',
         'What is the role of the ribosome in a cell?',
         '["Energy production", "DNA replication", "Protein synthesis", "Lipid storage"]', 2,
         'Ribosomes are the cellular machinery that synthesize proteins by translating messenger RNA (mRNA) sequences into chains of amino acids.', 10),
        ('Science', 'Biology', 'medium',
         'What is an ecosystem?',
         '["A single species in its habitat", "All the plants in a region", "A community of organisms interacting with their physical environment", "The food chain only"]', 2,
         'An ecosystem consists of all the living organisms (biotic) in an area interacting with each other and with the non-living (abiotic) environment such as water, soil, and climate.', 10),
        ('Science', 'Biology', 'hard',
         'What is the difference between mitosis and meiosis?',
         '["Mitosis produces 4 cells; meiosis produces 2", "Mitosis produces 2 identical diploid cells; meiosis produces 4 genetically unique haploid cells", "They are the same process", "Meiosis occurs in all body cells"]', 1,
         'Mitosis yields 2 genetically identical diploid cells (for growth/repair). Meiosis yields 4 genetically unique haploid cells (for sexual reproduction).', 13),
        ('Science', 'Biology', 'hard',
         'What is the Hardy-Weinberg principle used for?',
         '["Calculating mutation rates", "Modeling allele frequencies in a non-evolving population as a baseline", "Predicting which species will survive", "Measuring biodiversity"]', 1,
         'Hardy-Weinberg equilibrium describes the allele and genotype frequencies expected in a population not undergoing evolution, providing a baseline to detect evolutionary change.', 14),
        ('Science', 'Biology', 'hard',
         'What are the four bases in DNA?',
         '["Alanine, Glycine, Cytosine, Thymine", "Adenine, Guanine, Cytosine, Thymine", "Adenine, Uracil, Cytosine, Guanine", "Adenine, Guanine, Cytosine, Serine"]', 1,
         'DNA contains four nitrogenous bases: Adenine (A), Guanine (G), Cytosine (C), and Thymine (T). In RNA, Thymine is replaced by Uracil.', 13),
        ('Science', 'Biology', 'medium',
         'What is a food chain\'s "apex predator"?',
         '["A plant at the base of the food chain", "An animal that is preyed upon by many species", "A predator at the top with no natural predators", "A decomposer in the ecosystem"]', 2,
         'An apex predator sits at the top of a food chain and is not regularly preyed upon by any other animal, playing a crucial role in regulating ecosystem balance.', 10),
        ('Science', 'Biology', 'hard',
         'What is CRISPR-Cas9 used for in biology?',
         '["Sequencing DNA rapidly", "A gene-editing tool that can precisely cut and modify DNA sequences", "Producing insulin in bacteria", "Cloning entire organisms"]', 1,
         'CRISPR-Cas9 is a revolutionary gene-editing technology that uses a guide RNA to direct the Cas9 enzyme to cut DNA at a specific location, enabling precise genetic modifications.', 14),

        # ── Chemistry ────────────────────────────────────────────────────────
        ('Science', 'Chemistry', 'easy',
         'What is the chemical symbol for water?',
         '["WA", "H2O", "HO2", "W"]', 1,
         'Water is composed of two hydrogen atoms bonded to one oxygen atom, giving it the chemical formula H₂O.', 7),
        ('Science', 'Chemistry', 'easy',
         'What is the atomic number of carbon?',
         '["2", "4", "6", "8"]', 2,
         'Carbon has 6 protons in its nucleus, giving it atomic number 6. It is the basis of all organic chemistry.', 7),
        ('Science', 'Chemistry', 'medium',
         'What holds atoms together in a covalent bond?',
         '["Electrostatic attraction between opposite charges", "Shared electrons between atoms", "Transfer of electrons from one atom to another", "Magnetic attraction"]', 1,
         'A covalent bond forms when two atoms share one or more pairs of electrons, creating a stable connection between non-metal atoms.', 10),
        ('Science', 'Chemistry', 'medium',
         'What does the periodic table organize elements by?',
         '["Alphabetical order", "Atomic mass only", "Increasing atomic number and recurring chemical properties", "Discovery date"]', 2,
         'The modern periodic table arranges elements by increasing atomic number. Elements in the same column (group) have similar chemical properties due to the same number of valence electrons.', 10),
        ('Science', 'Chemistry', 'medium',
         'What is an exothermic reaction?',
         '["A reaction that absorbs heat from surroundings", "A reaction that releases heat to the surroundings", "A reaction requiring a catalyst", "A reaction that only occurs at high temperatures"]', 1,
         'An exothermic reaction releases energy (usually as heat) to the surroundings. Examples include combustion and many oxidation reactions.', 10),
        ('Science', 'Chemistry', 'medium',
         'What is the pH scale used to measure?',
         '["Temperature of a solution", "The concentration of dissolved salts", "The acidity or basicity (alkalinity) of a solution", "The density of a liquid"]', 2,
         'The pH scale (0–14) measures how acidic or basic a solution is. pH 7 is neutral, below 7 is acidic, and above 7 is basic (alkaline).', 10),
        ('Science', 'Chemistry', 'hard',
         'What is Avogadro\'s number and what does it represent?',
         '["6.022 × 10²³ — the number of particles in one mole of a substance", "3.14 × 10⁸ — the speed of light constant", "9.8 m/s² — gravitational acceleration", "1.38 × 10⁻²³ — Boltzmann constant"]', 0,
         'Avogadro\'s number (6.022 × 10²³) is the number of atoms, molecules, or ions in one mole of a substance, linking macroscopic measurements to atomic-scale quantities.', 13),
        ('Science', 'Chemistry', 'hard',
         'What is an ionic bond?',
         '["Sharing of electrons between atoms", "Electrostatic attraction between positively and negatively charged ions formed by electron transfer", "A bond between two metal atoms", "A weak intermolecular force"]', 1,
         'Ionic bonds form when one atom transfers electrons to another, creating oppositely charged ions (cation and anion) that attract each other, typical of metal-nonmetal compounds like NaCl.', 13),
        ('Science', 'Chemistry', 'hard',
         'What is Le Chatelier\'s principle?',
         '["Energy cannot be created or destroyed", "A system at equilibrium will shift to oppose any imposed change", "Reaction rate doubles with every 10°C increase", "Gases expand to fill their container"]', 1,
         'Le Chatelier\'s principle states that if a stress (change in concentration, temperature, or pressure) is applied to a system at equilibrium, the system shifts to minimize that stress.', 14),
        ('Science', 'Chemistry', 'medium',
         'What type of element is found on the left side of the periodic table?',
         '["Nonmetals", "Metalloids", "Metals", "Noble gases"]', 2,
         'Metals occupy the left and center of the periodic table. They are generally shiny, malleable, good conductors of heat and electricity.', 10),
        ('Science', 'Chemistry', 'hard',
         'In organic chemistry, what distinguishes a saturated hydrocarbon from an unsaturated one?',
         '["Saturated hydrocarbons contain only C-C single bonds; unsaturated contain one or more double or triple bonds", "Saturated ones contain oxygen atoms", "Unsaturated ones only contain hydrogen", "Saturated ones have a ring structure"]', 0,
         'Saturated hydrocarbons (alkanes) have only single C-C bonds. Unsaturated hydrocarbons (alkenes, alkynes) contain one or more double or triple bonds between carbon atoms.', 14),
        ('Science', 'Chemistry', 'medium',
         'What is a catalyst?',
         '["A substance consumed in a reaction", "A substance that increases reaction rate without being consumed", "A product of a chemical reaction", "A type of chemical bond"]', 1,
         'A catalyst speeds up a chemical reaction by providing an alternative pathway with lower activation energy, and it is not permanently consumed in the process.', 10),

        # ── Physics ───────────────────────────────────────────────────────────
        ('Science', 'Physics', 'easy',
         'What is Newton\'s First Law of Motion?',
         '["F = ma", "An object at rest stays at rest, and an object in motion stays in motion, unless acted upon by an external force", "Every action has an equal and opposite reaction", "Energy cannot be created or destroyed"]', 1,
         'Newton\'s First Law (the law of inertia) states that objects maintain their state of motion unless a net external force acts on them.', 8),
        ('Science', 'Physics', 'easy',
         'What is the formula for Newton\'s Second Law of Motion?',
         '["E = mc²", "F = ma", "v = d/t", "P = mv"]', 1,
         'Newton\'s Second Law states that Force equals mass times acceleration (F = ma), meaning a larger force produces a larger acceleration for the same mass.', 8),
        ('Science', 'Physics', 'medium',
         'What is kinetic energy?',
         '["Energy stored in an object\'s position", "Energy of motion", "Energy released in chemical reactions", "Electrical energy"]', 1,
         'Kinetic energy is the energy an object possesses due to its motion. KE = ½mv², where m is mass and v is velocity.', 10),
        ('Science', 'Physics', 'medium',
         'What is the speed of light in a vacuum approximately equal to?',
         '["3 × 10⁶ m/s", "3 × 10⁸ m/s", "3 × 10¹⁰ m/s", "3 × 10⁴ m/s"]', 1,
         'The speed of light in a vacuum (c) is approximately 3 × 10⁸ m/s (299,792,458 m/s). It is a fundamental constant in physics.', 11),
        ('Science', 'Physics', 'medium',
         'What type of wave requires a medium to travel through?',
         '["Electromagnetic waves", "Light waves", "Mechanical waves", "Radio waves"]', 2,
         'Mechanical waves (like sound and water waves) require a medium (solid, liquid, or gas) to propagate. Electromagnetic waves can travel through a vacuum.', 10),
        ('Science', 'Physics', 'medium',
         'What is Ohm\'s Law?',
         '["Power = Voltage × Current", "Voltage = Current × Resistance (V = IR)", "Current = Power / Voltage", "Resistance = Voltage × Current"]', 1,
         'Ohm\'s Law states that voltage (V) equals current (I) multiplied by resistance (R): V = IR. It describes the relationship between these electrical quantities in a conductor.', 11),
        ('Science', 'Physics', 'hard',
         'What is the law of conservation of energy?',
         '["Energy can be created from nothing in nuclear reactions", "The total energy of an isolated system remains constant — energy transforms but is not created or destroyed", "Kinetic energy is always conserved in collisions", "Thermal energy always increases"]', 1,
         'The law of conservation of energy (first law of thermodynamics) states that energy cannot be created or destroyed, only converted from one form to another.', 13),
        ('Science', 'Physics', 'hard',
         'What phenomenon does the Doppler effect describe?',
         '["The bending of light around massive objects", "The change in observed frequency of a wave due to relative motion between source and observer", "The interference of two waves", "The reflection of sound off surfaces"]', 1,
         'The Doppler effect describes how the observed frequency of a wave changes when the source and observer are moving relative to each other — e.g., a passing ambulance siren.', 13),
        ('Science', 'Physics', 'hard',
         'In the photoelectric effect, what did Einstein explain about light?',
         '["Light travels in straight lines", "Light is a wave only", "Light consists of quantized packets of energy (photons) that can eject electrons from a metal", "Light slows down in a vacuum"]', 2,
         'Einstein\'s 1905 explanation of the photoelectric effect showed that light comes in discrete energy packets called photons, supporting quantum theory and earning him the Nobel Prize.', 14),
        ('Science', 'Physics', 'hard',
         'What is the second law of thermodynamics?',
         '["Energy is conserved in all processes", "The entropy of an isolated system tends to increase over time", "Every action has an equal reaction", "Absolute zero is unattainable"]', 1,
         'The second law of thermodynamics states that the entropy (disorder) of an isolated system always increases over time, explaining why heat flows from hot to cold naturally.', 14),

        # ── Earth Science ─────────────────────────────────────────────────────
        ('Science', 'Earth Science', 'easy',
         'What causes earthquakes?',
         '["Volcanic eruptions only", "The movement and collision of tectonic plates", "Meteorite impacts", "Ocean currents"]', 1,
         'Earthquakes occur when stress built up along tectonic plate boundaries or faults is suddenly released, sending seismic waves through the Earth.', 8),
        ('Science', 'Earth Science', 'medium',
         'What are the three types of rock in the rock cycle?',
         '["Igneous, sedimentary, and metamorphic", "Granite, limestone, and marble", "Volcanic, oceanic, and continental", "Hard, soft, and medium"]', 0,
         'The three major rock types are igneous (formed from cooled magma/lava), sedimentary (formed from compacted sediments), and metamorphic (formed by heat and pressure transforming existing rocks).', 10),
        ('Science', 'Earth Science', 'medium',
         'What is the greenhouse effect?',
         '["The cooling of Earth by clouds", "The trapping of solar heat in Earth\'s atmosphere by greenhouse gases", "The reflection of sunlight by ice caps", "The seasonal warming in summer"]', 1,
         'Greenhouse gases (CO₂, water vapor, methane) absorb and re-emit infrared radiation, trapping heat in the atmosphere and warming Earth\'s surface.', 10),
        ('Science', 'Earth Science', 'medium',
         'At which type of plate boundary do two tectonic plates move apart?',
         '["Convergent boundary", "Transform boundary", "Divergent boundary", "Subduction zone"]', 2,
         'At divergent boundaries, plates move apart and magma rises to fill the gap, creating new oceanic crust. The Mid-Atlantic Ridge is a prominent example.', 11),
        ('Science', 'Earth Science', 'hard',
         'What is the difference between weather and climate?',
         '["They are the same thing", "Weather is short-term atmospheric conditions; climate is long-term average patterns", "Climate changes daily; weather is stable", "Weather only refers to temperature; climate includes precipitation"]', 1,
         'Weather describes short-term atmospheric conditions at a specific time and place. Climate refers to the long-term average of weather patterns over a region (typically 30+ years).', 12),
        ('Science', 'Earth Science', 'hard',
         'What is the theory of continental drift, and who proposed it?',
         '["Earth\'s magnetic field moves continents — proposed by Newton", "Continents were once joined and have drifted apart over millions of years — proposed by Alfred Wegener", "Ocean floors spread due to volcanic activity — proposed by Darwin", "Continents move due to tidal forces — proposed by Einstein"]', 1,
         'Alfred Wegener (1912) proposed that Earth\'s continents were once a single landmass (Pangaea) that broke apart and drifted to their current positions, supported by fossil and geological evidence.', 14),
    ]


# ── Player helpers ─────────────────────────────────────────────────────────────

def get_or_create_player(email, username=None):
    with get_db() as db:
        row = db.execute("SELECT * FROM players WHERE email=?", (email,)).fetchone()
        if row:
            return dict(row)
        uname = username or email.split('@')[0]
        db.execute(
            "INSERT INTO players (email, username) VALUES (?,?)",
            (email, uname)
        )
        return dict(db.execute("SELECT * FROM players WHERE email=?", (email,)).fetchone())


def get_player(player_id):
    with get_db() as db:
        row = db.execute("SELECT * FROM players WHERE id=?", (player_id,)).fetchone()
        return dict(row) if row else None


def update_player(player_id, **kwargs):
    allowed = {'username', 'avatar', 'role', 'xp', 'level', 'streak', 'last_login'}
    fields = {k: v for k, v in kwargs.items() if k in allowed}
    if not fields:
        return
    sql = "UPDATE players SET " + ", ".join(f"{k}=?" for k in fields) + " WHERE id=?"
    with get_db() as db:
        db.execute(sql, list(fields.values()) + [player_id])


def add_xp(player_id, xp):
    p = get_player(player_id)
    new_xp = p['xp'] + xp
    new_level = max(1, new_xp // 100 + 1)
    update_player(player_id, xp=new_xp, level=new_level)
    return new_xp, new_level


# ── Question helpers ───────────────────────────────────────────────────────────

def get_subjects():
    with get_db() as db:
        rows = db.execute("SELECT DISTINCT subject FROM questions ORDER BY subject").fetchall()
        return [r['subject'] for r in rows]


def get_topics(subject):
    with get_db() as db:
        rows = db.execute(
            "SELECT DISTINCT topic FROM questions WHERE subject=? ORDER BY topic", (subject,)
        ).fetchall()
        return [r['topic'] for r in rows]


def get_questions(subject=None, topic=None, difficulty=None, limit=10):
    sql = "SELECT * FROM questions WHERE 1=1"
    params = []
    if subject:
        sql += " AND subject=?"; params.append(subject)
    if topic:
        sql += " AND topic=?"; params.append(topic)
    if difficulty:
        sql += " AND difficulty=?"; params.append(difficulty)
    sql += " ORDER BY RANDOM() LIMIT ?"
    params.append(limit)
    with get_db() as db:
        rows = db.execute(sql, params).fetchall()
        result = []
        for r in rows:
            q = dict(r)
            q['choices'] = json.loads(q['choices'])
            result.append(q)
        return result


# ── Session helpers ────────────────────────────────────────────────────────────

def create_session(player_id, mode, subject, topic, difficulty):
    with get_db() as db:
        cur = db.execute(
            "INSERT INTO game_sessions (player_id, mode, subject, topic, difficulty) VALUES (?,?,?,?,?)",
            (player_id, mode, subject, topic, difficulty)
        )
        return cur.lastrowid


def complete_session(session_id, score, total, xp_earned, time_taken, answers):
    with get_db() as db:
        db.execute(
            "UPDATE game_sessions SET score=?, total=?, xp_earned=?, time_taken=?, answers=?, completed=1 WHERE id=?",
            (score, total, xp_earned, time_taken, json.dumps(answers), session_id)
        )


def get_session(session_id):
    with get_db() as db:
        row = db.execute("SELECT * FROM game_sessions WHERE id=?", (session_id,)).fetchone()
        return dict(row) if row else None


def get_player_sessions(player_id, limit=10):
    with get_db() as db:
        rows = db.execute(
            "SELECT * FROM game_sessions WHERE player_id=? AND completed=1 ORDER BY created_at DESC LIMIT ?",
            (player_id, limit)
        ).fetchall()
        return [dict(r) for r in rows]


# ── Leaderboard ────────────────────────────────────────────────────────────────

def get_leaderboard(limit=20):
    with get_db() as db:
        rows = db.execute("""
            SELECT p.id, p.username, p.avatar, p.xp, p.level,
                   COUNT(s.id) as games_played,
                   SUM(CASE WHEN s.completed=1 THEN s.score ELSE 0 END) as total_score
            FROM players p
            LEFT JOIN game_sessions s ON s.player_id = p.id
            GROUP BY p.id
            ORDER BY p.xp DESC
            LIMIT ?
        """, (limit,)).fetchall()
        return [dict(r) for r in rows]


# ── Daily challenge ────────────────────────────────────────────────────────────

def get_daily_challenge():
    today = date.today().isoformat()
    with get_db() as db:
        row = db.execute(
            "SELECT * FROM daily_challenges WHERE challenge_date=?", (today,)
        ).fetchone()
        if row:
            return dict(row)
        # Create today's challenge
        subjects = ['Math', 'Science', 'Language', 'History']
        import random
        subject = subjects[hash(today) % len(subjects)]
        qs = get_questions(subject=subject, limit=5)
        ids = [q['id'] for q in qs]
        db.execute(
            "INSERT INTO daily_challenges (challenge_date, subject, question_ids) VALUES (?,?,?)",
            (today, subject, json.dumps(ids))
        )
        return {'challenge_date': today, 'subject': subject, 'question_ids': json.dumps(ids)}


# ── Subject mastery ────────────────────────────────────────────────────────────

def get_subject_mastery(player_id):
    """Return {subject: pct_correct} for all subjects the player has attempted."""
    with get_db() as db:
        rows = db.execute("""
            SELECT gs.subject,
                   SUM(gs.score)  AS correct,
                   SUM(gs.total)  AS total
            FROM game_sessions gs
            WHERE gs.player_id=? AND gs.completed=1 AND gs.subject IS NOT NULL AND gs.subject != ''
            GROUP BY gs.subject
        """, (player_id,)).fetchall()
        result = {}
        for r in rows:
            if r['total']:
                result[r['subject']] = round(r['correct'] / r['total'] * 100)
        return result


# ── Achievements ───────────────────────────────────────────────────────────────

ACHIEVEMENT_DEFS = [
    {'id': 'first_game',   'badge': '🎮', 'name': 'First Steps',      'desc': 'Play your first game'},
    {'id': 'ten_games',    'badge': '🔟', 'name': '10 Games Played',  'desc': 'Complete 10 games'},
    {'id': 'perfect',      'badge': '💯', 'name': 'Perfect Score',    'desc': 'Get 100% on any game'},
    {'id': 'streak_3',     'badge': '🔥', 'name': 'On Fire',          'desc': '3-day login streak'},
    {'id': 'streak_7',     'badge': '🌟', 'name': 'Week Warrior',     'desc': '7-day login streak'},
    {'id': 'math_master',  'badge': '➕', 'name': 'Math Master',      'desc': '80%+ accuracy in Math'},
    {'id': 'sci_master',   'badge': '🔬', 'name': 'Science Ace',      'desc': '80%+ accuracy in Science'},
    {'id': 'cs_master',    'badge': '💻', 'name': 'Code Wizard',      'desc': '80%+ accuracy in Computer Science'},
    {'id': 'level_5',      'badge': '⬆️', 'name': 'Level 5',          'desc': 'Reach level 5'},
    {'id': 'level_10',     'badge': '🏅', 'name': 'Level 10',         'desc': 'Reach level 10'},
    {'id': 'xp_500',       'badge': '⚡', 'name': '500 XP',           'desc': 'Earn 500 total XP'},
    {'id': 'xp_1000',      'badge': '💎', 'name': '1000 XP',          'desc': 'Earn 1000 total XP'},
    {'id': 'daily_done',   'badge': '📅', 'name': 'Daily Champion',   'desc': 'Complete a daily challenge'},
    {'id': 'survival',     'badge': '💀', 'name': 'Survivor',         'desc': 'Complete survival mode'},
    {'id': 'speed_demon',  'badge': '⚡', 'name': 'Speed Demon',      'desc': 'Complete blitz mode'},
]

def get_player_achievements(player_id):
    """Return list of earned achievement defs for a player."""
    player = get_player(player_id)
    sessions = get_player_sessions(player_id, limit=1000)
    mastery = get_subject_mastery(player_id)

    earned_ids = set()
    if sessions:
        earned_ids.add('first_game')
    if len(sessions) >= 10:
        earned_ids.add('ten_games')
    if any(s['score'] == s['total'] and s['total'] > 0 for s in sessions):
        earned_ids.add('perfect')
    if player and player.get('streak', 0) >= 3:
        earned_ids.add('streak_3')
    if player and player.get('streak', 0) >= 7:
        earned_ids.add('streak_7')
    if mastery.get('Math', 0) >= 80:
        earned_ids.add('math_master')
    if mastery.get('Science', 0) >= 80:
        earned_ids.add('sci_master')
    if mastery.get('Computer Science', 0) >= 80:
        earned_ids.add('cs_master')
    if player and player.get('level', 1) >= 5:
        earned_ids.add('level_5')
    if player and player.get('level', 1) >= 10:
        earned_ids.add('level_10')
    if player and player.get('xp', 0) >= 500:
        earned_ids.add('xp_500')
    if player and player.get('xp', 0) >= 1000:
        earned_ids.add('xp_1000')
    if any(s['mode'] == 'daily' for s in sessions):
        earned_ids.add('daily_done')
    if any(s['mode'] == 'survival' and s['score'] > 0 for s in sessions):
        earned_ids.add('survival')
    if any(s['mode'] == 'blitz' for s in sessions):
        earned_ids.add('speed_demon')

    return [
        {**d, 'earned': d['id'] in earned_ids}
        for d in ACHIEVEMENT_DEFS
    ]


# ── Leagues ────────────────────────────────────────────────────────────────────

LEAGUES = [
    {'id': 'bronze',   'name': 'Bronze',   'icon': '🥉', 'min_xp': 0,      'color': '#cd7f32', 'bg': 'rgba(205,127,50,.08)',  'border': 'rgba(205,127,50,.3)'},
    {'id': 'silver',   'name': 'Silver',   'icon': '🥈', 'min_xp': 500,    'color': '#94a3b8', 'bg': 'rgba(148,163,184,.08)', 'border': 'rgba(148,163,184,.3)'},
    {'id': 'gold',     'name': 'Gold',     'icon': '🥇', 'min_xp': 1500,   'color': '#d97706', 'bg': 'rgba(217,119,6,.08)',   'border': 'rgba(217,119,6,.3)'},
    {'id': 'platinum', 'name': 'Platinum', 'icon': '💎', 'min_xp': 3000,   'color': '#0ea5e9', 'bg': 'rgba(14,165,233,.08)',  'border': 'rgba(14,165,233,.3)'},
    {'id': 'diamond',  'name': 'Diamond',  'icon': '💠', 'min_xp': 6000,   'color': '#8b5cf6', 'bg': 'rgba(139,92,246,.08)',  'border': 'rgba(139,92,246,.3)'},
    {'id': 'master',   'name': 'Master',   'icon': '👑', 'min_xp': 12000,  'color': '#dc2626', 'bg': 'rgba(220,38,38,.08)',   'border': 'rgba(220,38,38,.3)'},
]


def get_league(xp):
    """Return the current league dict for a given XP total."""
    current = LEAGUES[0]
    for lg in LEAGUES:
        if xp >= lg['min_xp']:
            current = lg
    return current


def get_next_league(xp):
    """Return the next league dict, or None if already Master."""
    for i, lg in enumerate(LEAGUES):
        if xp < lg['min_xp']:
            return lg
    return None


def get_league_progress(xp):
    """Return a dict with current league, next league, xp_in_tier, xp_needed, and pct."""
    current = get_league(xp)
    nxt = get_next_league(xp)
    if nxt is None:
        return {
            'current': current,
            'next': None,
            'xp_in_tier': xp - current['min_xp'],
            'xp_needed': 0,
            'pct': 100,
        }
    tier_size = nxt['min_xp'] - current['min_xp']
    xp_in_tier = xp - current['min_xp']
    xp_needed = nxt['min_xp'] - xp
    pct = round(xp_in_tier / tier_size * 100)
    return {
        'current': current,
        'next': nxt,
        'xp_in_tier': xp_in_tier,
        'xp_needed': xp_needed,
        'pct': pct,
    }


def get_league_members(league_id, limit=50):
    """Return players currently in a specific league."""
    league = next((lg for lg in LEAGUES if lg['id'] == league_id), None)
    if league is None:
        return []
    next_league = next((lg for lg in LEAGUES if lg['min_xp'] > league['min_xp']), None)
    with get_db() as db:
        if next_league:
            rows = db.execute(
                "SELECT * FROM players WHERE xp >= ? AND xp < ? ORDER BY xp DESC LIMIT ?",
                (league['min_xp'], next_league['min_xp'], limit)
            ).fetchall()
        else:
            rows = db.execute(
                "SELECT * FROM players WHERE xp >= ? ORDER BY xp DESC LIMIT ?",
                (league['min_xp'], limit)
            ).fetchall()
    return [dict(r) for r in rows]
