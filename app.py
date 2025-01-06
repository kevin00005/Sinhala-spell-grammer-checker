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

    corrections_data = {}
    subject = None
    for line in contents.splitlines():
        line = line.strip()
        if not line:
            continue
        if ":" in line:
            subject = line[:-1]
            corrections_data[subject] = {}
        elif "->" in line:
            incorrect, correct = line.split("->")
            corrections_data[subject][incorrect.strip()] = correct.strip()

    sentences = [s.strip() for s in text.replace(",", ".").split(".") if s.strip()]

    corrected_sentences = []

    for sentence in sentences:
        words = sentence.split()
        if not words:
            corrected_sentences.append(sentence)
            continue

        applicable_corrections = {}
        matched_subjects = []

        for word in words:
            if word in subjects:
                matched_subjects.append(word)
                for key, rules in corrections_data.items():
                    if word in key.split(","):
                        applicable_corrections = {**applicable_corrections, **rules}

        # Apply corrections based on matched subjects
        corrected_sentence = sentence
        for incorrect, correct in applicable_corrections.items():
            if incorrect in corrected_sentence:
                corrected_sentence = re.sub(rf'\b{re.escape(incorrect)}\b', correct, corrected_sentence)

        corrected_sentences.append(corrected_sentence)

    corrected_text = ". ".join(corrected_sentences) + "." if corrected_sentences else ""
    return corrected_text

# Function to handle user input and display results
def process_input():
    user_input = input_text.get("1.0", tk.END).strip()

    if not user_input:
        messagebox.showerror("Error", "Please enter a sentence.")
        return

    # Step 1: Perform spell check
    spell_check_errors, spell_checked_sentence = check_and_suggest_sentence(user_input)

    # Step 2: Perform grammar check on the spell-checked sentence
    grammar_checked_sentence = correct_sentence_with_rules(spell_checked_sentence)

    # Display results
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, f"Spell Check Result:\n{spell_check_errors}\n\n")
    result_text.insert(tk.END, f"Grammar Check Result:\n{grammar_checked_sentence}")

# Function to handle spell check only
def process_spell_check():
    user_input = input_text.get("1.0", tk.END).strip()

    if not user_input:
        messagebox.showerror("Error", "Please enter a sentence.")
        return

    # Perform spell check only
    spell_check_errors, spell_checked_sentence = check_and_suggest_sentence(user_input)

    # Display results
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, f"Spell Check Result:\n{spell_check_errors}\n\n")
    result_text.insert(tk.END, f"Corrected Sentence (Spell Check Only):\n{spell_checked_sentence}")

# Creating the UI
root = tk.Tk()
root.title("Sinhala Grammar and Spell Checker")
root.geometry("1000x800")

# Input label and text box
input_label = tk.Label(root, text="Enter your sentence:")
input_label.pack(pady=5)

input_text = tk.Text(root, height=12, width=100)
input_text.pack(pady=5)

# Buttons to process the input
process_button = tk.Button(root, text="Check Grammar", command=process_input)
process_button.pack(pady=5)

spell_check_button = tk.Button(root, text="Check Spelling ", command=process_spell_check)
spell_check_button.pack(pady=5)

# Result label and text box
result_label = tk.Label(root, text="Results:")
result_label.pack(pady=5)

result_text = tk.Text(root, height=26, width=100, state="normal")
result_text.pack(pady=5)

# Run the application
root.mainloop()
