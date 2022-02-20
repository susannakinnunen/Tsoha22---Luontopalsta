from db import db

def send_image(name,data):    
    image_sql = "INSERT INTO images (name,data) VALUES (:name,:data) RETURNING id"
    result = db.session.execute(image_sql, {"name":name, "data":data})
    db.session.commit()
    image_id = result.fetchone()[0]
    return image_id

def add_message_id(message_id,image_id):
    sql = "UPDATE images SET message_id=:message_id WHERE id=:image_id"
    db.session.execute(sql, {"message_id":message_id,"image_id":image_id})
    db.session.commit()
    return True

def get_list_image():
    sql = "SELECT id,message_id FROM images"
    result = db.session.execute(sql)
    return result.fetchall()
