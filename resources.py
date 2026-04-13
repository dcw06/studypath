"""
Educational platform resource links for QuizArena.
Maps subject/topic → curated external resources (no API keys needed).
"""

# ── Khan Academy topic URLs ────────────────────────────────────────────
# Format: https://www.khanacademy.org/[path]
KA_BASE = "https://www.khanacademy.org"

# ── Resource definitions ───────────────────────────────────────────────
# Each resource: {'title', 'url', 'platform', 'type', 'icon'}
# platform: 'khan' | 'youtube' | 'wikipedia' | 'openstax' | 'desmos' | 'wolfram' | 'coursera'
# type: 'lesson' | 'video' | 'article' | 'tool' | 'course'

TOPIC_RESOURCES = {

    # ── MATH ──────────────────────────────────────────────────────────
    "Algebra": [
        {"title": "Algebra Basics",        "url": f"{KA_BASE}/math/algebra",                          "platform": "khan",      "type": "lesson", "icon": "🎓"},
        {"title": "Algebra I",             "url": f"{KA_BASE}/math/algebra",                          "platform": "khan",      "type": "course", "icon": "🎓"},
        {"title": "Algebra II",            "url": f"{KA_BASE}/math/algebra2",                         "platform": "khan",      "type": "course", "icon": "🎓"},
        {"title": "Algebraic expressions", "url": "https://en.wikipedia.org/wiki/Algebraic_expression","platform": "wikipedia", "type": "article","icon": "📖"},
        {"title": "Desmos Graphing Calculator","url": "https://www.desmos.com/calculator",            "platform": "desmos",    "type": "tool",   "icon": "🧮"},
        {"title": "OpenStax College Algebra","url": "https://openstax.org/books/college-algebra/pages/1-introduction-to-prerequisites","platform":"openstax","type":"lesson","icon":"📚"},
    ],
    "Arithmetic": [
        {"title": "Pre-algebra",           "url": f"{KA_BASE}/math/pre-algebra",                      "platform": "khan",      "type": "course", "icon": "🎓"},
        {"title": "Arithmetic",            "url": f"{KA_BASE}/math/arithmetic",                       "platform": "khan",      "type": "course", "icon": "🎓"},
        {"title": "Number theory basics",  "url": "https://en.wikipedia.org/wiki/Number_theory",       "platform": "wikipedia", "type": "article","icon": "📖"},
    ],
    "Calculus": [
        {"title": "AP Calculus AB",        "url": f"{KA_BASE}/math/ap-calculus-ab",                   "platform": "khan",      "type": "course", "icon": "🎓"},
        {"title": "AP Calculus BC",        "url": f"{KA_BASE}/math/ap-calculus-bc",                   "platform": "khan",      "type": "course", "icon": "🎓"},
        {"title": "Calculus (OpenStax)",   "url": "https://openstax.org/books/calculus-volume-1/pages/1-introduction","platform":"openstax","type":"lesson","icon":"📚"},
        {"title": "Desmos Scientific Calc","url": "https://www.desmos.com/scientific",                "platform": "desmos",    "type": "tool",   "icon": "🧮"},
        {"title": "Wolfram Alpha — Derivatives","url": "https://www.wolframalpha.com/calculators/derivative-calculator/","platform":"wolfram","type":"tool","icon":"🔢"},
        {"title": "Wolfram Alpha — Integrals","url": "https://www.wolframalpha.com/calculators/integral-calculator/","platform":"wolfram","type":"tool","icon":"🔢"},
        {"title": "Calculus — Wikipedia",  "url": "https://en.wikipedia.org/wiki/Calculus",           "platform": "wikipedia", "type": "article","icon": "📖"},
    ],
    "Differential Equations": [
        {"title": "Differential Equations (Khan)","url": f"{KA_BASE}/math/differential-equations",   "platform": "khan",      "type": "course", "icon": "🎓"},
        {"title": "ODE — Wikipedia",       "url": "https://en.wikipedia.org/wiki/Ordinary_differential_equation","platform":"wikipedia","type":"article","icon":"📖"},
        {"title": "OpenStax — Calc Vol 2 (ODEs)","url": "https://openstax.org/books/calculus-volume-2/pages/1-introduction","platform":"openstax","type":"lesson","icon":"📚"},
        {"title": "Wolfram ODE Solver",    "url": "https://www.wolframalpha.com/calculators/ode-calculator/","platform":"wolfram","type":"tool","icon":"🔢"},
        {"title": "MIT OCW — 18.03 ODEs",  "url": "https://ocw.mit.edu/courses/18-03-differential-equations-spring-2010/","platform":"coursera","type":"course","icon":"🏫"},
    ],
    "Linear Algebra": [
        {"title": "Linear Algebra (Khan)", "url": f"{KA_BASE}/math/linear-algebra",                   "platform": "khan",      "type": "course", "icon": "🎓"},
        {"title": "MIT OCW — 18.06",       "url": "https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/","platform":"coursera","type":"course","icon":"🏫"},
        {"title": "Linear Algebra — Wikipedia","url": "https://en.wikipedia.org/wiki/Linear_algebra", "platform": "wikipedia", "type": "article","icon": "📖"},
        {"title": "OpenStax — Linear Algebra","url": "https://openstax.org/books/university-physics-volume-1/pages/1-introduction","platform":"openstax","type":"lesson","icon":"📚"},
        {"title": "Wolfram Matrix Calculator","url": "https://www.wolframalpha.com/calculators/matrix-calculator/","platform":"wolfram","type":"tool","icon":"🔢"},
    ],
    "Probability": [
        {"title": "Statistics & Probability (Khan)","url": f"{KA_BASE}/math/statistics-probability",  "platform": "khan",      "type": "course", "icon": "🎓"},
        {"title": "Probability — Wikipedia","url": "https://en.wikipedia.org/wiki/Probability",      "platform": "wikipedia", "type": "article","icon": "📖"},
        {"title": "OpenStax — Introductory Statistics","url": "https://openstax.org/books/introductory-statistics/pages/1-introduction","platform":"openstax","type":"lesson","icon":"📚"},
    ],
    "Statistics": [
        {"title": "AP Statistics (Khan)",  "url": f"{KA_BASE}/math/ap-statistics",                    "platform": "khan",      "type": "course", "icon": "🎓"},
        {"title": "Statistics (Khan)",     "url": f"{KA_BASE}/math/statistics-probability",           "platform": "khan",      "type": "course", "icon": "🎓"},
        {"title": "OpenStax Statistics",   "url": "https://openstax.org/books/introductory-statistics/pages/1-introduction","platform":"openstax","type":"lesson","icon":"📚"},
        {"title": "Statistics — Wikipedia","url": "https://en.wikipedia.org/wiki/Statistics",        "platform": "wikipedia", "type": "article","icon": "📖"},
    ],

    # ── SCIENCE ───────────────────────────────────────────────────────
    "Biology": [
        {"title": "Biology (Khan)",        "url": f"{KA_BASE}/science/biology",                       "platform": "khan",      "type": "course", "icon": "🎓"},
        {"title": "AP Biology (Khan)",     "url": f"{KA_BASE}/science/ap-biology",                    "platform": "khan",      "type": "course", "icon": "🎓"},
        {"title": "OpenStax Biology 2e",   "url": "https://openstax.org/books/biology-2e/pages/1-introduction","platform":"openstax","type":"lesson","icon":"📚"},
        {"title": "Cell biology — Wikipedia","url": "https://en.wikipedia.org/wiki/Cell_biology",    "platform": "wikipedia", "type": "article","icon": "📖"},
    ],
    "Chemistry": [
        {"title": "Chemistry (Khan)",      "url": f"{KA_BASE}/science/chemistry",                     "platform": "khan",      "type": "course", "icon": "🎓"},
        {"title": "AP Chemistry (Khan)",   "url": f"{KA_BASE}/science/ap-chemistry-beta",             "platform": "khan",      "type": "course", "icon": "🎓"},
        {"title": "OpenStax Chemistry 2e", "url": "https://openstax.org/books/chemistry-2e/pages/1-introduction","platform":"openstax","type":"lesson","icon":"📚"},
        {"title": "Periodic Table (Ptable)","url": "https://ptable.com",                              "platform": "wolfram",   "type": "tool",   "icon": "⚗️"},
        {"title": "Wolfram Chemistry",     "url": "https://www.wolframalpha.com/examples/science/chemistry/","platform":"wolfram","type":"tool","icon":"🔢"},
    ],
    "Physics": [
        {"title": "Physics (Khan)",        "url": f"{KA_BASE}/science/physics",                       "platform": "khan",      "type": "course", "icon": "🎓"},
        {"title": "AP Physics 1 (Khan)",   "url": f"{KA_BASE}/science/ap-physics-1",                  "platform": "khan",      "type": "course", "icon": "🎓"},
        {"title": "OpenStax University Physics","url": "https://openstax.org/books/university-physics-volume-1/pages/1-introduction","platform":"openstax","type":"lesson","icon":"📚"},
        {"title": "Physics — Wikipedia",   "url": "https://en.wikipedia.org/wiki/Physics",            "platform": "wikipedia", "type": "article","icon": "📖"},
        {"title": "Wolfram Physics",       "url": "https://www.wolframalpha.com/examples/science/physics/","platform":"wolfram","type":"tool","icon":"🔢"},
    ],
    "Earth Science": [
        {"title": "Earth & Space (Khan)",  "url": f"{KA_BASE}/science/cosmology-and-astronomy",       "platform": "khan",      "type": "course", "icon": "🎓"},
        {"title": "Earth science — Wikipedia","url": "https://en.wikipedia.org/wiki/Earth_science",  "platform": "wikipedia", "type": "article","icon": "📖"},
        {"title": "OpenStax Astronomy",    "url": "https://openstax.org/books/astronomy/pages/1-introduction","platform":"openstax","type":"lesson","icon":"📚"},
    ],

    # ── LANGUAGE ──────────────────────────────────────────────────────
    "Grammar": [
        {"title": "Grammar (Khan)",        "url": f"{KA_BASE}/humanities/grammar",                    "platform": "khan",      "type": "course", "icon": "🎓"},
        {"title": "Purdue OWL — Grammar",  "url": "https://owl.purdue.edu/owl/general_writing/grammar/index.html","platform":"coursera","type":"lesson","icon":"🏫"},
        {"title": "English grammar — Wikipedia","url": "https://en.wikipedia.org/wiki/English_grammar","platform":"wikipedia","type":"article","icon":"📖"},
    ],
    "Vocabulary": [
        {"title": "Vocabulary (Khan)",     "url": f"{KA_BASE}/humanities/grammar",                    "platform": "khan",      "type": "lesson", "icon": "🎓"},
        {"title": "Merriam-Webster",       "url": "https://www.merriam-webster.com",                  "platform": "wikipedia", "type": "tool",   "icon": "📖"},
        {"title": "Vocabulary.com",        "url": "https://www.vocabulary.com",                       "platform": "coursera",  "type": "tool",   "icon": "🏫"},
    ],
    "Literature": [
        {"title": "Reading & Language Arts (Khan)","url": f"{KA_BASE}/ela",                           "platform": "khan",      "type": "course", "icon": "🎓"},
        {"title": "Project Gutenberg",     "url": "https://www.gutenberg.org",                        "platform": "coursera",  "type": "tool",   "icon": "🏫"},
        {"title": "SparkNotes",            "url": "https://www.sparknotes.com",                       "platform": "wikipedia", "type": "article","icon": "📖"},
        {"title": "Poetry Foundation",     "url": "https://www.poetryfoundation.org",                 "platform": "coursera",  "type": "lesson", "icon": "🏫"},
    ],
    "Writing": [
        {"title": "Writing (Khan)",        "url": f"{KA_BASE}/humanities/grammar/syntax-sentences-and-clauses/v/the-essay-introduction","platform":"khan","type":"lesson","icon":"🎓"},
        {"title": "Purdue OWL",            "url": "https://owl.purdue.edu/owl/general_writing/the_writing_process/","platform":"coursera","type":"lesson","icon":"🏫"},
        {"title": "Grammarly Blog",        "url": "https://www.grammarly.com/blog/category/handbook/","platform":"coursera", "type":"lesson","icon":"🏫"},
    ],
    "Reading Comprehension": [
        {"title": "Reading (Khan)",        "url": f"{KA_BASE}/ela/cc-2nd-reading-informational-text", "platform": "khan",      "type": "lesson", "icon": "🎓"},
        {"title": "SAT Reading Prep (Khan)","url": f"{KA_BASE}/test-prep/sat/new-sat-tips-planning/x0a8c2e5f3a014af0:about-the-sat-reading-and-writing-module/a/new-sat-reading-faq","platform":"khan","type":"lesson","icon":"🎓"},
    ],

    # ── HISTORY ───────────────────────────────────────────────────────
    "American History": [
        {"title": "US History (Khan)",     "url": f"{KA_BASE}/humanities/us-history",                 "platform": "khan",      "type": "course", "icon": "🎓"},
        {"title": "AP US History (Khan)",  "url": f"{KA_BASE}/humanities/ap-us-history",              "platform": "khan",      "type": "course", "icon": "🎓"},
        {"title": "American History — Wikipedia","url": "https://en.wikipedia.org/wiki/History_of_the_United_States","platform":"wikipedia","type":"article","icon":"📖"},
        {"title": "Library of Congress",   "url": "https://www.loc.gov/classroommaterials/",          "platform": "coursera",  "type": "lesson", "icon": "🏫"},
    ],
    "World Wars": [
        {"title": "World War I (Khan)",    "url": f"{KA_BASE}/humanities/world-history/euro-hist/wwi-tutorial",  "platform": "khan", "type": "lesson", "icon": "🎓"},
        {"title": "World War II (Khan)",   "url": f"{KA_BASE}/humanities/world-history/euro-hist/wwii-summary",  "platform": "khan", "type": "lesson", "icon": "🎓"},
        {"title": "WWI — Wikipedia",       "url": "https://en.wikipedia.org/wiki/World_War_I",        "platform": "wikipedia", "type": "article","icon": "📖"},
        {"title": "WWII — Wikipedia",      "url": "https://en.wikipedia.org/wiki/World_War_II",       "platform": "wikipedia", "type": "article","icon": "📖"},
    ],
    "Ancient Civilizations": [
        {"title": "Ancient History (Khan)","url": f"{KA_BASE}/humanities/world-history",              "platform": "khan",      "type": "course", "icon": "🎓"},
        {"title": "Ancient Egypt — Wikipedia","url": "https://en.wikipedia.org/wiki/Ancient_Egypt",  "platform": "wikipedia", "type": "article","icon": "📖"},
        {"title": "Ancient Rome — Wikipedia","url": "https://en.wikipedia.org/wiki/Ancient_Rome",    "platform": "wikipedia", "type": "article","icon": "📖"},
        {"title": "Ancient Greece — Wikipedia","url": "https://en.wikipedia.org/wiki/Ancient_Greece","platform": "wikipedia", "type": "article","icon": "📖"},
    ],
    "Modern History": [
        {"title": "Modern World History (Khan)","url": f"{KA_BASE}/humanities/world-history",        "platform": "khan",      "type": "course", "icon": "🎓"},
        {"title": "Cold War — Wikipedia",  "url": "https://en.wikipedia.org/wiki/Cold_War",           "platform": "wikipedia", "type": "article","icon": "📖"},
    ],
    "World History": [
        {"title": "World History (Khan)",  "url": f"{KA_BASE}/humanities/world-history",              "platform": "khan",      "type": "course", "icon": "🎓"},
        {"title": "AP World History (Khan)","url": f"{KA_BASE}/humanities/ap-world-history",          "platform": "khan",      "type": "course", "icon": "🎓"},
    ],
    "Geography": [
        {"title": "World Geography — Wikipedia","url": "https://en.wikipedia.org/wiki/Geography",    "platform": "wikipedia", "type": "article","icon": "📖"},
        {"title": "CIA World Factbook",    "url": "https://www.cia.gov/the-world-factbook/",          "platform": "coursera",  "type": "tool",   "icon": "🏫"},
        {"title": "Google Maps",           "url": "https://maps.google.com",                          "platform": "wolfram",   "type": "tool",   "icon": "🗺️"},
    ],

    # ── COMPUTER SCIENCE ──────────────────────────────────────────────
    "Programming": [
        {"title": "Intro to Programming (Khan)","url": f"{KA_BASE}/computing/computer-programming",  "platform": "khan",      "type": "course", "icon": "🎓"},
        {"title": "Python.org Tutorial",   "url": "https://docs.python.org/3/tutorial/",              "platform": "coursera",  "type": "lesson", "icon": "🏫"},
        {"title": "freeCodeCamp",          "url": "https://www.freecodecamp.org",                     "platform": "coursera",  "type": "course", "icon": "🏫"},
        {"title": "CS50 (Harvard)",        "url": "https://cs50.harvard.edu/x/",                      "platform": "coursera",  "type": "course", "icon": "🏫"},
        {"title": "MDN Web Docs",          "url": "https://developer.mozilla.org",                    "platform": "coursera",  "type": "lesson", "icon": "🏫"},
    ],
    "Data Structures": [
        {"title": "Algorithms (Khan)",     "url": f"{KA_BASE}/computing/computer-science/algorithms", "platform": "khan",      "type": "course", "icon": "🎓"},
        {"title": "Data structures — Wikipedia","url": "https://en.wikipedia.org/wiki/Data_structure","platform":"wikipedia","type":"article","icon":"📖"},
        {"title": "Visualgo — DS Visualizer","url": "https://visualgo.net",                           "platform": "wolfram",   "type": "tool",   "icon": "🔢"},
        {"title": "GeeksForGeeks — DSA",   "url": "https://www.geeksforgeeks.org/data-structures/",  "platform": "coursera",  "type": "lesson", "icon": "🏫"},
    ],
    "Algorithms": [
        {"title": "Algorithms (Khan)",     "url": f"{KA_BASE}/computing/computer-science/algorithms", "platform": "khan",      "type": "course", "icon": "🎓"},
        {"title": "Algorithm — Wikipedia", "url": "https://en.wikipedia.org/wiki/Algorithm",          "platform": "wikipedia", "type": "article","icon": "📖"},
        {"title": "Big-O Cheat Sheet",     "url": "https://www.bigocheatsheet.com",                   "platform": "wolfram",   "type": "tool",   "icon": "🔢"},
        {"title": "MIT OCW — Algorithms",  "url": "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/","platform":"coursera","type":"course","icon":"🏫"},
    ],
    "Databases": [
        {"title": "SQL Tutorial (Khan)",   "url": f"{KA_BASE}/computing/computer-programming/sql",    "platform": "khan",      "type": "course", "icon": "🎓"},
        {"title": "SQLZoo",                "url": "https://sqlzoo.net",                                "platform": "wolfram",   "type": "tool",   "icon": "🔢"},
        {"title": "Database — Wikipedia",  "url": "https://en.wikipedia.org/wiki/Database",           "platform": "wikipedia", "type": "article","icon": "📖"},
        {"title": "SQLite Tutorial",       "url": "https://www.sqlitetutorial.net",                   "platform": "coursera",  "type": "lesson", "icon": "🏫"},
    ],
    "Networking": [
        {"title": "Internet 101 (Khan)",   "url": f"{KA_BASE}/computing/computers-and-internet",      "platform": "khan",      "type": "course", "icon": "🎓"},
        {"title": "Computer network — Wikipedia","url": "https://en.wikipedia.org/wiki/Computer_network","platform":"wikipedia","type":"article","icon":"📖"},
        {"title": "Cisco Networking Academy","url": "https://www.netacad.com",                        "platform": "coursera",  "type": "course", "icon": "🏫"},
    ],
    "Cybersecurity": [
        {"title": "Cybersecurity (Khan)",  "url": f"{KA_BASE}/computing/computers-and-internet/xcae6f4a7ff015e7d:online-data-security","platform":"khan","type":"lesson","icon":"🎓"},
        {"title": "Cybersecurity — Wikipedia","url": "https://en.wikipedia.org/wiki/Computer_security","platform":"wikipedia","type":"article","icon":"📖"},
        {"title": "OWASP Top 10",          "url": "https://owasp.org/www-project-top-ten/",           "platform": "coursera",  "type": "lesson", "icon": "🏫"},
        {"title": "TryHackMe (beginner)",  "url": "https://tryhackme.com",                            "platform": "coursera",  "type": "course", "icon": "🏫"},
    ],

    # ── ECONOMICS ─────────────────────────────────────────────────────
    "Microeconomics": [
        {"title": "Microeconomics (Khan)", "url": f"{KA_BASE}/economics-finance-domain/microeconomics","platform":"khan",       "type": "course", "icon": "🎓"},
        {"title": "AP Microeconomics (Khan)","url": f"{KA_BASE}/economics-finance-domain/ap-microeconomics","platform":"khan","type":"course","icon":"🎓"},
        {"title": "OpenStax Microeconomics","url": "https://openstax.org/books/principles-microeconomics-3e/pages/1-introduction","platform":"openstax","type":"lesson","icon":"📚"},
        {"title": "Microeconomics — Wikipedia","url": "https://en.wikipedia.org/wiki/Microeconomics", "platform": "wikipedia", "type": "article","icon": "📖"},
    ],
    "Macroeconomics": [
        {"title": "Macroeconomics (Khan)", "url": f"{KA_BASE}/economics-finance-domain/macroeconomics","platform":"khan",       "type": "course", "icon": "🎓"},
        {"title": "AP Macroeconomics (Khan)","url": f"{KA_BASE}/economics-finance-domain/ap-macroeconomics","platform":"khan","type":"course","icon":"🎓"},
        {"title": "OpenStax Macroeconomics","url": "https://openstax.org/books/principles-macroeconomics-3e/pages/1-introduction","platform":"openstax","type":"lesson","icon":"📚"},
        {"title": "Macroeconomics — Wikipedia","url": "https://en.wikipedia.org/wiki/Macroeconomics", "platform": "wikipedia", "type": "article","icon": "📖"},
    ],
    "Personal Finance": [
        {"title": "Personal Finance (Khan)","url": f"{KA_BASE}/college-careers-more/personal-finance", "platform": "khan",     "type": "course", "icon": "🎓"},
        {"title": "Investopedia",          "url": "https://www.investopedia.com",                     "platform": "wikipedia", "type": "article","icon": "📖"},
        {"title": "Consumer Finance Protection","url": "https://www.consumerfinance.gov/consumer-tools/","platform":"coursera","type":"tool","icon":"🏫"},
    ],

    # ── PSYCHOLOGY ────────────────────────────────────────────────────
    "Intro Psychology": [
        {"title": "Intro to Psychology (Khan)","url": f"{KA_BASE}/science/health-and-medicine/mental-health","platform":"khan","type":"course","icon":"🎓"},
        {"title": "OpenStax Psychology 2e","url": "https://openstax.org/books/psychology-2e/pages/1-introduction","platform":"openstax","type":"lesson","icon":"📚"},
        {"title": "Psychology — Wikipedia","url": "https://en.wikipedia.org/wiki/Psychology",         "platform": "wikipedia", "type": "article","icon": "📖"},
        {"title": "Crash Course Psychology","url": "https://www.youtube.com/playlist?list=PL8dPuuaLjXtOPRKzVLY0jJY-uHOH9KVU6","platform":"youtube","type":"video","icon":"▶️"},
    ],
    "Cognitive Psychology": [
        {"title": "Cognitive psychology — Wikipedia","url": "https://en.wikipedia.org/wiki/Cognitive_psychology","platform":"wikipedia","type":"article","icon":"📖"},
        {"title": "OpenStax — Thinking & Intelligence","url": "https://openstax.org/books/psychology-2e/pages/7-introduction","platform":"openstax","type":"lesson","icon":"📚"},
        {"title": "MIT OCW — Cognitive Science","url": "https://ocw.mit.edu/courses/9-00sc-introduction-to-psychology-fall-2011/","platform":"coursera","type":"course","icon":"🏫"},
    ],
    "Developmental Psychology": [
        {"title": "Developmental psychology — Wikipedia","url": "https://en.wikipedia.org/wiki/Developmental_psychology","platform":"wikipedia","type":"article","icon":"📖"},
        {"title": "OpenStax — Lifespan Development","url": "https://openstax.org/books/psychology-2e/pages/9-introduction","platform":"openstax","type":"lesson","icon":"📚"},
        {"title": "Crash Course — Developmental Psych","url": "https://www.youtube.com/watch?v=hxesHCOlmXU","platform":"youtube","type":"video","icon":"▶️"},
    ],
}

# ── Subject-level resources (shown on subject pages) ──────────────────
SUBJECT_RESOURCES = {
    "Math": [
        {"title": "Khan Academy Math",     "url": f"{KA_BASE}/math",                                  "platform": "khan",      "type": "course", "icon": "🎓"},
        {"title": "Wolfram MathWorld",     "url": "https://mathworld.wolfram.com",                    "platform": "wolfram",   "type": "article","icon": "🔢"},
        {"title": "Desmos Calculator",     "url": "https://www.desmos.com/calculator",                "platform": "desmos",    "type": "tool",   "icon": "🧮"},
        {"title": "OpenStax Math",         "url": "https://openstax.org/subjects/math",               "platform": "openstax",  "type": "course", "icon": "📚"},
        {"title": "Paul's Online Math Notes","url": "https://tutorial.math.lamar.edu",               "platform": "coursera",  "type": "lesson", "icon": "🏫"},
        {"title": "MIT OCW Mathematics",   "url": "https://ocw.mit.edu/courses/mathematics/",         "platform": "coursera",  "type": "course", "icon": "🏫"},
    ],
    "Science": [
        {"title": "Khan Academy Science",  "url": f"{KA_BASE}/science",                               "platform": "khan",      "type": "course", "icon": "🎓"},
        {"title": "OpenStax Science",      "url": "https://openstax.org/subjects/science",            "platform": "openstax",  "type": "course", "icon": "📚"},
        {"title": "PhET Interactive Simulations","url": "https://phet.colorado.edu",                  "platform": "wolfram",   "type": "tool",   "icon": "🔢"},
        {"title": "CK-12 Science",         "url": "https://www.ck12.org/science/",                   "platform": "coursera",  "type": "course", "icon": "🏫"},
    ],
    "Language": [
        {"title": "Khan Academy ELA",      "url": f"{KA_BASE}/ela",                                   "platform": "khan",      "type": "course", "icon": "🎓"},
        {"title": "Purdue OWL",            "url": "https://owl.purdue.edu",                           "platform": "coursera",  "type": "lesson", "icon": "🏫"},
        {"title": "Project Gutenberg",     "url": "https://www.gutenberg.org",                        "platform": "coursera",  "type": "tool",   "icon": "🏫"},
        {"title": "Merriam-Webster",       "url": "https://www.merriam-webster.com",                  "platform": "wikipedia", "type": "tool",   "icon": "📖"},
    ],
    "History": [
        {"title": "Khan Academy History",  "url": f"{KA_BASE}/humanities",                            "platform": "khan",      "type": "course", "icon": "🎓"},
        {"title": "World History Encyclopedia","url": "https://www.worldhistory.org",                 "platform": "wikipedia", "type": "article","icon": "📖"},
        {"title": "Library of Congress",   "url": "https://www.loc.gov/classroommaterials/",          "platform": "coursera",  "type": "lesson", "icon": "🏫"},
        {"title": "History Channel",       "url": "https://www.history.com",                          "platform": "coursera",  "type": "lesson", "icon": "🏫"},
    ],
    "Computer Science": [
        {"title": "Khan Academy Computing","url": f"{KA_BASE}/computing",                             "platform": "khan",      "type": "course", "icon": "🎓"},
        {"title": "CS50 (Harvard/edX)",    "url": "https://cs50.harvard.edu/x/",                      "platform": "coursera",  "type": "course", "icon": "🏫"},
        {"title": "freeCodeCamp",          "url": "https://www.freecodecamp.org",                     "platform": "coursera",  "type": "course", "icon": "🏫"},
        {"title": "MIT OCW Computer Science","url": "https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/","platform":"coursera","type":"course","icon":"🏫"},
        {"title": "The Odin Project",      "url": "https://www.theodinproject.com",                   "platform": "coursera",  "type": "course", "icon": "🏫"},
    ],
    "Economics": [
        {"title": "Khan Academy Economics","url": f"{KA_BASE}/economics-finance-domain",              "platform": "khan",      "type": "course", "icon": "🎓"},
        {"title": "OpenStax Economics",    "url": "https://openstax.org/subjects/social-sciences",    "platform": "openstax",  "type": "course", "icon": "📚"},
        {"title": "Investopedia",          "url": "https://www.investopedia.com",                     "platform": "wikipedia", "type": "article","icon": "📖"},
        {"title": "Econlib",               "url": "https://www.econlib.org",                          "platform": "coursera",  "type": "lesson", "icon": "🏫"},
    ],
    "Psychology": [
        {"title": "Khan Academy Psychology","url": f"{KA_BASE}/science/health-and-medicine",          "platform": "khan",      "type": "course", "icon": "🎓"},
        {"title": "OpenStax Psychology",   "url": "https://openstax.org/books/psychology-2e/pages/1-introduction","platform":"openstax","type":"course","icon":"📚"},
        {"title": "APA Psychology Resources","url": "https://www.apa.org/topics",                    "platform": "coursera",  "type": "lesson", "icon": "🏫"},
        {"title": "Crash Course Psychology","url": "https://www.youtube.com/playlist?list=PL8dPuuaLjXtOPRKzVLY0jJY-uHOH9KVU6","platform":"youtube","type":"video","icon":"▶️"},
    ],
}

# ── Platform metadata ──────────────────────────────────────────────────
PLATFORMS = {
    "khan":      {"name": "Khan Academy",   "icon": "🎓", "color": "#14BF96", "bg": "rgba(20,191,150,.12)", "border": "rgba(20,191,150,.25)"},
    "youtube":   {"name": "YouTube",        "icon": "▶️",  "color": "#FF0000", "bg": "rgba(255,0,0,.10)",     "border": "rgba(255,0,0,.2)"},
    "wikipedia": {"name": "Wikipedia",      "icon": "📖",  "color": "#94a3b8", "bg": "rgba(148,163,184,.10)", "border": "rgba(148,163,184,.2)"},
    "openstax":  {"name": "OpenStax",       "icon": "📚",  "color": "#EC6B2D", "bg": "rgba(236,107,45,.12)",  "border": "rgba(236,107,45,.25)"},
    "desmos":    {"name": "Desmos",         "icon": "🧮",  "color": "#6B4FBB", "bg": "rgba(107,79,187,.12)",  "border": "rgba(107,79,187,.25)"},
    "wolfram":   {"name": "Wolfram Alpha",  "icon": "🔢",  "color": "#FF6600", "bg": "rgba(255,102,0,.12)",   "border": "rgba(255,102,0,.25)"},
    "coursera":  {"name": "External",       "icon": "🏫",  "color": "#6366f1", "bg": "rgba(99,102,241,.12)",  "border": "rgba(99,102,241,.25)"},
}

def get_resources_for_topic(subject: str, topic: str) -> list:
    """Return resources for a specific topic, falling back to subject resources."""
    resources = TOPIC_RESOURCES.get(topic, [])
    if not resources:
        resources = SUBJECT_RESOURCES.get(subject, [])
    return resources[:6]  # cap at 6

def get_resources_for_subject(subject: str) -> list:
    """Return top subject-level resources."""
    return SUBJECT_RESOURCES.get(subject, [])

def get_all_topic_resources(subject: str, topic: str) -> list:
    """Return combined topic + subject resources, deduplicated."""
    seen = set()
    result = []
    for r in TOPIC_RESOURCES.get(topic, []) + SUBJECT_RESOURCES.get(subject, []):
        if r["url"] not in seen:
            seen.add(r["url"])
            result.append(r)
    return result[:8]
