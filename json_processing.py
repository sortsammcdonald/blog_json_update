import json

class CorrectJson:
    def __init__(self, filepath):
        self.filepath = filepath

    def extract_entries(self):
        # Load JSON data from a file
        with open(self.filepath, 'r') as file:
            data = json.load(file)

    def remove_all_duplicates(data):
        seen = set()
        unique_data = []
        for item in data:
            # Convert dictionary to a frozenset of its items to make it hashable
            item_frozenset = frozenset(item.items())
            if item_frozenset not in seen:
                seen.add(item_frozenset)
                unique_data.append(item)
        return unique_data
    
class GenJson
    def __init__(self, json_to_check):
        self.json_to_check = json_to_check

    def gen_correct_json(self):
        with open(self.json_to_check, 'w') as file:
            json.dump(self.json_to_check, file, indent=4)
   

# Remove duplicates from the data

# Save the updated data back to the file

