import os
from google.generativeai import GenerativeModel
import csv
import json
from tkinter import filedialog, messagebox

def generate_flashcards():
    # Prompt user to select the input file (extracted Japanese words CSV)
    input_file_path = filedialog.askopenfilename(
        title="Select Extracted Words CSV",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    if not input_file_path:
        messagebox.showwarning("Input Needed", "Please select an input CSV file.")
        return

    # Prompt user to select the output location for flashcard CSV file
    output_file_path = filedialog.asksaveasfilename(
        title="Save Flashcard CSV",
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        initialfile="flashcard_info.csv"
    )
    if not output_file_path:
        messagebox.showwarning("Output Needed", "Please select a location to save the flashcard CSV file.")
        return

    # Define the generation configuration for the Gemini AI model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    # Initialize the model
    model = GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    # Start a chat session
    chat_session = model.start_chat(history=[])

    # Send the initial format instruction prompt without processing output
    initial_instruction = "Reply only with the following format: {\"hiragana\": \"hiragana reading\", \"meaning\": \"English meaning\"}"
    chat_session.send_message(initial_instruction)

    try:
        # Read the extracted words from the input CSV file
        with open(input_file_path, mode='r', encoding='utf-8') as input_csvfile:
            reader = csv.reader(input_csvfile)
            next(reader)  # Skip header
            kanji_words = [row[0] for row in reader if row]

        # Send the combined prompt for all kanji words
        combined_prompt = " | ".join([f"{kanji} Reply only with the following format: {{\"hiragana\": \"hiragana reading\", \"meaning\": \"English meaning\"}}" for kanji in kanji_words])
        response = chat_session.send_message(combined_prompt)
        response_text = response.text

        # Write results to the output CSV file
        with open(output_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Question', 'Answer'])

            response_data_list = response_text.split('|')
            for kanji_word, response_data in zip(kanji_words, response_data_list):
                try:
                    response_data = json.loads(response_data)
                    hiragana_reading = response_data.get("hiragana", "")
                    english_meaning = response_data.get("meaning", "")
                    writer.writerow([kanji_word, f"{hiragana_reading}, {english_meaning}"])
                except json.JSONDecodeError:
                    print(f"Error decoding JSON for word: {kanji_word} with response: {response_data}")
                except Exception as e:
                    print(f"An error occurred for word: {kanji_word} with response: {response_data}. Error: {e}")

        messagebox.showinfo("Success", "Flashcard CSV file generated successfully.")
        os.startfile(output_file_path)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")