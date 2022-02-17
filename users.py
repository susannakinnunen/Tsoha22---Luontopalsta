#from pickle import FALSE
from db import db
from flask import session, abort, request
from werkzeug.security import check_password_hash, generate_password_hash
import secrets

def login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["csrf_token"] = secrets.token_hex(16)
            return True
        else:
            return False

def logout():
    del session["user_id"]

def register(username, password):
    hash_value = generate_password_hash(password)

    try:
        sql = "INSERT INTO users (username,password,is_admin) VALUES (:username,:password, FALSE)"
        db.session.execute(sql, {"username":username, "password":hash_value, "is_admin":False})
        db.session.commit()
    except:
        return False

    return login(username, password)

def get_user_name():
    userid = user_id()
    if userid != 0:
        sql = "SELECT username FROM users WHERE id=:userid"
        result = db.session.execute(sql, {"userid":userid})
        list_result = result.fetchone()
        username = list_result[0]
        return username
    else:
        return False


def user_id():
    return session.get("user_id",0)

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

def is_admin():
    userid = user_id()
    print(f"printtaa userid:{userid}")
    sql = "SELECT is_admin FROM users WHERE id=:user_id"
    result = db.session.execute(sql, {"user_id":userid})
    list_result = result.fetchone()
    if list_result != None:
        print(f"printtaa list_result[0] {list_result}")
        is_admin_value = list_result[0]
        if is_admin_value:
            return True
        else:
            return False
    else:
        return False