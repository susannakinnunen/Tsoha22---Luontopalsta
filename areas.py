from db import db
import users

def get_list_area():
    sql = "SELECT A.content, U.username, A.sent_at FROM areas A, users U WHERE A.user_id=U.id AND A.visible=True ORDER BY A.id"
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

def get_area_creator_id(area_content):
    sql= "SELECT user_id FROM areas WHERE content=:area_content"
    result = db.session.execute(sql, {"area_content":area_content})
    list_result = result.fetchone()
    area_creator_id = list_result[0]
    return area_creator_id

def send_report_area(area_content,report_message_content):
    area_id = get_area_id(area_content)
    area_creator_id = get_area_creator_id(area_content)
    reporter = users.user_id()
    sql = "INSERT INTO reported_areas (area_id, sent_at, area_creator_id, reporter, report_message_content) VALUES (:area_id, NOW(), :area_creator_id, :reporter, :report_message_content)"
    result = db.session.execute(sql, {"area_id":area_id, "area_creator_id":area_creator_id, "reporter":reporter, "report_message_content":report_message_content})
    db.session.commit()
    return True

def get_list_reported_areas():
    sql = "SELECT A.content, Ua.username, Ub.username, R.report_message_content, R.sent_at  FROM areas A, users Ua, users Ub, reported_areas R WHERE A.id=R.area_id AND Ua.id=R.area_creator_id AND Ub.id=R.reporter AND A.visible=True"
    result = db.session.execute(sql)
    return result.fetchall()

def hide_area(content):
    sql = "UPDATE areas SET visible=False WHERE content=:content"
    db.session.execute(sql, {"content":content})
    db.session.commit()
    return True