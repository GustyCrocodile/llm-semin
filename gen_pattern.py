import ijson
import random
import json
import re

def extract_lemma_base(cql):
    """Extract base word/pattern from CQL query."""
    # Try to extract lemma value from patterns like [lemma="word"] or [tag="pattern"]
    match = re.search(r'(?:lemma|word)="([^"]+)"', cql)
    if match:
        # Remove regex patterns and get clean base
        base = match.group(1)
        base = base.replace('.*', '').replace('.', '').replace('*', '')
        return base if base else None
    return None

def generate_pattern_combinations(num_combinations=600):
    """
    Generate CQL combinations with starting/ending/containing patterns.
    
    Args:
        json_file_path: Path to the input JSON file
        num_combinations: Number of combinations to generate (default 600)
    
    Returns:
        List of dictionaries with new CQL and prompt combinations
    """    
    combinations = []
    
    # Common prefixes and suffixes for Latvian
    prefixes = ['ne', 'aiz', 'ap', 'at', 'ie', 'iz', 'no', 'pa', 'pie', 'pār', 'sa', 'uz']
    suffixes = ['iem', 'ām', 'iem', 'as', 'os', 'us', 'is', 'ts', 'šana', 'šanas', 'īgs', 'īga']
    
    # Pattern generation functions
    def starts_with_pattern(data):
        """Generate 'starts with' patterns."""
        lemma_base = extract_lemma_base(data['cql'])
        if lemma_base and len(lemma_base) >= 2:
            prefix = lemma_base[:random.randint(2, min(4, len(lemma_base)))]
        else:
            prefix = random.choice(prefixes)
        
        return {
            'cql': f'[lemma="{prefix}.*"]',
            'prompt': f'vārdi, kas sākas ar {prefix}-',
            'type': 'P'
        }
    
    def ends_with_pattern(data):
        """Generate 'ends with' patterns."""
        lemma_base = extract_lemma_base(data['cql'])
        if lemma_base and len(lemma_base) >= 2:
            suffix = lemma_base[-random.randint(2, min(4, len(lemma_base))):]
        else:
            suffix = random.choice(suffixes)
        
        return {
            'cql': f'[lemma=".*{suffix}"]',
            'prompt': f'vārdi, kas beidzas ar -{suffix}',
            'type': 'P'
        }
    
    def contains_pattern(data):
        """Generate 'contains' patterns."""
        lemma_base = extract_lemma_base(data['cql'])
        if lemma_base and len(lemma_base) >= 3:
            start = random.randint(1, len(lemma_base) - 2)
            middle = lemma_base[start:start + random.randint(2, min(3, len(lemma_base) - start))]
        else:
            middle = random.choice(['an', 'in', 'ar', 'at', 'is'])
        
        return {
            'cql': f'[lemma=".*{middle}.*"]',
            'prompt': f'vārdi, kas satur {middle}',
            'type': 'P'
        }
    
    def specific_length_starts_ends(data):
        """Generate patterns for N-letter words starting and ending with specific letters."""
        lemma_base = extract_lemma_base(data['cql'])
        
        # Choose word length (2-5 letters)
        length = random.randint(3, 6)
        
        if lemma_base and len(lemma_base) >= 2:
            start_letter = lemma_base[0]
            end_letter = lemma_base[-1]
        else:
            # Common Latvian letters
            letters = 'abcdefghijklmnoprstuv'
            start_letter = random.choice(letters)
            end_letter = random.choice(letters)
        
        # Build pattern with dots for middle letters
        dots = '.' * (length - 2)
        
        return {
            'cql': f'[lemma="{start_letter}{dots}{end_letter}"]',
            'prompt': f'{length} burtu vārdi, kas sākas ar {start_letter}- un beidzas ar -{end_letter}',
            'type': 'P'
        }
    
    def starts_with_multiple_chars(data):
        """Generate patterns starting with 2-3 specific characters."""
        lemma_base = extract_lemma_base(data['cql'])
        
        if lemma_base and len(lemma_base) >= 2:
            chars = lemma_base[:random.randint(2, min(3, len(lemma_base)))]
        else:
            chars = random.choice(prefixes)
        
        return {
            'cql': f'[lemma="{chars}.*"]',
            'prompt': f'vārdi, kas sākas ar {chars}',
            'type': 'P'
        }
    
    def ends_with_multiple_chars(data):
        """Generate patterns ending with 2-3 specific characters."""
        lemma_base = extract_lemma_base(data['cql'])
        
        if lemma_base and len(lemma_base) >= 2:
            chars = lemma_base[-random.randint(2, min(3, len(lemma_base))):]
        else:
            chars = random.choice(suffixes)
        
        return {
            'cql': f'[lemma=".*{chars}"]',
            'prompt': f'vārdi, kas beidzas ar {chars}',
            'type': 'P'
        }
    
    def exact_length_pattern(data):
        """Generate patterns for exact word length."""
        length = random.randint(3, 7)
        dots = '.' * length
        
        return {
            'cql': f'[lemma="{dots}"]',
            'prompt': f'vārdi ar tieši {length} burtiem',
            'type': 'P'
        }
    
    # Pattern types with weights
    pattern_functions = [
        (starts_with_pattern, 20),
        (ends_with_pattern, 20),
        (contains_pattern, 15),
        (specific_length_starts_ends, 20),
        (starts_with_multiple_chars, 10),
        (ends_with_multiple_chars, 10),
        (exact_length_pattern, 5)
    ]
    
    # Create weighted list
    weighted_patterns = []
    for func, weight in pattern_functions:
        weighted_patterns.extend([func] * weight)
    
    # Generate combinations
    for _ in range(num_combinations):
        # Select random pattern function
        pattern_func = random.choice(weighted_patterns)
        
        # Select random data point as base
        data = random.choice(original_data)
        
        # Generate combination
        combo = pattern_func(data)
        combinations.append(combo)
    
    return combinations


def save_combinations(combinations, output_file='p_data.json'):
    """Save generated combinations to a JSON file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(combinations, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(combinations)} pattern combinations to {output_file}")


# Example usage
if __name__ == "__main__":
    
    # Generate combinations
    combinations = generate_pattern_combinations(num_combinations=200)
    
    # Save to file
    save_combinations(combinations)
    
    # Print first 10 examples
    # print("\nFirst 10 generated pattern combinations:")
    # for i, combo in enumerate(combinations[:10], 1):
    #     print(f"\n{i}. CQL: {combo['cql']}")
    #     print(f"   Prompt: {combo['prompt']}")
    #     print(f"   Type: {combo['type']}")