from db import db
import users,areas

def get_list_message(area_content):
    area_id = areas.get_area_id(area_content)
    sql = "SELECT M.content, U.username, M.sent_at FROM messages M, users U, areas A WHERE M.user_id=U.id AND A.id=:area_id AND M.area_id=:area_id ORDER BY M.id"
    result = db.session.execute(sql, {"area_id":area_id})
    return result.fetchall()

def send_message(message_content,area_content):
    user_id = users.user_id()
    area_id = areas.get_area_id(area_content)
    if user_id == 0:
        return False
    sql = "INSERT INTO messages (content, user_id, area_id, sent_at) VALUES (:content, :user_id, :area_id, NOW())"
    db.session.execute(sql, {"content":message_content, "user_id":user_id, "area_id":area_id})
    db.session.commit()
    return True

