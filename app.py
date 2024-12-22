import tkinter as tk
from tkinter import messagebox
from fuzzywuzzy import fuzz
import re

# Function to check and suggest corrections for a word
def check_and_suggest(word):
    try:
        with open("./dic/sinhalaDic.text", "r", encoding="UTF-8") as f:
            contents = f.read()
            dictionary = [
                w.lower().replace('\u200d', '')
                for w in contents.splitlines()
            ]
    except FileNotFoundError:
        return "Dictionary file not found. Please ensure the file is in the correct location."

    word = word.lower().replace('\u200d', '')

    if word in dictionary:
        return "No suggestions found."

    suggestions = sorted(
        dictionary,
        key=lambda x: fuzz.ratio(word, x),
        reverse=True
    )[:3] 

    return suggestions if suggestions else "No suggestions found."

# Function to check and suggest corrections for a sentence
def check_and_suggest_sentence(sentence):
    words = sentence.split()
    corrected_sentence = []
    errors = []

    for word in words:
        clean_word = re.sub(r'[^\u0D80-\u0DFF]', '', word)
        suggestions = check_and_suggest(clean_word)

        if suggestions != "No suggestions found.":
            errors.append((clean_word, suggestions))
            corrected_word = word.replace(clean_word, suggestions[0])
            corrected_sentence.append(corrected_word)
        else:
            corrected_sentence.append(word)

    error_report = ""
    if errors:
        for error in errors:
            error_report += f"Error: '{error[0]}', Suggestions: {', '.join(error[1])}\n"

    corrected_paragraph = ' '.join(corrected_sentence)
    return error_report, corrected_paragraph

# Function to correct sentences using grammar rules
def correct_sentence_with_rules(text):
    try:
        with open("./dic/sinhalaGrm.text", "r", encoding="UTF-8") as f:
            contents = f.read()

        with open("./dic/sinhalaSub.text", "r", encoding="UTF-8") as f:
            subjects = [line.strip() for line in f.readlines() if line.strip()]

    except FileNotFoundError:
        return "Required file(s) not found. Please ensure the files are in the correct location."
