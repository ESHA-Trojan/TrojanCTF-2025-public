from flask import Flask, request, render_template_string, make_response, redirect, url_for
import sqlite3
import os
import sys

app = Flask(__name__)
app.config['DATABASE'] = 'bank.db'
FLAG = os.environ.get('FLAG', 'Trojan{a_one_of_a_kind_sql_injecter09876898765}')

# Initialize database
def init_db():
    with sqlite3.connect(app.config['DATABASE']) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INTEGER PRIMARY KEY, 
                     username TEXT UNIQUE, 
                     password TEXT,
                     balance INTEGER DEFAULT 100)''')
        conn.execute('''CREATE TABLE IF NOT EXISTS flags
                     (id INTEGER PRIMARY KEY,
                     secret TEXT)''')
        
        # Add some sample data
        if not conn.execute("SELECT 1 FROM users WHERE username='alice'").fetchone():
            conn.executemany("INSERT INTO users (username, password) VALUES (?, ?)",
                           [('alice', 'password123'), ('bob', 'qwerty')])
            conn.execute("INSERT INTO flags (secret) VALUES (?)", (FLAG,))
        conn.commit()

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Bank of Insecurity</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 2rem auto; }
        .alert { padding: 1rem; border-radius: 4px; margin: 1rem 0; }
        .success { background: #e6f7e6; border: 1px solid #2e7d32; }
        .error { background: #ffebee; border: 1px solid #c62828; }
        .account { background: #e3f2fd; border: 1px solid #1565c0; padding: 1rem; }
    </style>
</head>
<body>
    <h1>Bank of Insecurity</h1>
    %s
</body>
</html>
'''

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        # Debugging hint (visible in HTML source)
        debug_comment = "<!-- Query format: SELECT * FROM users WHERE username='[user_input]' AND password='[user_input]' -->"
        
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"

        print(f"[DEBUG] Computed MAC: {query}")
        sys.stdout.flush()
        
        try:
            with sqlite3.connect(app.config['DATABASE']) as conn:
                user = conn.execute(query).fetchone()
                
            if user:
                resp = make_response(render_template_string(HTML_TEMPLATE % f'''
                <div class="account">
                    <h2>Welcome {user[1]}!</h2>
                    <p>Your balance: ${user[3]}</p>
                    <p>Flag: {FLAG}</p>
                </div>
                '''))
                resp.set_cookie('user', user[1])
                return resp
            else:
                return render_template_string(HTML_TEMPLATE % f'''
                {debug_comment}
                <div class="alert error">
                    Invalid credentials
                </div>
                '''), 401
        except sqlite3.Error as e:
            return render_template_string(HTML_TEMPLATE % f'''
            <div class="alert error">
                Database error: {str(e)}
            </div>
            '''), 500
    
    return render_template_string(HTML_TEMPLATE % '''
    <form method="POST">
        <h2>Login</h2>
        <p><input type="text" name="username" placeholder="Username"></p>
        <p><input type="password" name="password" placeholder="Password"></p>
        <p><button type="submit">Login</button></p>
    </form>
    ''')

def create_app(host='0.0.0.0', port=5000):
    init_db()
    app.run(host=host, port=port)

if __name__ == '__main__':
    create_app(host='0.0.0.0', port=5000)