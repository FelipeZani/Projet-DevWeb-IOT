from flask_mailman import EmailMessage



accounts_to_confirm = {}

def add_dict_confirmation_list(user_id,user_info):
    global accounts_to_confirm
    accounts_to_confirm[user_id] = user_info

def send_mail(to_mail,user_name,user_token):
    try:
        url_validation = f"http://127.0.0.1:5000/signup/{str(user_token)}"
        msg = EmailMessage(
            subject="Sign up validation",
            body=f"Dear {str(user_name)},\nPlease click on the following link in order to validate your signup in our website:\n{url_validation}",
            from_email="projetweb.iot@gmail.com",
            to=[to_mail]
        )
        msg.send()
        
        print(f"Email sent successfully to {to_mail}")        
    except Exception as e:
         print(f"Email failed {to_mail}\n error: {e}")