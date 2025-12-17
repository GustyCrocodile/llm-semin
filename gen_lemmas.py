import json
import pathlib
pathlib.Path('data').mkdir(exist_ok=True) 


file_path = 'leksemas.txt'
lemma_list = []


with open(file_path, 'r', encoding='utf-8') as f:
    lemma_list = f.read().splitlines()

result = []

for lemma in lemma_list:
    cql_string = f'lemma="{lemma}"'
    prompt = f'leksēmu "{lemma}"'
    result.append({
        "cql": cql_string,
        "prompt": prompt,
        "type": "L"
    })

with open("data/l_data.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)
