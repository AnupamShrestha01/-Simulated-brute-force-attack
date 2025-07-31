from flask import Flask, render_template_string, request, redirect, session

app = Flask(__name__)
app.secret_key = 'demo123'

# Two hardcoded user accounts
users = {
    "admin": {
        "password": "password123",
        "email": "admin@demo.com",
        "phone": "9810174579",
        "account": "0011223344",
        "address": "Newyork",
        "balance": 50000
    },
    "user01": {
        "password": "letmein123",
        "email": "user@demo.com",
        "phone": "9876543210",
        "account": "5544332211",
        "address": "China",
        "balance": 25000
    }
}

# HTML template for login page
login_page = '''
<h2> Mobile Banking Login</h2>
<form method="post">
  Username: <input type="text" name="username"><br><br>
  Password: <input type="password" name="password"><br><br>
  <input type="submit" value="Login">
</form>
{% if error %}<p style="color:red;">{{ error }}</p>{% endif %}
'''

# HTML template for dashboard
dashboard_page = '''
<h2>Welcome, {{ user }}</h2>
<p><b>Email:</b> {{ data.email }}</p>
<p><b>Phone:</b> {{ data.phone }}</p>
<p><b>Account Number:</b> {{ data.account }}</p>
<p><b>Address:</b> {{ data.address }}</p>
<p><b>Balance:</b> ${{ data.balance }}</p>

<hr>
<h3> Transfer Money</h3>
<form method="post" action="/transfer">
  To Account: <input type="text" name="to"><br>
  Amount ($): <input type="number" name="amount"><br>
  <input type="submit" value="Transfer">
</form>

<hr>
<h3> Change Password</h3>
<form method="post" action="/change">
  New Password: <input type="password" name="newpass"><br>
  <input type="submit" value="Update">
</form>

<br><a href="/logout"> Logout</a>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        uname = request.form['username']
        pword = request.form['password']
        if uname in users and users[uname]['password'] == pword:
            session['user'] = uname
            return redirect('/dashboard')
        else:
            error = 'Invalid credentials.'
    return render_template_string(login_page, error=error)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    uname = session['user']
    return render_template_string(dashboard_page, user=uname, data=users[uname])

@app.route('/transfer', methods=['POST'])
def transfer():
    if 'user' not in session:
        return redirect('/')
    uname = session['user']
    amount = float(request.form['amount'])
    if amount > users[uname]['balance']:
        return "<p style='color:red;'> Insufficient balance. <a href='/dashboard'>Back</a></p>"
    users[uname]['balance'] -= amount
    return f"<p> Transferred ${amount:.2f} to {request.form['to']} successfully. <a href='/dashboard'>Back</a></p>"

@app.route('/change', methods=['POST'])
def change_password():
    if 'user' not in session:
        return redirect('/')
    uname = session['user']
    users[uname]['password'] = request.form['newpass']
    return "<p> Password changed successfully. <a href='/dashboard'>Back</a></p>"

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
 app.run(debug=True)
