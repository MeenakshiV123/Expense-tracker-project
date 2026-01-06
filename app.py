from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    amount REAL NOT NULL,
                    date TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('SELECT * FROM expenses')
    expenses = c.fetchall()
    total = sum(exp[2] for exp in expenses)  # Sum amounts
    conn.close()
    return render_template('index.html', expenses=expenses, total=total)

@app.route('/add', methods=['POST'])
def add_expense():
    category = request.form['category']
    amount = float(request.form['amount'])
    date = request.form['date']
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('INSERT INTO expenses (category, amount, date) VALUES (?, ?, ?)', (category, amount, date))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:expense_id>')
def delete_expense(expense_id):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)