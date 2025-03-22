# Overview

Decided to look at this project again, my goal is to:
- Update the code to that to generate a JSON feed based on Squarespace blog post.
- Use the JSON feed to generate a RAG implementation for an LLM to answer questions relevant to to the topics.

# 2025.03.22

I have refactored the code so now all functions are defined before main. 

Still need to work out how to append single file.

# 2025.03.14

I've updated the `md_to_json` and `json_processing` files. I think I will keep them seperate so `md_to_json` is used generate the initial json file, while `json_processing` will be used to add new entries to existing files and check there are no duplicate entries.

Creating an append function is quite challenging. Will have to review this next time.

## Next steps
- Add append function to `json_processing`.

# 2025.03.08

Had to adjust the md_to_json file, it wasn't adding all entries to JSON file.

Next have to update JSON processing file and integrate into md_to_json file.

# 2025.03.04

Encapulasted the steps in main into a function. Maybe could be tidier in function, but I think this could enable me to iterate over multiple files in a folder. 

The programme can now iterate over all files in a directory to build a JSON file.

# 2025.03.01

Not too much progress today. Still debating best way to check for new entries 

# 2025.02.28

In addition to some more json operations I would like to implement some file operations, in particular creating a source of existing files that can be checked against if new files are added.

When new files are found this could then also trigger updating the JSON file.

Maybe I should review the Think Python chapter on [files](https://allendowney.github.io/ThinkPython/chap13.html) 

# 2025.02.26

- Added json_processing programme

This file should contain all code for processing the JSON file. Currently it only has function to check for replicate entries in a JSON file. But I should move over json functions in md_to_json to that file.

Also it's not a well written programme at this stage.

# 2024.12.19

In testing the programme works, I should be able to create a JSON file containing all my main blog's posts. 

Extracting the text from it is likely to be quite tedious, could be a low energy, annoying task to tackle during the holidays.

# 2024.12.18

Looks like I will have to include meta-data similar to that used by Astro to format the JSON correctly.

I should take a sample blog, add the metadata, and test the programme to see if it works.

# 2024.12.17 

Need to remove functions related to Astro formatting