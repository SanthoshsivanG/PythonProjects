import csv
import easyocr
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import json
import sys
import google.generativeai as genai
import Create_Flashcard

# Initialize EasyOCR reader for Japanese
reader = easyocr.Reader(['ja'], gpu=False)

# Define the main GUI window
root = tk.Tk()
root.title("Japanese Text Extractor")
root.geometry("500x200")

def load_api_key():
    if getattr(sys, 'frozen', False):  # Check if running as a PyInstaller bundle
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.abspath(".")

    config_path = os.path.join(base_path, 'config.json')

    try:
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
            api_key = config.get("api_key")
            if not api_key:
                raise ValueError("API key is missing in config.json.")
            genai.configure(api_key=api_key)
    except FileNotFoundError:
        messagebox.showerror("Error",
                             "Config file 'config.json' not found in the executable directory. Please create it and add your API key.")
        root.destroy()  # Close the GUI if config file is missing
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        root.destroy()  # Close the GUI if API key is missing
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        root.destroy()

# Load API key
load_api_key()

# Function to select image and extract Japanese text
def extract_text_from_image():
    image_path = filedialog.askopenfilename(title="Select Image",
                                            filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if not image_path:
        return

    output_file = filedialog.asksaveasfilename(
        title="Save Extracted Words",
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        initialfile="extracted_japanese_words.csv"
    )
    if not output_file:
        return

    try:
        results = reader.readtext(image_path, detail=0)
        japanese_text = ' '.join(results)
        extracted_words = japanese_text.split()

        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Japanese Word'])
            for word in extracted_words:
                writer.writerow([word])

        messagebox.showinfo("Success", "CSV file generated successfully with extracted words.")
        os.startfile(output_file)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to generate flashcards
def generate_flashcards_gui():
    try:
        Create_Flashcard.generate_flashcards()
        messagebox.showinfo("Success", "Flashcard CSV file generated successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Add label and buttons to the window
label = tk.Label(root, text="Japanese Text Extraction and Flashcard Generation", font=("Arial", 14))
label.pack(pady=20)

extract_button = tk.Button(root, text="Step 1 : Select Image and Target CSV", command=extract_text_from_image,
                           font=("Arial", 12), width=40)
extract_button.pack(pady=10)

flashcard_button = tk.Button(root, text="Step 2 : Generate Flashcards Items to CSV", command=generate_flashcards_gui,
                             font=("Arial", 12), width=40)
flashcard_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
