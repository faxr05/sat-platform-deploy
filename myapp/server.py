from flask import Flask, request, jsonify, send_file
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
DB_DIR = os.environ.get('DATA_DIR', '.')
DB_PATH = os.path.join(DB_DIR, 'sat_platform.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, timeout=15)
    conn.row_factory = sqlite3.Row
    return conn

# HTML sahifani ochib beruvchi asosiy yo'nalish
@app.route('/')
def home():
    return send_file('index.html')

# Mavjud testlarni HTML'dagi Login oynasiga jo'natish
@app.route('/api/tests', methods=['GET'])
def get_tests():
    conn = get_db_connection()
    tests = conn.execute('SELECT id, title, duration FROM tests').fetchall()
    conn.close()
    return jsonify([dict(t) for t in tests])

# Tanlangan testning savollarini HTML'ga jo'natish
@app.route('/api/questions/<int:test_id>', methods=['GET'])
def get_questions(test_id):
    conn = get_db_connection()
    questions = conn.execute('''
        SELECT id, q_text, opt_a, opt_b, opt_c, opt_d, correct_opt 
        FROM questions WHERE test_id = ?
    ''', (test_id,)).fetchall()
    conn.close()
    
    # Ma'lumotni frontend tushunadigan formatga o'tkazish
    formatted_q = []
    for q in questions:
        formatted_q.append({
            'id': q['id'],
            'text': q['q_text'],
            'options': [q['opt_a'], q['opt_b'], q['opt_c'], q['opt_d']],
            'correct': ['A', 'B', 'C', 'D'].index(q['correct_opt']) # A,B,C,D ni 0,1,2,3 indeksga aylantirish
        })
    return jsonify(formatted_q)

# O'quvchi testni yakunlaganda natijani bazaga saqlash
@app.route('/api/submit', methods=['POST'])
def submit_results():
    data = request.json
    student_name = data.get('student_name')
    test_id = data.get('test_id')
    score = data.get('score')
    total_q = data.get('total_q')
    time_spent_min = data.get('time_spent_min')
    date_now = datetime.now().strftime("%Y-%m-%d %H:%M")

    conn = get_db_connection()
    conn.execute('''
        INSERT INTO results (student_name, test_id, score, total_q, time_spent_min, date_taken) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (student_name, test_id, score, total_q, time_spent_min, date_now))
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    # Serverni 5000-portda ishga tushirish
    app.run(debug=False, port=int(os.environ.get('PORT', 5000)))

