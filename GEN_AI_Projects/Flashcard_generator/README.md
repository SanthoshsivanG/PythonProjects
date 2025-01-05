# Flashcard generator for Kanji

I have been using Quizlet for long time to study and revise kanji for Japanese studies.
Even though Quizlet does a great job by providing easy ways to create flashcard , I want to automate the process.

I used to enter every kanji on Quizlet and their corresponding English meaning and Hiragana readings manually. So, I decided to automate it using python by following steps

Step 1 : Take screenshot of a page that contain kanji readings 

Step 2 : Using Python, Generate a csv file (a) of all the kanji words present in the screenshot

Step 3 : send the contents of the csv file (a) one by one to Gemini AI and ask for Hiragana and English meaning of that respective kanjis and store it in another csv file(b)

Step 4 : Upload the csv file(b) to Quizlet to generate all flashcard items in an Instant.

Tools used

Tkinter, pillow, EasyOCR, Python, Gemini AI API

