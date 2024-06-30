import os
import re
import pandas as pd

# Define the path to the directory containing the text files
input_path = "C:/Users/Seni/PycharmProjects/adayofTracy/anki/filetxt"
output_path = "C:/Users/Seni/PycharmProjects/adayofTracy/anki/filecsv"

# Ensure output directory exists
os.makedirs(output_path, exist_ok=True)

# Regex patterns for identifying titles, answers, and keys
title_pattern = re.compile(r'^[IVXLCDM]+\.')
answer_pattern = re.compile(r'^[abcd]\)')
key_pattern = re.compile(r'^[A-D]$')

# List all .txt files in the directory
file_names = [f for f in os.listdir(input_path) if f.endswith('.txt')]

# Process each file
for file_name in file_names:
    with open(os.path.join(input_path, file_name), 'r', encoding='utf-8') as file:
        current_questions = []
        current_title = None
        for line in file:
            line = line.strip()
            if title_pattern.match(line):  # New title found
                # If there are questions under the previous title, save them to a CSV
                if current_questions and current_title:
                    df = pd.DataFrame(current_questions)
                    title_for_filename = re.sub(r'[^a-zA-Z0-9]+', '_', current_title)
                    df.to_csv(os.path.join(output_path, f"{title_for_filename}.csv"), sep='|', index=False)
                    current_questions = []  # Reset for the next title
                current_title = line  # Update the current title
            elif line:
                # Process question, answer, or key
                if answer_pattern.match(line) or key_pattern.match(line):
                    if key_pattern.match(line):
                        current_questions[-1]['key'] = line
                    else:
                        answer_key = 'answer_' + line[0].upper()
                        current_questions[-1][answer_key] = line[3:]
                else:
                    # New question
                    current_questions.append({'question': line, 'answer_A': '', 'answer_B': '', 'answer_C': '', 'answer_D': '', 'key': ''})

        # Don't forget to save the last title's questions to a CSV
        if current_questions and current_title:
            df = pd.DataFrame(current_questions)
            title_for_filename = re.sub(r'[^a-zA-Z0-9]+', '_', current_title)
            df.to_csv(os.path.join(output_path, f"{title_for_filename}.csv"), sep='|', index=False)