from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Dictionary containing all chatbot responses
responses = {
    'programs': {
        'keywords': ['program', 'course', 'degree', 'major', 'study', 'available'],
        'response': "We offer various programs including:\n• Computer Science\n• Business Administration\n• Engineering\n• Medicine\n• Arts and Humanities\n• Social Sciences\n\nWhich program interests you?"
    },
    'fees': {
        'keywords': ['fee', 'cost', 'price', 'tuition', 'payment', 'expensive'],
        'response': "Our fee structure is:\n• Undergraduate: $15,000 per year\n• Graduate: $20,000 per year\n• Application Fee: $50\n\nScholarships are available for eligible students!"
    },
    'admission': {
        'keywords': ['admission', 'requirement', 'eligibility', 'qualify', 'criteria', 'apply'],
        'response': "Admission requirements:\n• High school diploma or equivalent\n• Minimum GPA of 3.0\n• Entrance exam scores\n• Letter of recommendation\n• Personal statement\n\nWould you like to know about the application process?"
    },
    'deadline': {
        'keywords': ['deadline', 'date', 'when', 'last date', 'time', 'submit'],
        'response': "Important deadlines:\n• Fall Semester: June 30th\n• Spring Semester: November 30th\n• Early Decision: April 15th\n\nDon't miss these dates!"
    },
    'scholarship': {
        'keywords': ['scholarship', 'financial aid', 'grant', 'funding', 'support'],
        'response': "We offer scholarships based on:\n• Academic merit (up to 50% tuition)\n• Sports achievements\n• Financial need\n• Community service\n\nContact our financial aid office for more details!"
    },
    'contact': {
        'keywords': ['contact', 'email', 'phone', 'reach', 'call', 'address'],
        'response': "You can reach us at:\n📧 Email: admissions@university.edu\n📞 Phone: +1-234-567-8900\n📍 Address: 123 University Ave, City, State\n\nOur office hours: Mon-Fri, 9 AM - 5 PM"
    },
    'application': {
        'keywords': ['how to apply', 'application process', 'apply online', 'submit'],
        'response': "Application process:\n1. Visit our website and create an account\n2. Fill out the online application form\n3. Upload required documents\n4. Pay the application fee\n5. Submit and track your application\n\nIt's simple and takes about 30 minutes!"
    }
}

# Greeting responses
greetings = ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']

# Function to find matching response
def get_response(user_message):
    # Convert message to lowercase for matching
    user_message = user_message.lower()
    
    # Check for greetings
    for greeting in greetings:
        if greeting in user_message:
            return "Hello! 👋 Welcome to our University Admission Office. I'm here to help you with information about programs, fees, admission requirements, deadlines, and more. How can I assist you today?"
    
    # Check for thank you
    if 'thank' in user_message or 'thanks' in user_message:
        return "You're welcome! 😊 Feel free to ask if you have any more questions about admissions. Good luck with your application!"
    
    # Check for goodbye
    if 'bye' in user_message or 'goodbye' in user_message:
        return "Goodbye! Best wishes for your academic journey. Feel free to come back anytime! 👋"
    
    # Search through all response categories
    for category, data in responses.items():
        for keyword in data['keywords']:
            if keyword in user_message:
                return data['response']
    
    # Default fallback response
    return "I'm sorry, I didn't quite understand that. 😅\n\nI can help you with:\n• Programs and courses\n• Admission requirements\n• Fee structure\n• Application deadlines\n• Scholarships\n• Contact information\n\nWhat would you like to know?"

# Route for home page
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle chat messages
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    bot_response = get_response(user_message)
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)
