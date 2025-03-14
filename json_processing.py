import json

class CorrectJson:
    def __init__(self, filepath, output_filepath):
        self.filepath = filepath
        self.output_filepath = output_filepath  # Add output file path

    def extract_entries(self):
        # Load JSON data from a file
        with open(self.filepath, 'r') as file:
            data = json.load(file)
        return data  # Return data so it can be used

    def remove_all_duplicates(self, data):
        seen = set()
        unique_data = []
        for item in data:
            # Convert dictionary to a frozenset of its items to make it hashable
            item_frozenset = frozenset(item.items())
            if item_frozenset not in seen:
                seen.add(item_frozenset)
                unique_data.append(item)
        return unique_data  # Return the cleaned list

    def gen_correct_json(self):
        # Extract and process the data
        data = self.extract_entries()
        unique_data = self.remove_all_duplicates(data)

        # Write cleaned data to output file
        with open(self.output_filepath, 'w') as file:
            json.dump(unique_data, file, indent=4)


def main():
    json_to_check = CorrectJson('entries.json','entries.json')
    json_to_check.gen_correct_json()

# Remove duplicates from the data

# Save the updated data back to the file

