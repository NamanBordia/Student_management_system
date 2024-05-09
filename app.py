from flask import Flask, request, jsonify, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)


with sqlite3.connect('students.db') as conn:
    conn.execute('''CREATE TABLE IF NOT EXISTS students
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     name TEXT, 
                     age INTEGER, 
                     grade INTEGER)''')

                        
                        
@app.route('/')
def home():
    with sqlite3.connect('students.db') as conn:
        students = conn.execute('SELECT * FROM students').fetchall()
    return render_template('student.html', students=students)

@app.route('/add', methods=['POST'])
def add_student():
    name = request.form['name']
    age = int(request.form['age'])
    grade = int(request.form['grade'])
    with sqlite3.connect('students.db') as conn:
        conn.execute('INSERT INTO students (name, age, grade) VALUES (?, ?, ?)', (name, age, grade))
    return redirect(url_for('home'))

@app.route('/update', methods=['POST'])
def update_student():
    student_id = int(request.form['id'])
    name = request.form['name']
    age = int(request.form['age'])
    grade = int(request.form['grade'])  
    with sqlite3.connect('students.db') as conn:
        conn.execute('UPDATE students SET name = ?, age = ?, grade = ? WHERE id = ?', (name, age, grade, student_id))
    return redirect(url_for('home'))

@app.route('/delete', methods=['POST'])
def delete_student():
    student_id = int(request.form['id'])
    with sqlite3.connect('students.db') as conn:
        conn.execute('DELETE FROM students WHERE id = ?', (student_id,))
    return redirect(url_for('home'))

@app.route('/search', methods=['GET'])
def search_students():
    search_query = request.args.get('query', '')
    with sqlite3.connect('students.db') as conn:
        results = conn.execute('SELECT * FROM students WHERE name LIKE ?', (f'%{search_query}%',)).fetchall()
    return jsonify(results)

