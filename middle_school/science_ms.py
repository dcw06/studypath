"""
Middle School Science Generator (Grades 6–8)
Covers: Cells & Life Science, Body Systems, Genetics, Atoms & Elements,
        Chemical Reactions, Earth Science, Plate Tectonics, Ecosystems,
        Astronomy, Physics Basics
"""
import random
import json

def _q(topic, diff, question, choices, answer_idx, explanation, grade=7):
    return ('Science', topic, diff, question, json.dumps(choices), answer_idx, explanation, grade)

def _shuffle_choices(correct, wrongs, rng):
    choices = list(rng.sample(wrongs, min(3, len(wrongs))))
    idx = rng.randint(0, min(3, len(choices)))
    choices.insert(idx, correct)
    return choices[:4], idx


def gen_cells(n=35, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What is the basic unit of life?", "Cell",
         ["Atom", "Molecule", "Organ"],
         "All living things are made of cells — the smallest unit of life.", 'easy', 6),
        ("What controls what enters and exits a cell?",
         "Cell membrane", ["Cell wall", "Nucleus", "Vacuole"],
         "The cell membrane is a selective barrier controlling substances in and out.", 'easy', 6),
        ("What is the function of the nucleus?", "Controls cell activities and contains DNA",
         ["Produces energy", "Stores water", "Digests waste"],
         "The nucleus is the 'control center' housing the cell's genetic material.", 'easy', 6),
        ("What organelle produces energy (ATP) for the cell?", "Mitochondria",
         ["Ribosome", "Vacuole", "Chloroplast"],
         "Mitochondria are the 'powerhouse of the cell,' producing ATP through cellular respiration.", 'medium', 7),
        ("Which organelle is found in plant cells but NOT animal cells?",
         "Chloroplast", ["Mitochondria", "Ribosome", "Cell membrane"],
         "Chloroplasts capture sunlight for photosynthesis — only in plant cells.", 'medium', 7),
        ("What is the difference between prokaryotic and eukaryotic cells?",
         "Eukaryotes have a membrane-bound nucleus; prokaryotes do not",
         ["Prokaryotes are larger than eukaryotes",
          "Eukaryotes have no organelles",
          "Prokaryotes only exist in animals"],
         "Bacteria are prokaryotes (no nucleus). Plants, animals, fungi are eukaryotes.", 'hard', 8),
        ("What process do cells use to divide and produce two identical cells?",
         "Mitosis", ["Meiosis", "Photosynthesis", "Osmosis"],
         "Mitosis produces identical daughter cells for growth and repair.", 'medium', 7),
        ("What is osmosis?",
         "The movement of water across a semipermeable membrane",
         ["The production of ATP", "Cell division", "Protein synthesis"],
         "Osmosis is a specific type of diffusion involving water molecules.", 'medium', 8),
        ("What is the role of ribosomes?", "Synthesize (make) proteins",
         ["Produce energy", "Store DNA", "Digest old organelles"],
         "Ribosomes read mRNA and assemble proteins from amino acids.", 'hard', 8),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Cells & Life Science', diff, q_text, choices, idx,
                     f"Correct: {ans}.", grade))
    return qs


def gen_body_systems(n=35, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What is the function of the circulatory system?",
         "Pump blood and transport oxygen/nutrients throughout the body",
         ["Break down food", "Filter waste from blood", "Control movement"],
         "The heart, blood, and vessels make up the circulatory system.", 'easy', 6),
        ("Which organ removes waste from the blood and produces urine?",
         "Kidney", ["Liver", "Lung", "Stomach"],
         "The kidneys filter blood and excrete waste as urine.", 'easy', 6),
        ("What is the function of the respiratory system?",
         "Exchange oxygen and carbon dioxide",
         ["Digest food", "Pump blood", "Send nerve signals"],
         "The lungs bring oxygen into the blood and remove CO2.", 'easy', 6),
        ("What is the role of the skeletal system?",
         "Support, protection, and movement",
         ["Produce hormones", "Filter blood", "Digest food"],
         "Bones support the body, protect organs, and anchor muscles.", 'easy', 6),
        ("Which system fights infection and disease?",
         "Immune system", ["Nervous system", "Endocrine system", "Digestive system"],
         "The immune system uses white blood cells and antibodies to fight pathogens.", 'medium', 7),
        ("What does the nervous system use to send signals?",
         "Electrical impulses through neurons",
         ["Hormones through the blood", "Muscles contracting", "Oxygen from lungs"],
         "Neurons transmit electrical signals throughout the nervous system.", 'medium', 7),
        ("What is the difference between arteries and veins?",
         "Arteries carry blood away from the heart; veins carry it back",
         ["Arteries carry blood back; veins carry it away",
          "They carry the same blood in the same direction",
          "Arteries only carry oxygenated blood"],
         "A = arteries away, V = veins return (to the heart).", 'medium', 7),
        ("What is the role of the endocrine system?",
         "Produce and regulate hormones",
         ["Control movement", "Digest food", "Transport oxygen"],
         "Glands like the thyroid and adrenal glands release hormones into the bloodstream.", 'hard', 8),
        ("Where does digestion begin?", "In the mouth",
         ["In the stomach", "In the small intestine", "In the esophagus"],
         "Saliva and chewing begin breaking down food in the mouth.", 'easy', 6),
        ("What is the function of the small intestine?",
         "Absorb nutrients into the bloodstream",
         ["Break down food with acid", "Store waste", "Filter toxins"],
         "The small intestine absorbs digested nutrients into the blood.", 'medium', 7),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Body Systems', diff, q_text, choices, idx,
                     f"Correct: {ans}.", grade))
    return qs


def gen_genetics(n=30, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What is DNA?", "The molecule that carries genetic information",
         ["A type of protein", "A cell organelle", "A type of carbohydrate"],
         "DNA (deoxyribonucleic acid) stores the instructions for building and running organisms.", 'easy', 7),
        ("What is a gene?", "A segment of DNA that codes for a specific trait",
         ["A chromosome", "A cell membrane protein", "An RNA molecule"],
         "Genes are sections of DNA that carry instructions for specific traits.", 'medium', 7),
        ("What is a dominant allele?",
         "An allele whose trait is expressed even if only one copy is present",
         ["An allele that is always harmful", "An allele that requires two copies to show",
          "An allele found only in males"],
         "Dominant alleles mask recessive ones. One copy is enough to show the trait.", 'medium', 7),
        ("If B (brown eyes) is dominant and b (blue eyes) is recessive, what eye color would Bb have?",
         "Brown", ["Blue", "Green", "Gray"],
         "Bb has one dominant allele (B), so brown eyes are expressed.", 'medium', 7),
        ("What is a Punnett square used for?",
         "Predicting the possible genetic outcomes of a cross",
         ["Drawing DNA structure", "Mapping the human genome",
          "Identifying mutations"],
         "Punnett squares show all possible allele combinations from two parents.", 'medium', 8),
        ("What is the term for an organism with two identical alleles (BB or bb)?",
         "Homozygous", ["Heterozygous", "Dominant", "Recessive"],
         "Homozygous = same alleles (BB or bb). Heterozygous = different (Bb).", 'hard', 8),
        ("What is a mutation?", "A change in the DNA sequence",
         ["Normal cell division", "Protein synthesis", "Gene expression"],
         "Mutations are changes to the nucleotide sequence of DNA.", 'medium', 8),
        ("What is natural selection?",
         "Organisms with favorable traits are more likely to survive and reproduce",
         ["All organisms reproduce equally", "Humans choose which animals survive",
          "Species change randomly with no pattern"],
         "Darwin's natural selection: favorable traits increase in populations over time.", 'hard', 8),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Genetics', diff, q_text, choices, idx,
                     f"Correct: {ans}.", grade))
    return qs


def gen_atoms_elements(n=35, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What are the three subatomic particles in an atom?",
         "Protons, neutrons, electrons",
         ["Protons, atoms, molecules", "Neutrons, ions, electrons", "Protons, photons, electrons"],
         "Atoms have protons (+) and neutrons in the nucleus, with electrons (-) orbiting.", 'easy', 7),
        ("What determines the identity of an element?",
         "The number of protons (atomic number)",
         ["The number of neutrons", "The number of electrons", "The atomic mass"],
         "Each element has a unique atomic number (proton count).", 'medium', 7),
        ("What is the atomic number of carbon?", "6",
         ["12", "8", "4"],
         "Carbon has 6 protons, giving it atomic number 6.", 'easy', 7),
        ("What is an ion?", "An atom with an unequal number of protons and electrons",
         ["An atom with extra neutrons", "A neutral atom", "A molecule of two atoms"],
         "Ions have a charge because they gained or lost electrons.", 'medium', 8),
        ("What is the periodic table organized by?",
         "Increasing atomic number (protons)",
         ["Alphabetical order", "Atomic mass only", "Date of discovery"],
         "Elements are arranged by atomic number from left to right, top to bottom.", 'easy', 7),
        ("What is an isotope?", "Atoms of the same element with different numbers of neutrons",
         ["Different elements with the same mass", "Atoms with different proton counts",
          "Charged atoms"],
         "Isotopes have the same atomic number but different mass numbers.", 'hard', 8),
        ("What type of bond involves sharing electrons?", "Covalent bond",
         ["Ionic bond", "Hydrogen bond", "Metallic bond"],
         "Covalent bonds form when atoms share electrons. Ionic bonds involve transfer.", 'hard', 8),
        ("What is the chemical symbol for water?", "H₂O",
         ["HO", "H₂O₂", "OH"],
         "Water = 2 hydrogen atoms + 1 oxygen atom.", 'easy', 6),
        ("How many electrons can the first energy level of an atom hold?", "2",
         ["8", "18", "32"],
         "The first shell holds max 2 electrons; second holds up to 8.", 'medium', 8),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Atoms & Elements', diff, q_text, choices, idx,
                     f"Correct: {ans}.", grade))
    return qs


def gen_earth_science(n=30, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What are Earth's four layers from outside to inside?",
         "Crust, mantle, outer core, inner core",
         ["Core, mantle, crust, atmosphere",
          "Crust, core, mantle, magma",
          "Lithosphere, asthenosphere, mesosphere, core"],
         "Earth's structure: thin crust → mantle → liquid outer core → solid inner core.", 'medium', 7),
        ("What causes earthquakes?", "Movement of tectonic plates",
         ["Volcanic eruptions", "Ocean currents", "Wind erosion"],
         "Earthquakes occur when tectonic plates move, collide, or slip.", 'easy', 6),
        ("What is a tectonic plate?", "A large section of Earth's crust that moves",
         ["A type of rock", "A layer of the atmosphere", "A volcanic mountain"],
         "Earth's lithosphere is divided into moving tectonic plates.", 'easy', 6),
        ("What type of boundary causes mountains to form?",
         "Convergent boundary (collision)",
         ["Divergent boundary", "Transform boundary", "Subduction zone only"],
         "When two plates collide (converge), rock folds upward forming mountains.", 'medium', 7),
        ("What is the theory of plate tectonics?",
         "Earth's crust is divided into plates that move over time",
         ["The Earth expands over time", "Continents were always in their current positions",
          "Earthquakes create new land"],
         "Plate tectonics explains continental drift, earthquakes, volcanoes, and mountain formation.", 'medium', 7),
        ("What is the rock cycle?",
         "The process by which rocks change from one type to another over time",
         ["The way rocks orbit the Earth", "A list of rock names",
          "The breakdown of rocks into soil"],
         "Rocks change between igneous, sedimentary, and metamorphic through heat, pressure, and erosion.", 'medium', 7),
        ("How are sedimentary rocks formed?", "Layers of sediment compressed over time",
         ["Cooling of magma", "Heat and pressure on existing rocks",
          "Volcanic eruptions"],
         "Sedimentary rocks form from compressed layers of sediment (sand, mud, shells).", 'easy', 6),
        ("What is weathering?", "The breaking down of rocks by water, wind, or ice",
         ["The movement of broken rock pieces", "The formation of new rock",
          "The heating of Earth's interior"],
         "Weathering breaks rocks down (physical or chemical). Erosion moves them.", 'medium', 7),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Earth Science', diff, q_text, choices, idx,
                     f"Correct: {ans}.", grade))
    return qs


def gen_ecosystems_ms(n=30, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What is a food chain?",
         "A sequence showing how energy passes from one organism to another",
         ["A list of all organisms in an ecosystem", "The way animals hunt",
          "A diagram of an animal's diet"],
         "Food chains show who eats whom: Producer → Primary Consumer → Secondary Consumer.", 'easy', 6),
        ("What is a producer?", "An organism that makes its own food through photosynthesis",
         ["An organism that eats plants", "An organism that eats animals",
          "An organism that decomposes dead matter"],
         "Plants and algae are producers — they convert sunlight into energy.", 'easy', 6),
        ("What is the role of decomposers in an ecosystem?",
         "Break down dead organisms and recycle nutrients",
         ["Eat living animals", "Produce oxygen", "Control predator populations"],
         "Decomposers (fungi, bacteria) break down dead material, returning nutrients to the soil.", 'medium', 7),
        ("What happens to energy as it moves up a food chain?",
         "Energy decreases (about 10% transfers at each level)",
         ["Energy increases", "Energy stays the same", "Energy doubles at each level"],
         "Only ~10% of energy passes to the next trophic level — the rest is lost as heat.", 'hard', 8),
        ("What is biodiversity?",
         "The variety of life forms in an ecosystem",
         ["The total mass of organisms", "The number of predators",
          "The amount of water in an ecosystem"],
         "High biodiversity makes ecosystems more resilient and stable.", 'medium', 7),
        ("What is a symbiotic relationship?", "A close relationship between two different species",
         ["A relationship between plants and soil", "Competition for the same food",
          "Seasonal migration patterns"],
         "Symbiosis includes mutualism, commensalism, and parasitism.", 'medium', 7),
        ("In mutualism, both organisms:", "Benefit from the relationship",
         ["Compete against each other", "One benefits, one is harmed",
          "One benefits, one is unaffected"],
         "Mutualism = both organisms benefit (e.g., bees and flowers).", 'easy', 7),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Ecosystems', diff, q_text, choices, idx,
                     f"Correct: {ans}.", grade))
    return qs


_TOPIC_GENERATORS = {
    'Cells & Life Science': [(gen_cells, {})],
    'Body Systems':         [(gen_body_systems, {})],
    'Genetics':             [(gen_genetics, {})],
    'Atoms & Elements':     [(gen_atoms_elements, {})],
    'Earth Science':        [(gen_earth_science, {})],
    'Ecosystems':           [(gen_ecosystems_ms, {})],
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
