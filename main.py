from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    # यहाँ हमने 'is_completed' कॉलम जोड़ा है (0 = अधूरा, 1 = पूरा)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_text TEXT NOT NULL,
            is_completed INTEGER DEFAULT 0
        )
    ''')
    # अगर टेबल पहले से बनी है, तो नया कॉलम जोड़ने के लिए (ताकि एरर न आए)
    try:
        cursor.execute('ALTER TABLE tasks ADD COLUMN is_completed INTEGER DEFAULT 0')
    except sqlite3.OperationalError:
        pass
    conn.commit()
    conn.close()

@app.route('/')
def home():
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    # id, text और status तीनों मँगाए हैं
    cursor.execute('SELECT id, task_text, is_completed FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task_content = request.form.get('task')
    if task_content:
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (task_text, is_completed) VALUES (?, 0)', (task_content,))
        conn.commit()
        conn.close()
    return redirect('/')

@app.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_task(task_id):
    # यह चेकबॉक्स पर क्लिक करने पर स्टेटस को 0 से 1 या 1 से 0 करेगा
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET is_completed = NOT is_completed WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
