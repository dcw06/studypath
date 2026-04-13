"""
High School Math Generator (Grades 9–12)
Covers: Algebra I & II, Geometry, Precalculus, Trigonometry,
        Statistics, Calculus (introductory)
"""
import random
import math
import json

def _q(topic, diff, question, choices, answer_idx, explanation, grade=10):
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

def _signed_term(coef, var):
    if coef == 0: return ''
    t = _term(abs(coef), var)
    return f'+ {t}' if coef > 0 else f'− {t}'


def gen_algebra1(n=40, seed=None):
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        qtype = r.choice(['linear', 'slope', 'system', 'inequality', 'factor_simple'])
        if qtype == 'linear':
            a = r.choice([2, 3, 4, 5, 6])
            b = r.randint(-10, 10)
            x = r.randint(-5, 5)
            c = a * x + b
            sign = '+' if b >= 0 else '−'
            babs = abs(b)
            q_text = f"Solve for x: {_term(a,'x')} {sign} {babs} = {c}"
            ans = str(x)
            wrongs = [str(x+1), str(x-1), str(x*2)]
            choices, idx = _shuffle_choices(ans, wrongs, r)
            qs.append(_q('Algebra I', 'easy', q_text, choices, idx,
                         f"{_term(a,'x')} = {c - b}, so x = {x}.", 9))
        elif qtype == 'slope':
            m = r.choice([-3,-2,-1,1,2,3])
            b = r.randint(-5, 5)
            q_text = f"What is the slope of the line: y = {_term(m,'x')} {'+' if b >= 0 else '−'} {abs(b)}?"
            ans = str(m)
            wrongs = [str(b), str(-m), str(m+1)]
            choices, idx = _shuffle_choices(ans, wrongs, r)
            qs.append(_q('Algebra I', 'easy', q_text, choices, idx,
                         f"In y = mx + b, the slope m = {m}.", 9))
        elif qtype == 'inequality':
            a = r.choice([2, 3, 4])
            b = r.randint(-6, 6)
            x = r.randint(-5, 5)
            c = a * x + b
            op = r.choice(['<', '>'])
            q_text = f"Solve: {_term(a,'x')} {'+' if b >= 0 else '−'} {abs(b)} {op} {c}"
            if op == '<':
                ans = f"x < {x}"
                wrongs = [f"x > {x}", f"x ≤ {x}", f"x = {x}"]
            else:
                ans = f"x > {x}"
                wrongs = [f"x < {x}", f"x ≥ {x}", f"x = {x}"]
            choices, idx = _shuffle_choices(ans, wrongs, r)
            qs.append(_q('Algebra I', 'medium', q_text, choices, idx,
                         f"Isolate x: {_term(a,'x')} {op} {c - b}, so {ans}.", 9))
        elif qtype == 'factor_simple':
            p = r.choice([2, 3, 4, 5, 6])
            q_val = r.choice([2, 3, 4, 5])
            c = p * q_val
            s = p + q_val
            q_text = f"Factor: x² + {s}x + {c}"
            ans = f"(x + {p})(x + {q_val})"
            wrongs = [f"(x + {p})(x − {q_val})", f"(x − {p})(x − {q_val})", f"(x + {c})(x + 1)"]
            choices, idx = _shuffle_choices(ans, wrongs, r)
            qs.append(_q('Algebra I', 'medium', q_text, choices, idx,
                         f"Find two numbers that multiply to {c} and add to {s}: {p} and {q_val}.", 9))
        else:
            a = r.choice([1, 2, 3])
            b = r.randint(-5, 5)
            c2 = r.choice([1, 2, 3])
            d = r.randint(-5, 5)
            x = r.randint(-5, 5)
            # a*x + b = c2*x + d
            d = a * x + b - c2 * x
            q_text = f"Solve: {_term(a,'x')} + {b} = {_term(c2,'x')} + {d}"
            ans = str(x)
            wrongs = [str(x+2), str(x-2), str(-x)]
            choices, idx = _shuffle_choices(ans, wrongs, r)
            qs.append(_q('Algebra I', 'medium', q_text, choices, idx,
                         f"Move x terms to one side: x = {x}.", 9))
    return qs


def gen_geometry_hs(n=40, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What is the sum of the interior angles of a triangle?",
         "180°", ["90°", "360°", "270°"],
         "All triangles have interior angles summing to 180°.", 'easy', 9),
        ("What is the sum of interior angles of a quadrilateral?",
         "360°", ["180°", "270°", "450°"],
         "A quadrilateral can be divided into 2 triangles: 2 × 180° = 360°.", 'easy', 9),
        ("In a right triangle, if the two legs are 3 and 4, what is the hypotenuse?",
         "5", ["7", "√7", "25"],
         "Pythagorean theorem: 3² + 4² = 9 + 16 = 25, so hypotenuse = 5.", 'easy', 9),
        ("What is the area formula for a circle?",
         "πr²", ["2πr", "πd", "2πr²"],
         "Area of circle = π × radius². Circumference = 2πr.", 'easy', 9),
        ("Two parallel lines are cut by a transversal. Alternate interior angles are:",
         "Equal", ["Supplementary", "Complementary", "Perpendicular"],
         "Alternate interior angles are equal when lines are parallel.", 'medium', 10),
        ("What is the definition of a congruent figure?",
         "Same shape and same size",
         ["Same shape, different size", "Same size, different shape", "Mirror image only"],
         "Congruent figures are identical in shape and size.", 'easy', 9),
        ("What is the formula for the volume of a rectangular prism?",
         "V = l × w × h",
         ["V = l + w + h", "V = 2(l + w)h", "V = (l × w)²"],
         "Volume = length × width × height.", 'easy', 9),
        ("In similar triangles, corresponding sides are:",
         "Proportional", ["Equal", "Parallel", "Perpendicular"],
         "Similar triangles have the same shape but different size — sides are proportional.", 'medium', 10),
        ("What is the midpoint formula for points (x₁,y₁) and (x₂,y₂)?",
         "((x₁+x₂)/2, (y₁+y₂)/2)",
         ["((x₁−x₂)/2, (y₁−y₂)/2)", "(x₁×x₂, y₁×y₂)", "((x₁+x₂), (y₁+y₂))"],
         "Midpoint averages the x and y coordinates separately.", 'medium', 10),
        ("What is a tangent line to a circle?",
         "A line that touches the circle at exactly one point",
         ["A line that passes through the center", "A line that cuts the circle in two places",
          "A line perpendicular to the radius"],
         "A tangent line touches (but doesn't cross) a circle at exactly one point.", 'medium', 10),
        ("The exterior angle of a triangle equals:",
         "The sum of the two non-adjacent interior angles",
         ["The adjacent interior angle", "180° minus the adjacent angle",
          "Half the sum of all interior angles"],
         "Exterior angle theorem: exterior angle = sum of the two remote interior angles.", 'hard', 11),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Geometry', diff, q_text, choices, idx,
                     f"Correct: {ans}.", grade))
    return qs


def gen_algebra2(n=40, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What is the discriminant of a quadratic ax² + bx + c?",
         "b² − 4ac",
         ["b² + 4ac", "−b ± √(b²−4ac)", "4ac − b²"],
         "The discriminant b² − 4ac determines the nature of roots.", 'medium', 10),
        ("If the discriminant is negative, the quadratic has:",
         "No real roots (two complex roots)",
         ["Two equal real roots", "Two different real roots", "One real root"],
         "Negative discriminant → square root of a negative → complex (imaginary) roots.", 'medium', 10),
        ("What is log₂(8)?", "3",
         ["2", "4", "8"],
         "log₂(8) asks: 2^? = 8. Answer: 2³ = 8, so log₂(8) = 3.", 'medium', 10),
        ("What is the inverse function of f(x) = 2x + 3?",
         "f⁻¹(x) = (x − 3)/2",
         ["f⁻¹(x) = 2x − 3", "f⁻¹(x) = (x + 3)/2", "f⁻¹(x) = x/2 + 3"],
         "Swap x and y, then solve for y: x = 2y+3 → y = (x−3)/2.", 'medium', 10),
        ("What is the sum of an arithmetic series with first term a, last term l, and n terms?",
         "n(a + l)/2",
         ["n × a", "na + d", "(a + l) × n"],
         "Arithmetic series sum = n × (first + last)/2.", 'hard', 11),
        ("What is i² equal to (where i = √−1)?",
         "−1", ["1", "i", "√−1"],
         "By definition, i = √(−1), so i² = −1.", 'medium', 10),
        ("What is the vertex form of a quadratic?",
         "y = a(x − h)² + k",
         ["y = ax² + bx + c", "y = a(x + h)² + k", "y = (x − h)(x − k)"],
         "Vertex form y = a(x−h)² + k has vertex at (h, k).", 'medium', 10),
        ("What does the absolute value |x| represent geometrically?",
         "Distance from x to 0 on the number line",
         ["The square of x", "The opposite of x", "The sign of x"],
         "|x| is the distance from x to the origin, always non-negative.", 'easy', 9),
        ("For f(x) = x² − 4, what are the zeros?",
         "x = 2 and x = −2",
         ["x = 4 and x = 0", "x = 2 only", "x = ±4"],
         "Set x² − 4 = 0 → x² = 4 → x = ±2.", 'medium', 10),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Algebra II', diff, q_text, choices, idx,
                     f"Correct: {ans}.", grade))
    return qs


def gen_trigonometry(n=35, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What is sin(30°)?", "1/2",
         ["√3/2", "√2/2", "1"],
         "sin(30°) = 1/2. Remember: 30-60-90 triangle ratios.", 'easy', 10),
        ("What is cos(60°)?", "1/2",
         ["√3/2", "√2/2", "0"],
         "cos(60°) = 1/2.", 'easy', 10),
        ("What is tan(45°)?", "1",
         ["0", "√2", "√3"],
         "tan(45°) = sin(45°)/cos(45°) = (√2/2)/(√2/2) = 1.", 'easy', 10),
        ("In a right triangle, SOH-CAH-TOA means:",
         "sin = Opposite/Hypotenuse, cos = Adjacent/Hypotenuse, tan = Opposite/Adjacent",
         ["sin = Adjacent/Hypotenuse, cos = Opposite/Hypotenuse, tan = Adjacent/Opposite",
          "sin = Hypotenuse/Opposite, cos = Hypotenuse/Adjacent, tan = Adjacent/Opposite",
          "All three equal Opposite/Adjacent"],
         "SOH-CAH-TOA is the mnemonic for the three basic trig ratios.", 'easy', 10),
        ("What is the period of y = sin(x)?",
         "2π", ["π", "π/2", "4π"],
         "The sine function completes one cycle every 2π radians (≈ 6.28).", 'medium', 11),
        ("What is the Pythagorean identity?",
         "sin²θ + cos²θ = 1",
         ["sin θ + cos θ = 1", "tan²θ + 1 = sec²θ is the only identity",
          "sin θ × cos θ = 1"],
         "The fundamental Pythagorean identity: sin²θ + cos²θ = 1.", 'medium', 10),
        ("Convert 180° to radians:",
         "π radians", ["2π radians", "π/2 radians", "90 radians"],
         "180° = π radians. Multiply degrees by π/180 to convert.", 'medium', 10),
        ("What is the Law of Sines?",
         "a/sin A = b/sin B = c/sin C",
         ["a² = b² + c² − 2bc cos A", "sin A = a/b", "a + b + c = 180°"],
         "The Law of Sines relates sides to the sines of opposite angles.", 'hard', 11),
        ("What is sin(90°)?", "1",
         ["0", "√2/2", "∞"],
         "At 90°, the unit circle gives sin = 1, cos = 0.", 'easy', 10),
        ("What is the inverse of sin(x)?", "arcsin(x) or sin⁻¹(x)",
         ["1/sin(x)", "cos(x)", "−sin(x)"],
         "arcsin is the inverse function that returns the angle given a sine value.", 'medium', 11),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Trigonometry', diff, q_text, choices, idx,
                     f"Correct: {ans}.", grade))
    return qs


def gen_statistics_hs(n=35, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What is the mean of {2, 4, 6, 8, 10}?", "6",
         ["5", "7", "8"],
         "Mean = sum/count = 30/5 = 6.", 'easy', 9),
        ("What is the median of {3, 7, 9, 12, 15}?", "9",
         ["7", "10", "12"],
         "Median is the middle value when sorted. Middle of 5 values = 3rd value = 9.", 'easy', 9),
        ("What does the standard deviation measure?",
         "The spread or variability of data around the mean",
         ["The middle value", "The most frequent value", "The range of the data"],
         "A high standard deviation means data is spread out; low means data is clustered.", 'medium', 10),
        ("What is a normal distribution?",
         "A bell-shaped, symmetric distribution centered at the mean",
         ["A distribution with no outliers", "A distribution skewed to the right",
          "A flat, uniform distribution"],
         "Normal distributions are symmetric: mean = median = mode, with data following the 68-95-99.7 rule.", 'medium', 10),
        ("In a normal distribution, about what % of data falls within 1 standard deviation of the mean?",
         "68%", ["95%", "99.7%", "50%"],
         "The 68-95-99.7 rule: 68% within 1σ, 95% within 2σ, 99.7% within 3σ.", 'hard', 11),
        ("What is the difference between a population and a sample?",
         "A population includes everyone; a sample is a subset",
         ["They are the same thing", "A sample is larger than a population",
          "A population is a type of graph"],
         "In statistics, we often study a sample to draw conclusions about a larger population.", 'medium', 10),
        ("What is a p-value?",
         "The probability of getting results as extreme as observed, assuming the null hypothesis is true",
         ["The probability that the hypothesis is true", "The sample size",
          "The correlation coefficient"],
         "A small p-value (< 0.05) suggests evidence against the null hypothesis.", 'hard', 12),
        ("What does a correlation coefficient of r = −0.9 indicate?",
         "A strong negative linear relationship",
         ["A weak negative relationship", "No relationship", "A strong positive relationship"],
         "r close to −1 = strong negative correlation; r close to +1 = strong positive.", 'hard', 11),
        ("What is the range of {4, 8, 15, 16, 23, 42}?", "38",
         ["19", "25", "46"],
         "Range = max − min = 42 − 4 = 38.", 'easy', 9),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Statistics', diff, q_text, choices, idx,
                     f"Correct: {ans}.", grade))
    return qs


def gen_precalculus(n=35, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What is the domain of f(x) = √x?",
         "x ≥ 0", ["All real numbers", "x > 0 only", "x ≤ 0"],
         "Square root requires non-negative input. Domain: x ≥ 0, or [0, ∞).", 'medium', 11),
        ("What is the domain of f(x) = 1/x?",
         "All real numbers except x = 0",
         ["All real numbers", "x > 0", "x ≥ 0"],
         "Division by zero is undefined, so x ≠ 0.", 'easy', 10),
        ("What is a composite function f(g(x))?",
         "Applying g first, then f to the result",
         ["Adding f and g", "Multiplying f and g",
          "The average of f and g"],
         "f(g(x)) means evaluate g(x) first, then use that result as input to f.", 'medium', 11),
        ("What is the exponential function?",
         "f(x) = aˣ, where a > 0 and a ≠ 1",
         ["f(x) = x^a", "f(x) = log(x)", "f(x) = a/x"],
         "Exponential functions have a constant base raised to a variable exponent.", 'medium', 11),
        ("What is the relationship between ln(x) and eˣ?",
         "They are inverse functions",
         ["They are the same function", "ln(x) = 2eˣ",
          "They have no relationship"],
         "ln(x) = log_e(x) is the inverse of eˣ: ln(eˣ) = x and e^(ln x) = x.", 'hard', 12),
        ("For a function to have an inverse, it must be:",
         "One-to-one (each output corresponds to exactly one input)",
         ["Continuous", "Defined for all real numbers", "Increasing only"],
         "A function must pass the horizontal line test to have an inverse.", 'hard', 11),
        ("What is an asymptote?",
         "A line that a graph approaches but never reaches",
         ["A line that intersects the graph", "The maximum of a function",
          "The y-intercept"],
         "Asymptotes show limiting behavior — the graph gets infinitely close but doesn't touch.", 'medium', 11),
        ("What is the end behavior of f(x) = x³ as x → ∞?",
         "f(x) → ∞",
         ["f(x) → 0", "f(x) → −∞", "f(x) → 1"],
         "Odd-degree polynomial with positive leading coefficient: right end goes up.", 'hard', 12),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Precalculus', diff, q_text, choices, idx,
                     f"Correct: {ans}.", grade))
    return qs


_TOPIC_GENERATORS = {
    'Algebra I':    [(gen_algebra1, {})],
    'Geometry':     [(gen_geometry_hs, {})],
    'Algebra II':   [(gen_algebra2, {})],
    'Trigonometry': [(gen_trigonometry, {})],
    'Statistics':   [(gen_statistics_hs, {})],
    'Precalculus':  [(gen_precalculus, {})],
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
