from flask import Flask, render_template, request, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app= Flask(__name__)
# Makes sure user can't modify cookie and can't give him admin rights or other bad things ;)
app.secret_key = "xdhZ5enkMV4oBBBlR9ElADGbKPOba42gRtGVbiqnFrY4lRp3ez0DYh1oTmCqmTNxDlOrOrkPGcxhCzZEdH4W21OE2eCpkkMH2NRU"

# SQL Alchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    gender = db.Column(db.String(6), nullable=False)
    role = db.Column(db.String(6), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    level = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(256), nullable=False)

# Routes
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/dashboard")
def dashboard():
    # Is connected ?
    if 'username' in session:
        return render_template("dashboard.html")
    else:
        return redirect(url_for("home"))

@app.route("/login", methods=["POST"])
def login():
    message = None 
    # Collect infos from form
    username = request.form.get("username")
    password = request.form.get("password")
    action = request.form.get("action")
    
    if action == "signin":
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                session["username"] = user.username
                session["gender"] = user.gender
                session["role"] = user.role
                session["birthdate"] = user.birthdate
                session["level"] = user.level
                session["email"] = user.email
                return redirect(url_for('dashboard'))
            else:
                message = "Incorrect username or password"
    
    elif action == "signup":
        email = request.form.get("email")
        gender = request.form.get("gender")
        role = request.form.get("role")
        birthdate_str = request.form.get("birthdate")
        birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d").date()
        if not username or not email or not password or not role or not birthdate_str or not gender:
            message = "All fields must be selected"
        elif User.query.filter_by(username=username).first():
            message = "Username already taken"
        elif User.query.filter_by(email=email).first():
            message = "Email already taken"
        elif gender != "male" and gender != "female":
            message = "Gender is incorrect"
        elif role != "parent" and role != "child":
            message = "Role is incorrect"
        elif birthdate > datetime.today().date():
            message = "You are not Marty McFly"
        else:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(
                username=username, 
                email=email, 
                password=hashed_password,
                gender = gender,
                role=role,
                birthdate=birthdate,
                level=0,
            )
            db.session.add(new_user)
            db.session.commit()
            session["username"] = new_user.username
            session["gender"] = new_user.gender
            session["role"] = new_user.role
            session["birthdate"] = new_user.birthdate
            session["level"] = new_user.level
            session["email"] = new_user.email
            return redirect(url_for("dashboard"))
    
    return render_template("signin.html", message=message)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)