"""
Elementary School Math Question Generator (K–5)
Covers: Counting, Addition, Subtraction, Multiplication, Division,
        Fractions, Place Value, Time, Money, Geometry, Patterns, Measurement
"""
import random
import json

def _q(topic, diff, question, choices, answer_idx, explanation, grade=2):
    return ('Math', topic, diff, question, json.dumps(choices), answer_idx, explanation, grade)

def _shuffle_choices(correct, wrongs, rng):
    choices = list(rng.sample(wrongs, min(3, len(wrongs))))
    idx = rng.randint(0, min(3, len(choices)))
    choices.insert(idx, correct)
    return choices[:4], idx


# ── Generators ──────────────────────────────────────────────────────────────

def gen_counting(n=40, seed=None):
    """Count objects within 0–20 (K)."""
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        count = r.randint(1, 20)
        ans = str(count)
        wrongs = [str(count + 1), str(count - 1 if count > 1 else count + 2), str(count + 2)]
        wrongs = [w for w in wrongs if w != ans]
        choices, idx = _shuffle_choices(ans, wrongs[:3], r)
        qs.append(_q('Counting', 'easy',
                     f"How many objects are there? {'⭐' * count}",
                     choices, idx, f"Count each star one by one. There are {count} stars.", 0))
    return qs


def gen_addition_basic(n=60, seed=None):
    """Addition within 20 (Grade 1) and within 100 (Grade 2)."""
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        grade = r.choice([1, 2])
        limit = 10 if grade == 1 else 50
        a = r.randint(1, limit)
        b = r.randint(1, limit)
        ans = a + b
        wrongs = [ans + 1, ans - 1, ans + 2]
        wrongs = [str(w) for w in wrongs if w != ans and w > 0]
        choices, idx = _shuffle_choices(str(ans), wrongs[:3], r)
        diff = 'easy' if grade == 1 else 'medium'
        qs.append(_q('Addition', diff, f"What is {a} + {b}?",
                     choices, idx, f"{a} + {b} = {ans}.", grade))
    return qs


def gen_subtraction_basic(n=50, seed=None):
    """Subtraction within 20 (Grade 1) and within 100 (Grade 2)."""
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        grade = r.choice([1, 2])
        limit = 20 if grade == 1 else 100
        a = r.randint(5, limit)
        b = r.randint(1, a)
        ans = a - b
        wrongs = [ans + 1, ans - 1, ans + 2]
        wrongs = [str(w) for w in wrongs if w != ans and w >= 0]
        choices, idx = _shuffle_choices(str(ans), wrongs[:3], r)
        diff = 'easy' if grade == 1 else 'medium'
        qs.append(_q('Subtraction', diff, f"What is {a} − {b}?",
                     choices, idx, f"{a} − {b} = {ans}.", grade))
    return qs


def gen_multiplication_tables(n=60, seed=None):
    """Times tables 1–12 (Grade 3)."""
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        a = r.randint(1, 12)
        b = r.randint(1, 12)
        ans = a * b
        wrongs = [ans + a, ans - b if ans > b else ans + b, ans + 1, (a + 1) * b]
        wrongs = [str(w) for w in wrongs if w != ans and w > 0]
        choices, idx = _shuffle_choices(str(ans), wrongs[:3], r)
        diff = 'easy' if max(a, b) <= 5 else ('medium' if max(a, b) <= 9 else 'hard')
        qs.append(_q('Multiplication', diff, f"What is {a} × {b}?",
                     choices, idx, f"{a} × {b} = {ans}.", 3))
    return qs


def gen_division_basic(n=40, seed=None):
    """Basic division (Grade 3–4)."""
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        divisor = r.randint(2, 12)
        quotient = r.randint(1, 12)
        dividend = divisor * quotient
        ans = quotient
        wrongs = [ans + 1, ans - 1 if ans > 1 else ans + 2, ans + 2]
        wrongs = [str(w) for w in wrongs if w != ans and w > 0]
        choices, idx = _shuffle_choices(str(ans), wrongs[:3], r)
        qs.append(_q('Division', 'medium', f"What is {dividend} ÷ {divisor}?",
                     choices, idx, f"{dividend} ÷ {divisor} = {ans}.", 3))
    return qs


def gen_place_value(n=40, seed=None):
    """Place value: hundreds, tens, ones (Grade 2–4)."""
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        qtype = r.choice(['ones', 'tens', 'hundreds'])
        if qtype == 'ones':
            num = r.randint(11, 99)
            digit = num % 10
            q_text = f"What is the ones digit of {num}?"
            expl = f"In {num}, the ones place is {digit}."
        elif qtype == 'tens':
            num = r.randint(10, 999)
            digit = (num // 10) % 10
            q_text = f"What is the tens digit of {num}?"
            expl = f"In {num}, the tens place is {digit}."
        else:
            num = r.randint(100, 999)
            digit = num // 100
            q_text = f"What is the hundreds digit of {num}?"
            expl = f"In {num}, the hundreds place is {digit}."
        ans = str(digit)
        wrongs = [str((digit + 1) % 10), str((digit + 2) % 10), str((digit + 3) % 10)]
        wrongs = [w for w in wrongs if w != ans]
        choices, idx = _shuffle_choices(ans, wrongs[:3], r)
        qs.append(_q('Place Value', 'easy', q_text, choices, idx, expl, 2))
    return qs


def gen_fractions_basic(n=40, seed=None):
    """Basic fractions: identify, compare, equivalent (Grade 2–4)."""
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        qtype = r.choice(['name', 'compare', 'equivalent'])
        if qtype == 'name':
            denom = r.choice([2, 3, 4, 6, 8])
            numer = r.randint(1, denom - 1)
            ans = f"{numer}/{denom}"
            part_words = {2: 'halves', 3: 'thirds', 4: 'fourths', 6: 'sixths', 8: 'eighths'}
            q_text = f"A shape is divided into {denom} equal parts. {numer} part(s) are shaded. What fraction is shaded?"
            expl = f"{numer} out of {denom} equal parts = {numer}/{denom}."
            wrongs = [f"{numer + 1}/{denom}", f"{numer}/{denom + 1}", f"{denom}/{numer}"]
            wrongs = [w for w in wrongs if w != ans]
        elif qtype == 'compare':
            denom = r.choice([4, 6, 8])
            n1, n2 = r.randint(1, denom - 1), r.randint(1, denom - 1)
            while n1 == n2:
                n2 = r.randint(1, denom - 1)
            bigger = n1 if n1 > n2 else n2
            ans = f"{bigger}/{denom}"
            q_text = f"Which fraction is larger: {n1}/{denom} or {n2}/{denom}?"
            expl = f"{bigger}/{denom} is larger because {bigger} > {min(n1,n2)}."
            other = n2 if n1 > n2 else n1
            wrongs = [f"{other}/{denom}", f"{n1 + n2}/{denom}", f"1/{denom}"]
            wrongs = [w for w in wrongs if w != ans]
        else:
            halves = r.randint(1, 3)
            ans = f"{halves * 2}/8"
            q_text = f"Which fraction equals {halves}/4?"
            expl = f"{halves}/4 = {halves*2}/8 (multiply top and bottom by 2)."
            wrongs = [f"{halves + 1}/8", f"{halves}/8", f"{halves * 2}/4"]
            wrongs = [w for w in wrongs if w != ans]
        choices, idx = _shuffle_choices(ans, wrongs[:3], r)
        qs.append(_q('Fractions', 'medium', q_text, choices, idx, expl, 3))
    return qs


def gen_time_reading(n=30, seed=None):
    """Read clocks / elapsed time (Grade 1–3)."""
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        hour = r.randint(1, 12)
        minute = r.choice([0, 15, 30, 45])
        minute_str = f"{minute:02d}"
        ans = f"{hour}:{minute_str}"
        wrongs = [f"{hour % 12 + 1}:{minute_str}",
                  f"{hour}:{(minute + 15) % 60:02d}",
                  f"{hour}:{(minute + 30) % 60:02d}"]
        wrongs = [w for w in wrongs if w != ans]
        choices, idx = _shuffle_choices(ans, wrongs[:3], r)
        diff = 'easy' if minute == 0 else 'medium'
        qs.append(_q('Time', diff,
                     f"A clock shows the hour hand on {hour} and the minute hand on {minute // 5 if minute else 12}. What time is it?",
                     choices, idx, f"Hour hand → {hour}, minute hand → {minute} minutes past = {ans}.", 2))
    return qs


def gen_money_counting(n=30, seed=None):
    """Count coins and dollars (Grade 1–3)."""
    r = random.Random(seed)
    coin_vals = {'penny': 1, 'nickel': 5, 'dime': 10, 'quarter': 25}
    qs = []
    for _ in range(n):
        coins = {name: r.randint(0, 4) for name in coin_vals}
        total = sum(val * coins[name] for name, val in coin_vals.items())
        if total == 0:
            coins['quarter'] = 1
            total = 25
        parts = [f"{cnt} {name}{'s' if cnt > 1 else ''}"
                 for name, cnt in coins.items() if cnt > 0]
        q_text = f"How many cents do you have? {', '.join(parts)}."
        ans = f"{total}¢"
        wrongs = [f"{total + 5}¢", f"{total - 1}¢" if total > 1 else f"{total + 1}¢",
                  f"{total + 10}¢"]
        wrongs = [w for w in wrongs if w != ans]
        choices, idx = _shuffle_choices(ans, wrongs[:3], r)
        qs.append(_q('Money', 'medium', q_text, choices, idx,
                     f"Add up each coin type: {total} cents total.", 2))
    return qs


def gen_area_perimeter_basic(n=30, seed=None):
    """Area and perimeter of rectangles (Grade 3–5)."""
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        w = r.randint(2, 15)
        h = r.randint(2, 15)
        qtype = r.choice(['area', 'perimeter'])
        if qtype == 'area':
            ans = w * h
            q_text = f"What is the area of a rectangle with width {w} and height {h}?"
            expl = f"Area = width × height = {w} × {h} = {ans}."
            wrongs = [2 * (w + h), w + h, w * h + w]
        else:
            ans = 2 * (w + h)
            q_text = f"What is the perimeter of a rectangle with width {w} and height {h}?"
            expl = f"Perimeter = 2 × (width + height) = 2 × ({w} + {h}) = {ans}."
            wrongs = [w * h, w + h, 2 * w + h]
        wrongs = [str(x) for x in wrongs if x != ans]
        choices, idx = _shuffle_choices(str(ans), wrongs[:3], r)
        qs.append(_q('Geometry', 'medium', q_text, choices, idx, expl, 4))
    return qs


def gen_patterns(n=25, seed=None):
    """Number patterns and sequences (K–3)."""
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        start = r.randint(1, 20)
        step = r.choice([2, 3, 5, 10])
        length = 4
        seq = [start + i * step for i in range(length)]
        next_val = start + length * step
        shown = ', '.join(str(x) for x in seq)
        ans = str(next_val)
        wrongs = [str(next_val + 1), str(next_val - 1), str(next_val + step)]
        wrongs = [w for w in wrongs if w != ans]
        choices, idx = _shuffle_choices(ans, wrongs[:3], r)
        qs.append(_q('Patterns', 'easy',
                     f"What comes next in the pattern? {shown}, ___",
                     choices, idx,
                     f"Each number increases by {step}. After {seq[-1]}, the next is {next_val}.", 2))
    return qs


def gen_word_problems_elem(n=40, seed=None):
    """Simple word problems (Grade 2–5)."""
    r = random.Random(seed)
    templates = [
        lambda: (lambda a, b: (
            f"Maria has {a} apples. She gets {b} more. How many does she have now?",
            a + b, f"{a} + {b} = {a + b}."))(r.randint(5, 30), r.randint(2, 20)),
        lambda: (lambda a, b: (
            f"There are {a} students in a class. {b} go home early. How many remain?",
            a - b, f"{a} − {b} = {a - b}."))(r.randint(15, 35), r.randint(2, 10)),
        lambda: (lambda a, b: (
            f"A baker bakes {a} cookies each tray. There are {b} trays. How many cookies total?",
            a * b, f"{a} × {b} = {a * b}."))(r.randint(3, 12), r.randint(2, 8)),
        lambda: (lambda a, b: (
            f"There are {a * b} candies shared equally among {b} friends. How many does each get?",
            a, f"{a * b} ÷ {b} = {a}."))(r.randint(3, 10), r.randint(2, 6)),
    ]
    qs = []
    for _ in range(n):
        fn = r.choice(templates)
        q_text, ans, expl = fn()
        if ans <= 0:
            continue
        wrongs = [ans + 1, ans - 1 if ans > 1 else ans + 2, ans + r.randint(2, 5)]
        wrongs = [str(w) for w in wrongs if w != ans]
        choices, idx = _shuffle_choices(str(ans), wrongs[:3], r)
        qs.append(_q('Word Problems', 'medium', q_text, choices, idx, expl, 3))
    return qs


# ── Master functions ─────────────────────────────────────────────────────────

_TOPIC_GENERATORS = {
    'Counting':       [(gen_counting, {})],
    'Addition':       [(gen_addition_basic, {})],
    'Subtraction':    [(gen_subtraction_basic, {})],
    'Multiplication': [(gen_multiplication_tables, {})],
    'Division':       [(gen_division_basic, {})],
    'Place Value':    [(gen_place_value, {})],
    'Fractions':      [(gen_fractions_basic, {})],
    'Time':           [(gen_time_reading, {})],
    'Money':          [(gen_money_counting, {})],
    'Geometry':       [(gen_area_perimeter_basic, {})],
    'Patterns':       [(gen_patterns, {})],
    'Word Problems':  [(gen_word_problems_elem, {})],
}

_DIFF_WEIGHTS = {
    'Counting':       {'easy': [gen_counting], 'medium': [gen_counting], 'hard': [gen_counting]},
    'Addition':       {'easy': [gen_addition_basic], 'medium': [gen_addition_basic], 'hard': [gen_addition_basic]},
    'Subtraction':    {'easy': [gen_subtraction_basic], 'medium': [gen_subtraction_basic], 'hard': [gen_subtraction_basic]},
    'Multiplication': {'easy': [gen_multiplication_tables], 'medium': [gen_multiplication_tables], 'hard': [gen_multiplication_tables]},
    'Division':       {'easy': [gen_division_basic], 'medium': [gen_division_basic], 'hard': [gen_division_basic]},
    'Place Value':    {'easy': [gen_place_value], 'medium': [gen_place_value], 'hard': [gen_place_value]},
    'Fractions':      {'easy': [gen_fractions_basic], 'medium': [gen_fractions_basic], 'hard': [gen_fractions_basic]},
    'Time':           {'easy': [gen_time_reading], 'medium': [gen_time_reading], 'hard': [gen_time_reading]},
    'Money':          {'easy': [gen_money_counting], 'medium': [gen_money_counting], 'hard': [gen_money_counting]},
    'Geometry':       {'easy': [gen_area_perimeter_basic], 'medium': [gen_area_perimeter_basic], 'hard': [gen_area_perimeter_basic]},
    'Patterns':       {'easy': [gen_patterns], 'medium': [gen_patterns], 'hard': [gen_patterns]},
    'Word Problems':  {'easy': [gen_word_problems_elem], 'medium': [gen_word_problems_elem], 'hard': [gen_word_problems_elem]},
}


def generate_for_topic(topic, difficulty='medium', count=10, seed=None):
    import random as _r
    r = _r.Random(seed)
    fns = (_DIFF_WEIGHTS.get(topic, {}).get(difficulty)
           or [fn for fn, _ in _TOPIC_GENERATORS.get(topic, [])])
    if not fns:
        return []
    pool = []
    for fn in fns:
        pool.extend(fn(seed=r.randint(0, 999999), n=max(count * 3, 30)))
    r.shuffle(pool)
    return [{'id': -(i+1), 'subject': r[0], 'topic': r[1], 'difficulty': r[2],
             'question': r[3], 'choices': json.loads(r[4]), 'answer': r[5],
             'explanation': r[6]} for i, r in enumerate(pool[:count])]


def generate_all(seed=42):
    r = random.Random(seed)
    all_qs = []
    for fns in _TOPIC_GENERATORS.values():
        for fn, kwargs in fns:
            all_qs.extend(fn(seed=r.randint(0, 999999), n=40, **kwargs))
    return all_qs


if __name__ == '__main__':
    qs = generate_all()
    from collections import Counter
    print(f"Total: {len(qs)}")
    for topic, cnt in sorted(Counter(q[1] for q in qs).items()):
        print(f"  {topic}: {cnt}")
