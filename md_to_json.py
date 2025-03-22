import unicodedata
import markdown
import re
import json
import os

class FileToProcess:
    def __init__(self, filepath):
        self.filepath = filepath

    def extract_content(self): 
        capturing = False
        content = []
        additional_content = []
        with open(self.filepath, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line == "---":
                    capturing = not capturing
                    continue
                if capturing:
                    content.append(line)
                else:
                    additional_content.append(line)
        return content, additional_content

    def write_to_file(self, filename, content):
        with open(filename, 'w', encoding='utf-8') as file:
            for line in content:
                file.write(line + '\n')

class GenDict:
    def __init__(self, content):
        self.content = content
        self.ref_dict = {}

    def gen_dict(self):
        for line in self.content:
            if ':' in line:
                key, value = line.split(':', 1)
                self.ref_dict[key.strip()] = value.strip()
        return self.ref_dict    
    
    def supplement_dict(self, content_val, key_name):
        self.ref_dict[key_name] = content_val
        return self.ref_dict

class GenHtml:
    def __init__(self, content):
        self.content = content

    def gen_html(self):
        html = markdown.markdown(' '.join(self.content))
        cleaned_html = re.sub(r'\s+', ' ', html)
        cleaned_html = re.sub(r'^\s+|\s+$', '', cleaned_html, flags=re.MULTILINE)
        return cleaned_html

class LsMdocs:
    def __init__(self, directory):
        self.directory = directory

    def gen_ls_files(self):
        return [os.path.join(self.directory, f) for f in os.listdir(self.directory) if os.path.isfile(os.path.join(self.directory, f))]

    def __iter__(self):
        return iter(self.gen_ls_files())

class UpdateJSON:
    def __init__(self, json_file):
        self.json_file = json_file

    def append_json(self, new_data):
        try:
            with open(self.json_file, 'r+', encoding='utf-8') as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = []
                data.append(new_data)
                file.seek(0)
                file.truncate()
                json.dump(data, file, indent=4)
        except FileNotFoundError:
            with open(self.json_file, 'w', encoding='utf-8') as file:
                json.dump([new_data], file, indent=4)

class JsonEntry:
    def __init__(self, md_to_process):
        self.md_to_process = md_to_process

    def create_json(self):
        text_processor = FileToProcess(self.md_to_process)
        primary_content, secondary_content = text_processor.extract_content()
        dict_processor = GenDict(primary_content)
        prim_dict = dict_processor.gen_dict()
        html_processor = GenHtml(secondary_content)
        html_text = html_processor.gen_html()
        prim_dict = dict_processor.supplement_dict(html_text, 'html')
        json_file = UpdateJSON('entries.json')
        json_file.append_json(prim_dict)

class Entries:
    def __init__(self, directory):
        self.directory = directory

    def gen_entries(self):
        file_path = os.path.abspath(self.directory)
        if not os.path.exists(file_path):
            print(f"Error: The directory {file_path} does not exist.")
            return
        ls_md_files = LsMdocs(file_path)
        for md_file in ls_md_files:
            entry = JsonEntry(md_file)
            entry.create_json()

def main():
    # Generate initial entries file
    directory = 'test'  
    entries = Entries(directory)
    entries.gen_entries()

if __name__ == '__main__':
    main()
