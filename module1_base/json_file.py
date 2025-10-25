import json


new_dict = {
    "Name": "File",
    "Age": 18,
    "Country": 'Russia'
}

with open("config.json", "w") as f:
    json.dump(new_dict, f)

with open("config.json") as f:
    json_dict = json.load(f)

print(json_dict)
