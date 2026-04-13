"""
College Math Generator
Covers: Single-Variable Calculus, Multivariable Calculus,
        Linear Algebra, Differential Equations, Discrete Math, Real Analysis
"""
import random
import json
import math

def _q(topic, diff, question, choices, answer_idx, explanation, grade=13):
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
    t = _term(abs(coef), var)
    return f'+ {t}' if coef > 0 else f'− {t}'


def gen_single_var_calculus(n=40, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What is the limit of sin(x)/x as x → 0?", "1",
         ["0", "∞", "undefined"],
         "L'Hôpital's or squeeze theorem: lim(x→0) sin(x)/x = 1.", 'medium', 13),
        ("What is the derivative of sin(x)?", "cos(x)",
         ["-cos(x)", "-sin(x)", "tan(x)"],
         "d/dx[sin(x)] = cos(x).", 'easy', 13),
        ("What is the derivative of eˣ?", "eˣ",
         ["xeˣ⁻¹", "eˣ ln(e)", "x·eˣ"],
         "eˣ is its own derivative: d/dx[eˣ] = eˣ.", 'easy', 13),
        ("What is the chain rule?",
         "d/dx[f(g(x))] = f'(g(x)) · g'(x)",
         ["d/dx[f(g(x))] = f'(x) + g'(x)",
          "d/dx[f(g(x))] = f'(x) · g'(x)",
          "d/dx[f(g(x))] = f(g'(x))"],
         "Chain rule: differentiate the outer function, then multiply by the derivative of the inner.", 'medium', 13),
        ("What is ∫eˣ dx?", "eˣ + C",
         ["eˣ·x + C", "eˣ/x + C", "ln(eˣ) + C"],
         "The antiderivative of eˣ is eˣ + C (eˣ is its own integral).", 'easy', 13),
        ("What is the Fundamental Theorem of Calculus (Part 1)?",
         "d/dx[∫ₐˣ f(t)dt] = f(x)",
         ["∫ₐᵇ f(x)dx = f(b) − f(a)",
          "Every continuous function has an antiderivative",
          "Integration and differentiation are unrelated"],
         "FTC Part 1: the derivative of an integral with variable upper limit is the integrand.", 'hard', 13),
        ("What is the integral ∫(1/x) dx?", "ln|x| + C",
         ["x⁻¹ + C", "1/(x²) + C", "log(x) + C"],
         "∫(1/x)dx = ln|x| + C. The absolute value handles negative x.", 'medium', 13),
        ("What is L'Hôpital's Rule used for?",
         "Evaluating limits of indeterminate forms (0/0 or ∞/∞)",
         ["Finding derivatives of products",
          "Evaluating definite integrals",
          "Solving differential equations"],
         "L'Hôpital: if lim f/g is 0/0 or ∞/∞, take lim f'/g' instead.", 'hard', 13),
        ("What is a critical point of f(x)?",
         "A point where f'(x) = 0 or f'(x) is undefined",
         ["A point where f(x) = 0", "The maximum of f(x)",
          "A point where f''(x) = 0"],
         "Critical points are candidates for local maxima, minima, or saddle points.", 'medium', 13),
        ("What does the second derivative test tell us?",
         "If f''(c) > 0 at a critical point, it's a local min; if < 0, it's a local max",
         ["If f''(c) > 0, it's a maximum", "The second derivative finds inflection points only",
          "f''(c) = 0 means there is a critical point"],
         "Positive second derivative = concave up = local minimum. Negative = concave down = local max.", 'hard', 14),
        ("What is integration by parts?",
         "∫u dv = uv − ∫v du",
         ["∫u dv = u'v + uv'", "∫u dv = ∫u dx + ∫v dx",
          "∫u dv = uv + C"],
         "Integration by parts (from product rule): choose u and dv, then apply ∫u dv = uv − ∫v du.", 'hard', 14),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Single-Variable Calculus', diff, q_text, choices, idx,
                     f"Correct: {ans}.", grade))
    return qs


def gen_multivariable_calculus(n=35, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What is a partial derivative?",
         "The derivative of a function with respect to one variable, holding others constant",
         ["The total derivative of a function", "The integral of a multivariable function",
          "The gradient of a function"],
         "∂f/∂x: differentiate f(x,y) with respect to x, treating y as constant.", 'medium', 14),
        ("What does the gradient ∇f represent?",
         "A vector pointing in the direction of steepest increase of f",
         ["The maximum value of f", "The area under f",
          "The rate of change with respect to time"],
         "∇f = (∂f/∂x, ∂f/∂y, ...) — points in the direction of maximum rate of increase.", 'hard', 14),
        ("What is a double integral used for?",
         "Computing volume under a surface or area of a 2D region",
         ["Differentiating a function twice",
          "Finding the slope of a surface",
          "Computing the arc length of a curve"],
         "∬f(x,y) dA computes signed volume between the surface and the xy-plane.", 'hard', 14),
        ("What is Stokes' Theorem?",
         "∬(curl F)·dS = ∮F·dr — relates surface integral of curl to line integral around boundary",
         ["The divergence theorem", "Green's theorem in 3D",
          "Gauss's law for electric fields"],
         "Stokes' theorem generalizes Green's theorem to 3D surfaces.", 'hard', 16),
        ("What is the divergence of a vector field?",
         "A scalar measuring the net outflow of the field from a point",
         ["The rotation of the field at a point",
          "The magnitude of the field",
          "The gradient of the field"],
         "div F = ∇·F = ∂Fx/∂x + ∂Fy/∂y + ∂Fz/∂z.", 'hard', 15),
        ("What is a critical point of f(x,y)?",
         "A point where both ∂f/∂x = 0 and ∂f/∂y = 0",
         ["A point where f(x,y) = 0",
          "A point where only ∂f/∂x = 0",
          "The maximum of f"],
         "Critical points require all partial derivatives to be zero simultaneously.", 'medium', 14),
        ("What is the chain rule for multivariable functions?",
         "dz/dt = (∂z/∂x)(dx/dt) + (∂z/∂y)(dy/dt)",
         ["dz/dt = ∂z/∂x + ∂z/∂y",
          "dz/dt = (∂z/∂x)(∂z/∂y)",
          "dz/dt = dz/dx · dx/dy"],
         "The multivariable chain rule sums products of partial derivatives along each path.", 'hard', 14),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Multivariable Calculus', diff, q_text, choices, idx,
                     f"Correct: {ans}.", grade))
    return qs


def gen_linear_algebra(n=35, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What is a vector space?",
         "A set of vectors closed under addition and scalar multiplication with specific axioms",
         ["A set of numbers", "A coordinate system", "A matrix"],
         "Vector spaces satisfy 8 axioms (commutativity, associativity, distributivity, etc.).", 'hard', 14),
        ("What is the determinant of a 2×2 matrix [[a,b],[c,d]]?",
         "ad − bc",
         ["ab − cd", "ad + bc", "ac − bd"],
         "det([[a,b],[c,d]]) = ad − bc.", 'medium', 13),
        ("What does it mean for a matrix to be singular?",
         "Its determinant is zero; it has no inverse",
         ["All entries are 1", "It is a square matrix",
          "It has more rows than columns"],
         "Singular matrices have det = 0 and no inverse; the system Ax = b may have no unique solution.", 'medium', 14),
        ("What is an eigenvalue?",
         "A scalar λ such that Av = λv for some nonzero vector v",
         ["A diagonal entry of a matrix", "The determinant of a matrix",
          "The rank of a matrix"],
         "Eigenvalues satisfy det(A − λI) = 0. They describe scaling along eigenvectors.", 'hard', 14),
        ("What is the rank of a matrix?",
         "The number of linearly independent rows or columns",
         ["The number of rows", "The determinant",
          "The number of zero entries"],
         "Rank = dimension of the column space = number of pivots in row echelon form.", 'hard', 14),
        ("What is the dot product of vectors u = (1,2,3) and v = (4,5,6)?",
         "32", ["15", "27", "21"],
         "u·v = 1×4 + 2×5 + 3×6 = 4 + 10 + 18 = 32.", 'easy', 13),
        ("What does it mean for vectors to be orthogonal?",
         "Their dot product is zero",
         ["They point in the same direction", "They have the same magnitude",
          "One is a scalar multiple of the other"],
         "Orthogonal vectors are perpendicular: u·v = 0.", 'medium', 13),
        ("What is the null space of a matrix A?",
         "The set of all vectors x such that Ax = 0",
         ["The set of zero rows in A", "The column space of A",
          "The set of eigenvalues"],
         "Null space (kernel) = all solutions to the homogeneous system Ax = 0.", 'hard', 15),
        ("What is the transpose of a matrix?",
         "A matrix formed by swapping rows and columns",
         ["The inverse of the matrix", "The matrix with negated entries",
          "The matrix multiplied by -1"],
         "The transpose (Aᵀ)ᵢⱼ = Aⱼᵢ — rows become columns and vice versa.", 'easy', 13),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Linear Algebra', diff, q_text, choices, idx,
                     f"Correct: {ans}.", grade))
    return qs


def gen_discrete_math(n=35, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What is a proposition in logic?", "A statement that is either true or false",
         ["A mathematical equation", "A type of proof", "A set of rules"],
         "Propositions have definite truth values. 'It is raining' is a proposition.", 'easy', 13),
        ("What is the contrapositive of 'If P then Q'?",
         "'If not Q then not P'",
         ["'If not P then not Q'", "'If Q then P'", "'P if and only if Q'"],
         "Contrapositive: ¬Q → ¬P. It is logically equivalent to the original P → Q.", 'medium', 13),
        ("What is proof by contradiction?",
         "Assuming the negation of what you want to prove and deriving a contradiction",
         ["Proving both sides are equal",
          "Using examples to prove a statement",
          "Proving a statement by induction"],
         "Assume ¬P is true, derive a contradiction, therefore P must be true.", 'medium', 13),
        ("What is mathematical induction?",
         "Proving a base case and showing if true for n, then true for n+1",
         ["Testing many specific cases",
          "Proving by contradiction",
          "Using limits to prove statements"],
         "Induction: prove P(1), then prove P(n) → P(n+1) to conclude P holds for all n.", 'medium', 13),
        ("How many subsets does a set with n elements have?",
         "2ⁿ", ["n!", "n²", "n(n-1)/2"],
         "Each element is either in or out: 2 choices per element → 2ⁿ subsets.", 'medium', 13),
        ("What is a bijection (bijective function)?",
         "A function that is both injective (one-to-one) and surjective (onto)",
         ["A function with no inverse", "A function mapping to only one value",
          "A function where multiple inputs share an output"],
         "Bijections have perfect one-to-one correspondence between domain and codomain.", 'hard', 14),
        ("What is the handshaking lemma?",
         "The sum of all vertex degrees in a graph equals twice the number of edges",
         ["Every graph has an Euler circuit",
          "Connected graphs have n-1 edges",
          "The degree of every vertex equals the number of vertices"],
         "Sum of degrees = 2|E|, because each edge contributes 1 to each endpoint's degree.", 'hard', 15),
        ("What does it mean for a graph to be connected?",
         "There is a path between every pair of vertices",
         ["Every vertex has the same degree",
          "The graph has no cycles",
          "Every vertex connects to every other vertex"],
         "A connected graph has no isolated components — you can reach any vertex from any other.", 'medium', 13),
        ("In how many ways can you arrange n distinct items?",
         "n! (n factorial)", ["n", "2ⁿ", "n²"],
         "n! = n × (n-1) × ... × 1. Permutation of n distinct items.", 'easy', 13),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Discrete Math', diff, q_text, choices, idx,
                     f"Correct: {ans}.", grade))
    return qs


def gen_diff_equations_college(n=30, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What is a differential equation?",
         "An equation relating a function to its derivatives",
         ["An equation with many variables", "A matrix equation",
          "An equation with only integers"],
         "DEs describe rates of change: e.g., dy/dx = ky describes exponential growth.", 'easy', 13),
        ("What is the general solution of dy/dx = ky?",
         "y = Ceᵏˣ",
         ["y = kx + C", "y = k ln(x) + C", "y = C/eˣ"],
         "Separable ODE: dy/y = k dx → ln|y| = kx + C → y = Aeᵏˣ.", 'medium', 14),
        ("What is an initial value problem (IVP)?",
         "A differential equation with specified values at a starting point",
         ["A differential equation with no solution",
          "A system of differential equations",
          "A boundary value problem"],
         "IVP: dy/dx = f(x,y), y(x₀) = y₀. The initial condition specifies a unique solution.", 'medium', 14),
        ("What is a homogeneous ODE?",
         "An ODE of the form L(y) = 0, where L is a linear differential operator",
         ["An ODE with constant coefficients only",
          "An ODE where all variables are equal",
          "An ODE with no derivatives"],
         "Homogeneous: the right-hand side is 0. Inhomogeneous includes a non-zero forcing term.", 'hard', 14),
        ("What does the Wronskian test determine for solutions y₁ and y₂?",
         "Whether y₁ and y₂ are linearly independent solutions",
         ["The particular solution to an ODE",
          "Whether an ODE is separable",
          "The stability of equilibrium points"],
         "W(y₁,y₂) ≠ 0 at some point → linearly independent → fundamental solution set.", 'hard', 15),
        ("For the ODE y'' + 4y = 0, what is the general solution?",
         "y = C₁cos(2x) + C₂sin(2x)",
         ["y = C₁e²ˣ + C₂e⁻²ˣ", "y = C₁cos(x) + C₂sin(x)",
          "y = C₁e²ˣ + C₂xe²ˣ"],
         "Char eq: r² + 4 = 0 → r = ±2i → general solution uses cos and sin.", 'hard', 15),
        ("What is Euler's method used for?",
         "Numerically approximating solutions to differential equations",
         ["Finding exact solutions to ODEs",
          "Solving systems of linear equations",
          "Evaluating definite integrals"],
         "Euler's method: yₙ₊₁ = yₙ + h·f(xₙ, yₙ). Simple but can be inaccurate for large h.", 'medium', 14),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Differential Equations', diff, q_text, choices, idx,
                     f"Correct: {ans}.", grade))
    return qs


_TOPIC_GENERATORS = {
    'Single-Variable Calculus': [(gen_single_var_calculus, {})],
    'Multivariable Calculus':   [(gen_multivariable_calculus, {})],
    'Linear Algebra':           [(gen_linear_algebra, {})],
    'Discrete Math':            [(gen_discrete_math, {})],
    'Differential Equations':   [(gen_diff_equations_college, {})],
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
