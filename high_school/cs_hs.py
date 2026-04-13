"""
High School Computer Science Generator (Grades 9–12)
Covers: Programming Fundamentals, Algorithms, Data Structures,
        Web Development, Cybersecurity, AP CS concepts
"""
import random
import json

def _q(topic, diff, question, choices, answer_idx, explanation, grade=10):
    return ('Computer Science', topic, diff, question, json.dumps(choices), answer_idx, explanation, grade)

def _shuffle_choices(correct, wrongs, rng):
    choices = list(rng.sample(wrongs, min(3, len(wrongs))))
    idx = rng.randint(0, min(3, len(choices)))
    choices.insert(idx, correct)
    return choices[:4], idx


def gen_programming_basics(n=40, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What is a variable?", "A named storage location that holds a value",
         ["A type of loop", "A mathematical operation", "A function that returns a value"],
         "Variables store data values and can be changed during program execution.", 'easy', 9),
        ("What is the output of: print(10 % 3) in Python?",
         "1", ["3", "0", "10"],
         "% is the modulo operator: 10 ÷ 3 = 3 remainder 1.", 'easy', 9),
        ("What is a boolean?", "A data type with only two values: True or False",
         ["A number between 0 and 1", "A type of loop", "A function that returns a string"],
         "Booleans represent logical values and are used in conditions.", 'easy', 9),
        ("What does the following Python code output?\nfor i in range(3):\n    print(i)",
         "0\n1\n2",
         ["1\n2\n3", "0\n1\n2\n3", "1\n2"],
         "range(3) generates 0, 1, 2. range starts at 0 by default.", 'easy', 9),
        ("What is a function?",
         "A reusable block of code that performs a specific task",
         ["A type of variable", "A loop structure", "A data type"],
         "Functions encapsulate logic, allow reuse, and can accept inputs (parameters) and return outputs.", 'easy', 9),
        ("What is recursion?",
         "When a function calls itself",
         ["When a loop runs forever", "When two functions call each other",
          "When a program restarts"],
         "Recursive functions call themselves with a smaller input until reaching a base case.", 'medium', 10),
        ("What is the difference between a compiled and interpreted language?",
         "Compiled languages translate to machine code before running; interpreted translate at runtime",
         ["Interpreted languages are always faster",
          "Compiled languages can only run on one operating system",
          "They are the same"],
         "C/C++ are compiled; Python/JavaScript are interpreted. Compiled is generally faster.", 'medium', 11),
        ("What does 'int' stand for in programming?", "Integer — a whole number data type",
         ["Internal variable", "Interactive", "Interpolation"],
         "int stores whole numbers (no decimal). float stores decimals.", 'easy', 9),
        ("What is the purpose of a return statement?",
         "To send a value back from a function to the caller",
         ["To end a loop", "To print a value", "To define a variable"],
         "return exits the function and passes a value back to where the function was called.", 'easy', 9),
        ("What is the difference between == and = in code?",
         "= assigns a value; == compares two values",
         ["They are the same", "== assigns; = compares",
          "= is for strings; == is for numbers"],
         "x = 5 assigns 5 to x. x == 5 checks if x is equal to 5.", 'easy', 9),
        ("What is object-oriented programming (OOP)?",
         "A programming paradigm using objects that combine data and behavior",
         ["Programming that uses only functions",
          "Programming without variables",
          "A type of assembly language"],
         "OOP organizes code into classes (blueprints) and objects (instances) with attributes and methods.", 'medium', 11),
        ("What is inheritance in OOP?",
         "When a class derives properties and methods from another class",
         ["When two objects share memory", "When a function is called multiple times",
          "When variables are declared globally"],
         "Inheritance lets a subclass reuse code from a parent class, enabling code reuse.", 'medium', 11),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Programming Fundamentals', diff, q_text, choices, idx,
                     f"Correct: {ans}.", grade))
    return qs


def gen_algorithms_ds(n=40, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What is the time complexity of binary search?",
         "O(log n)", ["O(n)", "O(n²)", "O(1)"],
         "Binary search halves the search space each step → O(log n).", 'hard', 12),
        ("What is the time complexity of bubble sort in the worst case?",
         "O(n²)", ["O(n log n)", "O(n)", "O(log n)"],
         "Bubble sort compares each element with every other → O(n²).", 'medium', 11),
        ("What data structure operates on LIFO (Last In, First Out)?",
         "Stack", ["Queue", "Array", "Linked List"],
         "Stacks: push adds to top, pop removes from top. LIFO = Last In, First Out.", 'medium', 10),
        ("What data structure operates on FIFO (First In, First Out)?",
         "Queue", ["Stack", "Tree", "Hash Table"],
         "Queues: enqueue adds to back, dequeue removes from front. FIFO.", 'medium', 10),
        ("What is a hash table?",
         "A data structure that maps keys to values using a hash function",
         ["A sorted list of values", "A type of tree", "A linked list with sorted nodes"],
         "Hash tables provide O(1) average lookup by mapping keys to array indices via hashing.", 'hard', 12),
        ("What is the difference between an array and a linked list?",
         "Arrays have fixed-size contiguous memory; linked lists use pointers to connect nodes",
         ["Arrays are slower for lookup", "Linked lists have O(1) random access",
          "Arrays can only store numbers"],
         "Arrays: fast lookup (O(1)), slow insert/delete. Linked lists: fast insert/delete, slow lookup (O(n)).", 'hard', 12),
        ("What is a binary tree?",
         "A tree where each node has at most two children",
         ["A tree with exactly two levels", "A tree that only stores numbers",
          "A sorted list"],
         "Binary trees have at most 2 children per node (left and right).", 'medium', 11),
        ("What does 'O(1)' mean?",
         "Constant time — the operation takes the same time regardless of input size",
         ["The operation takes 1 second", "Linear time",
          "The operation uses 1 unit of memory"],
         "Big O notation describes how runtime scales. O(1) = constant, O(n) = linear.", 'medium', 11),
        ("What is the purpose of a sorting algorithm?",
         "To arrange elements in a specific order",
         ["To search for a specific element", "To insert elements efficiently",
          "To remove duplicates from a list"],
         "Sorting algorithms (merge sort, quick sort, etc.) arrange data for efficient searching.", 'easy', 10),
        ("What is recursion's base case?",
         "The condition that stops the recursive calls",
         ["The first recursive call", "The return value of the function",
          "The parameter of the function"],
         "Without a base case, recursion continues infinitely, causing a stack overflow.", 'medium', 11),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Algorithms & Data Structures', diff, q_text, choices, idx,
                     f"Correct: {ans}.", grade))
    return qs


def gen_web_dev_basics(n=30, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What does HTML stand for?",
         "HyperText Markup Language",
         ["High Transfer Markup Language", "HyperText Machine Language",
          "HyperTransfer Markup Language"],
         "HTML is the standard language for structuring web pages.", 'easy', 9),
        ("What does CSS stand for?",
         "Cascading Style Sheets",
         ["Computer Style Sheets", "Creative Style Sheets", "Cascading Standard Scripts"],
         "CSS controls the visual presentation (colors, fonts, layout) of HTML elements.", 'easy', 9),
        ("What is the purpose of JavaScript in web development?",
         "To add interactivity and dynamic behavior to web pages",
         ["To structure web page content", "To style web pages",
          "To store data on a server"],
         "HTML = structure, CSS = style, JavaScript = behavior/interactivity.", 'easy', 9),
        ("What is a URL?", "Uniform Resource Locator — the address of a web resource",
         ["Universal Rendering Language", "User Resource Link",
          "Unified Remote Location"],
         "URLs identify the location of web pages and other resources on the internet.", 'easy', 9),
        ("What is the difference between GET and POST HTTP methods?",
         "GET retrieves data; POST submits data to be processed",
         ["POST retrieves; GET submits", "They are the same",
          "GET is for images; POST is for text"],
         "GET appends data to URL; POST sends data in request body (more secure for sensitive data).", 'medium', 11),
        ("What is a responsive web design?",
         "A design that adapts to different screen sizes",
         ["A design that responds quickly to clicks", "A design with animations",
          "A design for mobile phones only"],
         "Responsive design uses CSS media queries to adjust layout for phones, tablets, and desktops.", 'medium', 10),
        ("What is a server-side language?",
         "A language that runs on the web server, not in the browser",
         ["A language that only works on smartphones",
          "Any language used in web development",
          "A language that runs in the browser"],
         "Python, Node.js, PHP run on servers. JavaScript runs in browsers (client-side).", 'medium', 11),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Web Development', diff, q_text, choices, idx,
                     f"Correct: {ans}.", grade))
    return qs


def gen_cybersecurity_basics(n=25, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What is phishing?",
         "A social engineering attack to trick users into revealing sensitive information",
         ["A type of software virus", "Unauthorized access to a network",
          "Flooding a server with requests"],
         "Phishing uses deceptive emails/sites to steal passwords, credit cards, etc.", 'easy', 10),
        ("What is encryption?",
         "The process of converting data into an unreadable format without a key",
         ["Compressing files", "Backing up data", "Scanning for viruses"],
         "Encryption protects data so only authorized parties with the key can read it.", 'medium', 10),
        ("What is a firewall?",
         "A security system that monitors and controls incoming/outgoing network traffic",
         ["A type of antivirus software", "A hardware device that stores data",
          "A program that speeds up internet connections"],
         "Firewalls filter traffic based on security rules, blocking unauthorized access.", 'medium', 10),
        ("What is two-factor authentication (2FA)?",
         "Using two verification methods to confirm identity",
         ["Changing your password twice", "Using a very long password",
          "Logging in from two devices simultaneously"],
         "2FA requires something you know (password) + something you have (phone/token).", 'easy', 10),
        ("What is malware?",
         "Software designed to damage or gain unauthorized access to systems",
         ["A type of programming language", "A secure encryption protocol",
          "A network monitoring tool"],
         "Malware includes viruses, worms, ransomware, spyware, and trojans.", 'easy', 9),
        ("What does HTTPS indicate about a website?",
         "The connection is encrypted using TLS/SSL",
         ["The website is government-owned", "The website loads faster",
          "The website has been verified as safe"],
         "HTTPS = HTTP + TLS encryption. The 'S' means the data is encrypted in transit.", 'medium', 10),
        ("What is a SQL injection attack?",
         "Inserting malicious SQL code into a query to manipulate a database",
         ["A type of phishing attack", "A denial of service attack",
          "Stealing encrypted passwords"],
         "SQL injection exploits unvalidated input to run unauthorized database commands.", 'hard', 12),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Cybersecurity', diff, q_text, choices, idx,
                     f"Correct: {ans}.", grade))
    return qs


_TOPIC_GENERATORS = {
    'Programming Fundamentals':    [(gen_programming_basics, {})],
    'Algorithms & Data Structures': [(gen_algorithms_ds, {})],
    'Web Development':             [(gen_web_dev_basics, {})],
    'Cybersecurity':               [(gen_cybersecurity_basics, {})],
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
