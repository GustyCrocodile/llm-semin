import json
import pathlib
pathlib.Path('data').mkdir(exist_ok=True) 

file_path = 'vardi.txt'
word_list = []


with open(file_path, 'r', encoding='utf-8') as f:
    word_list = f.read().splitlines()

result = []

for word in word_list:
    cql_string = f'word="{word}"'
    prompt = f'vārdformu "{word}"'
    result.append({
        "cql": cql_string,
        "prompt": prompt,
        "type": "W"
    })

with open("data/w_data.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)
