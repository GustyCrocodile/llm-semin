import ijson
import json
import os
from typing import Dict, Any

def stream_process_and_format(input_filepath: str, output_filepath: str, field_to_format: str) -> None:
    """
    Streams a large JSON file, applies the 'enclose_in_brackets' formatting 
    function to a specified field in each object, and streams the modified 
    objects to a new JSON list file.

    :param input_filepath: Path to the input JSON file (list of objects).
    :param output_filepath: Path to the output JSON file.
    :param field_to_format: The key of the field whose value needs brackets added.
    """
    
    # Simple formatting function (defined inline for clarity)
    def enclose_in_brackets(value: str) -> str:
        return f"[{value}]"

    print(f"Starting streaming process for '{field_to_format}' field...")
    
    # 1. Setup the output file stream
    first_item_written = False
    
    try:
        with open(input_filepath, 'rb') as input_f, \
             open(output_filepath, 'w', encoding='utf-8') as output_f:
            
            output_f.write('[\n')
            
            # ijson.items() streams each object from the top-level array
            objects_stream = ijson.items(input_f, 'item')
            
            # 2. Iterate and process each object
            for index, item in enumerate(objects_stream):
                
                if (index + 1) % 10000 == 0:
                    print(f"-> Processed {index + 1:,} items...")

                # --- A. Apply Formatting ---
                if field_to_format in item:
                    value = item[field_to_format]
                    if isinstance(value, str):
                        item[field_to_format] = enclose_in_brackets(value)
                    # Note: You might add logic here to handle non-string values if necessary
                
                # --- B. Stream the Output ---
                
                # Add a comma before the object if it's not the first one
                if first_item_written:
                    output_f.write(',\n')
                
                # Write the JSON object to the file
                # Use indent=2 for human readability, or remove for max file size reduction
                json.dump(item, output_f, ensure_ascii=False, indent=2)
                
                first_item_written = True

            # 3. Write the closing bracket of the JSON list
            output_f.write('\n]')

    except FileNotFoundError:
        print(f"Error: Could not find input file at {input_filepath}.")
        # Attempt to clean up the output file if it was partially written
        if os.path.exists(output_filepath) and os.path.getsize(output_filepath) > 1:
             print("Warning: Output file is incomplete. Please check it.")
    except ijson.JSONError as e:
        print(f"Error: Invalid JSON format in input file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    print(f"\nProcessing complete. Results saved to {output_filepath}")


# 2. Run the streaming function, targeting the "city" field
stream_process_and_format("result_t_dataset.json", "t_data_res.json", "cql")

