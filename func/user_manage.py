from django.contrib.auth.models import User

def get_username(email) :
    if email != 'admin@mail.com' :
        username = User.objects.get(email=email).username
        if username :
            return username
        
    return None

def check_email(username, email) :
    if username != 'admin' and email != 'admin@mail.com' :
        return email == User.objects.get(username=username).email
    
    return False