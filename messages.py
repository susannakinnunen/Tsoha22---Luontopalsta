from db import db
import users,areas

def get_list_message(area_content,time):
    area_id = areas.get_area_id(area_content,time)
    sql = "SELECT M.content, U.username, M.sent_at, M.id FROM messages M, users U, areas A WHERE M.user_id=U.id AND M.area_id = A.id AND A.id=:area_id AND M.area_id=:area_id AND M.visible=True AND A.sent_at=:area_creation_time ORDER BY M.id"
    result = db.session.execute(sql, {"area_id":area_id, "area_creation_time":time})
    return result.fetchall()

def search(query):
    sql = "SELECT M.content, A.content, U.username, M.sent_at, M.id FROM messages M, areas A, users U WHERE M.content LIKE :query AND M.area_id = A.id AND A.visible=True AND M.visible=True and M.user_id=U.id"
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    messages = result.fetchall()
    return messages

def get_list_ob_info():
    sql = "SELECT day, time, message_id, location FROM observation_info"
    result = db.session.execute(sql)
    return result.fetchall()    

def send_message(message_content,area_content,time,observation_date,observation_time,location):
    user_id = users.user_id()
    area_id = areas.get_area_id(area_content,time)
    if user_id == 0:
        return False
    sql_messages = "INSERT INTO messages (content, user_id, area_id, sent_at, visible) VALUES (:content, :user_id, :area_id, NOW(), True) RETURNING id"
    result = db.session.execute(sql_messages, {"content":message_content, "user_id":user_id, "area_id":area_id})
    db.session.commit()
    message_id = result.fetchone()[0]
    sql_observation_info = "INSERT INTO observation_info (day,time,message_id,location) VALUES (:observation_date, :observation_time, :message_id, :location)"
    db.session.execute(sql_observation_info, {"observation_date":observation_date, "observation_time":observation_time, "message_id":message_id, "location":location})
    db.session.commit()
    return message_id

def get_message(message_id):
    sql = "SELECT content FROM messages WHERE id=:message_id AND visible=True"
    result = db.session.execute(sql, {"message_id":message_id})
    list_result = result.fetchone()
    message_content = list_result[0]
    return message_content

def get_message_creator_id(message_id):
    sql= "SELECT user_id FROM messages WHERE id=:message_id"
    result = db.session.execute(sql, {"message_id":message_id})
    list_result = result.fetchone()
    message_creator_id = list_result[0]
    return message_creator_id

def get_message_creator_name(message_id):
    sql= "SELECT username FROM messages M, users U WHERE M.id=:message_id and U.id=M.user_id"
    result = db.session.execute(sql, {"message_id":message_id})
    list_result = result.fetchone()
    message_creator_id = list_result[0]
    return message_creator_id

def send_report_message(message_id,report_message_content, area_content, message_sent_at, area_sent_at):
    reporter = users.user_id()
    message_creator_id = get_message_creator_id(message_id)
    area_id = areas.get_area_id(area_content,area_sent_at)
    sql = "INSERT INTO reported_messages (message_id, area_id, sent_at, message_creator_id, reporter, report_message_content,org_message_sent_at) "\
            "VALUES (:message_id, :area_id, NOW(), :message_creator_id, :reporter, :report_message_content, :message_sent_at)"
    result = db.session.execute(sql, {"message_id":message_id, "area_id":area_id, "message_creator_id":message_creator_id, "reporter":reporter, "report_message_content":report_message_content, "message_sent_at":message_sent_at})
    db.session.commit()
    return True

def get_list_reported_messages():
    sql = "SELECT M.content, M.area_id, Ua.username, Ub.username, R.report_message_content, R.sent_at, A.content, M.sent_at, R.id, M.id FROM messages M, users Ua, users Ub, reported_messages R, areas A " \
            "WHERE M.id=R.message_id AND Ua.id=R.message_creator_id AND Ub.id=R.reporter AND M.area_id=A.id AND A.id=R.area_id AND M.visible=True AND A.visible=True"
    result = db.session.execute(sql)
    return result.fetchall()

def hide_message(message_id):
    sql = "UPDATE messages SET visible=False WHERE id=:message_id"
    db.session.execute(sql, {"message_id":message_id})
    db.session.commit()
    return True

def remove_message_report(message_report_id):
    sql = "DELETE FROM reported_messages WHERE id=:message_report_id"
    db.session.execute(sql, {"message_report_id":message_report_id})
    db.session.commit()
    return True

def edit_message(message_id, edited_message):
    sql= "UPDATE messages SET content=:edited_message WHERE id=:message_id"
    db.session.execute(sql, {"edited_message":edited_message, "message_id":message_id,})
    db.session.commit()
    return True


def delete_message(message_id):
    sql = "UPDATE messages SET visible=False WHERE id=:message_id"
    db.session.execute(sql, {"message_id":message_id})
    db.session.commit()
    return True

def get_area_id_with_message_id(message_id):
    sql= "SELECT area_id FROM messages WHERE id=:message_id"
    result = db.session.execute(sql, {"message_id":message_id})
    list_result = result.fetchone()
    area_id = list_result[0]
    return area_id
