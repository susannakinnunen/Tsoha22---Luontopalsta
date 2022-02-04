from db import db
import users

def get_list_area():
    sql = "SELECT A.content, U.username, A.sent_at FROM areas A, users U WHERE A.user_id=U.id ORDER BY A.id"
    result = db.session.execute(sql)
    return result.fetchall()

def send_area(title):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO areas (content, user_id, sent_at) VALUES (:content, :user_id, NOW())"
    db.session.execute(sql, {"content":title, "user_id":user_id})
    db.session.commit()
    return True