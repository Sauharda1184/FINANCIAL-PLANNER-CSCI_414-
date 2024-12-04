from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
import sqlite3
import pymongo


app = Flask(__name__)
app.secret_key = 'your_secret_key'
bcrypt = Bcrypt(app)

#MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client['questionsDatabase']
faq_collection = db["frequent_asked_questions"]

# Database connection helper
def get_db_connection():
    conn = sqlite3.connect('finance.db')
    conn.row_factory = sqlite3.Row
    return conn

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        payment_method = request.form['payment_method']
        
        connection = get_db_connection()
        try:
            connection.execute('INSERT INTO users (name, email, password, payment_method) VALUES (?, ?, ?, ?)', 
                              (name, email, password, payment_method))
            connection.commit()
            flash('Signup successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Email already exists. Try another one.', 'danger')
        finally:
            connection.close()
    
    return render_template('signup.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        connection = get_db_connection()
        user = connection.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        connection.close()
        
        if user and bcrypt.check_password_hash(user['password'], password):
            session['user_id'] = user['user_id']
            session['name'] = user['name']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    
    return render_template('login.html')

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.', 'danger')
        return redirect(url_for('login'))
    return render_template('dashboard.html', name=session['name'])

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# Add a Budget
@app.route('/add_budget', methods=['GET', 'POST'])
def add_budget():
    if 'user_id' not in session:
        flash('Please log in to add a budget.', 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        user_id = session['user_id']
        connection = get_db_connection()
        connection.execute('INSERT INTO budgets (user_id) VALUES (?)', (user_id,))
        connection.commit()
        connection.close()
        flash('Budget added successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('add_budget.html')

# Add Income
@app.route('/add_income', methods=['GET', 'POST'])
def add_income():
    if 'user_id' not in session:
        flash('Please log in to add income.', 'danger')
        return redirect(url_for('login'))
    
    connection = get_db_connection()
    budgets = connection.execute('SELECT * FROM budgets WHERE user_id = ?', (session['user_id'],)).fetchall()
    categories = connection.execute('SELECT * FROM categories').fetchall()
    connection.close()
    
    if request.method == 'POST':
        budget_id = request.form['budget_id']
        category_id = request.form['category_id']
        name = request.form['name']
        dollar_amount = request.form['dollar_amount']
        
        connection = get_db_connection()
        connection.execute('INSERT INTO incomes (budget_id, category_id, name, dollar_amount) VALUES (?, ?, ?, ?)',
                           (budget_id, category_id, name, dollar_amount))
        connection.commit()
        connection.close()
        flash('Income added successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('add_income.html', budgets=budgets, categories=categories)

# Add Expense
@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if 'user_id' not in session:
        flash('Please log in to add expenses.', 'danger')
        return redirect(url_for('login'))
    
    connection = get_db_connection()
    budgets = connection.execute('SELECT * FROM budgets WHERE user_id = ?', (session['user_id'],)).fetchall()
    categories = connection.execute('SELECT * FROM categories').fetchall()
    connection.close()
    
    if request.method == 'POST':
        budget_id = request.form['budget_id']
        category_id = request.form['category_id']
        name = request.form['name']
        dollar_amount = request.form['dollar_amount']
        
        connection = get_db_connection()
        connection.execute('INSERT INTO expenses (budget_id, category_id, name, dollar_amount) VALUES (?, ?, ?, ?)',
                           (budget_id, category_id, name, dollar_amount))
        connection.commit()
        connection.close()
        flash('Expense added successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('add_expense.html', budgets=budgets, categories=categories)

# View Reports
@app.route('/reports')
def reports():
    if 'user_id' not in session:
        flash('Please log in to view reports.', 'danger')
        return redirect(url_for('login'))
    
    connection = get_db_connection()
    incomes = connection.execute('''
        SELECT i.name, i.dollar_amount, c.name as category 
        FROM incomes i
        JOIN categories c ON i.category_id = c.category_id
        WHERE i.budget_id IN (SELECT budget_id FROM budgets WHERE user_id = ?)
    ''', (session['user_id'],)).fetchall()
    
    expenses = connection.execute('''
        SELECT e.name, e.dollar_amount, c.name as category 
        FROM expenses e
        JOIN categories c ON e.category_id = c.category_id
        WHERE e.budget_id IN (SELECT budget_id FROM budgets WHERE user_id = ?)
    ''', (session['user_id'],)).fetchall()
    
    connection.close()
    
    return render_template('reports.html', incomes=incomes, expenses=expenses)


@app.route('/questions')
def questions():
    questions = faq_collection.find()
    faqs_list = list(questions)
    return render_template('questions.html', questions = faqs_list)
if __name__ == '__main__':
    app.run(debug=True)
