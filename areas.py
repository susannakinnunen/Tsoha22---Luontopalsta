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
    result = db.session.execute(sql, {"content":title, "user_id":user_id})
    db.session.commit()
    return True

def get_area_id(area_content):
    sql_area_id = "SELECT id FROM areas WHERE content=:content"
    area_id_result = db.session.execute(sql_area_id, {"content":area_content})
    list_area_id = area_id_result.fetchone()
    area_id = list_area_id[0]
    return area_id

def send_report_area(area_content,area_creator_user,reporter,message_content):
    area_id = get_area_id()
    sql = "INSERT INTO reported (area_id, sent_at, area_creator_user, reporter, report_message_content) VALUES (:area_id, NOW(), :area_creator_user, :reporter, :message_content)"
    result = db.session.execute(sql, {"area_id":area_id, "area_creator_user":area_creator_user, "reporter":reporter, "report_message_content":message_content})
    db.session.commit()
    return True
