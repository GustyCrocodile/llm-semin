import json
import requests
import time
import ijson # Used for streaming the input JSON file
import os # Used for file operations

# Configuration
# infile = 'data/w_data.json'
# outfile = 'result_dataset_streamed.json' # Renamed output file
API_URL = 'https://nosketch.korpuss.lv/bonito/run.cgi/concordance'
SLEEP_TIME = 0.1 # Time to wait between requests
PAGESIZE = 5

def stream_process_dataset(infile, outfile):
    """
    Streams the input JSON file (assumed to be a list of objects), 
    processes each object, and immediately streams the result to the 
    output JSON file. This saves memory and prevents data loss if the 
    script is interrupted.
    """
    
    # 1. Setup the output file stream
    # We will manually write the start of the JSON array '[' to the output file.
    if os.path.exists(outfile):
        os.remove(outfile) # Remove existing file to start fresh

    # Use a session for efficient connection pooling
    session = requests.Session()
    
    # Flag to track if the first object has been written (to manage commas)
    first_item_written = False
    
    print(f"Opening input file: {infile}")
    print(f"Opening output file stream: {outfile}")

    try:
        with open(infile, 'rb') as input_f, \
             open(outfile, 'w', encoding='utf-8') as output_f:
            
            # Write the opening bracket of the JSON list
            output_f.write('[\n')
            
            # ijson.items() streams the content. 'item' specifies the array elements.
            # 'data.' is required if the top-level element is an array.
            objects = ijson.items(input_f, 'item')
            
            # 2. Iterate through each object streamed from the input file
            for index, item in enumerate(objects):
                
                # Print progress every 100 items
                if (index + 1) % 100 == 0:
                    print(f"-> Processed {index + 1:,} items...")
                
                cql_query = item.get("cql")
                
                if not cql_query:
                    # Skip invalid items but log it
                    print(f"Skipping item {index}: No 'cql' found.")
                    continue

                # Construct the JSON payload structure required by the API
                # The 'cql' from the file is inserted into the request payload.
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
                params = {
                    'corpname': 'LVK2022',
                    'pagesize': PAGESIZE,
                    # Dump the JSON data, ensuring it's compact for the API
                    'json': json.dumps(payload_data, separators=(',', ':'))
                }

                kwic_results = []
                
                # --- A. Make HTTP Request ---
                try:
                    response = session.get(API_URL, params=params, timeout=15)
                    response.raise_for_status() # Raise error for bad status codes
                    api_response = response.json()
                    # print(api_response)
                    
                    # --- B. Extract Results ---
                    # Check if 'Lines' exists in response and is a non-empty list
                    lines_list = api_response.get('Lines')
                    if lines_list and isinstance(lines_list, list) and len(lines_list) > 0:
                        
                        # Extract the required strings from the response structure
                        for line in lines_list:
                            # The 'Kwic' is a list of tokens (dicts), e.g., [{"str": "Pie"}, {"str": "mācību"}]
                            kwic_tokens = [token.get('str', '') for token in line.get('Kwic', []) if isinstance(token, dict)]
                            full_phrase = " ".join(kwic_tokens)
                            
                            # Only add non-empty phrases
                            if full_phrase:
                                kwic_results.append(full_phrase)

                except requests.exceptions.RequestException as e:
                    print(f"Error requesting item {index}: {e}. Setting 'response' to empty list.")
                except json.JSONDecodeError:
                    print(f"Error parsing JSON response for item {index}. Setting 'response' to empty list.")

                
                # --- C. Stream the Output ---
                # Only write to file if results were found, as per your initial requirement
                if kwic_results:
                    # 1. Add the new attribute to the current item
                    # NOTE: Renamed the attribute to 'response' as requested in the prompt
                    item['response'] = kwic_results
                    item['cql'] = cql_query
                    # 2. Add a comma before the object if it's not the first one
                    if first_item_written:
                        output_f.write(',\n')
                    
                    # 3. Write the JSON object to the file
                    # Using json.dumps with indent=4 for human readability
                    # NOTE: Using a single line dump might be faster for huge files
                    json.dump(item, output_f, ensure_ascii=False, indent=4)
                    
                    first_item_written = True

                # Optional: Sleep briefly to be polite to the server
                time.sleep(SLEEP_TIME)

            # 3. Write the closing bracket of the JSON list
            output_f.write('\n]')

    except FileNotFoundError:
        print(f"Error: Could not find input file at {infile}.")
    except Exception as e:
        print(f"An unexpected error occurred during processing: {e}")
    finally:
        session.close() # Close the requests session

    print(f"\nDone! Results streamed and saved to {outfile}")

if __name__ == "__main__":
    stream_process_dataset("d_dataset.json", "result_d_dataset.json")
    # stream_process_dataset("data/l_data.json", "l_data_res.json")
    # stream_process_dataset("data/w_data.json", "w_data_res.json")