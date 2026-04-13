"""
Middle School Math Generator (Grades 6–8)
Covers: Integers, Ratios & Proportions, Expressions & Equations,
        Geometry, Statistics, Functions, Linear Equations,
        Systems of Equations, Pythagorean Theorem, Probability
"""
import random
import json

def _q(topic, diff, question, choices, answer_idx, explanation, grade=7):
    return ('Math', topic, diff, question, json.dumps(choices), answer_idx, explanation, grade)

def _shuffle_choices(correct, wrongs, rng):
    choices = list(rng.sample(wrongs, min(3, len(wrongs))))
    idx = rng.randint(0, min(3, len(choices)))
    choices.insert(idx, correct)
    return choices[:4], idx

def _term(coef, var):
    if coef == 1: return var
    if coef == -1: return f'-{var}'
    return f'{coef}{var}'


def gen_integers(n=60, seed=None):
    """Integer operations (Grade 6)."""
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        op = r.choice(['+', '-', '*', '/'])
        a = r.randint(-15, 15)
        b = r.randint(-15, 15)
        if b == 0: b = r.choice([-1, 1, 2, -2])
        if op == '+':
            ans = a + b
            q_text = f"What is {a} + ({b})?"
            expl = f"{a} + ({b}) = {ans}."
        elif op == '-':
            ans = a - b
            q_text = f"What is {a} − ({b})?"
            expl = f"{a} − ({b}) = {a} + ({-b}) = {ans}."
        elif op == '*':
            ans = a * b
            q_text = f"What is {a} × {b}?"
            expl = f"{'Positive' if ans > 0 else 'Negative'} × {'positive' if b > 0 else 'negative'} = {ans}."
        else:
            b_safe = b if b != 0 else 1
            ans = a // b_safe if a % b_safe == 0 else None
            if ans is None:
                a = b_safe * r.randint(-8, 8)
                ans = a // b_safe
            q_text = f"What is {a} ÷ {b_safe}?"
            expl = f"{a} ÷ {b_safe} = {ans}."
            b = b_safe
        diff = 'easy' if op in ['+', '-'] else 'medium'
        wrongs = [str(ans + 1), str(ans - 1), str(-ans)]
        wrongs = [w for w in wrongs if w != str(ans)]
        choices, idx = _shuffle_choices(str(ans), wrongs[:3], r)
        qs.append(_q('Integers', diff, q_text, choices, idx, expl, 6))
    return qs


def gen_absolute_value(n=30, seed=None):
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        n_val = r.randint(-20, 20)
        ans = abs(n_val)
        q_text = f"What is |{n_val}|?"
        expl = f"Absolute value is the distance from 0. |{n_val}| = {ans}."
        wrongs = [str(n_val), str(-ans - 1), str(ans + 1)]
        wrongs = [w for w in wrongs if w != str(ans)]
        choices, idx = _shuffle_choices(str(ans), wrongs[:3], r)
        qs.append(_q('Integers', 'easy', q_text, choices, idx, expl, 6))
    return qs


def gen_ratios_proportions(n=50, seed=None):
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        qtype = r.choice(['simplify', 'unit_rate', 'proportion'])
        if qtype == 'simplify':
            import math
            a = r.randint(2, 10)
            b = r.randint(2, 10)
            g = math.gcd(a * r.randint(1, 5), b * r.randint(1, 5))
            big_a = a * g
            big_b = b * g
            ans = f"{big_a // g}:{big_b // g}"
            q_text = f"Simplify the ratio {big_a}:{big_b}."
            expl = f"GCD of {big_a} and {big_b} is {g}. {big_a}÷{g}:{big_b}÷{g} = {ans}."
            wrongs = [f"{big_a}:{big_b}", f"{big_a // g + 1}:{big_b // g}", f"{big_b // g}:{big_a // g}"]
        elif qtype == 'unit_rate':
            price = r.randint(2, 10) * r.randint(2, 8)
            qty = r.randint(2, 8)
            unit = price // qty if price % qty == 0 else None
            if unit is None:
                price = qty * r.randint(2, 10)
                unit = price // qty
            ans = f"${unit} each"
            q_text = f"${price} for {qty} items. What is the unit price?"
            expl = f"${price} ÷ {qty} = ${unit} per item."
            wrongs = [f"${unit + 1} each", f"${unit - 1} each" if unit > 1 else f"${unit + 2} each", f"${price} each"]
        else:
            a = r.randint(2, 10)
            b = r.randint(2, 10)
            c = a * r.randint(2, 6)
            d = b * (c // a)
            ans = str(d)
            q_text = f"Solve the proportion: {a}/{b} = {c}/x"
            expl = f"Cross multiply: {a}·x = {b}·{c}, so x = {b * c}//{a} = {d}."
            wrongs = [str(d + 1), str(c), str(b)]
        wrongs = [w for w in wrongs if w != ans]
        choices, idx = _shuffle_choices(ans, wrongs[:3], r)
        qs.append(_q('Ratios & Proportions', 'medium', q_text, choices, idx, expl, 6))
    return qs


def gen_percentages_ms(n=40, seed=None):
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        pct = r.choice([10, 20, 25, 50, 75])
        total = r.choice([20, 40, 60, 80, 100, 200])
        ans = pct * total // 100
        q_text = f"What is {pct}% of {total}?"
        expl = f"{pct}% of {total} = ({pct}/100) × {total} = {ans}."
        wrongs = [str(ans + 5), str(ans - 5) if ans > 5 else str(ans + 10), str(pct)]
        wrongs = [w for w in wrongs if w != str(ans)]
        choices, idx = _shuffle_choices(str(ans), wrongs[:3], r)
        qs.append(_q('Ratios & Proportions', 'medium', q_text, choices, idx, expl, 7))
    return qs


def gen_expressions_equations_ms(n=60, seed=None):
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        qtype = r.choice(['evaluate', 'one_step', 'two_step', 'inequality'])
        if qtype == 'evaluate':
            a = r.randint(1, 8)
            b = r.randint(-10, 10)
            x = r.randint(-5, 5)
            ans = a * x + b
            q_text = f"Evaluate {_term(a,'x')} + ({b}) when x = {x}."
            expl = f"{a}({x}) + ({b}) = {a * x} + ({b}) = {ans}."
            wrongs = [str(ans + a), str(ans - a), str(a * x)]
        elif qtype == 'one_step':
            a = r.randint(2, 10)
            x = r.randint(-8, 8)
            c = a + x
            ans = x
            q_text = f"Solve: {_term(a,'x')} = {a * x}"
            expl = f"Divide both sides by {a}: x = {a * x}/{a} = {ans}."
            wrongs = [str(ans + 1), str(ans * a), str(-ans)]
        elif qtype == 'two_step':
            a = r.randint(2, 6)
            b = r.randint(-10, 10)
            x = r.randint(-5, 5)
            c = a * x + b
            ans = x
            sign_b = f"+ {b}" if b >= 0 else f"− {-b}"
            q_text = f"Solve: {_term(a,'x')} {sign_b} = {c}"
            expl = f"Subtract {b}: {a}x = {c - b}. Divide by {a}: x = {ans}."
            wrongs = [str(ans + 1), str(ans - 1), str(c // a if a != 0 else ans + 2)]
        else:  # inequality
            a = r.randint(1, 6)
            b = r.randint(-10, 10)
            x = r.randint(1, 8)
            c = a * x + b
            ans = f"x > {x}"
            q_text = f"Solve: {_term(a,'x')} + ({b}) > {c}"
            expl = f"Subtract {b}: {a}x > {c-b}. Divide by {a}: x > {x}."
            wrongs = [f"x < {x}", f"x = {x}", f"x > {x + 1}"]
        wrongs = [w for w in wrongs if w != str(ans)]
        choices, idx = _shuffle_choices(str(ans), wrongs[:3], r)
        qs.append(_q('Expressions & Equations', 'medium', q_text, choices, idx, expl, 7))
    return qs


def gen_geometry_ms(n=50, seed=None):
    import math as _math
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        qtype = r.choice(['angle', 'circle_area', 'circle_circ', 'pythagorean', 'volume_cylinder'])
        if qtype == 'angle':
            a = r.randint(10, 80)
            angle_type = r.choice(['complementary', 'supplementary'])
            if angle_type == 'complementary':
                ans = 90 - a
                q_text = f"Two angles are complementary. One is {a}°. What is the other?"
                expl = f"Complementary angles add to 90°. 90° − {a}° = {ans}°."
            else:
                ans = 180 - a
                q_text = f"Two angles are supplementary. One is {a}°. What is the other?"
                expl = f"Supplementary angles add to 180°. 180° − {a}° = {ans}°."
            wrongs = [str(ans + 10), str(ans - 10), str(360 - a)]
        elif qtype == 'circle_area':
            radius = r.randint(2, 10)
            ans_val = round(_math.pi * radius ** 2, 2)
            ans = f"{ans_val}"
            q_text = f"What is the area of a circle with radius {radius}? (Use π ≈ 3.14)"
            expl = f"Area = π r² = 3.14 × {radius}² = 3.14 × {radius**2} ≈ {ans}."
            approx = round(3.14 * radius ** 2, 2)
            ans = str(approx)
            wrongs = [str(round(3.14 * radius, 2)), str(round(3.14 * (radius + 1)**2, 2)), str(round(3.14 * radius ** 2 * 2, 2))]
        elif qtype == 'circle_circ':
            radius = r.randint(2, 10)
            approx = round(2 * 3.14 * radius, 2)
            ans = str(approx)
            q_text = f"What is the circumference of a circle with radius {radius}? (Use π ≈ 3.14)"
            expl = f"C = 2πr = 2 × 3.14 × {radius} = {ans}."
            wrongs = [str(round(3.14 * radius ** 2, 2)), str(round(3.14 * radius, 2)), str(round(2 * 3.14 * (radius + 1), 2))]
        elif qtype == 'pythagorean':
            triples = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (6, 8, 10)]
            a_leg, b_leg, hyp = r.choice(triples)
            qtype2 = r.choice(['find_hyp', 'find_leg'])
            if qtype2 == 'find_hyp':
                ans = str(hyp)
                q_text = f"A right triangle has legs {a_leg} and {b_leg}. What is the hypotenuse?"
                expl = f"a² + b² = c². {a_leg}² + {b_leg}² = {a_leg**2 + b_leg**2} = {hyp}²."
                wrongs = [str(hyp + 1), str(a_leg + b_leg), str(hyp - 1)]
            else:
                ans = str(a_leg)
                q_text = f"A right triangle has one leg = {b_leg} and hypotenuse = {hyp}. What is the other leg?"
                expl = f"a² = c² − b² = {hyp**2} − {b_leg**2} = {a_leg**2}. a = {a_leg}."
                wrongs = [str(a_leg + 1), str(hyp - b_leg), str(a_leg - 1)]
        else:  # volume_cylinder
            r_val = r.randint(2, 8)
            h_val = r.randint(2, 12)
            approx = round(3.14 * r_val ** 2 * h_val, 1)
            ans = str(approx)
            q_text = f"Find the volume of a cylinder with radius {r_val} and height {h_val}. (Use π ≈ 3.14)"
            expl = f"V = πr²h = 3.14 × {r_val}² × {h_val} = {ans}."
            wrongs = [str(round(3.14 * r_val * h_val, 1)), str(round(approx * 2, 1)), str(round(approx - 10, 1))]
        wrongs = [w for w in wrongs if w != str(ans)]
        choices, idx = _shuffle_choices(str(ans), wrongs[:3], r)
        qs.append(_q('Geometry', 'medium', q_text, choices, idx, expl, 7))
    return qs


def gen_statistics_ms(n=40, seed=None):
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        n_items = r.randint(5, 8)
        data = sorted([r.randint(1, 20) for _ in range(n_items)])
        mean_val = round(sum(data) / len(data), 1)
        mid = n_items // 2
        median_val = data[mid] if n_items % 2 == 1 else (data[mid-1] + data[mid]) / 2
        range_val = data[-1] - data[0]
        qtype = r.choice(['mean', 'median', 'range'])
        data_str = ', '.join(str(x) for x in data)
        if qtype == 'mean':
            ans = str(mean_val)
            q_text = f"Find the mean: {data_str}"
            expl = f"Sum = {sum(data)}, count = {n_items}. Mean = {sum(data)}/{n_items} = {mean_val}."
            wrongs = [str(median_val), str(range_val), str(mean_val + 1)]
        elif qtype == 'median':
            ans = str(median_val)
            q_text = f"Find the median: {data_str}"
            expl = f"Sorted: {data_str}. Middle value = {median_val}."
            wrongs = [str(mean_val), str(data[0]), str(data[-1])]
        else:
            ans = str(range_val)
            q_text = f"Find the range: {data_str}"
            expl = f"Range = max − min = {data[-1]} − {data[0]} = {range_val}."
            wrongs = [str(range_val + 1), str(mean_val), str(data[-1])]
        wrongs = [w for w in wrongs if w != ans]
        choices, idx = _shuffle_choices(ans, wrongs[:3], r)
        qs.append(_q('Statistics', 'medium', q_text, choices, idx, expl, 7))
    return qs


def gen_linear_equations_ms(n=50, seed=None):
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        m = r.choice([i for i in range(-6, 7) if i != 0])
        b = r.randint(-8, 8)
        qtype = r.choice(['slope', 'y_intercept', 'evaluate'])
        line_str = (f"y = {_term(m,'x')} + {b}" if b >= 0 else f"y = {_term(m,'x')} − {-b}")
        if qtype == 'slope':
            ans = str(m)
            q_text = f"What is the slope of the line {line_str}?"
            expl = f"In y = mx + b, m is the slope. Here m = {m}."
            wrongs = [str(b), str(-m), str(m + 1)]
        elif qtype == 'y_intercept':
            ans = str(b)
            q_text = f"What is the y-intercept of {line_str}?"
            expl = f"The y-intercept is b = {b}."
            wrongs = [str(m), str(b + 1), str(-b)]
        else:
            x_val = r.randint(-4, 4)
            y_val = m * x_val + b
            ans = str(y_val)
            q_text = f"For {line_str}, find y when x = {x_val}."
            expl = f"y = {m}({x_val}) + {b} = {m * x_val} + {b} = {y_val}."
            wrongs = [str(y_val + 1), str(m * x_val), str(y_val - 1)]
        wrongs = [w for w in wrongs if w != ans]
        choices, idx = _shuffle_choices(ans, wrongs[:3], r)
        qs.append(_q('Linear Equations', 'medium', q_text, choices, idx, expl, 8))
    return qs


def gen_probability_ms(n=35, seed=None):
    r = random.Random(seed)
    qs_pool = [
        lambda: (lambda n, d: (
            f"A bag has {d} marbles: {n} red, {d - n} blue. What is the probability of picking red?",
            f"{n}/{d}", [f"{d-n}/{d}", f"{n}/{d+1}", f"1/{d}"],
            f"P(red) = {n}/{d}.", 'medium', 7))(r.randint(1, 8), r.randint(2, 10)),
        lambda: (lambda faces: (
            f"A fair die has {faces} faces. What is the probability of rolling a 1?",
            f"1/{faces}", [f"1/{faces+1}", f"2/{faces}", f"1/{faces-1}"],
            f"There's 1 favorable outcome out of {faces} equally likely outcomes.", 'easy', 7))(r.choice([4, 6, 8, 10, 12])),
    ]
    qs = []
    for _ in range(n):
        fn = r.choice(qs_pool)
        q_text, ans, wrongs, expl, diff, grade = fn()
        wrongs = [w for w in wrongs if w != ans]
        choices, idx = _shuffle_choices(ans, wrongs[:3], r)
        qs.append(_q('Probability', diff, q_text, choices, idx, expl, grade))
    return qs


_TOPIC_GENERATORS = {
    'Integers':               [(gen_integers, {}), (gen_absolute_value, {})],
    'Ratios & Proportions':   [(gen_ratios_proportions, {}), (gen_percentages_ms, {})],
    'Expressions & Equations':[(gen_expressions_equations_ms, {})],
    'Geometry':               [(gen_geometry_ms, {})],
    'Statistics':             [(gen_statistics_ms, {})],
    'Linear Equations':       [(gen_linear_equations_ms, {})],
    'Probability':            [(gen_probability_ms, {})],
}

_DIFF_WEIGHTS = {
    'Integers': {'easy': [gen_integers, gen_absolute_value], 'medium': [gen_integers], 'hard': [gen_integers]},
    'Ratios & Proportions': {'easy': [gen_percentages_ms], 'medium': [gen_ratios_proportions, gen_percentages_ms], 'hard': [gen_ratios_proportions]},
    'Expressions & Equations': {'easy': [gen_expressions_equations_ms], 'medium': [gen_expressions_equations_ms], 'hard': [gen_expressions_equations_ms]},
    'Geometry': {'easy': [gen_geometry_ms], 'medium': [gen_geometry_ms], 'hard': [gen_geometry_ms]},
    'Statistics': {'easy': [gen_statistics_ms], 'medium': [gen_statistics_ms], 'hard': [gen_statistics_ms]},
    'Linear Equations': {'easy': [gen_linear_equations_ms], 'medium': [gen_linear_equations_ms], 'hard': [gen_linear_equations_ms]},
    'Probability': {'easy': [gen_probability_ms], 'medium': [gen_probability_ms], 'hard': [gen_probability_ms]},
}


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
            all_qs.extend(fn(seed=r.randint(0, 999999), n=50))
    return all_qs
