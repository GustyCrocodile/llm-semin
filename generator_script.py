import random
import json

class CQLQueryGenerator:
    """Generate diverse CQL queries for testing model capabilities"""
    
    def __init__(self):
        # Sample vocabulary
        self.words = ["cat", "dog", "run", "jump", "happy", "sad", "quickly", "slowly", 
                      "house", "tree", "car", "book", "write", "read", "think", "say"]
        self.lemmas = ["be", "have", "do", "say", "get", "make", "go", "know", "take", 
                       "see", "come", "think", "look", "want", "give", "use", "find", "tell"]
        self.pos_tags = ["NN", "VB", "JJ", "RB", "DT", "IN", "PRP", "MD", "VBG", "VBN"]
        self.prepositions = ["in", "on", "at", "by", "with", "from", "to", "for"]
        self.determiners = ["the", "a", "an", "this", "that", "these", "those"]
        
    def generate_simple_queries(self, n=50):
        """Generate simple single-token queries"""
        queries = []
        
        # Word searches
        for _ in range(n // 5):
            word = random.choice(self.words)
            queries.append({
                "query": f'[word="{word}"]',
                "description": f"Find exact word '{word}'",
                "complexity": "simple"
            })
        
        # Lemma searches
        for _ in range(n // 5):
            lemma = random.choice(self.lemmas)
            queries.append({
                "query": f'[lemma="{lemma}"]',
                "description": f"Find lemma '{lemma}'",
                "complexity": "simple"
            })
        
        # POS tag searches
        for _ in range(n // 5):
            tag = random.choice(self.pos_tags)
            queries.append({
                "query": f'[tag="{tag}"]',
                "description": f"Find words with POS tag '{tag}'",
                "complexity": "simple"
            })
        
        # Case-insensitive searches
        for _ in range(n // 5):
            word = random.choice(self.words)
            queries.append({
                "query": f'[lc="{word.lower()}"]',
                "description": f"Find '{word}' (case-insensitive)",
                "complexity": "simple"
            })
        
        # Regex patterns
        for _ in range(n // 5):
            pattern = random.choice([".*ing", ".*ed", ".*ly", "un.*", "re.*"])
            queries.append({
                "query": f'[word="{pattern}"]',
                "description": f"Find words matching pattern '{pattern}'",
                "complexity": "simple"
            })
        
        return queries
    
    def generate_sequence_queries(self, n=50):
        """Generate queries with word sequences"""
        queries = []
        
        # Two-word sequences
        for _ in range(n // 4):
            w1, w2 = random.sample(self.words, 2)
            queries.append({
                "query": f'[word="{w1}"][word="{w2}"]',
                "description": f"Find sequence '{w1} {w2}'",
                "complexity": "medium"
            })
        
        # Three-word sequences
        for _ in range(n // 4):
            w1, w2, w3 = random.sample(self.words, 3)
            queries.append({
                "query": f'[word="{w1}"][word="{w2}"][word="{w3}"]',
                "description": f"Find sequence '{w1} {w2} {w3}'",
                "complexity": "medium"
            })
        
        # Word + POS sequences
        for _ in range(n // 4):
            word = random.choice(self.words)
            tag = random.choice(self.pos_tags)
            queries.append({
                "query": f'[word="{word}"][tag="{tag}"]',
                "description": f"Find '{word}' followed by {tag}",
                "complexity": "medium"
            })
        
        # Determiner + noun patterns
        for _ in range(n // 4):
            det = random.choice(self.determiners)
            queries.append({
                "query": f'[word="{det}"][tag="NN.*"]',
                "description": f"Find '{det}' followed by a noun",
                "complexity": "medium"
            })
        
        return queries
    
    def generate_distance_queries(self, n=30):
        """Generate queries with distance operators"""
        queries = []
        
        for _ in range(n // 3):
            w1, w2 = random.sample(self.words, 2)
            dist = random.randint(1, 5)
            queries.append({
                "query": f'[word="{w1}"][]{{0,{dist}}}[word="{w2}"]',
                "description": f"Find '{w1}' within {dist} words of '{w2}'",
                "complexity": "medium"
            })
        
        for _ in range(n // 3):
            w1, w2 = random.sample(self.words, 2)
            queries.append({
                "query": f'[word="{w1}"][]{1,3}[word="{w2}"]',
                "description": f"Find '{w1}' and '{w2}' with 1-3 words between",
                "complexity": "medium"
            })
        
        for _ in range(n // 3):
            lemma = random.choice(self.lemmas)
            queries.append({
                "query": f'[lemma="{lemma}"][]{0,2}[tag="NN"]',
                "description": f"Find lemma '{lemma}' within 2 words of a noun",
                "complexity": "medium"
            })
        
        return queries
    
    def generate_complex_queries(self, n=40):
        """Generate complex queries with multiple conditions"""
        queries = []
        
        # OR conditions
        for _ in range(n // 5):
            w1, w2 = random.sample(self.words, 2)
            queries.append({
                "query": f'[word="{w1}|{w2}"]',
                "description": f"Find either '{w1}' or '{w2}'",
                "complexity": "medium"
            })
        
        # Combined attributes
        for _ in range(n // 5):
            word = random.choice(self.words)
            tag = random.choice(self.pos_tags)
            queries.append({
                "query": f'[word="{word}" & tag="{tag}"]',
                "description": f"Find '{word}' with POS tag {tag}",
                "complexity": "complex"
            })
        
        # Negation
        for _ in range(n // 5):
            word = random.choice(self.words)
            queries.append({
                "query": f'[word!="{word}"]',
                "description": f"Find any word except '{word}'",
                "complexity": "medium"
            })
        
        # Complex sequences with alternatives
        for _ in range(n // 5):
            w1 = random.choice(self.words)
            w2, w3 = random.sample(self.words, 2)
            queries.append({
                "query": f'[word="{w1}"][word="{w2}|{w3}"]',
                "description": f"Find '{w1}' followed by '{w2}' or '{w3}'",
                "complexity": "complex"
            })
        
        # Multiple POS patterns
        for _ in range(n // 5):
            queries.append({
                "query": '[tag="DT"][tag="JJ.*"][tag="NN.*"]',
                "description": "Find determiner + adjective + noun pattern",
                "complexity": "complex"
            })
        
        return queries
    
    def generate_advanced_queries(self, n=30):
        """Generate advanced queries with structural constraints"""
        queries = []
        
        # Within sentence boundaries
        for _ in range(n // 3):
            w1, w2 = random.sample(self.words, 2)
            queries.append({
                "query": f'[word="{w1}"][]{0,10}[word="{w2}"] within <s/>',
                "description": f"Find '{w1}' and '{w2}' within same sentence",
                "complexity": "advanced"
            })
        
        # Verb phrase patterns
        for _ in range(n // 3):
            queries.append({
                "query": '[tag="MD"][tag="VB"]',
                "description": "Find modal verb followed by base verb",
                "complexity": "advanced"
            })
        
        # Prepositional phrases
        for _ in range(n // 3):
            prep = random.choice(self.prepositions)
            queries.append({
                "query": f'[word="{prep}"][tag="DT"]?[tag="JJ"]?[tag="NN.*"]',
                "description": f"Find prepositional phrase starting with '{prep}'",
                "complexity": "advanced"
            })
        
        return queries
    
    def generate_all(self):
        """Generate all query types"""
        all_queries = []
        all_queries.extend(self.generate_simple_queries(50))
        all_queries.extend(self.generate_sequence_queries(50))
        all_queries.extend(self.generate_distance_queries(30))
        all_queries.extend(self.generate_complex_queries(40))
        all_queries.extend(self.generate_advanced_queries(30))
        
        # Shuffle to mix complexity levels
        random.shuffle(all_queries)
        
        return all_queries
    
    def save_queries(self, queries, filename="cql_queries.txt", format="txt"):
        """Save queries to file in specified format"""
        if format == "txt":
            with open(filename, "w", encoding="utf-8") as f:
                for i, q in enumerate(queries, 1):
                    f.write(f"# Query {i}: {q['description']} (Complexity: {q['complexity']})\n")
                    f.write(f"{q['query']}\n\n")
        
        elif format == "json":
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(queries, f, indent=2, ensure_ascii=False)
        
        elif format == "jsonl":
            with open(filename, "w", encoding="utf-8") as f:
                for q in queries:
                    f.write(json.dumps(q, ensure_ascii=False) + "\n")
        
        elif format == "csv":
            import csv
            with open(filename, "w", encoding="utf-8", newline='') as f:
                writer = csv.DictWriter(f, fieldnames=["query", "description", "complexity"])
                writer.writeheader()
                writer.writerows(queries)
        
        print(f"Saved {len(queries)} queries to {filename}")
        
        # Print statistics
        complexity_counts = {}
        for q in queries:
            complexity_counts[q['complexity']] = complexity_counts.get(q['complexity'], 0) + 1
        
        print("\nQuery complexity distribution:")
        for complexity, count in sorted(complexity_counts.items()):
            print(f"  {complexity}: {count}")


# Main execution
if __name__ == "__main__":
    generator = CQLQueryGenerator()
    
    # Generate all queries
    queries = generator.generate_all()
    
    # Save in multiple formats
    generator.save_queries(queries, "cql_queries.json", format="json")
    
    print(f"\nTotal queries generated: {len(queries)}")
    print("\nSample queries:")
    for q in random.sample(queries, 5):
        print(f"  {q['query']}")
        print(f"  → {q['description']}")
        print()
