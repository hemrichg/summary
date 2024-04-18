from random import randint

def validate_creditentials(username, password):
    if not username:
        return "Username cannot be blank."
    
    if not password:
        return "Password cannot be blank."
    
    if len(username) > 5:
        return "Username cannot be longer than 5 characters."
    
    if len(password) > 5:
        return "Password cannot be longer than 5 characters."
    
    return "valid"

def add_user_to_db(db, username, password):
    if username in db:
        return "Username already exists..."
    
    db[username] = {
        "password": password,
        "token": None
    }

    return "Successful registration..."

def user_logged_in(db, username, password):
    if username in db:
        if password == db[username]["password"]:
            return True
    
    return False

def create_token_for_user(db, username):
    rnd = randint(100,999)
    token = f"tokenFor{username}{rnd}"
    db[username]["token"] = token

    return token

def token_in_db(db, token):
    for k, v in db.items():
        if v["token"] == token:
            return True
    
    return False
