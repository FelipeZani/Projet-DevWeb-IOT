from flask import Flask, render_template, request, redirect, session, url_for
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
    fname = db.Column(db.String(32), nullable=False)
    lname = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    gender = db.Column(db.String(6), nullable=False)
    role = db.Column(db.String(6), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    level = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)

# Routes
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/signin")
def signin():
    session.clear() # avoid creating new account while still having session infos
    return render_template("signin.html")

@app.route("/dashboard")
def dashboard():
    # Is connected ?
    if 'username' in session and session["verified"]:
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
            if not user: # user doesnt exists
                message = "Incorrect username or password"
            elif check_password_hash(user.password, password) and user.is_verified:
                add_points(user.username, 1)
                session["username"] = user.username
                session["fname"] = user.fname
                session["lname"] = user.lname
                session["gender"] = user.gender
                session["role"] = user.role
                session["birthdate"] = user.birthdate.strftime("%Y-%m-%d")
                session["level"] = user.level
                session["email"] = user.email
                session["verified"] = 1
                return redirect(url_for('dashboard'))
            elif not user.is_verified:
                message = "You are not in the family yet, please wait for admin to accept you"
            else:
                message = "Incorrect username or password"
    
    elif action == "signup":
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        email = request.form.get("email")
        gender = request.form.get("gender")
        role = request.form.get("role")
        birthdate_str = request.form.get("birthdate")
        birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d").date()
        if not username or not email or not password or not role or not birthdate_str or not gender or not fname or not lname:
            message = "All fields must be filled"
        elif User.query.filter_by(username=username).first():
            message = "Username already taken"
        elif User.query.filter_by(email=email).first():
            message = "Email already taken"
        elif gender not in ["male", "female"]:
            message = "Gender is incorrect"
        elif role not in ["parent", "child"]:
            message = "Role is incorrect"
        elif birthdate > datetime.today().date():
            message = "You are not Marty McFly"
        elif len(username) > 32 or len(username) < 3 or len(email) > 64 or len(email) < 3 or len(password) > 32  or len(password) < 0 or len(fname) < 3 or len(fname) > 32 or len(lname) < 3 or len(lname) > 32:
            message = "username, first name and last name are 32 chars max, email is 64 chars max"
        else:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(
                username=username, 
                fname=fname,
                lname=lname,
                email=email, 
                password=hashed_password,
                gender = gender,
                role=role,
                birthdate=birthdate,
                level=0,
                is_verified=0,
            )
            db.session.add(new_user)
            db.session.commit()
            message = "Wait for the administrator to accept you in the family"
    return render_template("signin.html", message=message)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/profile")
def profile():
    if 'username' in session and session["verified"]:
        users = User.query.filter(User.username != session["username"], User.is_verified == 1).all()
        return render_template("profile.html", users=users)
    else :
        return redirect(url_for("home"))
    
@app.route("/user/<int:user_id>")
def user_profile(user_id):
    user = User.query.get(user_id)
    if user and user.is_verified:
        add_points(session["username"], 1)
        return render_template("user_profile.html", user=user)
    else:
        return redirect(url_for("profile"))

@app.route("/change_password", methods=["POST"])
def change_password():
    if 'username' not in session:
        return redirect(url_for('home'))

    user = User.query.filter_by(username=session['username']).first()
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    
    # Checks if the current password is correct
    if not check_password_hash(user.password, current_password):
        session.clear()
        return redirect(url_for("signin", message="Old password is wrong. The password haven't been changed, please reconnect"))
    
    # makes sure new password is different from old one
    if new_password == current_password:
        session.clear()
        return redirect(url_for("signin", message="New password must be different from old one, please reconnect"))
    
    # generates new password
    user.password = generate_password_hash(new_password)
    db.session.commit()
    session.clear()
    
    return redirect(url_for("signin", message="Password sucessfully changed, please reconnect"))

@app.route('/change_email', methods=['POST'])
def change_email():
    if 'username' not in session:
        return redirect(url_for('home'))
    
    user = User.query.filter_by(username=session['username']).first()

    new_email = request.form.get('email')

    if User.query.filter_by(email=new_email).first():
        return redirect(url_for('profile', message="Email already taken"))

    user.email = new_email
    db.session.commit()

    return redirect(url_for('profile', message="Email successfully changed"))

@app.route("/admin_panel")
def admin_panel():
    if 'username'not in session and session["level"] < 20:
        return redirect(url_for("dashboard"))
    
    return render_template("admin_panel.html")

# Functions

def add_points(username, points):
    user = User.query.filter_by(username=username).first()
    
    if not user:
        return False 
    
    user.level += points
    db.session.commit()
    return True


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)