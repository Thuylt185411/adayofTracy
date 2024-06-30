import csv
import os
import re
import pandas as pd

# Define the path to the directory containing the text files
path = "C:/Users/Seni/PycharmProjects/adayofTracy/anki/filetxt"

# List all .txt files in the directory
file_names = [str(f).replace('.txt', '') for f in os.listdir(path) if f.endswith('.txt')]

# Function to check if a line is an answer
def is_title(line):
    return re.match(r'^[IVXLCDM]+\.', line)
def is_answerA(line):
    return re.match(r'^a\)', line)
def is_answerB(line):
    return re.match(r'^b\)', line)
def is_answerC(line):
    return re.match(r'^c\)', line)
def is_answerD(line):
    return re.match(r'^d\)', line)

# Function to check if a line is a key
def is_key(line):
    return len(str(line).strip()) == 1 and line.isupper()
list_title = []


# Process each file
for file_name in file_names:
    file_path = os.path.join(path, file_name + '.txt')  # Use os.path.join for better path handling
    questions = []

    # Open and read the file
    with open(file_path, encoding="utf-8") as f:
        current_question = {'no':'', 'type': '', 'question': '',  'answerA': '', 'answerB': '', 'answerC': '', 'answerD': '', 'key': ''}
        for line in f:
            line = line.strip()

            if is_answerA(line):  # Answer A
                current_question['answerA'] = line
            elif is_answerB(line):  # Answer B
                current_question['answerB'] = line
            elif is_answerC(line):  # Answer C
                current_question['answerC'] = line
            elif is_answerD(line):  # Answer D
                current_question['answerD'] = line
            elif is_key(line):  # Key
                if line == 'A': current_question['key'] = 1
                elif line == 'B': current_question['key'] = 2
                elif line == 'C': current_question['key'] = 3
                elif line == 'D': current_question['key'] = 4

                questions.append(current_question)  # Save the current question
                current_question = {'no':'', 'type': '', 'question': '', 'answerA': '', 'answerB': '', 'answerC': '', 'answerD': '', 'key': ''}

            elif is_title(line):
                list_title.append(line)
                if len(list_title) > 1:
                    data_df = pd.DataFrame(questions)
                    data_df = data_df.dropna()
                    file_path_csv = os.path.join('C:/Users/Seni/PycharmProjects/adayofTracy/anki/filecsv',
                                                 str(len(list_title)-1) + file_name + '.csv')
                    data_df.to_csv(file_path_csv, sep='|', index=False)
                    questions = []


            else:
                # If the line is not an answer or a key, it's part of the question
                if current_question['question']:
                    current_question['question'] += ' '
                current_question['question'] += line
                current_question['no'] = current_question['question'][:10]


        # Don't forget to add the last question if it doesn't end with a key
        if current_question['question']:
            questions.append(current_question)

    # Convert the list of questions to a DataFrame
    data_df = pd.DataFrame(questions)
    data_df = data_df.dropna()

    # Define the output CSV file path
    file_path_csv = os.path.join('C:/Users/Seni/PycharmProjects/adayofTracy/anki/filecsv', file_name + '.csv')
    # Save DataFrame to CSV
    data_df.to_csv(file_path_csv, sep='|', index=False)