# Sinhala Grammar and Spell Checker

This repository contains a Python-based Sinhala Grammar and Spell Checker application. It uses Tkinter for the graphical user interface (GUI) and fuzzy string matching to provide spelling suggestions and grammar corrections. The tool processes Sinhala text input to check for spelling errors and apply grammar rules for improved accuracy and readability.

## Features

1. **Spell Checking:**
   - Identifies misspelled Sinhala words.
   - Provides up to three suggestions for corrections using fuzzy matching.

2. **Grammar Checking:**
   - Analyzes sentences based on predefined grammar rules.
   - Applies appropriate corrections to match the grammar standards.

3. **User-Friendly Interface:**
   - Built with Tkinter for a simple and intuitive GUI.
   - Provides real-time feedback and suggestions.

## Directory Structure

```plaintext
.
├── dic/
│   ├── sinhalaDic.text    # Dictionary file containing valid Sinhala words.
│   ├── sinhalaGrm.text    # Grammar rules for sentence correction.
│   └── sinhalaSub.text    # Subject-specific grammar data.
├── main.py                # Main Python file for the application.
└── README.md              # Documentation for the repository.
```

## Installation

1. Clone the repository:

  https://github.com/kevin00005/Sinhala-spell-grammer-checker.git
   ```

2. Install the required dependencies:

   pip install fuzzywuzzy
   ```

3. Run the application:

   python main.py
   ```

## Usage

1. Launch the application by running `main.py`.
2. Enter your Sinhala sentence in the input box.
3. Click "Check Grammar" to perform both spell checking and grammar correction.
4. Click "Check Spelling" to perform only spell checking.
5. View the results in the output box below.

## File Descriptions

- **`main.py`**
  - The main application file, implementing the spell checker, grammar checker, and GUI interface.

- **`dic/sinhalaDic.text`**
  - A text file containing a list of valid Sinhala words for spell checking.

- **`dic/sinhalaGrm.text`**
  - A text file containing grammar rules for correcting sentences.

- **`dic/sinhalaSub.text`**
  - A text file with subject-specific grammar data to apply corrections based on context.

## How It Works

1. **Spell Checking:**
   - Reads the Sinhala dictionary file.
   - Compares input words with dictionary entries using fuzzy string matching.
   - Suggests the closest matches for misspelled words.

2. **Grammar Checking:**
   - Reads grammar rules and subject-specific data.
   - Identifies subjects in the input text.
   - Applies relevant grammar rules to correct the sentences.

3. **GUI Interaction:**
   - Provides a user interface for input and output.
   - Displays suggestions and corrected sentences in real-time.

## Requirements

- Python 3.6 or later
- Libraries:
  - `tkinter` (built-in with Python)
  - `fuzzywuzzy`

## Known Issues

- Requires the dictionary and grammar files to be present in the `dic/` folder.
- Limited to the accuracy and coverage of the dictionary and grammar rules.



## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgements

- [FuzzyWuzzy](https://github.com/seatgeek/fuzzywuzzy) for string matching.
- Sinhala language enthusiasts for providing grammar and dictionary data.

---



