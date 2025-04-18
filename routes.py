from flask import render_template, flash, redirect, url_for, session
from models import User, Blog
from forms import RegistrationForm, LoginForm 
from app import app

# إضافة SECRET_KEY للسيشن
app.config['SECRET_KEY'] = 'your_secret_key_here'  # غيّرها لقيمة سرية قوية

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', title='Home', cssFile='home.css')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html', title='about', cssFile='about.css')

@app.route('/faculties', methods=['GET'])
def faculties():
    return render_template('faculties.html', title='Faculties')
    
@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html', title='contacat')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # لو المستخدم عامل login بالفعل، يروح للـ index
    if 'user' in session:
        flash('You are already logged in!', 'info')
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'mohamed@gmail.com' and form.password.data == '123456':
            session['user'] = form.email.data  # نخزن المستخدم في السيشن
            flash(f'Login Successful for {form.email.data}', 'success')
            return redirect(url_for('index'))
        else:
            flash(f'Invalid Credentials', 'danger')
    return render_template('login.html', title='login', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.name.data}', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', title='register', form=form)

@app.route('/sql_data', methods=['GET'])
def sql_data():
    users = User.query.all()
    html = "<h1>User Emails and Passwords</h1><ul>"
    for user in users:
        html += f"<li>Email: {user.email} - Password: {user.password}</li>"
    html += "</ul>"
    return html

# إضافة route لـ logout
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user', None)  # إزالة المستخدم من السيشن
    flash('You have been logged out!', 'success')
    return redirect(url_for('index'))