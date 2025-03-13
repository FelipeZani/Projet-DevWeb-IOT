from flask import Flask, jsonify
from flask_mailman import Mail, EmailMessage

app = Flask(__name__)

app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = "projetweb.iot@gmail.com"
app.config['MAIL_PASSWORD'] = "kpdm hdvx jtic fvul"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


def send_mail(to_mail,user_name,url_validation):
    try:
        msg = EmailMessage(
            subject="Sign up validation",
            body="Dear "+user_name+",\nPlease click on the following link in order to validate you enrollment in our app:\n"+url_validation,
            from_email="projetweb.iot@gmail.com",
            to=[to_mail]
        )
        msg.send()
        return jsonify({"message": "Email sent successfully"}), 202  
    except Exception as e:
        return jsonify({"error": str(e)}), 500