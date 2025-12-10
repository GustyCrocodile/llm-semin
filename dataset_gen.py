import json
import random
import re

# ==========================================
# 1. LINGUISTIC DATA & CONSTANTS
# ==========================================

# Common Latvian Lemmas for realistic lexical generation
NOUNS = [
    "māja", "koks", "sun", "galds", "laiks", "ceļš", "draugs", "darbs", 
    "rīga", "jūra", "mežs", "skola", "valsts", "cilvēks", "bērns", "dzīve"
]
VERBS = [
    "būt", "iet", "darīt", "redzēt", "zināt", "gribēt", "varēt", "nākt", 
    "ņemt", "dot", "runāt", "meklēt", "saukt", "kļūt", "palikt"
]
ADJECTIVES = [
    "labs", "liels", "jauns", "balts", "melns", "skaists", "garš", "vecs", 
    "mazs", "augsts", "zems", "sarkans", "zaļš", "gudrs", "stiprs"
]
PREPOSITIONS = ["uz", "pie", "no", "ar", "par", "bez", "pēc"]

# LIMA v2.2.2 Tagset Mappings
# Mapping Latvian NL terms to Regex components for the 'tag' attribute
# Format: (Latvian Name, Regex Pattern)
POS_MAP = {
    "lietvārds": "n",           # Noun
    "darbības vārds": "v",      # Verb
    "īpašības vārds": "a",      # Adjective
    "vietniekvārds": "p",       # Pronoun
    "apstākļa vārds": "r",      # Adverb
    "prievārds": "s",           # Preposition
    "saiklis": "c",             # Conjunction
    "partikula": "q",           # Particle
    "izsaukuma vārds": "i"      # Interjection
}

# Morphology mappings (Key: NL term, Value: Regex char, Position index roughly implied for context)
CASES = {
    "nominatīvā": ("n", "Nom"),
    "ģenitīvā": ("g", "Gen"),
    "datīvā": ("d", "Dat"),
    "akuzatīvā": ("a", "Acc"),
    "lokatīvā": ("l", "Loc"),
    "vokatīvā": ("v", "Voc")
}

NUMBERS = {
    "vienskaitlī": "s",
    "daudzskaitlī": "p"
}

GENDERS = {
    "vīriešu dzimtē": "m",
    "sieviešu dzimtē": "f"
}

# Verb specific
TENSES = {
    "tagadnē": "p",  # Present
    "pagātnē": "s",  # Past (s, not p, to avoid confusion with plural/present in other slots usually)
    "nākotnē": "f"   # Future
}

# Adjective specific
DEFINITENESS = {
    "noteiktais": "y",
    "nenoteiktais": "n"
}

# ==========================================
# 2. QUERY GENERATORS
# ==========================================

def gen_simple_lemma():
    """Generate simple lemma search."""
    lemma = random.choice(NOUNS + VERBS + ADJECTIVES)
    prompt = f"Atrodi visus vārda '{lemma}' lietojumus."
    cql = f'[lemma="{lemma}"]'
    return prompt, cql

def gen_exact_word():
    """Generate exact word form search."""
    word = random.choice(NOUNS) # Simplified usage of lemma as word for demo
    prompt = f"Meklē precīzu vārdu formu '{word}'."
    cql = f'[word="{word}"]'
    return prompt, cql

def gen_morphology_noun():
    """Generate noun queries with morphological constraints."""
    # Noun Tag Structure in LIMA: n[Type][Gender][Number][Case]...
    # Regex: n.[Gender][Number][Case].*
    
    gender_nl, gender_code = random.choice(list(GENDERS.items()))
    case_nl, (case_code, _) = random.choice(list(CASES.items()))
    number_nl, number_code = random.choice(list(NUMBERS.items()))
    
    # Randomly combine features to create variety
    mode = random.randint(1, 3)
    
    if mode == 1: # Case only
        prompt = f"Atrodi visus lietvārdus {case_nl}."
        # n (pos) . (type) . (gender) . (number) [case]
        cql = f'[tag="n....{case_code}.*"]'
        
    elif mode == 2: # Gender and Case
        prompt = f"Meklē {gender_nl} lietvārdus {case_nl}."
        # n . [gender] . [case]
        cql = f'[tag="n..{gender_code}.{case_code}.*"]'
        
    else: # Gender, Number, Case
        prompt = f"Atrodi {gender_nl} lietvārdus {number_nl} {case_nl}."
        # n . [gender] [number] [case]
        cql = f'[tag="n..{gender_code}{number_code}{case_code}.*"]'
        
    return prompt, cql

def gen_morphology_verb():
    """Generate verb queries."""
    # Verb Tag Structure: v[Type][Mood][Tense]...
    tense_nl, tense_code = random.choice(list(TENSES.items()))
    
    prompt = f"Atrodi darbības vārdus {tense_nl}."
    # v . . [tense]
    cql = f'[tag="v..{tense_code}.*"]'
    return prompt, cql

def gen_morphology_adj():
    """Generate adjective queries."""
    # Adj Tag Structure: a[Degree][Gender][Number][Case][Definiteness]
    def_nl, def_code = random.choice(list(DEFINITENESS.items()))
    case_nl, (case_code, _) = random.choice(list(CASES.items()))
    
    prompt = f"Atrodi {def_nl} īpašības vārdu {case_nl}."
    # a . . . [case] [def]
    cql = f'[tag="a....{case_code}{def_code}.*"]'
    return prompt, cql

def gen_wildcard_queries():
    """Generate Startswith, Endswith, Contains."""
    substring = random.choice(["ne", "sa", "pie", "no", "tā"])
    mode = random.choice(["starts", "ends", "contains"])
    
    if mode == "starts":
        prompt = f"Meklē vārdus, kas sākas ar '{substring}'."
        cql = f'[word="{substring}.*"]'
    elif mode == "ends":
        prompt = f"Atrodi vārdus, kas beidzas ar '{substring}'."
        cql = f'[word=".*{substring}"]'
    else:
        prompt = f"Meklē vārdus, kas satur burtu savienojumu '{substring}'."
        cql = f'[word=".*{substring}.*"]'
    return prompt, cql

def gen_sequence_queries():
    """Generate syntactic sequences."""
    mode = random.randint(1, 4)
    
    if mode == 1: # Adj + Noun (Agreement)
        case_nl, (case_code, _) = random.choice(list(CASES.items()))
        prompt = f"Atrodi īpašības vārdu, kam seko lietvārds, abi {case_nl}."
        # Using unified attribute for case match logic usually requires variable referencing in complex systems,
        # but standard CQL often implies explicit tags. We will use explicit tags.
        cql = f'[tag="a....{case_code}.*"] [tag="n....{case_code}.*"]'
        
    elif mode == 2: # Preposition + Noun
        prep = random.choice(PREPOSITIONS)
        prompt = f"Frāze, kas sākas ar prievārdu '{prep}', kam seko lietvārds."
        cql = f'[lemma="{prep}" & tag="s.*"] [tag="n.*"]'
        
    elif mode == 3: # Noun + Genitive Noun (Genitive Chain)
        prompt = f"Lietvārds, kam seko cits lietvārds ģenitīvā."
        cql = f'[tag="n.*"] [tag="n....g.*"]'
        
    elif mode == 4: # Any Token sequence
        prompt = f"Vārds 'ir', kam seko jebkurš viens vārds un tad vārds 'kas'."
        cql = f'[word="ir"] [] [word="kas"]'
        
    return prompt, cql

def gen_distance_queries():
    """Generate distance/proximity queries."""
    lemma1 = random.choice(NOUNS)
    lemma2 = random.choice(VERBS)
    dist = random.randint(1, 5)
    
    prompt = f"Atrodi lemmu '{lemma1}', kurai seko lemma '{lemma2}' ar maksimālo atstatumu {dist} vārdi."
    cql = f'[lemma="{lemma1}"] []{{0,{dist}}} [lemma="{lemma2}"]'
    return prompt, cql

def gen_logical_queries():
    """Generate AND/OR/NOT queries."""
    mode = random.choice(["and", "or", "not"])
    
    if mode == "and":
        # Noun AND Plural
        prompt = "Atrodi vārdus, kas ir lietvārdi daudzskaitlī (izmantojot loģisko UN)."
        cql = '[tag="n.*" & tag="n..p.*"]'
    elif mode == "or":
        lemma1 = random.choice(NOUNS)
        lemma2 = random.choice(NOUNS)
        prompt = f"Atrodi vārdu, kas ir vai nu '{lemma1}', vai '{lemma2}'."
        cql = f'[word="{lemma1}" | word="{lemma2}"]'
    elif mode == "not":
        prompt = "Atrodi jebkuru vārdu, kas nav komats."
        cql = '[word!=","]'
        
    return prompt, cql

def gen_complex_sentence_structure():
    """Generate queries for sentence boundaries or structures."""
    prompt = "Atrodi teikuma sākumu (pirmo vārdu)."
    cql = '<s> []'
    return prompt, cql

# ==========================================
# 3. MAIN GENERATION LOOP
# ==========================================

def generate_dataset(num_samples=1500):
    dataset = []
    
    # We assign weights to different types to ensure balance
    # 0: Simple Lemma/Word (20%)
    # 1: Morphology (Noun/Verb/Adj) (40%)
    # 2: Wildcards (10%)
    # 3: Sequences (15%)
    # 4: Distance (10%)
    # 5: Logic/Misc (5%)
    
    generators = [
        gen_simple_lemma, gen_exact_word, 
        gen_morphology_noun, gen_morphology_verb, gen_morphology_adj,
        gen_wildcard_queries, gen_sequence_queries, gen_distance_queries,
        gen_logical_queries, gen_complex_sentence_structure
    ]
    
    # Weighted distribution
    weights = [10, 10, 20, 10, 10, 10, 15, 10, 4, 1]
    
    for _ in range(num_samples):
        gen_func = random.choices(generators, weights=weights, k=1)[0]
        prompt, cql = gen_func()
        
        entry = {
            "instruction_latvian": prompt,
            "cql_query": cql
        }
        dataset.append(entry)
        
    return dataset

# ==========================================
# 4. EXECUTION
# ==========================================

if __name__ == "__main__":
    data = generate_dataset(1500)
    
    # Save to JSON
    output_filename = "latvian_cql_dataset.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
    print(f"Successfully generated {len(data)} CQL queries in '{output_filename}'.")
    
    # Preview
    print("\n--- Preview of first 5 entries ---")
    for item in data[:5]:
        print(json.dumps(item, indent=2, ensure_ascii=False))