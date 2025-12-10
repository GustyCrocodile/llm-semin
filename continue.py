import json
import requests
import time

# Configuration
INPUT_FILE = 'latvian_cql_dataset.json'
OUTPUT_FILE = 'result_dataset.json'
API_URL = 'https://nosketch.korpuss.lv/bonito/run.cgi/concordance'

def process_dataset():
    # 1. Load the dataset
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find {INPUT_FILE}.")
        return

    print(f"Processing {len(data)} items...")

    # 2. Iterate through each object in the dataset
    for index, item in enumerate(data):
        cql_query = item.get("cql_query")
        
        if not cql_query:
            print(f"Skipping item {index}: No 'cql_query' found.")
            continue

        # Construct the JSON payload structure required by the API
        payload_data = {
            "concordance_query": [
                {
                    "queryselector": "cqlrow",
                    "cql": cql_query,
                    "default_attr": "lemma"
                }
            ],
            "mlsort_options": [
                {
                    "skey": "kw",
                    "attr": "doc.id",
                    "ctx": "0",
                    "bward": "",
                    "icase": ""
                }
            ]
        }

        # Prepare request parameters
        # Note: The 'json' param requires a stringified JSON object
        params = {
            'corpname': 'LVK2022',
            'pagesize': 5,
            'json': json.dumps(payload_data, separators=(',', ':'))
        }

        try:
            # Make the request
            response = requests.get(API_URL, params=params)
            response.raise_for_status() # Raise error for bad status codes
            
            api_response = response.json()
            
            # Extract results
            kwic_results = []
            
            # Check if 'Lines' exists in response
            if 'Lines' in api_response:
                for line in api_response['Lines']:
                    # Each 'Kwic' is a list of tokens (dicts), e.g., [{"str": "Pie"}, {"str": "mācību"}]
                    # We join them to form a readable string.
                    kwic_tokens = [token.get('str', '') for token in line.get('Kwic', [])]
                    full_phrase = " ".join(kwic_tokens)
                    kwic_results.append(full_phrase)
            
            # Append expected result to the current object
            item['expected_result'] = kwic_results
            print(f"Item {index + 1}: Found {len(kwic_results)} results for query '{cql_query}'")

        except requests.exceptions.RequestException as e:
            print(f"Error requesting item {index}: {e}")
            item['expected_result'] = [] # Set empty if failed
        except json.JSONDecodeError:
            print(f"Error parsing JSON response for item {index}")
            item['expected_result'] = []

        # Optional: Sleep briefly to be polite to the server
        time.sleep(0.5)

    # 3. Save the result to a new file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print(f"\nDone! Results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    process_dataset()