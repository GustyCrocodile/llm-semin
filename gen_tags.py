import itertools
import json

import pathlib
pathlib.Path('data').mkdir(exist_ok=True) 

t_val = {
    "lietvārdu": {
        "kods": "n",
        "tips": {
            "sugas vārds": "c",
            "īpašvārds": "p"
        },
        "dzimte": {
            "vīriešu dzimtē": "m",
            "sieviešu dzimtē": "f",
            "nepiemīt dzimte": "0"
        },
        "skaitlis": {
            "vienskaitlī": "s",
            "daudzskaitlī": "p",
            "vienskaitlinieku": "v",
            "daudzskaitlinieku": "d",
            "nepiemīt skaitlis": "0"
        },
        "locījums": {
            "nominatīvā": "n",
            "ģenitīvā": "g",
            "datīvā": "d",
            "akuzatīvā": "a",
            "lokatīvā": "l",
            "vokatīvā": "v",
            "nepiemīt locījums": "0"
        },
        "deklinācijas": {
            "1. deklinācijas": "1",
            "2. deklinācijas": "2",
            "3. deklinācijas": "3",
            "4. deklinācijas": "4",
            "5. deklinācijas": "5",
            "6. deklinācijas": "6",
            "nepiemīt deklinācija": "0",
            "ģenitīvenis": "g",
            "atgriezenisks": "r"
        }
    }, 
    "darbības vārdu": {
        "kods": "v",
        "tips": {
            "patstāvīgu": "m",
            "modālu": "o",
            "fāzes": "p",
            "izpausmes veida": "e",
            "palīgverba \"būt\"": "c",
            "saitiņverba \"kļūt\"": "t",
            "palīgverba \“tikt\”, \“tapt\”": "a",
        },
        "atgriezenisks": ["n", "y"],
        "izteiksmē": {
            "īstenības izteiksmē": "i",
            "atstāstījuma izteiksmē": "r",
            "vēlējuma izteiksmē": "c",
            "vajadzības izteiksmē": "d",
            "pavēles izteiksmē": "m",
            "nenoteiksmes izteiksmē": "n",
            "divdabi": "p",
        },
        "laikā": {
            "tagadnes": "p",
            "nākotnes": "f",
            "pagātnes": "s",
            "nepiemīt laiks": "0"
        },
        "pārejamība": {
            "pārejošu": "t",
            "nepārejošu": "i"
        },
        "konjugācijas": {
            "1.konjugācijas": "1",
            "2.konjugācijas": "2",
            "3.konjugācijas": "3",
            "nekārtnais": "i"
        },
        "persona": {
            "1. personā": "1",
            "2. personā": "2",
            "3. personā": "3",
            "persona nepiemīt": "0"
        },
        "skaitlis": {
            "vienskaitlis": "s",
            "daudzskaitlis": "p",
            "skaitlis nepiemīt": "0"
        },
        "kārta": {
            "darāmā kārtā": "a",
            "kārtā nepiemīt": "0"
        },
        "noliegums": {
            "nav nolieguma":"n", 
            "ir nolieguma":"y"
        }
    },
    "darbības vārdu divdabja formā": {
        "kods": "v",
        "tips": {
            "patstāvīgu": "m",
            "modālu": "o",
            "fāzes": "p",
            "izpausmes veida": "e",
            "palīgverba \"būt\"": "c",
            "saitiņverba \"kļūt\"": "t",
            "palīgverba \“tikt\”, \“tapt\”": "a",
        },
        "atgriezenisks": {
            "nav atgriezenisks": "n",
            "atgriezenisks": "y"
        },
        "izteiksmē": {
            "īstenības": "i",
            "atstāstījuma": "r",
            "vēlējuma": "c",
            "vajadzības": "d",
            "pavēles": "m",
            "nenoteiksme": "n",
            "divdabis": "p",
        },
        "lokāmība": {
            "lokāms": "d",
            "daļēji lokāms": "p",
            "nelokāms": "u"
        },
        "dzimte": {
            "vīriešu dzimtē": "m",
            "sieviešu dzimtē": "f",
            "dzimte nepiemīt": "0"
        },
        "skaitlis": {
            "vienskaitlī": "s",
            "daudzskaitlī": "p",
            "skaitlis nepiemīt": "0"
        },
        "locījums": {
            "nominatīvā": "n",
            "ģenitīvā": "g",
            "datīvā": "d",
            "akuzatīvā": "a",
            "lokatīvā": "l",
            "vokatīvā": "v",
            "nepiemīt locījums": "0"
        },
        "kārta": {
            "darāmā kārtā": "a",
            "ciešamā kārtā": "p",
            "nepiemīt kārta": "0"
        },
        "laiks": {
            "tagadne": "p",
            "nākotne": "f",
            "pagātne": "s",
            "nepiemīt laiks": "0"
        },
        "noteiktība": {
            "nenoteiktais": "n",
            "noteiktais": "y",
            "nepiemīt laiks": "0"
        },
        "pakāpe": {
            "pārejošs": "t",
            "nepārejošs": "i",
            "pārejošs": "t",
            "nepiemīt laiks": "0"
        },
        "noliegums": {
            "nav nolieguma":"n", 
            "ir nolieguma":"y"
        }
    },
    "īpašības vārds": {
        "kods": "a",
        "tips": {
            "kādības": "f",
            "attieksmes": "r"
        },
        "dzimte": {
            "vīriešu dzimtē": "m",
            "sieviešu dzimtē": "f",
            "nepiemīt dzimte": "0"
        },
        "skaitlis": {
            "vienskaitlī": "s",
            "daudzskaitlī": "p",
            "nepiemīt skaitlis": "0"
        },
        "locījums": {
            "nominatīvā": "n",
            "ģenitīvā": "g",
            "datīvā": "d",
            "akuzatīvā": "a",
            "lokatīvā": "l",
            "vokatīvā": "v",
            "nepiemīt locījums": "0"
        },
        "noteiktība": {
            "nenoteikts": "n",
            "noteikts": "y"
        },
        "pakāpe": {
            "pamata pakāpē": "p",
            "pārākajā pakāpē": "c",
            "vispārākajā pakāpē": "s"
        }
    },
    "skaitļa vārds": {
        "kods": "m",
        "tips": {
            "pamata":"c",
            "kārtas": "o",
            "daļskaitlis": "f"
        },
        "uzbūve": {
            "vienkāršs": "s",
            "saliktenis": "c"
        },
        "dzimte": {
            "vīriešu dzimtē": "m",
            "sieviešu dzimtē": "f",
            "nepiemīt dzimte": "0"
        },
        "skaitlis": {
            "vienskaitlī": "s",
            "daudzskaitlī": "p",
        },
        "locījums": {
            "nominatīvā": "n",
            "ģenitīvā": "g",
            "datīvā": "d",
            "akuzatīvā": "a",
            "lokatīvā": "l",
            "vokatīvā": "v",
            "nepiemīt locījums": "0"
        }
    },
    "vietniekvārds": {
        "kods": "p",
        "tips": {
            "personas": "p",
            "atgriezeniskais": "x",
            "piederības": "s",
            "norādāmais": "d",
            "nenoteiktais": "i",
            "jautājamais": "q",
            "attieksmes": "r",
            "noteiktais": "g"
        },
        "persona": {
            "1. personā": "1",
            "2. personā": "2",
            "3. personā": "3",
            "nepiemīt persona": "0"
        },
        "dzimte": {
            "vīriešu dzimtē": "m",
            "sieviešu dzimtē": "f",
            "nepiemīt dzimte": "0"
        },
        "skaitlis": {
            "vienskaitlī": "s",
            "daudzskaitlī": "p",
            "nepiemīt skaitlis": "0"
        },
        "locījums": {
            "nominatīvā": "n",
            "ģenitīvā": "g",
            "datīvā": "d",
            "akuzatīvā": "a",
            "lokatīvā": "l"
        },
        "noliegums": {
            "nav nolieguma": "n", 
            "ir nolieguma": "y"
        }
    },
    "apstākļa vārds": {
        "kods":"r",
        "pakāpe": {
            "pamata": "p",
            "pārākā": "c",
            "vispārākā": "s",
            "nepiemīt pakāpe": "0"
        },
        "grupa":{
            "mēra": "q",
            "veida": "m",
            "vietas": "p",
            "laika": "t"
        },
        "prievārdisks": {
            "ir prievārdisks": "y",
            "nav prievārdisks": "n"
        } 
    },
    "prievārdu": {
        "kods": "s",
        "novietojums": {
            "pirms": "p",
            "pēc": "t"
        },
        "skaitlis": {
            "vienskaitlī": "s",
            "daudzskaitlī": "p",
            "nepiemīt skaitlis": "0"
        },
        "reakcija": {
            "ģenitīvā": "g",
            "datīvā": "d",
            "akuzatīvā": "a",
            "nepiemīt reakcija": "0"
        }
    },
    "saikli": {
        "kods": "c",
        "tips": {
            "sakārtojuma": "c",
            "pakārtojuma": "s"
        }
    },
    "izsauksmes vārdu": {
        "kods": "i"
    },
    "partikulu": {
        "kods": "q"
    },
    "saīsinājumu": {
        "kods": "y",
        "tips": {
            "sugasvārda": "n",
            "īpašvārda": "p",
            "īpašības vārda": "a",
            "verbālo": "v",
            "apstākļā": "r",
            "diskursa iezīmētāja": "d"
        }
    },
    "pieturzīmi": {
        "kods": "z",
        "tips": {
            "komats": "c",
            "pēdiņa": "q",
            "punkts": "s",
            "iekava": "b",
            "defise/domu zīme": "d",
            "kols": "o",
            "citu": "x"
        }
    },
    "bezmorfoloģijas elementus": {
        "kods": "x",
        "tips": {
            "vārdus svešvalodā": "f",
            "skaitļi cipariem": "n",
            "kārtas skaitļi cipariem": "o",
            "URI": "u",
            "citus": "x"
        }
    }
}

# def generate_cql_entries(data):
#     results = []


#     for pos, pos_data in data.items():
#         pos_query_list = []
#         prompt_str = ""
#         query = ""

#         pos_code = pos_data.get("kods")
        
#         prompt_str += pos
#         query += pos_code

#         for pos_key, pos_val in pos_data:
    

#         # results.append({
#         #     "cql": f'[tag="{query}"]',
#         #     "prompt": prompt_str,
#         #     "type": "T"
#         # })
    
#     return results

import re

def generate_cql_tags_limited(data_dict, max_active_settings=5):
    """
    Generates CQL tags but limits complexity to prevent memory crashes.
    
    Args:
        data_dict (dict): The dictionary of attributes.
        max_active_settings (int): Maximum number of attributes allowed to have 
                                   values simultaneously (default 5).
                                   remaining attributes will be skipped ('.').
    """
    for pos_name, attributes in data_dict.items():
        # 1. Extract prefix
        prefix = attributes.get("kods", "")
        
        # 2. Get attribute keys (excluding 'kods') in a fixed order
        # We store keys in a list to access them by index later
        attr_keys = [k for k in attributes.keys() if k != "kods"]
        total_attrs = len(attr_keys)
        
        # 3. Pre-process options for all keys to avoid re-parsing inside loops
        # options_map[key_index] = list of (Description, Code)
        options_map = {}
        
        for i, key in enumerate(attr_keys):
            val = attributes[key]
            opts = []
            
            if isinstance(val, dict):
                for desc, code in val.items():
                    opts.append((desc, code))
            elif isinstance(val, list):
                for item in val:
                    opts.append((item, item))
            elif isinstance(val, str):
                opts.append((val, val))
            
            options_map[i] = opts

        # 4. Generate combinations based on "Active Settings" limit
        # We loop from 0 active settings (all skipped) up to max_active_settings
        # If total_attrs < max_active, we stop at total_attrs
        
        limit = min(total_attrs, max_active_settings)
        
        for r in range(limit + 1):
            # Pick 'r' indices to be ACTIVE (have values)
            # The rest will be SKIPPED (force value '.')
            for active_indices in itertools.combinations(range(total_attrs), r):
                
                # Convert tuple of indices to a set for fast lookup
                active_set = set(active_indices)
                
                # Build the list of lists for itertools.product
                current_product_args = []
                
                for i in range(total_attrs):
                    if i in active_set:
                        # Use the real options we parsed earlier
                        current_product_args.append(options_map[i])
                    else:
                        # Force this key to be skipped
                        # Description is empty, Code is '.'
                        current_product_args.append([("", ".")])
                
                # Generate Cartesian product for this specific configuration of active keys
                for combo in itertools.product(*current_product_args):
                    # combo is a tuple of (Description, Code)
                    
                    # Extract Descriptions (filter empty ones)
                    desc_parts = [pos_name] + [item[0] for item in combo if item[0]]
                    
                    # Extract Codes
                    code_parts = [item[1] for item in combo]
                    
                    # Construct Raw Tag
                    raw_tag = prefix + "".join(code_parts)
                    
                    # formatting: replace trailing dots with .*
                    if "." in raw_tag:
                        final_tag = re.sub(r'\.+$', '.*', raw_tag)
                    else:
                        final_tag = raw_tag

                    final_name = ", ".join(reversed(desc_parts))
                    
                    yield ({
                        "cql": f'tag="{final_tag}"',
                        "prompt": final_name,
                        "type": "T"
                    })


# with open("data/t_data_v3.json", "w", encoding="utf-8") as f:
#     json.dump(output, f, indent=2, ensure_ascii=False)

output = generate_cql_tags_limited(t_val, max_active_settings=5)

with open('data/t_data.json', 'w') as f:
    f.write("[\n")
    for result in output:
        json.dump(result, f, indent=2, ensure_ascii=False)
        f.write(",\n")
    f.write("]")


# # Just to prove it works without crashing, we iterate and print a few
# try:
    
                

#             # print(f"Sample {counter}: {result}")
            
#     print(f"Total combinations generated: {counter}")
    
# except KeyboardInterrupt:
#     print("Stopped by user.")

# with open('data/t_data_v3.json', 'a') as f:
    


# with open("data/t_data_v3.json", "w", encoding="utf-8") as f:
#     json.dump(output, f, indent=2, ensure_ascii=False)

print("done")