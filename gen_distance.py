import ijson
import random
import json

def generate_random_combinations(json_file_path, num_combinations=600):
    """
    Generate random CQL and prompt combinations from a JSON file.
    
    Args:
        json_file_path: Path to the input JSON file
        num_combinations: Number of combinations to generate (default 600)
    
    Returns:
        List of dictionaries with new CQL and prompt combinations
    """
    # Read the original data using ijson
    original_data = []
    with open(json_file_path, 'rb') as f:
        parser = ijson.items(f, 'item')
        for item in parser:
            original_data.append(item)
    
    if not original_data:
        raise ValueError("No data found in JSON file")
    
    combinations = []
    
    # Combination patterns
    patterns = [
        # Distance between tokens (2-4 words)
        lambda d1, d2: {
            'cql': f'{d1["cql"]} [ ]{{2,4}}{d2["cql"]}',
            'prompt': f'{d1["prompt"]} un {d2["prompt"]} ar 2-4 vārdiem starpā',
            'type': 'D'
        },
        # One word in between
        lambda d1, d2: {
            'cql': f'{d1["cql"]} [ ] {d2["cql"]}',
            'prompt': f'{d1["prompt"]} un {d2["prompt"]} ar vienu vārdu starpā',
            'type': 'D'
        },
        # Repeating 2 times
        lambda d1, d2: {
            'cql': f'{d1["cql"]}{{2}}',
            'prompt': f'{d1["prompt"]} atkārtots 2 reizes',
            'type': 'D'
        },
        # Repeating at least 2 times
        lambda d1, d2: {
            'cql': f'{d1["cql"]}{{2,}}',
            'prompt': f'{d1["prompt"]} atkārtots vismaz 2 reizes',
            'type': 'D'
        },
        # Distance 1-3 words
        lambda d1, d2: {
            'cql': f'{d1["cql"]} [ ]{{1,3}}{d2["cql"]}',
            'prompt': f'{d1["prompt"]} ar 1-3 vārdiem starpā pirms {d2["prompt"]}',
            'type': 'D'
        },
        # Exact 2 words in between
        lambda d1, d2: {
            'cql': f'{d1["cql"]} [ ]{{2}}{d2["cql"]}',
            'prompt': f'{d1["prompt"]} ar tieši 2 vārdiem starpā pirms {d2["prompt"]}',
            'type': 'D'
        },
        # Repeating 3 times
        lambda d1, d2: {
            'cql': f'{d1["cql"]}{{3}}',
            'prompt': f'{d1["prompt"]} atkārtots 3 reizes',
            'type': 'D'
        },
        # Donsecutive tokens
        lambda d1, d2: {
            'cql': f'{d1["cql"]} {d2["cql"]}',
            'prompt': f'{d1["prompt"]} tieši pirms {d2["prompt"]}',
            'type': 'D'
        }
    ]
    
    for _ in range(num_combinations):
        # Select random pattern
        pattern = random.choice(patterns)
        
        # Select random data points
        d1 = random.choice(original_data)
        d2 = random.choice(original_data)
        
        # Generate combination
        combo = pattern(d1, d2)
        combinations.append(combo)
    
    return combinations


def save_combinations(combinations, output_file='d_dataset.json'):
    """Save generated combinations to a JSON file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(combinations, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(combinations)} combinations to {output_file}")


# Example usage
if __name__ == "__main__":
    input_file = "combined_data.json"  # Replace with your input file path
    
    # Generate combinations
    combinations = generate_random_combinations(input_file, num_combinations=600)
    
    # Save to file
    save_combinations(combinations)
    
    # Print first 5 examples
    print("\nFirst 5 generated combinations:")
    for i, combo in enumerate(combinations[:5], 1):
        print(f"\n{i}. CQL: {combo['cql']}")
        print(f"   Prompt: {combo['prompt']}")
        print(f"   Type: {combo['type']}")