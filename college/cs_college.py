"""
College Computer Science Generator
Covers: Data Structures, Algorithms, Databases, Operating Systems,
        Networking, Theory of Computation, Software Engineering
"""
import random
import json

def _q(topic, diff, question, choices, answer_idx, explanation, grade=13):
    return ('Computer Science', topic, diff, question, json.dumps(choices), answer_idx, explanation, grade)

def _shuffle_choices(correct, wrongs, rng):
    choices = list(rng.sample(wrongs, min(3, len(wrongs))))
    idx = rng.randint(0, min(3, len(choices)))
    choices.insert(idx, correct)
    return choices[:4], idx


def gen_data_structures_college(n=40, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What is the time complexity of inserting into a balanced BST?",
         "O(log n)", ["O(n)", "O(1)", "O(n log n)"],
         "Balanced BSTs (AVL, Red-Black) maintain height O(log n) → insertion is O(log n).", 'medium', 13),
        ("What is a heap?",
         "A complete binary tree satisfying the heap property (parent ≥ or ≤ children)",
         ["A sorted array", "A linked list with sorted nodes", "A type of hash table"],
         "Max-heap: parent ≥ children. Min-heap: parent ≤ children. Used in priority queues.", 'medium', 13),
        ("What is the time complexity of heapify (building a heap from an array)?",
         "O(n)", ["O(n log n)", "O(log n)", "O(n²)"],
         "Building a heap is O(n) — more efficient than inserting n elements one at a time.", 'hard', 14),
        ("What is a red-black tree?",
         "A self-balancing BST where nodes are colored red or black to maintain balance",
         ["A BST sorted by color", "A tree with at most 2 red nodes",
          "A hash table using colors for collision resolution"],
         "Red-black trees guarantee O(log n) operations by enforcing color-based balance rules.", 'hard', 14),
        ("What is a trie (prefix tree)?",
         "A tree structure for storing strings, where each edge represents a character",
         ["A balanced BST for integers", "A hash map with string keys",
          "A graph for string matching"],
         "Tries support O(m) lookup (m = string length), ideal for prefix searches.", 'hard', 14),
        ("What is a graph's adjacency matrix vs adjacency list?",
         "Matrix: O(V²) space, O(1) edge lookup; List: O(V+E) space, O(degree) edge lookup",
         ["Both use O(V²) space", "List is always better than matrix",
          "Matrix only works for directed graphs"],
         "Matrix: dense graphs. List: sparse graphs (more common in practice).", 'hard', 15),
        ("What is amortized analysis?",
         "Analyzing the average cost per operation over a sequence of operations",
         ["Worst-case analysis", "Analysis of recursive algorithms",
          "Comparing two algorithms"],
         "Amortized analysis gives a tighter bound when expensive operations are rare.", 'hard', 15),
        ("What is the difference between DFS and BFS?",
         "DFS uses a stack (goes deep); BFS uses a queue (explores level by level)",
         ["DFS is always faster", "BFS uses more memory than DFS always",
          "They always produce the same traversal order"],
         "DFS: stack/recursion, explores far first. BFS: queue, finds shortest path in unweighted graphs.", 'medium', 13),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Data Structures', diff, q_text, choices, idx,
                     f"Correct: {ans}.", grade))
    return qs


def gen_algorithms_college(n=40, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What is the time complexity of merge sort?",
         "O(n log n) in all cases",
         ["O(n²)", "O(n)", "O(log n)"],
         "Merge sort divides in half (log n levels) and merges (n per level) → O(n log n).", 'medium', 13),
        ("What is dynamic programming?",
         "Breaking a problem into overlapping subproblems and storing solutions to avoid recomputation",
         ["A recursive algorithm", "An algorithm that uses graphs",
          "A brute-force search algorithm"],
         "DP uses memoization or tabulation to solve overlapping subproblems efficiently.", 'hard', 14),
        ("What is the greedy algorithm approach?",
         "Making the locally optimal choice at each step, hoping to reach a global optimum",
         ["Trying all possible solutions", "Using dynamic programming",
          "Dividing the problem in half"],
         "Greedy works when locally optimal choices lead to global optimum (e.g., Dijkstra's, Huffman coding).", 'medium', 13),
        ("What does P vs NP ask?",
         "Whether every problem whose solution can be verified in polynomial time can also be solved in polynomial time",
         ["Whether all sorting algorithms are equivalent",
          "Whether fast computers can solve all problems",
          "Whether NP-hard problems are unsolvable"],
         "P = solvable in poly time. NP = verifiable in poly time. P = NP? Unknown — one of the greatest open problems.", 'hard', 15),
        ("What is an NP-complete problem?",
         "A problem in NP that every other NP problem can be reduced to in polynomial time",
         ["Any problem that is unsolvable", "A problem solvable only with exponential memory",
          "The hardest problem in P"],
         "NP-complete problems are the hardest in NP; if any has a poly-time solution, all NP problems do.", 'hard', 15),
        ("What is Dijkstra's algorithm used for?",
         "Finding shortest paths in a weighted graph with non-negative weights",
         ["Finding minimum spanning trees", "Topological sorting",
          "Finding all-pairs shortest paths"],
         "Dijkstra's: greedy BFS variant using a priority queue, O((V+E) log V) with a binary heap.", 'hard', 14),
        ("What is a divide-and-conquer algorithm?",
         "An algorithm that divides the problem into smaller subproblems, solves them, and combines",
         ["An algorithm that tests all solutions",
          "An algorithm that solves problems from bottom up",
          "An algorithm that uses graphs"],
         "Classic examples: merge sort, quick sort, binary search, Strassen's matrix multiplication.", 'medium', 13),
        ("What is the Floyd-Warshall algorithm?",
         "An algorithm for finding all-pairs shortest paths in a weighted graph",
         ["An algorithm for finding minimum spanning trees",
          "A single-source shortest path algorithm",
          "An algorithm for topological sorting"],
         "Floyd-Warshall: O(V³) DP algorithm for all-pairs shortest paths, handles negative edges.", 'hard', 15),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Algorithms', diff, q_text, choices, idx,
                     f"Correct: {ans}.", grade))
    return qs


def gen_databases(n=35, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What does SQL stand for?",
         "Structured Query Language",
         ["Structured Question Language", "Standard Query Logic",
          "Sequential Query Language"],
         "SQL is the standard language for managing relational databases.", 'easy', 13),
        ("What is a primary key?",
         "A column (or set of columns) that uniquely identifies each row in a table",
         ["The first column in a table", "A column that can contain NULL values",
          "A foreign key from another table"],
         "Primary keys enforce uniqueness and are not NULL.", 'easy', 13),
        ("What is a foreign key?",
         "A column that references the primary key of another table",
         ["The most important column in a table",
          "A column that stores unique values",
          "A type of index"],
         "Foreign keys establish relationships between tables and enforce referential integrity.", 'medium', 13),
        ("What is normalization in database design?",
         "Organizing data to reduce redundancy and improve integrity",
         ["Making queries run faster", "Adding indexes to a database",
          "Backing up a database"],
         "Normal forms (1NF, 2NF, 3NF, BCNF) progressively reduce data redundancy.", 'medium', 14),
        ("What does ACID stand for in database transactions?",
         "Atomicity, Consistency, Isolation, Durability",
         ["Accuracy, Completeness, Integrity, Durability",
          "Atomicity, Concurrency, Isolation, Durability",
          "Accuracy, Consistency, Integrity, Dependability"],
         "ACID properties ensure reliable database transactions.", 'hard', 14),
        ("What is the difference between SQL and NoSQL databases?",
         "SQL is relational with fixed schema; NoSQL is non-relational with flexible schema",
         ["NoSQL is always faster", "SQL can't handle large data",
          "They are the same with different names"],
         "Relational DBs (MySQL, PostgreSQL) use tables. NoSQL (MongoDB, Redis) use documents/key-value/etc.", 'medium', 14),
        ("What is an index in a database?",
         "A data structure that speeds up data retrieval operations",
         ["A list of all tables", "The primary key column",
          "A backup of the database"],
         "Indexes (often B-trees) allow O(log n) lookup instead of O(n) full table scans.", 'medium', 13),
        ("What is a JOIN in SQL?",
         "Combining rows from two or more tables based on a related column",
         ["Adding a new column to a table", "Merging two databases",
          "Copying a table to another database"],
         "INNER JOIN returns matching rows. LEFT JOIN includes all left table rows.", 'medium', 13),
        ("What is a transaction?",
         "A sequence of operations treated as a single unit — either all succeed or all fail",
         ["A single SQL query", "A database backup", "A connection to a database"],
         "Transactions use BEGIN, COMMIT, ROLLBACK to ensure ACID properties.", 'medium', 14),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Databases', diff, q_text, choices, idx,
                     f"Correct: {ans}.", grade))
    return qs


def gen_operating_systems(n=35, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What is a process?",
         "A program in execution with its own memory and resources",
         ["A stored program on disk", "A function call", "A hardware component"],
         "Processes are isolated execution environments managed by the OS.", 'easy', 13),
        ("What is a thread?",
         "A lightweight unit of execution within a process, sharing the process's memory",
         ["A separate process", "A type of file", "An OS interrupt"],
         "Threads share memory within a process — lighter than processes, but need synchronization.", 'medium', 13),
        ("What is deadlock?",
         "A state where processes wait indefinitely for resources held by each other",
         ["When a process uses too much CPU",
          "When memory is full",
          "When two processes run simultaneously"],
         "Deadlock: Process A holds R1, waits for R2; Process B holds R2, waits for R1. Circular wait.", 'hard', 14),
        ("What is virtual memory?",
         "An abstraction allowing processes to use more memory than physically available",
         ["Memory that doesn't physically exist",
          "RAM that is very fast",
          "Memory allocated at compile time"],
         "Virtual memory uses disk as extended RAM, with pages swapped in/out as needed.", 'medium', 14),
        ("What is paging in an OS?",
         "Dividing memory into fixed-size blocks (pages) mapped between virtual and physical address",
         ["Splitting a program into multiple files",
          "Sending data over a network in packets",
          "Loading a program from disk"],
         "Paging avoids external fragmentation by mapping virtual pages to physical frames.", 'hard', 14),
        ("What is a mutex?",
         "A mutual exclusion lock preventing multiple threads from accessing a resource simultaneously",
         ["A type of process scheduler", "A memory allocation method",
          "A network protocol"],
         "Mutexes ensure only one thread at a time enters a critical section.", 'medium', 14),
        ("What is the difference between preemptive and cooperative scheduling?",
         "Preemptive: OS can interrupt processes; Cooperative: processes voluntarily yield",
         ["Cooperative is more efficient for all cases",
          "Preemptive is only for single-core systems",
          "They are the same in modern OSes"],
         "Modern OSes use preemptive scheduling to prevent any one process from monopolizing CPU.", 'hard', 15),
        ("What is the purpose of a cache?",
         "A fast, small memory that stores frequently accessed data to reduce access time",
         ["Permanent storage for programs", "Extended RAM",
          "A type of hard drive"],
         "Cache (L1/L2/L3) exploits locality of reference to bridge the CPU-RAM speed gap.", 'medium', 13),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Operating Systems', diff, q_text, choices, idx,
                     f"Correct: {ans}.", grade))
    return qs


def gen_networking(n=30, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What does TCP/IP stand for?",
         "Transmission Control Protocol / Internet Protocol",
         ["Transfer Control Protocol / Internet Protocol",
          "Transmission Communication Protocol / IP",
          "Technical Control Protocol / Internet Program"],
         "TCP/IP is the foundational communication protocol of the internet.", 'easy', 13),
        ("What is the difference between TCP and UDP?",
         "TCP is reliable with handshaking; UDP is fast but unreliable (no guarantee of delivery)",
         ["UDP is more reliable than TCP", "They are identical",
          "TCP is faster than UDP"],
         "TCP: connection-oriented, ordered, error-checked. UDP: connectionless, lower overhead.", 'medium', 13),
        ("What is DNS?",
         "Domain Name System — translates domain names to IP addresses",
         ["A type of encryption", "A file transfer protocol",
          "A web server software"],
         "DNS resolves 'google.com' to its IP address.", 'easy', 13),
        ("What is an IP address?",
         "A numerical label identifying a device on a network",
         ["A website URL", "A type of network cable",
          "A domain name"],
         "IPv4: 4 octets (e.g., 192.168.1.1). IPv6: 128-bit hex address.", 'easy', 13),
        ("What is the OSI model?",
         "A 7-layer conceptual framework for network communication",
         ["An internet protocol", "A type of hardware",
          "A programming language for networks"],
         "OSI layers: Physical, Data Link, Network, Transport, Session, Presentation, Application.", 'medium', 14),
        ("What is a subnet mask?",
         "A mask that separates the network portion and host portion of an IP address",
         ["A firewall rule", "An encryption key",
          "A domain name extension"],
         "E.g., 255.255.255.0 means first 3 octets = network, last = host.", 'hard', 14),
        ("What is HTTP vs HTTPS?",
         "HTTP is unencrypted; HTTPS uses TLS encryption for secure communication",
         ["They are the same protocol", "HTTPS is always slower",
          "HTTP is more secure than HTTPS"],
         "HTTPS adds TLS/SSL encryption, protecting data in transit.", 'medium', 13),
        ("What is latency in networking?",
         "The time delay between sending and receiving data",
         ["The speed of data transfer", "The number of packets lost",
          "The size of a network"],
         "Latency (measured in ms) affects real-time applications like video calls and gaming.", 'easy', 13),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Networking', diff, q_text, choices, idx,
                     f"Correct: {ans}.", grade))
    return qs


def gen_theory_of_computation(n=30, seed=None):
    r = random.Random(seed)
    qs_pool = [
        ("What is a Turing machine?",
         "A theoretical model of computation with infinite tape and a set of rules",
         ["An early physical computer", "A type of algorithm",
          "A programming language"],
         "Turing machines define what is computable — the foundation of computational theory.", 'medium', 14),
        ("What is the halting problem?",
         "The problem of determining whether a program will halt or run forever — undecidable",
         ["Finding the fastest algorithm", "Deciding if a program is correct",
          "Sorting a list of programs"],
         "Turing proved the halting problem is undecidable — no algorithm can solve it in general.", 'hard', 15),
        ("What is a regular language?",
         "A language that can be recognized by a finite automaton (DFA or NFA)",
         ["Any language a computer can process",
          "A language with only regular expressions",
          "A context-free language"],
         "Regular languages are the simplest in the Chomsky hierarchy, recognized by finite automata.", 'medium', 14),
        ("What does NFA stand for?",
         "Nondeterministic Finite Automaton",
         ["Normalized Finite Algorithm", "Nondeterministic Function Array",
          "New Formal Automaton"],
         "NFAs can be in multiple states simultaneously; equivalent to DFAs in expressive power.", 'medium', 14),
        ("What is a context-free grammar?",
         "A formal grammar where each production rule has a single nonterminal on the left side",
         ["A grammar with no rules", "A grammar for natural language only",
          "A grammar recognized by finite automata"],
         "CFGs generate context-free languages (CFL), used in programming language parsers.", 'hard', 15),
        ("What is the Church-Turing thesis?",
         "Any effectively computable function can be computed by a Turing machine",
         ["All problems can be solved by computers",
          "Church invented the Turing machine",
          "Quantum computers are more powerful than Turing machines"],
         "The thesis equates effective computation with Turing machine computability.", 'hard', 16),
        ("What is a pushdown automaton?",
         "A finite automaton with an additional stack memory",
         ["A Turing machine without infinite tape",
          "A DFA with extra states",
          "A nondeterministic Turing machine"],
         "PDAs recognize context-free languages — the stack allows matching brackets and recursion.", 'hard', 15),
    ]
    qs = []
    for _ in range(n):
        q_text, ans, wrongs, diff, grade = r.choice(qs_pool)
        choices, idx = _shuffle_choices(ans, r.sample(wrongs, min(3, len(wrongs))), r)
        qs.append(_q('Theory of Computation', diff, q_text, choices, idx,
                     f"Correct: {ans}.", grade))
    return qs


_TOPIC_GENERATORS = {
    'Data Structures':       [(gen_data_structures_college, {})],
    'Algorithms':            [(gen_algorithms_college, {})],
    'Databases':             [(gen_databases, {})],
    'Operating Systems':     [(gen_operating_systems, {})],
    'Networking':            [(gen_networking, {})],
    'Theory of Computation': [(gen_theory_of_computation, {})],
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
