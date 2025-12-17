import ijson
from typing import Optional

def stream_count_json_objects(filepath: str) -> Optional[int]:
    """
    Streams through a JSON file that contains a single list of objects 
    and returns the total count of objects without loading the entire 
    list into memory.

    :param filepath: Path to the input JSON file (must be a list/array).
    :return: The count of objects, or None if an error occurs.
    """
    
    count = 0
    print(f"Starting to stream and count objects in {filepath}...")

    try:
        # Open the file in binary read mode ('rb') as required by ijson
        with open(filepath, 'rb') as f:
            
            # ijson.items(f, 'item') yields each element from the top-level array
            # in the JSON file (e.g., [{}, {}, ...])
            # We don't care about the object itself, only that it exists.
            objects_stream = ijson.items(f, 'item')
            
            # Iterate through the stream and increment the counter
            for _ in objects_stream:
                count += 1
                
                # Optional: Print progress for very large files
                if count % 10000 == 0:
                    print(f"  ... Count reached {count:,}")
            
            print("\nStreaming complete.")
            return count

    except FileNotFoundError:
        print(f"Error: Input file not found at {filepath}.")
        return None
    except ijson.JSONError as e:
        print(f"Error: Invalid JSON format in {filepath}. Error: {e}")
        print("Note: Ensure the file contains a single top-level array, e.g., `[{}, {}, ...]`")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

# 2. Run the streaming counter function
result_count = stream_count_json_objects("data_v2.json")

# 3. Print final result
if result_count is not None:
    print(f"\n✅ Total objects counted: {result_count:,}")

# Clean up (optional)
# import os
# os.remove(DUMMY_FILE)