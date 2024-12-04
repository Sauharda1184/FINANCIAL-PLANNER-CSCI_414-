import sqlite3
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client['questionsDatabase']
faq_collection = db["frequent_asked_questions"]
faq_collection.delete_many({})
data = [
    {"question": "Why should I use this website", "answer":"Use this website to manage your budget and track spending habits"},
    {"question": "How do I add an income?", "answer": "To add an income, navigate to the 'Add Income' section on the dashboard. Enter the income source, amount, and category, and click 'Save'. This will update your budget and reflect in your overall financial overview."},
    {"question": "Can I view reports on my spending?","answer": "Yes! The 'View Reports' section provides a summary of your income and expenses by category. You can easily visualize your spending patterns and identify areas to cut back."},
    {"question": "How do I make a budget for a specific goal (e.g., saving for a vacation)?", "answer": "You can create a separate budget specifically for your goal by adding a new budget in the 'Add Budget' section and labeling it accordingly. Track your income and expenses related to that goal to stay on target."},
]

faq_collection.insert_many(data)
# Function to create and initialize the database
def create_finance_db():
    connection = sqlite3.connect('finance.db')
    cursor = connection.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            payment_method TEXT
        )
    ''')
    
    # Create budgets table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budgets (
            budget_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    # Create categories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    
    # Insert default categories
    cursor.executemany('''
        INSERT OR IGNORE INTO categories (name) VALUES (?)
    ''', [
        ('Housing',),
        ('Transportation',),
        ('Food',),
        ('Utilities',),
        ('Entertainment',),
        ('Healthcare',),
        ('Savings',),
        ('Other',)
    ])
    
    # Create incomes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS incomes (
            income_id INTEGER PRIMARY KEY AUTOINCREMENT,
            budget_id INTEGER NOT NULL,
            category_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            dollar_amount REAL NOT NULL,
            FOREIGN KEY (budget_id) REFERENCES budgets(budget_id),
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
        )
    ''')
    
    # Create expenses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
            budget_id INTEGER NOT NULL,
            category_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            dollar_amount REAL NOT NULL,
            FOREIGN KEY (budget_id) REFERENCES budgets(budget_id),
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
        )
    ''')

    # Commit changes and close the connection
    connection.commit()
    connection.close()

if __name__ == '__main__':
    create_finance_db()
    print("Database created successfully!")
