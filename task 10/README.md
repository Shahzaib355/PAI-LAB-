# Hadith Generator Web Application

A simple and beautiful web application that displays authentic Hadiths from verified Islamic sources.

## Features

- Generate random Hadiths from authentic collections
- Filter Hadiths by category (Character, Faith, Charity, Knowledge, etc.)
- Search Hadiths by keyword
- Display complete reference information including:
  - Book name and reference number
  - Chapter information
  - Narrator name
  - Category

## Hadith Sources

All Hadiths are from authenticated collections:
- Sahih al-Bukhari
- Sahih Muslim
- Sunan al-Tirmidhi
- Sunan Abu Dawud
- Sunan Ibn Majah

These are part of the Kutub al-Sittah (The Six Books), the most trusted Hadith collections in Sunni Islam.

## Installation

1. Install Python (if not already installed)

2. Install required packages:
```
pip install -r requirements.txt
```

## Running the Application

1. Open terminal in the project directory

2. Run the Flask application:
```
python app.py
```

3. Open your web browser and go to:
```
http://127.0.0.1:5000
```

## How to Use

1. **Generate Random Hadith**: Select a category from the dropdown menu and click "Generate Hadith"

2. **Search Hadiths**: Enter a keyword in the search box and click "Search" to find specific Hadiths

3. **View Details**: Each Hadith displays complete verification information including the source book, reference number, chapter, and narrator

## Project Structure

```
hadith-generator/
├── app.py                 # Flask backend application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── templates/
│   └── index.html        # Main HTML page
└── static/
    ├── style.css         # Styling
    └── script.js         # Frontend JavaScript
```

## Technologies Used

- Backend: Flask (Python)
- Frontend: HTML, CSS, JavaScript
- Design: Responsive and modern UI

## Note

This is a beginner-level project created for educational purposes. All Hadiths included have been verified from authentic sources with proper references.
