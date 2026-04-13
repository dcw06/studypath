"""
Procedural math question generator for QuizArena.

Each generator function returns a list of 8-element tuples:
  (subject, topic, difficulty, question, choices_json, answer_idx, explanation, grade)

Questions are generated with random numbers so every DB seed produces fresh variety.
Run this module directly to preview generated questions.
"""

import random
import json
import math
from fractions import Fraction

rng = random.Random()   # seeded per-call for reproducibility within a batch


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

def _q(topic, diff, question, choices, answer_idx, explanation, grade=9):
    return ('Math', topic, diff, question, json.dumps(choices), answer_idx, explanation, grade)


def _shuffle_choices(correct, wrongs, rng):
    """Place `correct` at a random index among the 4 choices; return (choices, idx)."""
    choices = list(rng.sample(wrongs, min(3, len(wrongs))))
    idx = rng.randint(0, 3)
    choices.insert(idx, correct)
    return choices[:4], idx


def _near(val, spread=None, n=3, avoid=None, rng=rng, integer=True):
    """Generate n plausible wrong answers near val."""
    avoid = {val} if avoid is None else set(avoid) | {val}
    spread = max(abs(val) * 0.4, 5) if spread is None else spread
    results, attempts = [], 0
    while len(results) < n and attempts < 200:
        attempts += 1
        delta = rng.uniform(-spread, spread)
        if delta == 0:
            continue
        candidate = val + delta
        if integer:
            candidate = round(candidate)
        else:
            candidate = round(candidate, 4)
        if candidate not in avoid:
            avoid.add(candidate)
            results.append(candidate)
    return results


def _fmt(x):
    """Format a number cleanly — integer if whole, else 2 dp."""
    if isinstance(x, float) and x == int(x):
        return str(int(x))
    if isinstance(x, float):
        return f"{x:.4f}".rstrip('0').rstrip('.')
    return str(x)


def _term(coef, var):
    """Format a coefficient × variable, suppressing explicit 1 and -1.
    Examples: _term(1,'x')→'x', _term(-1,'x')→'-x', _term(2,'x')→'2x'
    """
    if coef == 1:
        return var
    if coef == -1:
        return f'-{var}'
    return f'{coef}{var}'


def _term_pow(coef, var, exp):
    """Format coef*var^exp, suppressing 1-coefficients and ^1 exponent.
    Examples: _term_pow(1,'x',2)→'x²', _term_pow(-1,'x',1)→'-x'
    Uses ^ notation (plain text).
    """
    v = var if exp == 1 else f'{var}^{exp}'
    return _term(coef, v)


def _signed_term(coef, var, leading=False):
    """Return a term with an explicit sign prefix for non-leading terms.
    leading=True: no '+' prefix (used for first term in expression).
    Examples (non-leading): _signed_term(1,'x')→'+ x', _signed_term(-2,'x')→'− 2x'
    """
    t = _term(coef, var)
    if leading:
        return t
    return f'+ {t}' if coef > 0 else f'− {_term(-coef, var)}'


# ──────────────────────────────────────────────────────────────────────────────
# ARITHMETIC
# ──────────────────────────────────────────────────────────────────────────────

def gen_addition(n=80, seed=None):
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        a = r.randint(10, 1000)
        b = r.randint(10, 1000)
        ans = a + b
        wrongs = []
        wrongs.append(a + b + r.choice([-1, 1]) * r.randint(1, 9))   # off by small amount
        wrongs.append(a + b + r.choice([-1, 1]) * r.randint(10, 99)) # off by medium amount
        wrongs.append(a * b)                                           # multiplication distractor
        wrongs = [w for w in wrongs if w != ans and w > 0]
        choices, idx = _shuffle_choices(ans, wrongs[:3], r)
        diff = 'easy' if max(a, b) < 300 else 'medium'
        qs.append(_q('Arithmetic', diff,
                     f"What is {a} + {b}?",
                     [str(c) for c in choices], idx,
                     f"{a} + {b} = {ans}."))
    return qs


def gen_subtraction(n=50, seed=None):
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        a = r.randint(20, 1000)
        b = r.randint(10, a)
        ans = a - b
        wrongs = [ans + r.choice([-1,1])*r.randint(1,9),
                  ans + r.choice([-1,1])*r.randint(10,50),
                  b - a if b > a else a + b]
        wrongs = [w for w in wrongs if w != ans]
        choices, idx = _shuffle_choices(ans, wrongs[:3], r)
        qs.append(_q('Arithmetic', 'easy',
                     f"What is {a} − {b}?",
                     [str(c) for c in choices], idx,
                     f"{a} − {b} = {ans}."))
    return qs


def gen_multiplication(n=60, seed=None):
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        a = r.randint(2, 99)
        b = r.randint(2, 99)
        ans = a * b
        wrongs = [ans + r.choice([-1,1]) * r.randint(1, max(1, a//2)),
                  (a+1)*b, a*(b+1)]
        wrongs = [w for w in wrongs if w != ans and w > 0]
        choices, idx = _shuffle_choices(ans, wrongs[:3], r)
        diff = 'easy' if max(a,b) <= 12 else ('medium' if max(a,b) <= 30 else 'hard')
        qs.append(_q('Arithmetic', diff,
                     f"What is {a} × {b}?",
                     [str(c) for c in choices], idx,
                     f"{a} × {b} = {ans}."))
    return qs


def gen_division(n=50, seed=None):
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        divisor  = r.randint(2, 50)
        quotient = r.randint(2, 50)
        dividend = divisor * quotient
        ans = quotient
        wrongs = [ans + r.choice([-1,1])*r.randint(1,5),
                  dividend - divisor,
                  divisor * (quotient + 1)]
        wrongs = [w for w in wrongs if w != ans and w > 0]
        choices, idx = _shuffle_choices(ans, wrongs[:3], r)
        qs.append(_q('Arithmetic', 'easy',
                     f"What is {dividend} ÷ {divisor}?",
                     [str(c) for c in choices], idx,
                     f"{dividend} ÷ {divisor} = {ans}."))
    return qs


def gen_percentage(n=60, seed=None):
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        pct  = r.choice([5,10,15,20,25,30,40,50,60,75,80])
        base = r.randint(2, 200) * r.choice([1, 2, 4, 5, 10])
        ans  = round(pct / 100 * base, 2)
        if ans == int(ans):
            ans = int(ans)
        wrong1 = round(pct / 100 * base * 2, 2)
        wrong2 = round((pct + 10) / 100 * base, 2)
        wrong3 = base - ans
        wrongs = [w for w in [wrong1, wrong2, wrong3] if w != ans and w > 0]
        choices, idx = _shuffle_choices(ans, wrongs[:3], r)
        diff = 'easy' if pct in [10, 50] else 'medium'
        qs.append(_q('Arithmetic', diff,
                     f"What is {pct}% of {base}?",
                     [str(c) for c in choices], idx,
                     f"{pct}% of {base} = {pct}/100 × {base} = {ans}."))
    return qs


def gen_fractions(n=50, seed=None):
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        op = r.choice(['add', 'sub', 'mul'])
        n1, d1 = r.randint(1, 9), r.randint(2, 12)
        n2, d2 = r.randint(1, 9), r.randint(2, 12)
        f1, f2 = Fraction(n1, d1), Fraction(n2, d2)
        if op == 'add':
            ans_f = f1 + f2
            symbol, verb = '+', 'adding'
        elif op == 'sub':
            if f1 < f2:
                f1, f2 = f2, f1
            ans_f = f1 - f2
            symbol, verb = '−', 'subtracting'
        else:
            ans_f = f1 * f2
            symbol, verb = '×', 'multiplying'
        ans_str = str(ans_f)
        # Build 3 wrong answers
        def frac_near(f):
            delta_n = r.randint(1, 3)
            candidates = [Fraction(f.numerator + delta_n, f.denominator),
                          Fraction(f.numerator - delta_n, f.denominator),
                          Fraction(f.numerator, f.denominator + 1)]
            for c in candidates:
                if c != f and c > 0:
                    return str(c)
            return str(Fraction(f.numerator + 1, f.denominator))
        wrongs = list({frac_near(ans_f), frac_near(ans_f + Fraction(1,d1)), str(Fraction(n1+n2, d1+d2))} - {ans_str})
        choices, idx = _shuffle_choices(ans_str, list(wrongs)[:3], r)
        qs.append(_q('Arithmetic', 'medium',
                     f"Compute: {f1} {symbol} {f2}",
                     choices, idx,
                     f"{f1} {symbol} {f2} = {ans_f} ({verb} fractions with LCD)."))
    return qs


def gen_order_of_operations(n=40, seed=None):
    r = random.Random(seed)
    qs = []
    templates = [
        lambda r: _pemdas_add_mul(r),
        lambda r: _pemdas_parens(r),
        lambda r: _pemdas_exp(r),
    ]
    for _ in range(n):
        fn = r.choice(templates)
        try:
            q = fn(r)
            if q:
                qs.append(q)
        except Exception:
            pass
    return qs


def _pemdas_add_mul(r):
    a = r.randint(1, 20)
    b = r.randint(1, 20)
    c = r.randint(1, 20)
    ans = a + b * c          # correct (multiplication first)
    wrong1 = (a + b) * c     # wrong (left-to-right)
    wrong2 = a * b + c       # wrong
    wrong3 = ans + r.randint(1, 10)
    wrongs = [w for w in [wrong1, wrong2, wrong3] if w != ans]
    choices, idx = _shuffle_choices(ans, wrongs[:3], r)
    return _q('Arithmetic', 'medium',
              f"Evaluate using order of operations: {a} + {b} × {c}",
              [str(c) for c in choices], idx,
              f"Multiplication before addition: {b} × {c} = {b*c}, then {a} + {b*c} = {ans}.")


def _pemdas_parens(r):
    a = r.randint(1, 15)
    b = r.randint(1, 15)
    c = r.randint(2, 10)
    ans = (a + b) * c
    wrong1 = a + b * c
    wrong2 = ans + c
    wrong3 = ans - r.randint(1, 8)
    wrongs = [w for w in [wrong1, wrong2, wrong3] if w != ans]
    choices, idx = _shuffle_choices(ans, wrongs[:3], r)
    return _q('Arithmetic', 'easy',
              f"Evaluate: ({a} + {b}) × {c}",
              [str(c) for c in choices], idx,
              f"Parentheses first: ({a} + {b}) = {a+b}, then × {c} = {ans}.")


def _pemdas_exp(r):
    base = r.randint(2, 8)
    exp  = r.randint(2, 4)
    add  = r.randint(1, 20)
    val  = base ** exp
    ans  = val + add
    wrong1 = (base + add) ** exp
    wrong2 = base * exp + add
    wrong3 = ans + r.randint(1, 10)
    wrongs = [w for w in [wrong1, wrong2, wrong3] if w != ans]
    choices, idx = _shuffle_choices(ans, wrongs[:3], r)
    return _q('Arithmetic', 'medium',
              f"Evaluate: {base}^{exp} + {add}",
              [str(c) for c in choices], idx,
              f"Exponent first: {base}^{exp} = {val}, then {val} + {add} = {ans}.")


def gen_gcd_lcm(n=40, seed=None):
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        # pick two numbers with a known GCD
        g = r.randint(2, 20)
        a_mul = r.randint(2, 15)
        b_mul = r.randint(2, 15)
        while b_mul == a_mul:
            b_mul = r.randint(2, 15)
        a, b = g * a_mul, g * b_mul
        gcd = math.gcd(a, b)
        lcm = a * b // gcd
        if r.random() < 0.5:
            ans = gcd
            q_text = f"Find the GCD (greatest common divisor) of {a} and {b}."
            expl = f"GCD({a},{b}) = {gcd}. Factor both: {a} = {g}×{a_mul}, {b} = {g}×{b_mul}."
        else:
            ans = lcm
            q_text = f"Find the LCM (least common multiple) of {a} and {b}."
            expl = f"LCM({a},{b}) = {a}×{b}÷GCD = {a*b}÷{gcd} = {lcm}."
        spread = max(g, 5)
        wrongs = [ans + spread, ans - spread if ans - spread > 0 else ans + 2*spread,
                  ans + 2*spread]
        wrongs = [w for w in wrongs if w != ans and w > 0]
        choices, idx = _shuffle_choices(ans, wrongs[:3], r)
        qs.append(_q('Arithmetic', 'medium', q_text,
                     [str(c) for c in choices], idx, expl))
    return qs


# ──────────────────────────────────────────────────────────────────────────────
# ALGEBRA
# ──────────────────────────────────────────────────────────────────────────────

def gen_linear_equations(n=80, seed=None):
    """ax + b = c  →  solve for x."""
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        a = r.choice([i for i in range(-10, 11) if i not in (0, 1, -1)])
        b = r.randint(-50, 50)
        x = r.randint(-20, 20)           # choose solution first
        c = a * x + b
        ans = x
        wrongs = [ans + r.randint(1,4), ans - r.randint(1,4),
                  round((c + b) / a if a != 0 else ans + 5)]
        wrongs = [w for w in wrongs if w != ans]
        choices, idx = _shuffle_choices(ans, wrongs[:3], r)
        diff = 'easy' if abs(a) <= 5 and abs(b) <= 20 else 'medium'
        sign_b = f"+ {b}" if b >= 0 else f"− {-b}"
        qs.append(_q('Algebra', diff,
                     f"Solve for x:  {_term(a,'x')} {sign_b} = {c}",
                     [f"x = {c}" for c in choices], idx,
                     f"Subtract {b} from both sides: {_term(a,'x')} = {c - b}. Divide by {a}: x = {ans}."))
    return qs


def gen_quadratic_formula(n=80, seed=None):
    """ax² + bx + c = 0 with integer roots."""
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        # Build from roots to guarantee integer solutions
        r1 = r.randint(-10, 10)
        r2 = r.randint(-10, 10)
        # (x - r1)(x - r2) = x² - (r1+r2)x + r1*r2
        a = 1
        b = -(r1 + r2)
        c = r1 * r2
        # discriminant
        disc = b*b - 4*a*c
        if disc < 0 or r1 == r2:
            continue   # skip degenerate
        ans_str = f"x = {r1} and x = {r2}" if r1 != r2 else f"x = {r1} (repeated)"
        wrong_roots = [(r1+1, r2), (r1, r2+1), (r1-1, r2+1)]
        wrongs = [f"x = {wr[0]} and x = {wr[1]}" for wr in wrong_roots if (wr[0],wr[1]) != (r1,r2)]
        choices, idx = _shuffle_choices(ans_str, wrongs[:3], r)
        sign_b = (_signed_term(b, 'x') if b != 0 else '')
        sign_c = f"+ {c}" if c > 0 else (f"− {-c}" if c < 0 else '')
        diff = 'medium' if max(abs(r1), abs(r2)) <= 5 else 'hard'
        qs.append(_q('Algebra', diff,
                     f"Find the roots of x² {sign_b} {sign_c} = 0".strip(),
                     choices, idx,
                     f"Factor as (x − {r1})(x − {r2}) = 0, so x = {r1} and x = {r2}."))
    return qs


def gen_quadratic_discriminant(n=40, seed=None):
    """Identify root type from discriminant."""
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        root_type = r.choice(['two_real', 'repeated', 'complex'])
        if root_type == 'two_real':
            r1, r2 = r.randint(-8, 8), r.randint(-8, 8)
            while r1 == r2:
                r2 = r.randint(-8, 8)
            b = -(r1 + r2); c = r1 * r2
            disc = b*b - 4*c
            ans = "Two distinct real roots"
            expl = f"Discriminant = b²−4ac = {disc} > 0 → two distinct real roots."
        elif root_type == 'repeated':
            root = r.randint(-5, 5)
            b = -2 * root; c = root * root
            disc = b*b - 4*c   # should be 0
            ans = "One repeated real root"
            expl = f"Discriminant = b²−4ac = {disc} = 0 → one repeated root, x = {root}."
        else:
            # complex: pick a > 0 with disc < 0
            b_val = r.choice([-4,-2,0,2,4])
            c_val = r.randint(2, 15)
            while b_val*b_val - 4*c_val >= 0:
                c_val += 1
            b, c = b_val, c_val
            disc = b*b - 4*c
            ans = "Two complex conjugate roots"
            expl = f"Discriminant = b²−4ac = {disc} < 0 → two complex conjugate roots."

        wrongs = ["Two distinct real roots", "One repeated real root", "Two complex conjugate roots"]
        wrongs = [w for w in wrongs if w != ans]
        choices, idx = _shuffle_choices(ans, wrongs, r)
        sign_b = (_signed_term(b, 'x') if b != 0 else '')
        sign_c = f"+ {c}" if c > 0 else (f"− {-c}" if c < 0 else '')
        qs.append(_q('Algebra', 'medium',
                     f"What is the nature of the roots of x² {sign_b} {sign_c} = 0?".strip(),
                     choices, idx, expl, 10))
    return qs


def gen_evaluate_expression(n=50, seed=None):
    """Evaluate f(x) = ax² + bx + c at a given x value."""
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        a = r.randint(-5, 5)
        b = r.randint(-10, 10)
        c = r.randint(-20, 20)
        xval = r.randint(-5, 5)
        ans = a * xval**2 + b * xval + c
        wrongs = [ans + r.randint(1, 10), ans - r.randint(1, 10),
                  a * xval + b * xval + c]   # forgot to square
        wrongs = [w for w in wrongs if w != ans]
        choices, idx = _shuffle_choices(ans, wrongs[:3], r)
        if a == 0:
            expr = f"{b}x + {c}" if b != 0 else str(c)
        else:
            sign_a = "" if a == 1 else (f"{a}" if a != -1 else "-")
            sign_b = f" + {b}x" if b > 0 else (f" − {-b}x" if b < 0 else "")
            sign_c = f" + {c}" if c > 0 else (f" − {-c}" if c < 0 else "")
            expr = f"{sign_a}x²{sign_b}{sign_c}"
        qs.append(_q('Algebra', 'easy' if abs(xval) <= 2 else 'medium',
                     f"Evaluate f(x) = {expr} at x = {xval}.",
                     [str(v) for v in choices], idx,
                     f"f({xval}) = {a}({xval})² + {b}({xval}) + {c} = {a*xval**2} + {b*xval} + {c} = {ans}."))
    return qs


def gen_systems_of_equations(n=50, seed=None):
    """2×2 linear system, integer solution."""
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        x = r.randint(-8, 8)
        y = r.randint(-8, 8)
        a1 = r.choice([i for i in range(-5,6) if i != 0])
        b1 = r.choice([i for i in range(-5,6) if i != 0])
        a2 = r.choice([i for i in range(-5,6) if i != 0])
        b2 = r.choice([i for i in range(-5,6) if i != 0])
        det = a1*b2 - a2*b1
        if det == 0:
            continue
        c1 = a1*x + b1*y
        c2 = a2*x + b2*y
        ans_str = f"x = {x}, y = {y}"
        wrongs = [f"x = {x+1}, y = {y}", f"x = {x}, y = {y+1}", f"x = {y}, y = {x}"]
        wrongs = [w for w in wrongs if w != ans_str]
        choices, idx = _shuffle_choices(ans_str, wrongs[:3], r)
        def fmt_eq(a, b, c):
            bsign = "+" if b >= 0 else "−"
            bval = abs(b)
            bterm = 'y' if bval == 1 else f'{bval}y'
            return f"{_term(a,'x')} {bsign} {bterm} = {c}"
        qs.append(_q('Algebra', 'medium',
                     f"Solve the system: {fmt_eq(a1,b1,c1)} and {fmt_eq(a2,b2,c2)}",
                     choices, idx,
                     f"Substituting x = {x}, y = {y} satisfies both equations. Determinant = {det}."))
    return qs


def gen_slope_intercept(n=50, seed=None):
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        m = r.choice([i for i in range(-8, 9) if i != 0])
        b_int = r.randint(-10, 10)
        qtype = r.choice(['slope', 'intercept', 'point', 'parallel'])

        line_str = f"y = {_term(m,'x')} + {b_int}" if b_int >= 0 else f"y = {_term(m,'x')} − {-b_int}"
        if qtype == 'slope':
            ans = m
            q_text = f"What is the slope of the line {line_str}?"
            expl = f"In slope-intercept form y = mx + b, the slope is the coefficient of x, which is {m}."
            wrongs = [b_int, -m, m + r.randint(1,3)]
        elif qtype == 'intercept':
            ans = b_int
            q_text = f"What is the y-intercept of the line {line_str}?"
            expl = f"In y = mx + b, the y-intercept is b = {b_int}."
            wrongs = [m, b_int + r.randint(1,3), b_int - r.randint(1,3)]
        elif qtype == 'point':
            x_val = r.randint(-5, 5)
            y_val = m * x_val + b_int
            ans = y_val
            q_text = f"For the line {line_str}, find y when x = {x_val}."
            expl = f"y = {m}({x_val}) + {b_int} = {m*x_val} + {b_int} = {ans}."
            wrongs = [ans + r.randint(1,5), m*x_val, ans - r.randint(1,5)]
        else:  # parallel
            ans = m
            slope2 = m + r.choice([-2,-1,1,2])
            q_text = f"A line parallel to y = {_term(slope2,'x')} + 3 has slope:"
            expl = f"Parallel lines have equal slopes. The slope of y = {_term(slope2,'x')} + 3 is {slope2}."
            ans = slope2
            wrongs = [-slope2, slope2 + 1, slope2 - 1]

        wrongs = [w for w in wrongs if w != ans]
        choices, idx = _shuffle_choices(ans, wrongs[:3], r)
        qs.append(_q('Algebra', 'easy' if qtype in ['slope','intercept'] else 'medium',
                     q_text, [str(c) for c in choices], idx, expl))
    return qs


def gen_exponents_logs(n=50, seed=None):
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        qtype = r.choice(['exp_simplify', 'log_eval', 'exp_equation', 'log_prop'])

        if qtype == 'exp_simplify':
            base = r.randint(2, 10)
            p = r.randint(1, 5)
            q_val = r.randint(1, 5)
            op = r.choice(['multiply', 'divide'])
            if op == 'multiply':
                ans = p + q_val
                q_text = f"Simplify: {base}^{p} × {base}^{q_val}"
                expl = f"When multiplying same base, add exponents: {base}^({p}+{q_val}) = {base}^{ans}."
                ans_str = f"{base}^{ans}"
                wrongs = [f"{base}^{p*q_val}", f"{base}^{p-q_val}", f"{base*2}^{ans}"]
            else:
                ans = p - q_val
                q_text = f"Simplify: {base}^{p} ÷ {base}^{q_val}"
                expl = f"When dividing same base, subtract exponents: {base}^({p}−{q_val}) = {base}^{ans}."
                ans_str = f"{base}^{ans}"
                wrongs = [f"{base}^{p+q_val}", f"{base}^{p*q_val}", f"{base}^{abs(ans)+1}"]
            wrongs = [w for w in wrongs if w != ans_str]
            choices, idx = _shuffle_choices(ans_str, wrongs[:3], r)
            qs.append(_q('Algebra', 'medium', q_text, choices, idx, expl, 10))

        elif qtype == 'log_eval':
            base = r.choice([2, 3, 5, 10])
            exp  = r.randint(1, 5)
            val  = base ** exp
            ans  = exp
            wrongs = [exp + 1, exp - 1, val - base]
            wrongs = [w for w in wrongs if w != ans]
            choices, idx = _shuffle_choices(ans, wrongs[:3], r)
            qs.append(_q('Algebra', 'medium',
                         f"Evaluate: log_{base}({val})",
                         [str(c) for c in choices], idx,
                         f"log_{base}({val}) = {ans} because {base}^{ans} = {val}.", 11))

        elif qtype == 'exp_equation':
            base = r.choice([2, 3, 5])
            exp  = r.randint(1, 5)
            rhs  = base ** exp
            ans  = exp
            wrongs = [exp + 1, exp - 1, exp * 2]
            wrongs = [w for w in wrongs if w != ans]
            choices, idx = _shuffle_choices(ans, wrongs[:3], r)
            qs.append(_q('Algebra', 'medium',
                         f"Solve for x: {base}^x = {rhs}",
                         [f"x = {c}" for c in choices], idx,
                         f"{base}^x = {rhs} = {base}^{ans}, so x = {ans}.", 10))

        else:  # log_prop
            b1, b2 = r.randint(2, 20), r.randint(2, 20)
            ans = round(math.log10(b1 * b2), 4)
            q_text = f"Using log properties, log({b1}) + log({b2}) = log( ? )"
            ans_str = str(b1 * b2)
            wrongs = [str(b1 + b2), str(b1 * b2 + 1), str(abs(b1 - b2) or b1)]
            wrongs = [w for w in wrongs if w != ans_str]
            choices, idx = _shuffle_choices(ans_str, wrongs[:3], r)
            qs.append(_q('Algebra', 'medium', q_text, choices, idx,
                         f"log(a) + log(b) = log(a×b): log({b1}) + log({b2}) = log({b1*b2}).", 11))

    return qs


# ──────────────────────────────────────────────────────────────────────────────
# CALCULUS
# ──────────────────────────────────────────────────────────────────────────────

def gen_derivatives_power_rule(n=80, seed=None):
    """d/dx [ax^n] = a*n*x^(n-1)."""
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        a = r.choice([i for i in range(-8, 9) if i not in (0, 1)])
        n_exp = r.randint(2, 7)
        # derivative: a*n*x^(n-1)
        new_coef = a * n_exp
        new_exp  = n_exp - 1
        if new_exp == 1:
            ans_str = _term(new_coef, 'x')
        elif new_exp == 0:
            ans_str = str(new_coef)
        else:
            ans_str = _term_pow(new_coef, 'x', new_exp)
        # wrongs: common mistakes
        wrong1 = _term_pow(a, 'x', n_exp - 1)       # forgot to multiply by n
        wrong2 = _term_pow(new_coef, 'x', n_exp)     # forgot to reduce power
        wrong3 = _term_pow(new_coef, 'x', n_exp + 1) # wrong direction
        wrongs = [w for w in [wrong1, wrong2, wrong3] if w != ans_str]
        choices, idx = _shuffle_choices(ans_str, wrongs[:3], r)
        qs.append(_q('Calculus', 'easy',
                     f"Find the derivative of f(x) = {_term_pow(a,'x',n_exp)}",
                     choices, idx,
                     f"Power rule: d/dx[ax^n] = a·n·x^(n−1). Here: {a}·{n_exp}·x^{n_exp-1} = {ans_str}.",
                     11))
    return qs


def gen_derivatives_poly(n=60, seed=None):
    """Derivative of polynomial f(x) = ax^3 + bx^2 + cx + d."""
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        a = r.choice([i for i in range(-5,6) if i != 0])
        b = r.choice([i for i in range(-8,9) if i != 0])
        c = r.choice([i for i in range(-10,11) if i != 0])
        d = r.randint(-15, 15)
        # f'(x) = 3ax^2 + 2bx + c
        da, db, dc = 3*a, 2*b, c
        def fmt_poly_der(a2, b1, c0):
            parts = []
            if a2 != 0:
                if a2 == 1: parts.append("x^2")
                elif a2 == -1: parts.append("-x^2")
                else: parts.append(f"{a2}x^2")
            if b1 != 0:
                if parts:
                    parts.append(f"{'+ ' if b1>0 else '- '}{abs(b1) if abs(b1)!=1 else ''}x")
                else:
                    parts.append(f"{b1 if abs(b1)!=1 else ('' if b1>0 else '-')}x")
            if c0 != 0:
                if parts:
                    parts.append(f"{'+ ' if c0>0 else '- '}{abs(c0)}")
                else:
                    parts.append(str(c0))
            return "".join(parts) if parts else "0"

        ans_str = fmt_poly_der(da, db, dc)
        wrong_a = fmt_poly_der(da+1, db, dc)
        wrong_b = fmt_poly_der(da, db+1, dc)
        wrong_c = fmt_poly_der(a, b, c)    # no derivative taken
        wrongs = [w for w in [wrong_a, wrong_b, wrong_c] if w != ans_str]
        choices, idx = _shuffle_choices(ans_str, wrongs[:3], r)
        def fmt_poly(a3, b2, c1, d0):
            parts = []
            if a3 != 0: parts.append(f"{a3}x^3")
            if b2 != 0: parts.append(f"{b2:+}x^2")
            if c1 != 0: parts.append(f"{c1:+}x")
            if d0 != 0: parts.append(f"{d0:+}")
            return "".join(parts)
        qs.append(_q('Calculus', 'medium',
                     f"Differentiate f(x) = {fmt_poly(a,b,c,d)}",
                     choices, idx,
                     f"f'(x) = 3({a})x² + 2({b})x + {c} = {ans_str}.", 12))
    return qs


def gen_derivative_at_point(n=50, seed=None):
    """Evaluate f'(x) at a specific x value."""
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        a = r.choice([i for i in range(-5,6) if i != 0])
        b = r.choice([i for i in range(-8,9) if i != 0])
        c = r.randint(-10, 10)
        x_val = r.randint(-5, 5)
        # f(x) = ax^2 + bx + c, f'(x) = 2ax + b
        deriv_at_x = 2 * a * x_val + b
        ans = deriv_at_x
        wrongs = [ans + r.randint(1,4), ans - r.randint(1,4), a * x_val**2 + b * x_val + c]
        wrongs = [w for w in wrongs if w != ans]
        choices, idx = _shuffle_choices(ans, wrongs[:3], r)
        sign_b = (_signed_term(b, 'x') if b != 0 else '')
        sign_c = f"+ {c}" if c > 0 else (f"− {-c}" if c < 0 else '')
        qs.append(_q('Calculus', 'medium',
                     f"Find f'({x_val}) for f(x) = {_term(a,'x')}² {sign_b} {sign_c}".strip(),
                     [str(v) for v in choices], idx,
                     f"f'(x) = 2({a})x + {b} = {2*a}x + {b}. At x = {x_val}: f'({x_val}) = {2*a}({x_val}) + {b} = {ans}.",
                     12))
    return qs


def gen_definite_integrals(n=60, seed=None):
    """Integral of ax^n from p to q."""
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        a = r.choice([i for i in range(-6,7) if i != 0])
        n_exp = r.randint(0, 4)
        p = r.randint(-4, 3)
        q = r.randint(p + 1, p + 6)
        # integral = a * [x^(n+1)/(n+1)] from p to q
        def antideriv(x): return a * (x ** (n_exp + 1)) / (n_exp + 1)
        ans = round(antideriv(q) - antideriv(p), 4)
        if ans == int(ans):
            ans = int(ans)
            ans_str = str(ans)
        else:
            ans_str = f"{ans:.3f}".rstrip('0').rstrip('.')
        wrongs_vals = [ans + r.randint(1,8), ans - r.randint(1,8),
                       round(antideriv(q), 2)]
        wrongs = [str(int(w)) if w == int(w) else f"{w:.3f}".rstrip('0').rstrip('.')
                  for w in wrongs_vals if w != ans]
        choices, idx = _shuffle_choices(ans_str, wrongs[:3], r)
        if n_exp == 0:
            expr = str(a)
        elif n_exp == 1:
            expr = f"{a}x"
        else:
            expr = f"{a}x^{n_exp}"
        qs.append(_q('Calculus', 'hard',
                     f"Evaluate the definite integral of {expr} from x = {p} to x = {q}.",
                     choices, idx,
                     f"Antiderivative is {a}x^{n_exp+1}/{n_exp+1}. Evaluate from {p} to {q}: {antideriv(q):.4f} − {antideriv(p):.4f} = {ans_str}.",
                     12))
    return qs


def gen_limits(n=40, seed=None):
    """Simple polynomial limits as x → a."""
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        # f(x) = ax^2 + bx + c, limit as x → x0 is just f(x0) for polynomials
        a = r.choice([1, 2, -1, 3, -2])
        b = r.randint(-5, 5)
        c = r.randint(-10, 10)
        x0 = r.randint(-5, 5)
        ans = a * x0**2 + b * x0 + c
        wrongs = [ans + r.randint(1,5), ans - r.randint(1,5),
                  a * x0 + b * x0 + c]
        wrongs = [w for w in wrongs if w != ans]
        choices, idx = _shuffle_choices(ans, wrongs[:3], r)
        sign_b = (_signed_term(b, 'x') if b != 0 else '')
        sign_c = f"+ {c}" if c > 0 else (f"− {-c}" if c < 0 else '')
        qs.append(_q('Calculus', 'easy',
                     f"Find the limit: lim (x→{x0}) of {_term(a,'x')}² {sign_b} {sign_c}".strip(),
                     [str(v) for v in choices], idx,
                     f"For a polynomial, substitute x = {x0}: {a}({x0})² + {b}({x0}) + {c} = {ans}.",
                     11))
    return qs


# ──────────────────────────────────────────────────────────────────────────────
# DIFFERENTIAL EQUATIONS
# ──────────────────────────────────────────────────────────────────────────────

def gen_ode_characteristic(n=90, seed=None):
    """
    Second-order linear ODE: ay'' + by' + cy = 0.
    Generate questions for all three root types.
    """
    r = random.Random(seed)
    qs = []

    for _ in range(n):
        root_type = r.choice(['distinct', 'repeated', 'complex'])

        if root_type == 'distinct':
            # Choose two distinct integer roots r1 ≠ r2
            r1 = r.randint(-6, 6)
            r2 = r.randint(-6, 6)
            while r1 == r2:
                r2 = r.randint(-6, 6)
            # (r - r1)(r - r2) = r² - (r1+r2)r + r1*r2
            a = 1
            b = -(r1 + r2)
            c = r1 * r2
            disc = b*b - 4*a*c  # should be > 0
            ans_form = f"y = C₁e^({r1}x) + C₂e^({r2}x)"
            explanation = (
                f"Characteristic equation: r² {_signed_term(b,'r') if b!=0 else ''} {'+' + str(c) if c > 0 else ('− ' + str(-c) if c < 0 else '')} = 0. "
                f"Discriminant = {disc} > 0 → two distinct real roots r₁ = {r1}, r₂ = {r2}. "
                f"General solution: {ans_form}."
            )
            wrong_forms = [
                f"y = (C₁ + C₂x)e^({r1}x)",
                f"y = e^({(r1+r2)//2}x)(C₁cos({abs(r1-r2)}x) + C₂sin({abs(r1-r2)}x))",
                f"y = C₁e^({r2}x) + C₂e^({-r1}x)"
            ]
            diff = 'medium'

        elif root_type == 'repeated':
            # r1 = r2 = -b/2a  →  pick r_val, set b=-2*r_val, c=r_val²
            r_val = r.randint(-5, 5)
            a = 1
            b = -2 * r_val
            c = r_val * r_val
            disc = b*b - 4*a*c   # = 0
            ans_form = f"y = (C₁ + C₂x)e^({r_val}x)"
            explanation = (
                f"Characteristic equation: r² {_signed_term(b,'r') if b!=0 else ''} {'+' + str(c) if c > 0 else ('− ' + str(-c) if c < 0 else '')} = 0. "
                f"Discriminant = {disc} = 0 → repeated root r = {r_val}. "
                f"General solution: {ans_form}."
            )
            wrong_forms = [
                f"y = C₁e^({r_val}x) + C₂e^({r_val+1}x)",
                f"y = C₁e^({r_val}x) + C₂e^({-r_val}x)",
                f"y = e^({r_val}x)(C₁cos({r_val}x) + C₂sin({r_val}x))"
            ]
            diff = 'medium'

        else:  # complex
            # roots = α ± βi  where α = -b/2a, β = sqrt(4ac-b²)/2a
            alpha = r.randint(-3, 3)
            beta  = r.randint(1, 5)
            # r² - 2α·r + (α² + β²) = 0
            a = 1
            b = -2 * alpha
            c = alpha**2 + beta**2
            disc = b*b - 4*a*c   # = -4β² < 0
            ans_form = f"y = e^({alpha}x)(C₁cos({beta}x) + C₂sin({beta}x))"
            explanation = (
                f"Characteristic equation: r² {_signed_term(b,'r') if b!=0 else ''} {'+' + str(c) if c > 0 else ('− ' + str(-c) if c < 0 else '')} = 0. "
                f"Discriminant = {disc} < 0 → complex roots {alpha} ± {beta}i. "
                f"General solution: {ans_form}."
            )
            wrong_forms = [
                f"y = C₁e^({alpha}x) + C₂e^({-alpha}x)",
                f"y = (C₁ + C₂x)e^({alpha}x)",
                f"y = e^({beta}x)(C₁cos({alpha}x) + C₂sin({alpha}x))"
            ]
            diff = 'hard'

        wrongs = [w for w in wrong_forms if w != ans_form]
        choices, idx = _shuffle_choices(ans_form, wrongs[:3], r)
        ode_b = (_signed_term(b, "y'") if b != 0 else '')
        ode_c = (f'+ {_term(c,"y")}' if c > 0 else (f'− {_term(-c,"y")}' if c < 0 else ''))
        char_b = (_signed_term(b, 'r') if b != 0 else '')
        char_c = (f'+ {c}' if c > 0 else (f'− {-c}' if c < 0 else ''))
        qs.append(_q('Differential Equations', diff,
                     f"Find the general solution of the ODE: y'' {ode_b} {ode_c} = 0  (i.e., characteristic eq: r² {char_b} {char_c} = 0)".strip(),
                     choices, idx, explanation, 13))

    return qs


def gen_ode_classify_roots(n=60, seed=None):
    """Given a,b,c — classify the type of roots of the characteristic equation."""
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        root_type = r.choice(['distinct', 'repeated', 'complex'])
        if root_type == 'distinct':
            r1 = r.randint(-5, 5)
            r2 = r.randint(-5, 5)
            while r1 == r2:
                r2 = r.randint(-5, 5)
            b = -(r1 + r2)
            c = r1 * r2
            disc = b*b - 4*c
            ans = "Two distinct real roots"
            expl = f"Discriminant = b² − 4ac = ({b})² − 4({c}) = {disc} > 0 → distinct real roots."
        elif root_type == 'repeated':
            r_val = r.randint(-5, 5)
            b = -2 * r_val
            c = r_val * r_val
            disc = 0
            ans = "One repeated real root"
            expl = f"Discriminant = ({b})² − 4({c}) = {disc} = 0 → one repeated root."
        else:
            alpha = r.randint(-3, 3)
            beta  = r.randint(1, 5)
            b = -2 * alpha
            c = alpha**2 + beta**2
            disc = b*b - 4*c
            ans = "Two complex conjugate roots"
            expl = f"Discriminant = ({b})² − 4({c}) = {disc} < 0 → complex roots {alpha}±{beta}i."

        a_val = 1
        wrongs = ["Two distinct real roots", "One repeated real root", "Two complex conjugate roots"]
        wrongs = [w for w in wrongs if w != ans]
        choices, idx = _shuffle_choices(ans, wrongs, r)
        char_b = (_signed_term(b, 'r') if b != 0 else '')
        char_c = (f'+ {c}' if c > 0 else (f'− {-c}' if c < 0 else ''))
        qs.append(_q('Differential Equations', 'medium',
                     f"Classify the roots of the characteristic equation: r² {char_b} {char_c} = 0".strip(),
                     choices, idx, expl, 13))
    return qs


def gen_ode_separable(n=40, seed=None):
    """dy/dx = ky  →  general solution y = Ce^(kx)."""
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        k = r.choice([i for i in range(-5, 6) if i != 0])
        ans_str = f"y = Ce^({k}x)" if k != 1 else "y = Ce^x"
        wrongs = [
            f"y = Ce^({-k}x)",
            f"y = C·({k}x)",
            f"y = C + e^({k}x)"
        ]
        wrongs = [w for w in wrongs if w != ans_str]
        choices, idx = _shuffle_choices(ans_str, wrongs[:3], r)
        qs.append(_q('Differential Equations', 'medium',
                     f"Solve the separable ODE: dy/dx = {_term(k,'y')}",
                     choices, idx,
                     f"Separate variables: dy/y = {k}dx. Integrate: ln|y| = {k}x + C₀. Exponentiate: y = Ce^({k}x).",
                     13))
    return qs


# ──────────────────────────────────────────────────────────────────────────────
# LINEAR ALGEBRA
# ──────────────────────────────────────────────────────────────────────────────

def gen_determinant_2x2(n=70, seed=None):
    """det([[a,b],[c,d]]) = ad - bc."""
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        a = r.randint(-8, 8)
        b = r.randint(-8, 8)
        c = r.randint(-8, 8)
        d = r.randint(-8, 8)
        ans = a * d - b * c
        wrongs = [a*d + b*c, a*c - b*d, ans + r.choice([-1,1])*r.randint(1,5)]
        wrongs = [w for w in wrongs if w != ans]
        choices, idx = _shuffle_choices(ans, wrongs[:3], r)
        diff = 'easy' if all(abs(v) <= 4 for v in [a,b,c,d]) else 'medium'
        qs.append(_q('Linear Algebra', diff,
                     f"Find det([[{a},{b}],[{c},{d}]])",
                     [str(v) for v in choices], idx,
                     f"det = ad − bc = ({a})({d}) − ({b})({c}) = {a*d} − {b*c} = {ans}.",
                     11))
    return qs


def gen_determinant_3x3(n=40, seed=None):
    """3×3 determinant via cofactor expansion."""
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        # Keep entries small to avoid huge numbers
        M = [[r.randint(-4, 4) for _ in range(3)] for _ in range(3)]
        a,b,c = M[0]
        d,e,f = M[1]
        g,h,i = M[2]
        det = (a*(e*i - f*h) - b*(d*i - f*g) + c*(d*h - e*g))
        ans = det
        wrongs = [ans + r.choice([-1,1])*r.randint(1,8),
                  ans + r.choice([-1,1])*r.randint(10,30),
                  a*e*i - b*f*g]  # partial diagonal
        wrongs = [w for w in wrongs if w != ans]
        choices, idx = _shuffle_choices(ans, wrongs[:3], r)
        row_strs = [f"[{M[i][0]},{M[i][1]},{M[i][2]}]" for i in range(3)]
        qs.append(_q('Linear Algebra', 'hard',
                     f"Compute the determinant of the 3×3 matrix: {row_strs[0]}, {row_strs[1]}, {row_strs[2]}",
                     [str(v) for v in choices], idx,
                     f"Using cofactor expansion along row 1: {a}({e*i-f*h}) − {b}({d*i-f*g}) + {c}({d*h-e*g}) = {ans}.",
                     12))
    return qs


def gen_matrix_multiply(n=50, seed=None):
    """2×2 matrix multiplication — one specific entry."""
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        A = [[r.randint(-5,5) for _ in range(2)] for _ in range(2)]
        B = [[r.randint(-5,5) for _ in range(2)] for _ in range(2)]
        # Compute C = AB
        C = [[sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
        # Ask for one entry
        row = r.randint(0, 1)
        col = r.randint(0, 1)
        ans = C[row][col]
        wrongs = [ans + r.choice([-1,1])*r.randint(1,6),
                  C[1-row][col], C[row][1-col]]
        wrongs = [w for w in wrongs if w != ans]
        choices, idx = _shuffle_choices(ans, wrongs[:3], r)
        def fmt2x2(M):
            return f"[[{M[0][0]},{M[0][1]}],[{M[1][0]},{M[1][1]}]]"
        row_label = ['first', 'second'][row]
        col_label = ['first', 'second'][col]
        qs.append(_q('Linear Algebra', 'medium',
                     f"For A = {fmt2x2(A)} and B = {fmt2x2(B)}, what is the {row_label}-row, {col_label}-column entry of A×B?",
                     [str(v) for v in choices], idx,
                     f"Row {row+1} of A · Column {col+1} of B = {A[row][0]}×{B[0][col]} + {A[row][1]}×{B[1][col]} = {A[row][0]*B[0][col]} + {A[row][1]*B[1][col]} = {ans}.",
                     12))
    return qs


def gen_dot_product(n=50, seed=None):
    """Dot product of two 3D integer vectors."""
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        u = [r.randint(-8, 8) for _ in range(3)]
        v = [r.randint(-8, 8) for _ in range(3)]
        ans = sum(u[i]*v[i] for i in range(3))
        wrongs = [ans + r.choice([-1,1])*r.randint(1,8),
                  sum(abs(u[i]*v[i]) for i in range(3)),
                  ans + r.choice([-1,1])*r.randint(10,25)]
        wrongs = [w for w in wrongs if w != ans]
        choices, idx = _shuffle_choices(ans, wrongs[:3], r)
        qs.append(_q('Linear Algebra', 'easy',
                     f"Find the dot product of u = ({u[0]},{u[1]},{u[2]}) and v = ({v[0]},{v[1]},{v[2]})",
                     [str(v2) for v2 in choices], idx,
                     f"u·v = {u[0]}×{v[0]} + {u[1]}×{v[1]} + {u[2]}×{v[2]} = {u[0]*v[0]} + {u[1]*v[1]} + {u[2]*v[2]} = {ans}.",
                     11))
    return qs


def gen_eigenvalues_2x2(n=50, seed=None):
    """Eigenvalues of a 2×2 matrix via characteristic polynomial."""
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        # Build from known eigenvalues
        l1 = r.randint(-5, 5)
        l2 = r.randint(-5, 5)
        trace = l1 + l2
        det   = l1 * l2
        # Use diagonal + small off-diagonal to keep it interesting
        # A = [[l1, 0],[0, l2]] — diagonal, simplest case
        a, d = l1 + r.randint(0,1), l2 + r.randint(0,1)
        # Adjust so eigenvalues are preserved for diagonal:
        a, b_, c_, d = l1, 0, 0, l2   # keep diagonal form for correctness
        ans_str = f"λ = {l1} and λ = {l2}" if l1 != l2 else f"λ = {l1} (repeated)"
        # Wrong: use trace/det errors
        wrong1 = f"λ = {l1+1} and λ = {l2}"
        wrong2 = f"λ = {l1} and λ = {l2+1}"
        wrong3 = f"λ = {l1+l2} and λ = {l1*l2}"
        wrongs = [w for w in [wrong1, wrong2, wrong3] if w != ans_str]
        choices, idx = _shuffle_choices(ans_str, wrongs[:3], r)
        qs.append(_q('Linear Algebra', 'hard',
                     f"Find the eigenvalues of the matrix [[{a},{b_}],[{c_},{d}]]",
                     choices, idx,
                     f"Characteristic polynomial: (λ − {a})(λ − {d}) − ({b_})({c_}) = 0. Roots: λ = {l1}, λ = {l2}.",
                     13))
    return qs


# ──────────────────────────────────────────────────────────────────────────────
# PROBABILITY & STATISTICS
# ──────────────────────────────────────────────────────────────────────────────

def gen_basic_probability(n=60, seed=None):
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        qtype = r.choice(['simple', 'complement', 'conditional'])
        if qtype == 'simple':
            total = r.randint(5, 50)
            fav   = r.randint(1, total - 1)
            g = math.gcd(fav, total)
            ans_str = f"{fav//g}/{total//g}" if total//g != 1 else str(fav//g)
            wrongs = [f"{(fav+1)//math.gcd(fav+1,total)}/{total//math.gcd(fav+1,total)}",
                      f"{total-fav}/{total}",
                      f"{fav}/{total+fav}"]
            wrongs = [w for w in wrongs if w != ans_str]
            choices, idx = _shuffle_choices(ans_str, wrongs[:3], r)
            qs.append(_q('Probability', 'easy',
                         f"A bag contains {total} items, {fav} of which are red. If you pick one at random, what is P(red)?",
                         choices, idx,
                         f"P(red) = favorable/total = {fav}/{total} = {ans_str}."))

        elif qtype == 'complement':
            p_num = r.randint(1, 9)
            p_den = 10
            comp_num = p_den - p_num
            ans_str = f"{comp_num}/{p_den}"
            wrongs = [f"{p_num}/{p_den}", f"{comp_num}/{p_num}", f"{p_num+comp_num}/{p_den}"]
            wrongs = [w for w in wrongs if w != ans_str]
            choices, idx = _shuffle_choices(ans_str, wrongs[:3], r)
            qs.append(_q('Probability', 'easy',
                         f"If P(A) = {p_num}/{p_den}, what is P(A')?",
                         choices, idx,
                         f"P(A') = 1 − P(A) = 1 − {p_num}/{p_den} = {comp_num}/{p_den}."))

        else:  # conditional
            p_a = r.randint(2, 8)
            p_b_given_a = r.randint(1, 4)
            p_ab = p_a * p_b_given_a
            denom = 100
            # P(B|A) = P(AB)/P(A)
            p_a_pct = p_a * 10
            p_ab_pct = p_ab
            ans = p_b_given_a * 10
            ans_str = f"{ans}%"
            wrongs = [f"{ans + 10}%", f"{p_ab_pct}%", f"{p_a_pct}%"]
            wrongs = [w for w in wrongs if w != ans_str]
            choices, idx = _shuffle_choices(ans_str, wrongs[:3], r)
            qs.append(_q('Probability', 'medium',
                         f"P(A) = {p_a_pct}%, P(A∩B) = {p_ab_pct}%. Find P(B|A).",
                         choices, idx,
                         f"P(B|A) = P(A∩B)/P(A) = {p_ab_pct}%/{p_a_pct}% = {ans}%."))
    return qs


def gen_combinations_permutations(n=50, seed=None):
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        n_val = r.randint(4, 12)
        k_val = r.randint(2, n_val)
        op = r.choice(['C', 'P'])
        if op == 'C':
            ans = math.comb(n_val, k_val)
            ans_str = str(ans)
            q_text = f"How many ways can you choose {k_val} items from {n_val} (order does NOT matter)? C({n_val},{k_val}) = ?"
            expl = f"C({n_val},{k_val}) = {n_val}! / ({k_val}! × {n_val-k_val}!) = {ans}."
        else:
            ans = math.perm(n_val, k_val)
            ans_str = str(ans)
            q_text = f"How many ordered arrangements of {k_val} items from {n_val}? P({n_val},{k_val}) = ?"
            expl = f"P({n_val},{k_val}) = {n_val}! / {n_val-k_val}! = {ans}."
        wrongs_vals = [ans + r.randint(1, max(1, ans//5)),
                       math.comb(n_val, k_val) if op == 'P' else math.perm(n_val, k_val),
                       ans - r.randint(1, max(1, ans//5))]
        wrongs = [str(w) for w in wrongs_vals if w != ans and w > 0]
        choices, idx = _shuffle_choices(ans_str, wrongs[:3], r)
        qs.append(_q('Probability', 'medium', q_text, choices, idx, expl, 11))
    return qs


def gen_expected_value(n=40, seed=None):
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        n_outcomes = r.randint(3, 5)
        values = [r.randint(-5, 20) for _ in range(n_outcomes)]
        # Generate probabilities that sum to 1 (use integers over denom)
        denom = r.choice([8, 10, 12, 20])
        parts = [r.randint(1, max(1, denom - n_outcomes + 1)) for _ in range(n_outcomes - 1)]
        parts.append(denom - sum(parts))
        if parts[-1] <= 0:
            continue
        probs = [p / denom for p in parts]
        ev = round(sum(v * p for v, p in zip(values, probs)), 3)
        if ev == int(ev):
            ev = int(ev)
            ans_str = str(ev)
        else:
            ans_str = f"{ev:.3f}".rstrip('0').rstrip('.')
        wrongs_vals = [ev + r.randint(1,3), ev - r.randint(1,3), sum(values) / n_outcomes]
        wrongs = [str(round(w,3)).rstrip('0').rstrip('.') if isinstance(w, float) else str(int(w))
                  for w in wrongs_vals if round(w,3) != ev]
        choices, idx = _shuffle_choices(ans_str, wrongs[:3], r)
        pairs = ", ".join(f"X={v} (p={parts[i]}/{denom})" for i, v in enumerate(values))
        qs.append(_q('Probability', 'hard',
                     f"Find E[X] for the distribution: {pairs}",
                     choices, idx,
                     f"E[X] = Σ x·P(x) = {' + '.join(f'{v}×{parts[i]}/{denom}' for i,v in enumerate(values))} = {ans_str}.",
                     12))
    return qs


def gen_statistics_descriptive(n=60, seed=None):
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        n_items = r.randint(5, 10)
        data = sorted([r.randint(-20, 100) for _ in range(n_items)])
        stat = r.choice(['mean', 'median', 'range', 'variance'])

        if stat == 'mean':
            ans = round(sum(data) / n_items, 3)
            if ans == int(ans): ans = int(ans)
            ans_str = str(ans)
            expl = f"Mean = sum/n = {sum(data)}/{n_items} = {ans_str}."
            wrongs_vals = [ans + r.randint(1,5), ans - r.randint(1,5), sum(data)]
        elif stat == 'median':
            if n_items % 2 == 1:
                ans = data[n_items // 2]
            else:
                ans = (data[n_items//2 - 1] + data[n_items//2]) / 2
            if isinstance(ans, float) and ans == int(ans): ans = int(ans)
            ans_str = str(ans)
            expl = f"Sorted data: {data}. Median is the middle value(s) = {ans_str}."
            wrongs_vals = [data[0], data[-1], round(sum(data)/n_items, 1)]
        elif stat == 'range':
            ans = max(data) - min(data)
            ans_str = str(ans)
            expl = f"Range = max − min = {max(data)} − {min(data)} = {ans}."
            wrongs_vals = [max(data), ans + r.randint(1,5), ans - r.randint(1,3)]
        else:  # variance
            mean_v = sum(data) / n_items
            var = round(sum((x - mean_v)**2 for x in data) / n_items, 2)
            ans = var
            ans_str = str(round(var, 2))
            expl = f"Variance = Σ(xᵢ − x̄)²/n. Mean = {mean_v:.2f}. Variance ≈ {var}."
            wrongs_vals = [round(math.sqrt(var), 2), var + r.randint(1,10), var * 2]

        wrongs = [str(round(w,2)) if isinstance(w, float) else str(int(w) if isinstance(w,int) else w)
                  for w in wrongs_vals if str(round(w,3) if isinstance(w,float) else w) != ans_str]
        choices, idx = _shuffle_choices(ans_str, wrongs[:3], r)
        qs.append(_q('Statistics', 'easy' if stat in ['mean','range'] else 'medium',
                     f"For the data set {data}, find the {stat}.",
                     choices, idx, expl))
    return qs


def gen_zscore(n=40, seed=None):
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        qtype = r.choice(['compute_z', 'find_x'])
        mu    = r.randint(50, 200)
        sigma = r.choice([5, 8, 10, 12, 15, 20, 25])
        if qtype == 'compute_z':
            x = mu + r.choice([-3,-2,-1,0,1,2,3]) * sigma
            z = (x - mu) / sigma
            ans = int(z) if z == int(z) else round(z, 2)
            ans_str = str(ans)
            expl = f"z = (x − μ)/σ = ({x} − {mu})/{sigma} = {ans_str}."
            wrongs_vals = [ans + 1, ans - 1, (mu - x) / sigma]
            wrongs = [str(w) for w in wrongs_vals if str(w) != ans_str]
            choices, idx = _shuffle_choices(ans_str, wrongs[:3], r)
            qs.append(_q('Statistics', 'medium',
                         f"A distribution has μ = {mu}, σ = {sigma}. What is the z-score for x = {x}?",
                         choices, idx, expl))
        else:
            z_val = r.choice([-2,-1,0,1,2])
            x_val = mu + z_val * sigma
            ans_str = str(x_val)
            wrongs = [str(mu + (z_val+1)*sigma), str(mu - (z_val-1)*sigma), str(mu + z_val*sigma + 5)]
            wrongs = [w for w in wrongs if w != ans_str]
            choices, idx = _shuffle_choices(ans_str, wrongs[:3], r)
            qs.append(_q('Statistics', 'medium',
                         f"A distribution has μ = {mu}, σ = {sigma}. For z = {z_val}, what is x?",
                         choices, idx,
                         f"x = μ + zσ = {mu} + ({z_val})({sigma}) = {x_val}."))
    return qs


def gen_hypothesis_testing_concepts(n=30, seed=None):
    r = random.Random(seed)
    templates = [
        ("A researcher sets α = 0.05 and gets p = {p}. What is the conclusion?",
         lambda p: ("Reject H₀" if p < 0.05 else "Fail to reject H₀"),
         lambda p: f"p = {p} {'<' if p < 0.05 else '≥'} α = 0.05 → {'reject' if p < 0.05 else 'fail to reject'} H₀.",
         ["Reject H₀", "Fail to reject H₀", "Accept H₁", "No conclusion possible"]),
        ("If a test has α = 0.05, what is the probability of a Type I error?",
         lambda _: "0.05",
         lambda _: "α is the significance level = probability of a Type I error (rejecting a true H₀).",
         ["0.05", "0.95", "0.50", "Cannot be determined"]),
        ("Increasing sample size generally _____ the standard error.",
         lambda _: "decreases",
         lambda _: "SE = σ/√n. As n increases, SE decreases.",
         ["decreases", "increases", "does not affect", "doubles"]),
        ("A 95% confidence interval means:",
         lambda _: "95% of such intervals contain the true parameter",
         lambda _: "A 95% CI means that if we repeat the procedure many times, 95% of the intervals will contain the true parameter.",
         ["95% of such intervals contain the true parameter",
          "There is a 95% chance the true parameter is in this specific interval",
          "95% of the data falls within the interval",
          "The sample statistic equals the parameter 95% of the time"]),
    ]
    qs = []
    for _ in range(n):
        template = r.choice(templates)
        q_text_template, ans_fn, expl_fn, option_pool = template
        p_val = r.choice([0.001, 0.01, 0.03, 0.07, 0.10, 0.20])
        q_text = q_text_template.format(p=p_val)
        ans_str = ans_fn(p_val)
        expl = expl_fn(p_val)
        wrongs = [o for o in option_pool if o != ans_str][:3]
        choices, idx = _shuffle_choices(ans_str, wrongs, r)
        qs.append(_q('Statistics', 'hard', q_text, choices, idx, expl, 13))
    return qs


# ──────────────────────────────────────────────────────────────────────────────
# Master generate function
# ──────────────────────────────────────────────────────────────────────────────

def generate_all(seed=42):
    """
    Generate the full procedural question bank.
    Returns a list of 8-tuples ready to INSERT into the questions table.
    """
    r = random.Random(seed)
    all_qs = []

    generators = [
        # Arithmetic
        (gen_addition,              {'n': 80}),
        (gen_subtraction,           {'n': 50}),
        (gen_multiplication,        {'n': 60}),
        (gen_division,              {'n': 50}),
        (gen_percentage,            {'n': 60}),
        (gen_fractions,             {'n': 50}),
        (gen_order_of_operations,   {'n': 40}),
        (gen_gcd_lcm,               {'n': 40}),
        # Algebra
        (gen_linear_equations,      {'n': 80}),
        (gen_quadratic_formula,     {'n': 70}),
        (gen_quadratic_discriminant,{'n': 40}),
        (gen_evaluate_expression,   {'n': 50}),
        (gen_systems_of_equations,  {'n': 50}),
        (gen_slope_intercept,       {'n': 50}),
        (gen_exponents_logs,        {'n': 50}),
        # Calculus
        (gen_derivatives_power_rule,{'n': 80}),
        (gen_derivatives_poly,      {'n': 60}),
        (gen_derivative_at_point,   {'n': 50}),
        (gen_definite_integrals,    {'n': 60}),
        (gen_limits,                {'n': 40}),
        # Differential Equations
        (gen_ode_characteristic,    {'n': 90}),
        (gen_ode_classify_roots,    {'n': 60}),
        (gen_ode_separable,         {'n': 40}),
        # Linear Algebra
        (gen_determinant_2x2,       {'n': 70}),
        (gen_determinant_3x3,       {'n': 40}),
        (gen_matrix_multiply,       {'n': 50}),
        (gen_dot_product,           {'n': 50}),
        (gen_eigenvalues_2x2,       {'n': 50}),
        # Probability
        (gen_basic_probability,     {'n': 60}),
        (gen_combinations_permutations,{'n': 50}),
        (gen_expected_value,        {'n': 40}),
        # Statistics
        (gen_statistics_descriptive,{'n': 60}),
        (gen_zscore,                {'n': 40}),
        (gen_hypothesis_testing_concepts,{'n': 30}),
    ]

    for fn, kwargs in generators:
        s = r.randint(0, 999999)
        batch = fn(seed=s, **kwargs)
        all_qs.extend(batch)

    return all_qs


# ──────────────────────────────────────────────────────────────────────────────
# Runtime generation (called per-session, not at seed time)
# ──────────────────────────────────────────────────────────────────────────────

# Maps topic name → list of (generator_fn, kwargs) pairs
_TOPIC_GENERATORS = {
    'Arithmetic': [
        (gen_addition,             {'n': 999}),
        (gen_subtraction,          {'n': 999}),
        (gen_multiplication,       {'n': 999}),
        (gen_division,             {'n': 999}),
        (gen_percentage,           {'n': 999}),
        (gen_fractions,            {'n': 999}),
        (gen_order_of_operations,  {'n': 999}),
        (gen_gcd_lcm,              {'n': 999}),
    ],
    'Algebra': [
        (gen_linear_equations,      {'n': 999}),
        (gen_quadratic_formula,     {'n': 999}),
        (gen_quadratic_discriminant,{'n': 999}),
        (gen_evaluate_expression,   {'n': 999}),
        (gen_systems_of_equations,  {'n': 999}),
        (gen_slope_intercept,       {'n': 999}),
        (gen_exponents_logs,        {'n': 999}),
    ],
    'Calculus': [
        (gen_derivatives_power_rule,{'n': 999}),
        (gen_derivatives_poly,      {'n': 999}),
        (gen_derivative_at_point,   {'n': 999}),
        (gen_definite_integrals,    {'n': 999}),
        (gen_limits,                {'n': 999}),
    ],
    'Differential Equations': [
        (gen_ode_characteristic,    {'n': 999}),
        (gen_ode_classify_roots,    {'n': 999}),
        (gen_ode_separable,         {'n': 999}),
    ],
    'Linear Algebra': [
        (gen_determinant_2x2,       {'n': 999}),
        (gen_determinant_3x3,       {'n': 999}),
        (gen_matrix_multiply,       {'n': 999}),
        (gen_dot_product,           {'n': 999}),
        (gen_eigenvalues_2x2,       {'n': 999}),
    ],
    'Probability': [
        (gen_basic_probability,        {'n': 999}),
        (gen_combinations_permutations,{'n': 999}),
        (gen_expected_value,           {'n': 999}),
    ],
    'Statistics': [
        (gen_statistics_descriptive,         {'n': 999}),
        (gen_zscore,                         {'n': 999}),
        (gen_hypothesis_testing_concepts,    {'n': 999}),
    ],
}

# Difficulty filter: easy uses simpler generators, hard uses harder ones
_DIFF_WEIGHTS = {
    'Arithmetic': {
        'easy':   [gen_addition, gen_subtraction, gen_multiplication],
        'medium': [gen_addition, gen_subtraction, gen_multiplication, gen_division,
                   gen_percentage, gen_fractions],
        'hard':   [gen_percentage, gen_fractions, gen_order_of_operations, gen_gcd_lcm],
    },
    'Algebra': {
        'easy':   [gen_linear_equations, gen_evaluate_expression, gen_slope_intercept],
        'medium': [gen_linear_equations, gen_quadratic_formula, gen_evaluate_expression,
                   gen_systems_of_equations, gen_slope_intercept],
        'hard':   [gen_quadratic_formula, gen_quadratic_discriminant, gen_systems_of_equations,
                   gen_exponents_logs],
    },
    'Calculus': {
        'easy':   [gen_derivatives_power_rule, gen_limits],
        'medium': [gen_derivatives_power_rule, gen_derivatives_poly, gen_derivative_at_point,
                   gen_limits],
        'hard':   [gen_derivatives_poly, gen_derivative_at_point, gen_definite_integrals],
    },
    'Differential Equations': {
        'easy':   [gen_ode_classify_roots],
        'medium': [gen_ode_characteristic, gen_ode_classify_roots],
        'hard':   [gen_ode_characteristic, gen_ode_separable],
    },
    'Linear Algebra': {
        'easy':   [gen_determinant_2x2, gen_dot_product],
        'medium': [gen_determinant_2x2, gen_matrix_multiply, gen_dot_product],
        'hard':   [gen_determinant_3x3, gen_matrix_multiply, gen_eigenvalues_2x2],
    },
    'Probability': {
        'easy':   [gen_basic_probability],
        'medium': [gen_basic_probability, gen_combinations_permutations],
        'hard':   [gen_combinations_permutations, gen_expected_value],
    },
    'Statistics': {
        'easy':   [gen_statistics_descriptive],
        'medium': [gen_statistics_descriptive, gen_zscore],
        'hard':   [gen_zscore, gen_hypothesis_testing_concepts],
    },
}


def generate_for_topic(topic, difficulty='medium', count=10, seed=None):
    """
    Generate `count` fresh questions for a specific math topic and difficulty.
    Returns a list of dicts with keys: subject, topic, difficulty, question,
    choices (list), answer (int index), explanation, id (negative fake ID).

    Called at game-start time so every session gets unique random questions.
    """
    import random as _random
    r = _random.Random(seed)

    # Pick which generators to use based on difficulty
    diff_map = _DIFF_WEIGHTS.get(topic, {})
    fns = diff_map.get(difficulty) or diff_map.get('medium') or [
        fn for fn, _ in _TOPIC_GENERATORS.get(topic, [])
    ]

    if not fns:
        return []

    # Generate a large pool then sample
    pool = []
    for fn in fns:
        s = r.randint(0, 999999)
        batch = fn(seed=s, n=max(count * 3, 30))
        pool.extend(batch)

    r.shuffle(pool)
    selected = pool[:count]

    results = []
    for i, row in enumerate(selected):
        # row is an 8-tuple: (subject, topic, diff, question, choices_json, answer, explanation, grade)
        results.append({
            'id':          -(i + 1),   # negative = procedural (not in DB)
            'subject':     row[0],
            'topic':       row[1],
            'difficulty':  row[2],
            'question':    row[3],
            'choices':     json.loads(row[4]),
            'answer':      row[5],
            'explanation': row[6],
        })
    return results


if __name__ == '__main__':
    qs = generate_all()
    from collections import Counter
    topics = Counter(q[1] for q in qs)
    print(f"Total generated: {len(qs)}")
    for topic, cnt in sorted(topics.items()):
        print(f"  {topic}: {cnt}")
