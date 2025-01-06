import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.models import load_model
import os

# Step 1: Load the Dataset
def load_data(filepath):
    data = pd.read_csv(filepath)
    # Handle missing or non-string values
    data['misspelled'] = data['misspelled'].fillna("").astype(str)
    data['corrected'] = data['corrected'].fillna("").astype(str)
    return data['misspelled'].tolist(), data['corrected'].tolist()

# Step 2: Train the Spell Checker Model
def train_spell_checker(x_train, y_train):
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(x_train + y_train)

    x_train_seq = tokenizer.texts_to_sequences(x_train)
    y_train_seq = tokenizer.texts_to_sequences(y_train)

    # Remove empty sequences
    x_train_seq = [seq for seq in x_train_seq if seq]
    y_train_seq = [seq for seq in y_train_seq if seq]

    # Determine max sequence length
    max_len = max(len(seq) for seq in x_train_seq + y_train_seq)

    # Pad sequences
    x_train_pad = pad_sequences(x_train_seq, maxlen=max_len, padding='post')
    y_train_pad = pad_sequences(y_train_seq, maxlen=max_len, padding='post')

    vocab_size = len(tokenizer.word_index) + 1

    model = Sequential([
        Embedding(vocab_size, 128, input_length=max_len),
        LSTM(128, return_sequences=True),
        Dense(vocab_size, activation='softmax')
    ])

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    y_train_pad = np.expand_dims(y_train_pad, -1)  # Reshape for sparse_categorical_crossentropy
    model.fit(x_train_pad, y_train_pad, epochs=20, batch_size=32)

    return model, tokenizer, max_len

# Step 3: Improved Grammar Checker Logic
def grammar_checker(sentence):
    words = sentence.split()
    if not words:
        return sentence  # Handle empty input gracefully

    if sentence.startswith("මම") and words[-1].endswith("මු"):
        words[-1] = words[-1][:-1] + "මි"  # Change verb ending for "මම"
    elif sentence.startswith("අපි") and words[-1].endswith("මි"):
        words[-1] = words[-1][:-1] + "මු"  # Change verb ending for "අපි"

    return " ".join(words)


# Step 4: Save and Load the Model
def save_model(model, tokenizer, max_len, filepath):
    model.save(filepath)
    with open(filepath + '_tokenizer.npy', 'wb') as f:
        np.save(f, tokenizer.word_index)
        np.save(f, [max_len])

def load_saved_model(filepath):
    model = load_model(filepath)
    with open(filepath + '_tokenizer.npy', 'rb') as f:
        word_index = np.load(f, allow_pickle=True).item()
        max_len = int(np.load(f)[0])

    tokenizer = Tokenizer()
    tokenizer.word_index = word_index
    return model, tokenizer, max_len

# Main Application
if __name__ == "__main__":
    if not os.path.exists('spell_checker_model.h5'):
        # Load dataset
        misspelled, corrected = load_data('spell_data.csv')

        # Train the model
        model, tokenizer, max_len = train_spell_checker(misspelled, corrected)

        # Save the model
        save_model(model, tokenizer, max_len, 'spell_checker_model.h5')
        print("Model trained and saved.")
    else:
        # Load pre-trained model
        model, tokenizer, max_len = load_saved_model('spell_checker_model.h5')
        print("Model loaded.")

    # Input loop
    if __name__ == "__main__":
        while True:
            user_input = input("\nEnter a Sinhala sentence (type 'exit' to quit): ")
            if user_input.lower() == "exit":
                break

            # Spell Check
            input_seq = pad_sequences(tokenizer.texts_to_sequences([user_input]), maxlen=max_len, padding='post')
            prediction = model.predict(input_seq)
            corrected_indices = np.argmax(prediction[0], axis=-1)
            corrected_sentence = tokenizer.sequences_to_texts([corrected_indices])[0]
            print("Corrected Sentence:", corrected_sentence)

            # Grammar Check
            grammar_checked = grammar_checker(user_input)
            print("Grammar Checked Sentence:", grammar_checked)
