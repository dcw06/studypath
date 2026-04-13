"""
College Statistics Generator
Covers: Probability Theory, Sampling Distributions, Hypothesis Testing,
        Confidence Intervals, Regression, ANOVA, Bayesian Statistics
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


def gen_probability_theory(n=40, seed=None):
    r = random.Random(seed)
    qs = []
    for _ in range(n):
        qtype = r.choice(['basic_prob', 'conditional', 'independence', 'bayes', 'complement'])
        if qtype == 'basic_prob':
            n_total = r.choice([4, 5, 6, 8, 10])
            n_success = r.randint(1, n_total - 1)
            from fractions import Fraction
            frac = Fraction(n_success, n_total)
            q_text = f"A bag has {n_success} red balls and {n_total - n_success} blue balls. What is the probability of drawing a red ball?"
            ans = f"{frac.numerator}/{frac.denominator}"
            # generate plausible wrongs
            wrongs = [f"{n_total - n_success}/{n_total}",
                      f"{n_success}/{n_success + n_total}",
                      f"1/{n_success}"]
            choices, idx = _shuffle_choices(ans, wrongs[:3], r)
            qs.append(_q('Probability Theory', 'easy',
                         q_text, choices, idx,
                         f"P(red) = {n_success}/{n_total} = {ans}.", 13))
        elif qtype == 'complement':
            p_num = r.randint(1, 9)
            p_den = 10
            comp_num = p_den - p_num
            q_text = f"If P(A) = {p_num}/10, what is P(A complement)?"
            ans = f"{comp_num}/10"
            wrongs = [f"{p_num}/10", f"{p_num + 1}/10", f"{p_den}/10"]
            choices, idx = _shuffle_choices(ans, wrongs[:3], r)
            qs.append(_q('Probability Theory', 'easy',
                         q_text, choices, idx,
                         f"P(A') = 1 - P(A) = 1 - {p_num}/10 = {comp_num}/10.", 13))
        else:
            # Pool questions
            pool_qs = [
                ("What is the probability of rolling a 6 on a fair die?",
                 "1/6", ["1/3", "1/2", "5/6"],
                 "A fair die has 6 equally likely outcomes; P(6) = 1/6.", 'easy', 13),
                ("Two fair coins are flipped. What is the probability of getting exactly one head?",
                 "1/2", ["1/4", "3/4", "1"],
                 "Outcomes: HH, HT, TH, TT. Exactly one head: HT, TH → P = 2/4 = 1/2.", 'easy', 13),
                ("What does P(A|B) represent?",
                 "The probability of A given that B has occurred",
                 ["The probability of A and B", "The probability of A or B",
                  "The probability of neither A nor B"],
                 "P(A|B) is the conditional probability of A given B.", 'medium', 13),
                ("If A and B are independent, what is P(A and B)?",
                 "P(A) × P(B)",
                 ["P(A) + P(B)", "P(A) + P(B) − P(A∪B)", "P(A|B)"],
                 "Independence means P(A∩B) = P(A)P(B).", 'medium', 13),
                ("Bayes' Theorem states: P(A|B) =",
                 "P(B|A)P(A) / P(B)",
                 ["P(A)P(B) / P(A|B)", "P(A∩B) / P(A)",
                  "P(B|A) / P(A)"],
                 "Bayes: P(A|B) = P(B|A)P(A)/P(B) — updates prior belief with evidence.", 'hard', 14),
                ("What is the expected value of a fair 6-sided die?",
                 "3.5", ["3", "4", "6"],
                 "E[X] = (1+2+3+4+5+6)/6 = 21/6 = 3.5.", 'medium', 13),
                ("What is the variance of a random variable?",
                 "E[(X − μ)²] — the average squared deviation from the mean",
                 ["The mean of X", "The standard deviation squared — it equals SD",
                  "The range of X"],
                 "Var(X) = E[X²] − (E[X])². Standard deviation = √Var(X).", 'medium', 14),
                ("What does 'mutually exclusive' mean for events A and B?",
                 "A and B cannot both occur simultaneously",
                 ["A and B are independent", "P(A) = P(B)",
                  "A occurs whenever B occurs"],
                 "Mutually exclusive: P(A∩B) = 0. If A happens, B cannot (and vice versa).", 'medium', 13),
            ]
            q_text, ans, wrongs, diff, grade = r.choice(pool_qs)
            choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
            qs.append(_q('Probability Theory', diff, q_text, choices, idx,
                         f"Correct: {ans}.", grade))
    return qs


def gen_distributions(n=35, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What is the normal distribution?",
         "A symmetric, bell-shaped distribution defined by mean μ and standard deviation σ",
         ["A distribution skewed to the right", "A discrete distribution",
          "A uniform distribution"],
         "Normal distribution: ~68% within 1σ, ~95% within 2σ, ~99.7% within 3σ.", 'medium', 13),
        ("What is the standard normal distribution?",
         "A normal distribution with μ = 0 and σ = 1",
         ["Any normal distribution", "A normal distribution with μ = 1",
          "A distribution where all values are positive"],
         "Z ~ N(0,1). Z-scores convert any normal distribution to standard normal.", 'medium', 13),
        ("What is the binomial distribution?",
         "The distribution of the number of successes in n independent trials with probability p",
         ["The distribution of continuous outcomes",
          "The distribution of waiting times",
          "A symmetric distribution around 0"],
         "Binomial(n,p): P(X=k) = C(n,k)pᵏ(1-p)ⁿ⁻ᵏ.", 'medium', 14),
        ("What is the Poisson distribution?",
         "The distribution of the number of events occurring in a fixed interval",
         ["The distribution of success/failure trials",
          "A continuous distribution for positive values",
          "The distribution of means"],
         "Poisson(λ): models rare events, P(X=k) = e⁻λλᵏ/k!, mean = variance = λ.", 'hard', 14),
        ("What is the Central Limit Theorem?",
         "The sampling distribution of the mean approaches normal as sample size increases",
         ["All data follows a normal distribution",
          "Larger samples have smaller means",
          "Population distributions determine sample distributions exactly"],
         "CLT: for large n, X̄ ~ N(μ, σ²/n) regardless of the population distribution.", 'hard', 14),
        ("What is the exponential distribution?",
         "A distribution modeling the time between events in a Poisson process",
         ["A distribution for count data", "The normal distribution squared",
          "A discrete distribution for failures"],
         "Exponential(λ): f(x) = λe⁻λˣ for x ≥ 0. Memoryless property.", 'hard', 15),
        ("What is the chi-squared distribution?",
         "The distribution of the sum of squared standard normal random variables",
         ["A distribution for proportions", "A normal distribution with positive values",
          "A distribution for correlation coefficients"],
         "χ²(k) = sum of k squared standard normals. Used in goodness-of-fit tests.", 'hard', 15),
        ("What is the t-distribution?",
         "A bell-shaped distribution with heavier tails than normal, used for small samples",
         ["The normal distribution", "A distribution only for large samples",
          "A discrete distribution"],
         "t-distribution has more probability in the tails. As df → ∞, t → N(0,1).", 'medium', 14),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Distributions', diff, q_text, choices, idx,
                     f"Correct: {ans}.", grade))
    return qs


def gen_hypothesis_testing(n=35, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What is the null hypothesis (H₀)?",
         "The hypothesis of no effect or no difference",
         ["The hypothesis we want to prove", "The hypothesis that is always true",
          "The hypothesis with the largest p-value"],
         "H₀ is the default assumption; we try to find evidence against it.", 'medium', 13),
        ("What is a Type I error?",
         "Rejecting the null hypothesis when it is actually true (false positive)",
         ["Failing to reject a false null hypothesis",
          "Accepting the alternative hypothesis incorrectly",
          "Using the wrong test statistic"],
         "Type I error (α): falsely concluding there is an effect when there isn't.", 'hard', 14),
        ("What is a Type II error?",
         "Failing to reject a false null hypothesis (false negative)",
         ["Rejecting a true null hypothesis",
          "Using the wrong significance level",
          "Selecting an unrepresentative sample"],
         "Type II error (β): missing a real effect — concluding no difference when there is one.", 'hard', 14),
        ("What is statistical power?",
         "The probability of correctly rejecting a false null hypothesis (1 − β)",
         ["The probability of Type I error", "The sample size",
          "The significance level α"],
         "Higher power → less chance of missing a real effect. Increased by larger n or effect size.", 'hard', 14),
        ("What is a p-value?",
         "The probability of observing results as extreme as the data, assuming H₀ is true",
         ["The probability H₀ is true", "The probability the result is meaningful",
          "The significance level α"],
         "A small p-value (< α) is evidence against H₀. It does NOT measure the probability H₀ is false.", 'hard', 14),
        ("What is a confidence interval?",
         "A range of values likely to contain the true population parameter",
         ["The exact value of a population parameter",
          "A p-value expressed as a range",
          "The range of the sample data"],
         "A 95% CI: if we repeated the experiment many times, 95% of intervals would contain the true value.", 'hard', 14),
        ("When should you use a t-test vs a z-test?",
         "t-test when σ is unknown or n is small; z-test when σ is known and n is large",
         ["Always use z-test", "Use t-test only for categorical data",
          "They are interchangeable"],
         "In practice, t-tests are almost always used since population σ is rarely known.", 'medium', 14),
        ("What is a chi-square goodness-of-fit test?",
         "A test comparing observed frequencies to expected frequencies",
         ["A test for correlation", "A test for normality",
          "A test comparing two means"],
         "Chi-square goodness of fit: χ² = Σ(O-E)²/E. Tests if data fits an expected distribution.", 'hard', 15),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Hypothesis Testing', diff, q_text, choices, idx,
                     f"Correct: {ans}.", grade))
    return qs


def gen_regression(n=30, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What does simple linear regression model?",
         "A linear relationship between one independent and one dependent variable",
         ["The average of two variables", "A nonlinear relationship between variables",
          "The correlation between multiple variables"],
         "Simple linear regression: Y = β₀ + β₁X + ε.", 'easy', 13),
        ("What does R² (coefficient of determination) measure?",
         "The proportion of variance in Y explained by the model",
         ["The slope of the regression line", "The correlation between X and Y",
          "The standard error of residuals"],
         "R² = 1 − SS_res/SS_tot. R² of 0.85 means 85% of variance is explained.", 'medium', 14),
        ("What is multicollinearity in multiple regression?",
         "High correlation between independent variables, making coefficients unstable",
         ["The residuals are correlated", "The dependent variable has outliers",
          "The model has too few variables"],
         "Multicollinearity inflates standard errors and makes it hard to interpret individual coefficients.", 'hard', 15),
        ("What is heteroscedasticity?",
         "Non-constant variance of residuals across levels of an independent variable",
         ["Equal variance of residuals", "A violation of the normality assumption",
          "Correlation between residuals"],
         "OLS assumes homoscedasticity (constant variance). Heteroscedasticity biases standard errors.", 'hard', 15),
        ("What is the purpose of the F-test in regression?",
         "To test whether the overall regression model is statistically significant",
         ["To test individual coefficients", "To test for normality",
          "To test for multicollinearity"],
         "The F-test (global test) tests H₀: all β = 0 simultaneously.", 'hard', 14),
        ("In logistic regression, what does the model output?",
         "The probability of a binary outcome",
         ["A continuous prediction", "A classification tree",
          "The log of the dependent variable"],
         "Logistic regression models P(Y=1) = 1/(1+e⁻ˡⁱⁿᵉᵃʳ ᵖʳᵉᵈⁱᶜᵗᵒʳ) — output is a probability.", 'hard', 15),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Regression Analysis', diff, q_text, choices, idx,
                     f"Correct: {ans}.", grade))
    return qs


_TOPIC_GENERATORS = {
    'Probability Theory':  [(gen_probability_theory, {})],
    'Distributions':       [(gen_distributions, {})],
    'Hypothesis Testing':  [(gen_hypothesis_testing, {})],
    'Regression Analysis': [(gen_regression, {})],
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
