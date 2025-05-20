from flask import Flask, request, make_response, render_template_string
import os

app = Flask(__name__)
FLAG = os.environ.get('FLAG', 'Trojan{Who_is_the_admin_now_58928924892892}')  # Default flag if not set

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Simple Auth Portal</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 2rem auto; }
        .alert { padding: 1rem; border-radius: 4px; margin: 1rem 0; }
        .alert-success { background: #e6f7e6; border: 1px solid #2e7d32; }
        .alert-error { background: #ffebee; border: 1px solid #c62828; }
    </style>
</head>
<body>
    <h1>Company Portal</h1>
    %s
</body>
</html>
'''

@app.route('/')
def index():
    resp = make_response(render_template_string(HTML_TEMPLATE % '''
    <div class="alert alert-success">
        Welcome to your employee portal
    </div>
    <nav>
        <p> To get a flag, go to Admin Dashboard. </p>
    </nav>
    '''))
    
    if not request.cookies.get('role'):
        resp.set_cookie('role', 'user', httponly=True)
    return resp

@app.route('/admin')
def admin():
    role = request.cookies.get('role', 'guest')
    
    if role == 'admin':
        return render_template_string(HTML_TEMPLATE % f'''
        <div class="alert alert-success">
            <h2>Admin Dashboard</h2>
            <p>Welcome administrator</p>
            <p>Flag: {FLAG}</p>
        </div>
        ''')
    else:
        return render_template_string(HTML_TEMPLATE % f'''
        <div class="alert alert-error">
            <h2>Access Denied</h2>
        </div>
        '''), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)