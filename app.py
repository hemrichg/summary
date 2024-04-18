from flask import Flask, request, send_file, render_template, make_response
from utils import validate_creditentials, add_user_to_db, user_logged_in, create_token_for_user, token_in_db

# TODO: help: form Content-Type:, Content-Length: master: Cookie:


users_db = {}


app = Flask(__name__)


@app.get("/")
def get_root():
    return "endpoints:\n\n" \
            + "/registration\tGET\n" \
            + "/registration\tPOST\n" \
            + "/login\t\t\tGET\n" \
            + "/login\t\t\tPOST\n" \
            + "/profile/<user>\tGET\n" \
            + "/master\t\tGET\n" \
            + "/protected\t\tGET"

@app.get("/registration")
def get_registration():
    return send_file("registration.html")

@app.post("/registration")
def post_registration():
    username = request.form["user"]
    password = request.form["pass"]

    creds_are_valid = validate_creditentials(username, password)

    if creds_are_valid == "valid":
        return add_user_to_db(users_db, username, password)
    else:
        return creds_are_valid

@app.get("/login")
def get_login():
    return send_file("login.html")

@app.post("/login")
def post_login():
    username = request.form["user"]
    password = request.form["pass"]
    
    creds_are_valid = validate_creditentials(username, password)

    if creds_are_valid == "valid":
        if user_logged_in(users_db, username, password):
            response = make_response(f"Welcome {username}!")
            response.set_cookie("token", create_token_for_user(users_db, username))

            return response
        
    else:
        return creds_are_valid

@app.get("/profile/<user>")
def get_profile(user):
    if len(user) < 25:
        if user in users_db:
            return render_template("profile.html", username=user)
    
        return f"{user} not found..."
    
    return "Invalid user..."


@app.get("/master")
def get_master():
    token = request.args.get("token")
    
    if token:
        if len(token) > 25:
            return "Invalid parameter..."
        
        if token_in_db(users_db, token):
            return "Route /protected has a query param 'masterPassword'.\nUse: VeryStrongPw1234"
        
        return "Wrong token..."

    return "This route has a query param 'token'. If you got your token, set it's value!"

@app.get("/protected")
def get_protected():
    password = request.args.get("masterPassword")
    token = request.cookies.get("token")

    if password:
        if len(password) < 25:
            if password == "VeryStrongPw1234":
                if token:
                    if token_in_db(users_db, token):
                        return "Feel the culture: https://mimox.com/"
                    
                    return "Invalid token..."

                return "You have no access for this site..."
                    
            return "Wrong password..."

        return "Wrong password..."

    return "You have no access for this site..."


if __name__ == "__main__":
    app.run(port=8080)