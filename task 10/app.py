from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

hadiths = [
    {
        "text": "The best among you are those who have the best manners and character.",
        "reference": "Sahih al-Bukhari 3559",
        "book": "Sahih al-Bukhari",
        "chapter": "Book 61, Hadith 68",
        "narrator": "Abdullah ibn Amr",
        "category": "Character"
    },
    {
        "text": "None of you truly believes until he loves for his brother what he loves for himself.",
        "reference": "Sahih al-Bukhari 13",
        "book": "Sahih al-Bukhari",
        "chapter": "Book 2, Hadith 6",
        "narrator": "Anas ibn Malik",
        "category": "Faith"
    },
    {
        "text": "The strong person is not the one who can wrestle someone else down. The strong person is the one who can control himself when he is angry.",
        "reference": "Sahih al-Bukhari 6114",
        "book": "Sahih al-Bukhari",
        "chapter": "Book 78, Hadith 141",
        "narrator": "Abu Huraira",
        "category": "Self-Control"
    },
    {
        "text": "Whoever believes in Allah and the Last Day should speak good or keep silent.",
        "reference": "Sahih al-Bukhari 6018",
        "book": "Sahih al-Bukhari",
        "chapter": "Book 78, Hadith 48",
        "narrator": "Abu Huraira",
        "category": "Speech"
    },
    {
        "text": "A good word is charity.",
        "reference": "Sahih al-Bukhari 2989",
        "book": "Sahih al-Bukhari",
        "chapter": "Book 56, Hadith 199",
        "narrator": "Abu Huraira",
        "category": "Charity"
    },
    {
        "text": "The most beloved deeds to Allah are those that are most consistent, even if they are small.",
        "reference": "Sahih al-Bukhari 6464",
        "book": "Sahih al-Bukhari",
        "chapter": "Book 81, Hadith 53",
        "narrator": "Aisha",
        "category": "Consistency"
    },
    {
        "text": "Make things easy and do not make them difficult, cheer people up and do not repel them.",
        "reference": "Sahih al-Bukhari 69",
        "book": "Sahih al-Bukhari",
        "chapter": "Book 3, Hadith 11",
        "narrator": "Anas ibn Malik",
        "category": "Kindness"
    },
    {
        "text": "The believer does not slander, curse, or speak in an obscene or foul manner.",
        "reference": "Sunan al-Tirmidhi 1977",
        "book": "Sunan al-Tirmidhi",
        "chapter": "Book 27, Hadith 83",
        "narrator": "Abdullah ibn Masud",
        "category": "Character"
    },
    {
        "text": "Whoever is not merciful to others will not be treated mercifully.",
        "reference": "Sahih al-Bukhari 5997",
        "book": "Sahih al-Bukhari",
        "chapter": "Book 78, Hadith 27",
        "narrator": "Abu Huraira",
        "category": "Mercy"
    },
    {
        "text": "The best of people are those who are most beneficial to people.",
        "reference": "Sahih al-Jami 3289",
        "book": "Sahih al-Jami",
        "chapter": "Authenticated by Al-Albani",
        "narrator": "Jabir ibn Abdullah",
        "category": "Service"
    },
    {
        "text": "Smiling in the face of your brother is charity.",
        "reference": "Sunan al-Tirmidhi 1956",
        "book": "Sunan al-Tirmidhi",
        "chapter": "Book 27, Hadith 62",
        "narrator": "Abu Dharr",
        "category": "Charity"
    },
    {
        "text": "He who does not thank people, does not thank Allah.",
        "reference": "Sunan Abu Dawud 4811",
        "book": "Sunan Abu Dawud",
        "chapter": "Book 43, Hadith 39",
        "narrator": "Abu Huraira",
        "category": "Gratitude"
    },
    {
        "text": "The best charity is that given when one has little.",
        "reference": "Sunan Abu Dawud 1677",
        "book": "Sunan Abu Dawud",
        "chapter": "Book 9, Hadith 122",
        "narrator": "Abu Huraira",
        "category": "Charity"
    },
    {
        "text": "Seek knowledge from the cradle to the grave.",
        "reference": "Sunan Ibn Majah 224",
        "book": "Sunan Ibn Majah",
        "chapter": "Introduction, Hadith 224",
        "narrator": "Anas ibn Malik",
        "category": "Knowledge"
    },
    {
        "text": "The seeking of knowledge is obligatory for every Muslim.",
        "reference": "Sunan Ibn Majah 224",
        "book": "Sunan Ibn Majah",
        "chapter": "Introduction, Hadith 224",
        "narrator": "Anas ibn Malik",
        "category": "Knowledge"
    }
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_hadith', methods=['POST'])
def get_hadith():
    data = request.get_json()
    category = data.get('category', 'all')
    
    if category == 'all':
        hadith = random.choice(hadiths)
    else:
        filtered_hadiths = [h for h in hadiths if h['category'].lower() == category.lower()]
        if filtered_hadiths:
            hadith = random.choice(filtered_hadiths)
        else:
            hadith = random.choice(hadiths)
    
    return jsonify(hadith)

@app.route('/search_hadith', methods=['POST'])
def search_hadith():
    data = request.get_json()
    keyword = data.get('keyword', '').lower()
    
    results = [h for h in hadiths if keyword in h['text'].lower() or keyword in h['category'].lower()]
    
    if results:
        return jsonify({'found': True, 'hadiths': results})
    else:
        return jsonify({'found': False, 'message': 'No hadith found with that keyword.'})

if __name__ == '__main__':
    app.run(debug=True)
