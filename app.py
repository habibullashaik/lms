from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# Dummy user storage (in-memory)
users = {}

# Course data
courses = {
    "Python": ["Introduction", "Data Structures", "OOP Concepts"],
    "Java": ["Syntax", "OOP Concepts", "Data Structures"],
    "C": ["Basics", "Pointers", "Memory Management"],
    "C++": ["OOP Concepts", "Templates", "STL"],
    "JavaScript": ["Syntax", "DOM Manipulation", "AJAX"],
    "HTML": ["Elements", "Forms", "CSS Integration"],
    "CSS": ["Selectors", "Box Model", "Flexbox"],
    "SQL": ["Queries", "Joins", "Database Design"],
    "Ruby": ["Syntax", "OOP", "Rails"],
    "Go": ["Syntax", "Concurrency", "Error Handling"]
}

# Theory content
theory_content = {
    "Python": {
        "Introduction": "Python is an interpreted, high-level programming language...",
        "Data Structures": "Python supports data structures like lists, tuples, sets...",
        "OOP Concepts": "Object-Oriented Programming in Python includes classes, inheritance..."
    },
    "Java": {
        "Syntax": "Java has a strict syntax with a lot of emphasis on type safety...",
        "OOP Concepts": "Java's object-oriented principles revolve around inheritance, encapsulation...",
        "Data Structures": "Java provides in-built support for various data structures..."
    },
    # Add similar theory for other courses
}

# Route for homepage (Dashboard)
@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', courses=courses)

# Route for signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users:
            flash('Username already exists. Try another one.')
        else:
            users[username] = password
            flash('Signup successful! You can now log in.')
            return redirect(url_for('login'))
    
    return render_template('signup.html')

# Route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            session['username'] = username
            flash('Login successful!')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.')

    return render_template('login.html')

# Route for logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))

# Route for course topics
@app.route('/course/<course_name>')
def course_topics(course_name):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    topics = courses.get(course_name, [])
    return render_template('topics.html', course_name=course_name, topics=topics)

# Route for theory
@app.route('/course/<course_name>/<topic>')
def theory(course_name, topic):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    theory = theory_content.get(course_name, {}).get(topic, "No theory available for this topic.")
    return render_template('theory.html', course_name=course_name, topic=topic, theory=theory)

# Route for assignment
@app.route('/course/<course_name>/<topic>/assignment', methods=['GET', 'POST'])
def assignment(course_name, topic):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        answer = request.form['answer']
        score = len(answer) * 10  # Dummy scoring logic
        return redirect(url_for('profile', score=score))
    return render_template('assignment.html', course_name=course_name, topic=topic)

# Route for profile with marks and stars
@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    score = request.args.get('score', 0, type=int)
    stars = "⭐" * (score // 10)
    return render_template('profile.html', score=score, stars=stars)

if __name__ == '__main__':
    app.run(debug=True)
