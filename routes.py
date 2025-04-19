from flask import render_template, flash, redirect, url_for, session
# Removed global import of User and Blog to avoid circular import
from forms import RegistrationForm, LoginForm 
from app import app
from __init__ import db
from models import User

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
    
from flask import request
from models import Blog

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        message = request.form.get('message')
        if name and message:
            new_blog = Blog(title=name, content=message, user_id=1)  # Adjust user_id as needed
            db.session.add(new_blog)
            db.session.commit()
            flash('Your message has been sent successfully!', 'success')
            return redirect(url_for('contact'))
        else:
            flash('Please fill in all fields.', 'danger')
    return render_template('contact.html', title='contact')

from __init__ import bcrypt

@app.route('/login', methods=['GET', 'POST'])
def login():
    from models import User  # Local import to avoid circular import
    # لو المستخدم عامل login بالفعل، يروح للـ index
    if 'user' in session:
        flash('You are already logged in!', 'info')
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            try:
                if bcrypt.check_password_hash(user.password, form.password.data):
                    session['user'] = user.email  # Store user email in session
                    flash(f'Login Successful for {user.name}', 'success')
                    return redirect(url_for('index'))
                else:
                    flash(f'Invalid Credentials', 'danger')
            except ValueError:
                # Password not hashed, fallback to plain text comparison
                if user.password == form.password.data:
                    session['user'] = user.email # Store user email in session
                    flash(f'Login Successful for {user.name}', 'success')
                    return redirect(url_for('index'))
                else:
                    flash(f'Invalid Credentials', 'danger')
        else:
            flash(f'Invalid Credentials', 'danger')
    return render_template('login.html', title='login', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    from models import User  # Local import to avoid circular import
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if email already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash("Email already registered. Please use a different email or login.", "danger")
            return render_template("register.html", form=form)
        
        # Check if phone number already exists
        existing_phone = User.query.filter_by(phone=form.phone.data).first()
        if existing_phone:
            flash("This number is used by another one.", "danger")
            return render_template("register.html", form=form)
            
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(name=form.name.data, email=form.email.data, password=hashed_password, phone=form.phone.data)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please login.", "success")
        return redirect(url_for("login"))
    else:
        return render_template("register.html", form=form,title='Register')

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
    session.pop('user', None)
    flash('You have been logged out.', 'info')  
    return redirect(url_for('index'))
