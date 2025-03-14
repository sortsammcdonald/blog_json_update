import unicodedata
import markdown
import re
import json
import os

class FileToProcess:
    def __init__(self, filepath):
        self.filepath = filepath

    def extract_content(self): 
        # Need to review removing Astro specific material
        # Only need to prepare one content list
        capturing = False
        content = []
        additional_content = []
        second_marker_found = False
        with open(self.filepath, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line == "---":
                    capturing = not capturing  # Toggle capturing state
                    if capturing and additional_content:
                        break  # Stop if second marker found
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
        cleaned_html = re.sub(r'\s+', ' ', html)  # Collapse multiple spaces to one
        cleaned_html = re.sub(r'^\s+|\s+$', '', cleaned_html, flags=re.MULTILINE)  # Trim spaces at each line's start and end
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
            with open(self.json_file, 'r+', encoding='utf-8')as file:
                try:
                    data = json.load(file)  # Load existing JSON
                except json.JSONDecodeError:
                    data = []  # If file is empty or corrupt, reset it

                data.append(new_data)
                file.seek(0)
                file.truncate()
                json.dump(data, file, indent=4)

        except FileNotFoundError:
            # If file doesn't exist, create it
            with open(self.json_file, 'w', encoding='utf-8') as file:
                json.dump([new_data], file, indent=4)
def main():

    

    cc_type = ['CC BY: https://creativecommons.org/licenses/by/4.0/', 'CC BY-SA: https://creativecommons.org/licenses/by-sa/4.0/', 'CC BY-NC: https://creativecommons.org/licenses/by-nc/4.0/', 'CC BY-NC-SA: https://creativecommons.org/licenses/by-nc-sa/4.0/', 'CC BY-ND: https://creativecommons.org/licenses/by-nd/4.0/', 'CC BY-NC-ND: https://creativecommons.org/licenses/by-nc-nd/4.0/', ' CC0: https://creativecommons.org/publicdomain/zero/1.0/']


    def create_json(md_to_process):
        text_processor = FileToProcess(md_to_process)
        primary_content, secondary_content = text_processor.extract_content()
        primary_filename = 'processed_header.txt'
        secondary_filename = 'additional_content.txt'

        text_processor.write_to_file(primary_filename, primary_content)
        text_processor.write_to_file(secondary_filename, secondary_content)
        dict_processor = GenDict(primary_content)  # Generate dictionary from primary content
        prim_dict = dict_processor.gen_dict()
        html_processor = GenHtml(secondary_content)  # Generate HTML from secondary content
        html_text = html_processor.gen_html()

        prim_dict = dict_processor.supplement_dict(html_text, 'html')
        prim_dict = dict_processor.supplement_dict(cc_type[0], 'license')

        json_file = UpdateJSON('entries.json')
        json_output = json_file.append_json(prim_dict)

        #return json_output

    #prim_dict['html'] = html_text
    #prim_dict['license'] = cc_type[0]
    
    #print(prim_dict)
    #print(html_text)


    # with open('entries.json', 'w') as file:
    #     json.dump(prim_dict,file, indent=4)

    
    #test = create_json('test_file3.md')
    #test
    #ls_md_files = LsMdocs('test')

    #file_path = '/home/sammcdonald/Documents/coding_projects/blog_json_update/test'
    
    file_path = os.path.abspath('test')  # Convert 'test' to an absolute path

    if not os.path.exists(file_path):
        print(f"Error: The directory {file_path} does not exist.")
        return

    ls_md_files = LsMdocs(file_path)
    for md_file in ls_md_files:
        create_json(md_file)
    
    for i in LsMdocs(file_path):
    #    print(i)
        create_json(i)

    #create_json(file_path)
    #create_json('test_file3.md')

if __name__ == '__main__':
    main()



