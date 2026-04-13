"""
High School Science Generator (Grades 9–12)
Covers: Biology, Chemistry, Physics, Earth & Environmental Science
"""
import random
import json

def _q(topic, diff, question, choices, answer_idx, explanation, grade=10):
    return ('Science', topic, diff, question, json.dumps(choices), answer_idx, explanation, grade)

def _shuffle_choices(correct, wrongs, rng):
    choices = list(rng.sample(wrongs, min(3, len(wrongs))))
    idx = rng.randint(0, min(3, len(choices)))
    choices.insert(idx, correct)
    return choices[:4], idx


def gen_biology_hs(n=40, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What is the central dogma of molecular biology?",
         "DNA → RNA → Protein",
         ["Protein → RNA → DNA", "RNA → DNA → Protein", "DNA → Protein → RNA"],
         "The central dogma: DNA is transcribed to RNA, which is translated into protein.", 'medium', 10),
        ("What is ATP?",
         "Adenosine triphosphate — the primary energy currency of cells",
         ["A type of protein", "A nucleotide that carries genetic information",
          "A structural component of cell membranes"],
         "ATP stores and transfers energy for nearly all cellular processes.", 'medium', 10),
        ("Where does photosynthesis occur in plant cells?",
         "Chloroplasts", ["Mitochondria", "Nucleus", "Ribosomes"],
         "Chloroplasts contain chlorophyll and carry out the light reactions and Calvin cycle.", 'easy', 9),
        ("What is the equation for cellular respiration?",
         "C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O + ATP",
         ["6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂",
          "C₆H₁₂O₆ → 6CO₂ + 6H₂O",
          "6O₂ + ATP → C₆H₁₂O₆ + CO₂"],
         "Cellular respiration: glucose + oxygen → carbon dioxide + water + energy (ATP).", 'medium', 10),
        ("What is the difference between mitosis and meiosis?",
         "Mitosis produces 2 identical diploid cells; meiosis produces 4 genetically unique haploid cells",
         ["Mitosis produces 4 cells; meiosis produces 2",
          "Mitosis is only in plants; meiosis is only in animals",
          "They are the same process"],
         "Mitosis: growth/repair. Meiosis: sexual reproduction — reduces chromosome number by half.", 'hard', 11),
        ("What is the Hardy-Weinberg equilibrium?",
         "A principle stating allele frequencies stay constant without evolutionary forces",
         ["The rate at which mutations occur",
          "The relationship between genotype and phenotype",
          "The speed of natural selection"],
         "Hardy-Weinberg: in the absence of mutation, drift, selection, etc., allele frequencies don't change.", 'hard', 12),
        ("What is enzyme specificity?",
         "Each enzyme catalyzes only specific reactions due to its active site shape",
         ["Enzymes work on any substrate", "Enzymes are consumed in reactions",
          "Enzymes work at any temperature"],
         "The 'lock and key' model: an enzyme's active site fits only certain substrates.", 'medium', 10),
        ("What is the function of DNA polymerase?",
         "Synthesize new DNA strands during replication",
         ["Transcribe DNA to RNA", "Translate RNA to protein",
          "Repair damaged cell membranes"],
         "DNA polymerase reads the template strand and builds a new complementary strand.", 'hard', 11),
        ("What are the stages of mitosis in order?",
         "Prophase, Metaphase, Anaphase, Telophase",
         ["Interphase, Prophase, Telophase, Cytokinesis",
          "Metaphase, Prophase, Anaphase, Telophase",
          "G1, S, G2, Mitosis"],
         "PMAT: Prophase (condense) → Metaphase (align) → Anaphase (separate) → Telophase (reform).", 'medium', 10),
        ("What causes sickle cell anemia?",
         "A single nucleotide mutation in the hemoglobin gene",
         ["A chromosomal deletion", "A viral infection of red blood cells",
          "Lack of iron in the diet"],
         "A point mutation changes one amino acid (Glu→Val) in hemoglobin, distorting red blood cells.", 'hard', 12),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Biology', diff, q_text, choices, idx, f"Correct: {ans}.", grade))
    return qs


def gen_chemistry_hs(n=40, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What is the molar mass of H₂O?", "18 g/mol",
         ["16 g/mol", "20 g/mol", "10 g/mol"],
         "H₂O: 2(1) + 16 = 18 g/mol.", 'easy', 9),
        ("What is Avogadro's number?", "6.022 × 10²³",
         ["6.022 × 10²⁰", "3.14 × 10²³", "1.008 × 10²³"],
         "One mole of any substance contains 6.022 × 10²³ particles.", 'easy', 10),
        ("What is a covalent bond?",
         "A bond formed by sharing electrons between atoms",
         ["A bond formed by transferring electrons", "A bond between metals",
          "A weak attraction between molecules"],
         "Covalent bonds share electrons (nonmetals). Ionic bonds transfer electrons (metal + nonmetal).", 'medium', 10),
        ("What is the pH of a neutral solution?", "7",
         ["0", "14", "10"],
         "pH 7 = neutral. pH < 7 = acidic. pH > 7 = basic.", 'easy', 9),
        ("What does Le Chatelier's Principle state?",
         "A system at equilibrium shifts to oppose changes in conditions",
         ["Reactions always favor products", "Temperature has no effect on equilibrium",
          "Catalysts shift equilibrium toward products"],
         "Le Chatelier: stress the system → equilibrium shifts to relieve the stress.", 'hard', 11),
        ("What is oxidation?",
         "Loss of electrons",
         ["Gain of electrons", "Addition of oxygen only", "Reduction of pH"],
         "OIL RIG: Oxidation Is Loss, Reduction Is Gain (of electrons).", 'medium', 10),
        ("What is the ideal gas law?",
         "PV = nRT",
         ["PV = RT", "P/V = nRT", "nPV = RT"],
         "P = pressure, V = volume, n = moles, R = gas constant, T = temperature.", 'medium', 11),
        ("What is electronegativity?",
         "The tendency of an atom to attract electrons in a bond",
         ["The number of electrons an atom has", "The charge of an ion",
          "The energy needed to remove an electron"],
         "Higher electronegativity = stronger pull on bonding electrons. Fluorine is most electronegative.", 'hard', 11),
        ("What type of reaction is: A + B → AB?",
         "Synthesis (combination) reaction",
         ["Decomposition reaction", "Single replacement reaction", "Combustion reaction"],
         "Synthesis: two substances combine to form one product.", 'medium', 10),
        ("What is a buffer solution?",
         "A solution that resists changes in pH",
         ["A very acidic solution", "A solution with no dissolved ions",
          "A supersaturated solution"],
         "Buffers (weak acid + conjugate base) absorb H⁺ or OH⁻ to maintain pH.", 'hard', 12),
        ("What happens to reaction rate when temperature increases?",
         "It increases because molecules move faster and collide more often",
         ["It decreases", "It stays the same", "It only changes for exothermic reactions"],
         "Higher temperature → more kinetic energy → more frequent and energetic collisions.", 'medium', 10),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Chemistry', diff, q_text, choices, idx, f"Correct: {ans}.", grade))
    return qs


def gen_physics_hs(n=40, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What is Newton's Second Law?",
         "F = ma (force equals mass times acceleration)",
         ["F = mv", "F = m/a", "F = ma²"],
         "Net force = mass × acceleration. Larger force → larger acceleration.", 'easy', 9),
        ("What is the unit of force in SI units?", "Newton (N)",
         ["Joule (J)", "Watt (W)", "Pascal (Pa)"],
         "1 Newton = 1 kg·m/s².", 'easy', 9),
        ("What is kinetic energy?",
         "Energy of motion: KE = ½mv²",
         ["Energy stored due to position", "Energy from chemical bonds",
          "Thermal energy of particles"],
         "KE = ½mv². Double the speed → 4× the kinetic energy.", 'medium', 10),
        ("What is the law of conservation of energy?",
         "Energy cannot be created or destroyed, only transformed",
         ["Energy is lost as heat in all processes",
          "Energy can be created from mass",
          "Kinetic and potential energy are always equal"],
         "Total energy in a closed system remains constant.", 'medium', 10),
        ("What is Ohm's Law?", "V = IR (voltage = current × resistance)",
         ["V = I/R", "V = IR²", "I = V²/R"],
         "Ohm's Law: Voltage (V) = Current (I) × Resistance (R).", 'easy', 10),
        ("What is the speed of light in a vacuum?",
         "3 × 10⁸ m/s", ["3 × 10⁶ m/s", "1 × 10⁸ m/s", "3 × 10¹⁰ m/s"],
         "c ≈ 3 × 10⁸ m/s (about 300,000 km/s).", 'medium', 11),
        ("What is the difference between scalar and vector quantities?",
         "Scalars have magnitude only; vectors have magnitude and direction",
         ["Vectors have magnitude only; scalars have direction",
          "They are the same thing",
          "Scalars use SI units; vectors use metric units"],
         "Speed is scalar; velocity is vector. Distance is scalar; displacement is vector.", 'medium', 10),
        ("What is the formula for gravitational potential energy?",
         "PE = mgh",
         ["PE = ½mv²", "PE = mv", "PE = m/h"],
         "PE = mass × gravitational acceleration × height.", 'medium', 10),
        ("What is momentum?", "p = mv (mass × velocity)",
         ["p = ma", "p = Ft", "p = m/v"],
         "Momentum = mass × velocity. It is a vector quantity.", 'medium', 10),
        ("What does the photoelectric effect demonstrate?",
         "Light behaves as particles (photons)",
         ["Light travels in waves", "Electrons can travel through vacuums",
          "Atoms emit heat when excited"],
         "Einstein's 1905 explanation of the photoelectric effect confirmed light's particle nature.", 'hard', 12),
        ("What is the difference between fission and fusion?",
         "Fission splits heavy atoms; fusion combines light atoms",
         ["Fusion splits atoms; fission combines them",
          "Both are the same nuclear process",
          "Fission is chemical; fusion is nuclear"],
         "Nuclear fission (e.g., uranium in reactors) splits atoms. Fusion (sun) combines hydrogen.", 'hard', 12),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Physics', diff, q_text, choices, idx, f"Correct: {ans}.", grade))
    return qs


def gen_earth_env_science_hs(n=35, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What causes the greenhouse effect?",
         "Greenhouse gases trap heat in Earth's atmosphere",
         ["The ozone layer blocks sunlight", "Volcanoes emit heat",
          "Ocean currents redistribute heat"],
         "CO₂, CH₄, and H₂O vapor absorb outgoing infrared radiation, warming the planet.", 'medium', 10),
        ("What is the difference between weather and climate?",
         "Weather is short-term atmospheric conditions; climate is long-term patterns",
         ["Weather is global; climate is local",
          "They are the same thing",
          "Climate is daily; weather is seasonal"],
         "Weather = today's forecast. Climate = average weather over 30+ years.", 'easy', 9),
        ("What is the carbon cycle?",
         "The movement of carbon through the atmosphere, biosphere, oceans, and geosphere",
         ["The process of photosynthesis only", "The burning of fossil fuels",
          "The seasonal change in CO₂ levels only"],
         "Carbon moves through living organisms, the air, oceans, rocks, and soil continuously.", 'medium', 10),
        ("What is biodiversity and why is it important?",
         "The variety of life; important for ecosystem stability and resilience",
         ["The total biomass of organisms", "The number of endangered species",
          "The genetic similarity within a species"],
         "High biodiversity provides ecosystem services and makes ecosystems more resilient to change.", 'medium', 10),
        ("What is the difference between renewable and nonrenewable energy?",
         "Renewable replenishes naturally; nonrenewable takes millions of years to form",
         ["Renewable is always more expensive",
          "Nonrenewable is always more efficient",
          "They produce the same amount of energy"],
         "Solar, wind, hydro = renewable. Coal, oil, gas = nonrenewable (fossil fuels).", 'easy', 9),
        ("What causes El Niño?",
         "Warming of the central and eastern Pacific Ocean surface temperatures",
         ["A polar vortex", "Solar flares", "Volcanic eruptions in the Pacific"],
         "El Niño: weakening of trade winds allows warm Pacific water to spread east, altering global weather.", 'hard', 11),
        ("What is the ozone layer and why is it important?",
         "A layer of ozone (O₃) in the stratosphere that absorbs UV radiation",
         ["A layer of CO₂ that warms the planet",
          "A layer of water vapor in the troposphere",
          "A layer of clouds that blocks sunlight"],
         "The ozone layer (stratosphere) absorbs 97-99% of the sun's ultraviolet radiation.", 'medium', 10),
        ("What is eutrophication?",
         "Excessive nutrient pollution causing algae blooms and oxygen depletion in water",
         ["The process of desertification", "The cooling of ocean water",
          "The formation of acid rain"],
         "Eutrophication: excess nutrients (N, P) → algae blooms → decomposition → oxygen depletion → dead zones.", 'hard', 12),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Earth & Environmental Science', diff, q_text, choices, idx,
                     f"Correct: {ans}.", grade))
    return qs


_TOPIC_GENERATORS = {
    'Biology':                      [(gen_biology_hs, {})],
    'Chemistry':                    [(gen_chemistry_hs, {})],
    'Physics':                      [(gen_physics_hs, {})],
    'Earth & Environmental Science': [(gen_earth_env_science_hs, {})],
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
