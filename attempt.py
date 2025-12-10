import requests
import json

# Your JSON structure
json_data = {
    "concordance_query": [
        {
            "queryselector": "cqlrow",
            "cql": "[lemma=\"pie\" & tag=\"s.*\"] [tag=\"n.*\"]",
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

# Option 1: Let requests handle everything
response = requests.get(
    'https://nosketch.korpuss.lv/bonito/run.cgi/concordance',
    params={
        'corpname': 'LVK2022',
        'pagesize': 5,
        'json': json.dumps(json_data, separators=(',', ':'))  # requests will URL-encode this automatically
    }
)

print(response.text)
# data = response.json()
# kwic = data['Lines'][0]['Kwic'][0]['str']
# print(data)