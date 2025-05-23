from flask import Flask, render_template, request, redirect, session, url_for,jsonify,send_file
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, Boolean, MetaData, inspect, text
from static.application_modules.mailing.mailling import add_dict_confirmation_list,accounts_to_confirm,send_mail
from flask_mailman import Mail
from sqlalchemy.orm import joinedload
from datetime import datetime
from time import time
from weasyprint import HTML
import matplotlib.pyplot as plt
import os
import re
import uuid
from io import BytesIO


app= Flask(__name__)
# Makes sure user can't modify cookie and can't give him admin rights or other bad things ;)
app.secret_key = "xdhZ5enkMV4oBBBlR9ElADGbKPOba42gRtGVbiqnFrY4lRp3ez0DYh1oTmCqmTNxDlOrOrkPGcxhCzZEdH4W21OE2eCpkkMH2NRU"

# SQL Alchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
metadata = MetaData()


with app.app_context():
    db.create_all()


# Config Mailman
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = "projetweb.iot@gmail.com"
app.config['MAIL_PASSWORD'] = "kpdm hdvx jtic fvul"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)


# Database model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    fname = db.Column(db.String(32), nullable=False)
    lname = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    gender = db.Column(db.String(12), nullable=False)
    role = db.Column(db.String(12), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    level = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)

class LoginHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    login_time = db.Column(db.DateTime, default=datetime.today, nullable=False)

class DelSuggestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, nullable=False)
    room_name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False) 

class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    objects = db.relationship('Object', backref='room', cascade='all, delete-orphan')

class Object(db.Model):
    __tablename__ = 'objects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100))
    description = db.Column(db.Text)
    consommation_kw_jour = db.Column(db.Float, nullable=True)  
    status = db.Column(db.Boolean, default=True)               
    date_ajout = db.Column(db.DateTime, default=datetime.today)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)



def generate_pie_chart(data, title):
    if not data:
        return None
    os.makedirs("static/tmp", exist_ok=True)

    labels = list(data.keys())
    values = list(data.values())
    plt.figure(figsize=(5, 5))
    plt.pie(values, labels=labels, autopct='%1.1f%%')
    plt.title(title)
    filename = f"static/tmp/pie_{uuid.uuid4()}.png"
    plt.savefig(filename, bbox_inches='tight')
    plt.close()
    return filename

def generate_bar_chart(data, title):
    if not data:
        return None
    os.makedirs("static/tmp", exist_ok=True)

    labels = list(data.keys())
    values = list(data.values())
    plt.figure(figsize=(6, 4))
    plt.bar(labels, values)
    plt.title(title)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    filename = f"static/tmp/bar_{uuid.uuid4()}.png"
    plt.savefig(filename)
    plt.close()
    return filename

# Routes
@app.route("/")
def home():
    if 'username' in session :
        return redirect(url_for("dashboard"))
    return render_template("home.html")


@app.route("/dashboard")
def dashboard():
    if 'username' not in session or not session.get("verified"):
        return redirect(url_for("home", message="Veuillez vous connecter pour accéder au tableau de bord."))

    # Récupérer les pièces pour le filtre
    rooms = Room.query.order_by(Room.name).all()

    # Récupérer tous les objets avec leurs informations de pièce
    objects_query = Object.query.options(joinedload(Object.room)).order_by(Object.name).all()

    # JSON
    objects_data = []
    for obj in objects_query:
        objects_data.append({
            "id": obj.id,
            "name": obj.name,
            "type": obj.type or "N/A",
            "description": obj.description or "",
            "room_id": obj.room_id,
            "room_name": obj.room.name if obj.room else "Pièce inconnue"
        })

    # Convertir en JSON
    import json
    objects_json = json.dumps(objects_data)

    return render_template("dashboard.html", rooms=rooms, objects_json=objects_json)

#Pour le login
@app.route("/login", methods=["POST"])
def login():
    # Collect form data from the frontend
    data = request.get_json()  # Getting data from the front
    username = data.get("username")
    password = data.get("password")
    action = data.get("action")
    
    # List for storing messages
    list_messages = []

    if action == "signin":
        user = User.query.filter_by(username=username).first()
        if not user: # User does not exist
            list_messages.append({'sin-form': "Incorrect username or password"})
        elif check_password_hash(user.password, password) and user.is_verified:
            # Set session variables
            session["username"] = user.username
            session["fname"] = user.fname
            session["lname"] = user.lname
            session["gender"] = user.gender
            session["role"] = user.role
            session["birthdate"] = user.birthdate.strftime("%Y-%m-%d")
            session["level"] = user.level
            session["email"] = user.email
            session["verified"] = 1

            add_points(session["username"], 1)
            log_user_login(session["username"])

            # Return a success message and redirect URL
            return jsonify({"success": True, "redirect": url_for('dashboard')}), 200
        elif not user.is_verified:
            list_messages.append({'nif': "You are not in the family yet, please wait for admin to accept you"})
        else:
            list_messages.append({'sin-form': "Incorrect username or password"})
    elif action == "signup":
        fname = data.get("fname") 
        lname = data.get("lname")
        email = data.get("email")
        gender = data.get("gender")
        role = data.get("role")
        birthdate_str = data.get("birthdate")
        birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d").date()

        # Validate fields
        if not username or not email or not password or not role or not birthdate_str or not gender or not fname or not lname:
            list_messages.append({'sup-form': "All fields must be filled"})
        if User.query.filter_by(username=username).first():
            list_messages.append({'susername': "Username already taken"})
        if User.query.filter_by(email=email).first():
            list_messages.append({'email': "Email already taken"})
        if gender not in ["male", "femelle"]:
            list_messages.append({'gender': "Gender is incorrect"})
        if role not in ["parent", "enfant"]:
            list_messages.append({'role': "Role is incorrect"})
        if birthdate > datetime.today().date():
            list_messages.append({'nif': "You are not Marty McFly"})
        elif len(username) > 32 or len(username) < 3 or len(email) > 64 or len(email) < 3 or len(password) > 32  or len(password) < 0 or len(fname) < 3 or len(fname) > 32 or len(lname) < 3 or len(lname) > 32:
            list_messages.append({"sup-form": "Username, first name, last name, and email should have specified max lengths"})
        
        if not list_messages:
            
            #creating a dict structure to store the users data, and an index to in order to implement mail confirmation system:
            # user is sent a mail containing link (tokien validation), click on it will trigger the validation of the mail
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            
            user_sup_data = { #user data dict
                "username":username, 
                "fname":fname,
                "lname":lname,
                "email" : email, 
                "password" : hashed_password,
                "gender": gender,
                "role" : role,
                "birthdate" : birthdate,  
            }

            user_id = str(uuid.uuid4())[0:12] #get the first 12 characters of the id 
            
            add_dict_confirmation_list(user_id,user_sup_data)
            
            send_mail(email,fname,user_id)
           
            return jsonify({"success":True,"message":"Confirmation Mail Sent"}),200
        
    # If validation failed, return error messages to frontend
    return jsonify({"success": False, "messages": list_messages}),401

#After clicking on the link user will have its token verified, in case of success added to the data base
@app.route("/signup/<userid>")
def confirm_email(userid):

    try:   
        user_data = accounts_to_confirm[userid]
        new_user = User(
            username = user_data["username"], 
            fname = user_data["fname"],
            lname = user_data["lname"],
            email = user_data["email"], 
            password = user_data["password"],
            gender = user_data["gender"],
            role = user_data["role"],
            birthdate = user_data["birthdate"],
            level=0,
            is_verified=0,
        )

        db.session.add(new_user)
        db.session.commit()
        
        del accounts_to_confirm[userid]

        return render_template("home.html"), 200
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"success": False, "message": "Invalid registration token!\n Error: "}), 400

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
    if 'username' not in session or not session["verified"]:
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
    if 'username' not in session or not session["verified"]:
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
    if 'username' not in session or session.get("level", 0) < 20 or not session.get("verified"):
         return redirect(url_for("dashboard"))

    all_room_suggestions = DelSuggestion.query.order_by(DelSuggestion.id.desc()).all()

    users = User.query.filter(User.username != session["username"]).all()

    return render_template("admin_panel.html", users=users, room_suggestions=all_room_suggestions)

@app.route("/verify_user/<int:user_id>", methods=["POST"])
def verify_user(user_id):
    if 'username' not in session or session["level"] < 20 or not session["verified"]:
        return redirect(url_for("dashboard"))

    user = User.query.get(user_id)
    if user:
        user.is_verified = True
        db.session.commit()
    
    return redirect(url_for("admin_panel"))

@app.route("/delete_user/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    if 'username' not in session or session["level"] < 20 or not session["verified"]:
        return redirect(url_for("dashboard"))

    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()

    return redirect(url_for("admin_panel"))

@app.route("/edit_user/<int:user_id>", methods=["GET", "POST"]) # GET is the form, POST is for processing new data
def edit_user(user_id):
    if 'username' not in session or session["level"] < 20 or not session["verified"]:
        return redirect(url_for("dashboard"))

    user = User.query.get(user_id)
    
    if not user:
        return redirect(url_for("admin_panel"))

    if request.method == "POST":
        message = None 
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        email = request.form.get("email")
        gender = request.form.get("gender")
        role = request.form.get("role")
        level = int(request.form.get("level"))
        birthdate_str = request.form.get("birthdate")
        birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d").date() if birthdate_str else user.birthdate

        if not email or not gender or not fname or not lname or not birthdate_str or not role or level is None:
            message = "All fields must be œfilled"
        elif User.query.filter_by(email=email).first() and email != user.email:
            message = "Email already taken"
        elif gender not in ["male", "femelle"]:
            message = "Gender is incorrect"
        elif role not in ["parent", "child"]:
            message = "Role is incorrect"
        elif birthdate > datetime.today().date():
            message = "He is not Marty McFly"
        elif level < 0:
            message = "Level must be positive"
        elif len(email) > 64 or len(email) < 3 or len(fname) < 3 or len(fname) > 32 or len(lname) < 3 or len(lname) > 32:
            message = "Username, first name, and last name are 32 chars max, email is 64 chars max"
        
        if message: # if there is an error
            return render_template("edit_user.html", user=user, message=message)
        
        # no error means we can update infos
        user.fname = fname
        user.lname = lname
        user.email = email
        user.gender = gender
        user.role = role
        user.birthdate = birthdate
        user.level = level 
        db.session.commit()
        
        return redirect(url_for("admin_panel"))

    return render_template("edit_user.html", user=user)

@app.route("/view_login_history/<int:user_id>")
def view_login_history(user_id):
    if 'username' not in session or session["level"] < 20 or not session["verified"]:
        return redirect(url_for("dashboard"))
    
    user = User.query.get(user_id)
    if user:
        history = LoginHistory.query.filter_by(username=user.username).order_by(LoginHistory.login_time.desc()).all()
        return render_template("view_login_history.html", history=history, user=user)
    else:
        return redirect(url_for("admin_panel"))

@app.route("/kill_admins", methods=["POST"]) # Removes admin rights of  everyone
def kill_admins():
    if 'username' not in session or session["level"] < 20 or not session["verified"]:
        return redirect(url_for("dashboard"))
    
    users = User.query.filter(User.level >= 20, User.username != session["username"]).all()
    
    for user in users:
        user.level = 0
        db.session.commit()
    
    return redirect(url_for("admin_panel"))

@app.route("/backup_db", methods=["POST"])
def backup_db():
    db_path = 'instance/database.db'
    backup_filename = f"backup_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.db"
    backup_path = f"backups/{backup_filename}"
    
    try:
        if not os.path.exists('backups'):
            os.makedirs('backups')
        with open(db_path, 'rb') as source_db:
            with open(backup_path, 'wb') as backup_db:
                backup_db.write(source_db.read())
        return redirect(url_for('admin_panel', message="Sucessfully backed up database"))
    except :
        return redirect(url_for('admin_panel', message="Error while backing up"))

@app.route("/config_maison", methods=["GET"])
def config_maison():
    if 'username' not in session or not session.get("verified"):
        return redirect(url_for("home", message="Veuillez vous connecter pour accéder au tableau de bord."))
    rooms = Room.query.all()
    return render_template("config_maison.html", rooms=rooms, selected_room=None)

@app.route('/create_piece', methods=['POST'])
def create_piece():
    if 'username' not in session or not session.get("verified"):
        return redirect(url_for("home", message="Veuillez vous connecter pour accéder au tableau de bord."))
    name = request.form.get('new_room')
    if name:
        new_room = Room(name=name)
        db.session.add(new_room)
        db.session.commit()
        rooms = Room.query.all()
    return redirect(url_for('config_maison'))

@app.route('/select_piece', methods=['GET'])
def select_piece():
    if 'username' not in session or not session.get("verified"):
        return redirect(url_for("home", message="Veuillez vous connecter pour accéder au tableau de bord."))
    room_id = request.args.get('room_id')
    selected_room = Room.query.get(room_id)
    rooms = Room.query.all()
    return render_template("config_maison.html", rooms=rooms, selected_room=selected_room)

@app.route('/add_object2', methods=['POST'])
def add_object2():
    if 'username' not in session or not session.get("verified"):
        return redirect(url_for("home", message="Veuillez vous connecter pour accéder au tableau de bord."))
    room_id = request.form.get('room_id')
    name = request.form.get('object_name')
    type_ = request.form.get('object_type')
    description = request.form.get('object_description')
    conso = request.form.get('object_consumption')

    if room_id and name and type_ and conso:
        new_object = Object(
            name=name,
            type=type_,
            description=description,
            room_id=room_id,
            consommation_kw_jour=conso,
        )
        db.session.add(new_object)
        db.session.commit()

    return redirect(url_for('select_piece', room_id=room_id))


@app.route('/delete_room2', methods=['POST'])
def delete_or_suggest_room():
    if 'username' not in session or not session.get("verified"): 
        return redirect(url_for("home"))
    
    room_id = request.form.get('room_id');
    if not room_id: 
        return redirect(url_for('config_maison'))
    
    room = Room.query.get(room_id);
    if not room: 
        return redirect(url_for('config_maison'))

    is_admin = session.get("level", 0) >= 20

    if is_admin:
        try:
            db.session.delete(room)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Erreur lors de la suppression de la pièce (Admin): {str(e)}") # DEBUG
    else:
        # not admin
        try:
            existing_suggestion = DelSuggestion.query.filter_by(
                room_id=room.id,
                username=session['username']
            ).first()

            if not existing_suggestion:
                suggestion = DelSuggestion(
                    room_id=room.id,
                    room_name=room.name,
                    username=session['username']
                )
                db.session.add(suggestion)
                db.session.commit()

        except Exception as e:
            db.session.rollback()
            print(f"Erreur lors de l'enregistrement de la suggestion (Non-Admin): {str(e)}") # DEBUG

    return redirect(url_for('config_maison'))

@app.route('/generate_report_global')
def generate_report_global():
    if 'username' not in session or not session.get("verified"):
        return redirect(url_for("home", message="Veuillez vous connecter."))

    rooms = Room.query.all()
    objets = []
    conso_totale = 0
    conso_par_piece = {}
    conso_par_type = {}

    for room in rooms:
        objets_room = room.objects
        for obj in objets_room:
            obj_data = {
                'name': obj.name,
                'type': obj.type,
                'piece': room.name,
                'conso': obj.consommation_kw_jour or 0
            }
            objets.append(obj_data)

            # Conso par pièce
            conso_par_piece[room.name] = conso_par_piece.get(room.name, 0) + obj_data['conso']
            # Conso par type
            if obj.type:
                conso_par_type[obj.type] = conso_par_type.get(obj.type, 0) + obj_data['conso']

            conso_totale += obj_data['conso']

    img_path_pie = generate_pie_chart(conso_par_piece, "Consommation par pièce")
    img_path_bar = generate_bar_chart(conso_par_type, "Consommation par type")

    html = render_template(
        "rapport_pdf.html", #
        username=session["username"],
        date=datetime.now().strftime("%d/%m/%Y %H:%M"),
        total_conso=round(conso_totale, 2),
        total_objets=len(objets),
        total_pieces=len(rooms),
        objets=objets,
        img_pie=img_path_pie,
        img_bar=img_path_bar
    )

    # Génération du PDF 
    pdf = HTML(string=html, base_url=request.host_url).write_pdf()

    # Envoi du fichier en tant que téléchargement
    return send_file(BytesIO(pdf), as_attachment=True, download_name="rapport_maison.pdf", mimetype='application/pdf')


@app.route('/approve_room_deletion/<int:suggestion_id>', methods=['POST'])
def approve_room_deletion(suggestion_id):
    if 'username' not in session or session.get("level", 0) < 20 or not session.get("verified"):
         return redirect(url_for("dashboard"))

    suggestion = DelSuggestion.query.get(suggestion_id)
    if not suggestion:
         return redirect(url_for('admin_panel', message="Suggestion not found."))

    room_id_to_delete = request.form.get('room_id_to_delete')

    room_to_delete = Room.query.get(room_id_to_delete)
    if room_to_delete:
        db.session.delete(room_to_delete)
    
    db.session.delete(suggestion)
    db.session.commit()

    return redirect(url_for('admin_panel', message="Room deletion approved."))

@app.route('/reject_room_deletion/<int:suggestion_id>', methods=['POST'])
def reject_room_deletion(suggestion_id):
    if 'username' not in session or session.get("level", 0) < 20 or not session.get("verified"):
         return redirect(url_for("dashboard"))

    suggestion = DelSuggestion.query.get(suggestion_id)
    if not suggestion:
         return redirect(url_for('admin_panel', message="Suggestion not found."))

    db.session.delete(suggestion)
    db.session.commit()

    return redirect(url_for('admin_panel', message="Suggestion rejected."))

@app.route('/delete_object2', methods=['POST'])
def delete_object2():
    object_id = request.form.get('object_id')
    room_id = request.form.get('room_id')

    obj = Object.query.get(object_id)
    if obj:
        db.session.delete(obj)
        db.session.commit()

    return redirect(url_for('select_piece', room_id=room_id))

@app.route('/edit_object2', methods=['POST'])
def edit_object2():
    if 'username' not in session or not session.get("verified"):
        return redirect(url_for("home", message="Veuillez vous connecter pour accéder au tableau de bord."))

    object_id = request.form.get('object_id')
    room_id = request.form.get('room_id')
    new_name = request.form.get('object_name')
    new_type = request.form.get('object_type')
    new_description = request.form.get('object_description')
    conso = request.form.get('object_consumption')

    obj = Object.query.get(object_id)
    if obj:
        #obj.name = new_name
        obj.type = new_type
        obj.description = new_description
        obj.consommation_kw_jour=conso
        db.session.commit()

    return redirect(url_for('select_piece', room_id=room_id))

def add_points(username, points):
    user = User.query.filter_by(username=username).first()
    
    if not user:
        return False 
    
    user.level += points
    db.session.commit()
    return True

def log_user_login(username):
    login_history = LoginHistory(username=username)
    db.session.add(login_history)
    db.session.commit()

# start server and init db
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
