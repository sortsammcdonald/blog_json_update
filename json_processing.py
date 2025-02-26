import json

# Load JSON data from a file
with open('entries.json', 'r') as file:
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

# Remove duplicates from the data
cleaned_data = remove_all_duplicates(data)

# Save the updated data back to the file
with open('entries.json', 'w') as file:
    json.dump(cleaned_data, file, indent=4)

