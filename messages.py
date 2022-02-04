from db import db
import users

def get_list_message():
    print("näkyykö2")
    sql = "SELECT M.content, U.username, M.sent_at, A.content FROM messages M, users U, areas A WHERE M.user_id=U.id AND M.area_id=A.id ORDER BY M.id"
    print("näkyykö3")
    result = db.session.execute(sql)
    print("näkyykö4S")
    return result.fetchall()

def send_message(content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO messages (content, user_id, sent_at) VALUES (:content, :user_id, NOW())"
    db.session.execute(sql, {"content":content, "user_id":user_id})
    db.session.commit()
    return True