from app import app
from flask import render_template, request, redirect, make_response
import users, areas, messages, images
from db import db

@app.route("/")
def index():
    list = areas.get_list_area()
    user_name = users.get_user_name()
    if user_name == False:
        return render_template("index.html", count=len(list), areas=list)
    if users.is_admin():
        is_admin = True
        return render_template("index.html", count=len(list), areas=list, is_admin=is_admin, user_name=user_name)
    else: 
        is_admin = False
    return render_template("index.html", count=len(list), areas=list,user_name=user_name)

@app.route("/edit_message/<string:message_id>")
def edit_message(message_id):
    message_content = messages.get_message(message_id)
    user_name = users.get_user_name()
    return render_template("edit_message.html", message_content=message_content,message_id=message_id, user_name=user_name)
  

@app.route("/send_message_edit", methods=["GET","POST"])
def send_message_edit():
    check_csrf = users.check_csrf()
    edited_message  = request.form["content"]
    message_id = request.form["message_id"]
    messages.edit_message(message_id,edited_message)
    area_content = areas.get_area_content(message_id)
    area_creation_time = areas.get_area_sent_at(area_content,message_id)
    return redirect("/messages/"+ str(area_content) + "/" + str(area_creation_time))

@app.route("/delete_message/<string:message_id>")
def delete_message(message_id):
    message_content = messages.get_message(message_id)
    area_content = areas.get_area_content(message_id)
    area_creation_time = areas.get_area_sent_at(area_content,message_id)
    return render_template("delete_message.html", message_content=message_content, message_id=message_id,area_content=area_content,area_creation_time=area_creation_time)

@app.route("/deletion_confirmation/<string:message_id>")
def deletion_confirmation(message_id):
    messages.delete_message(message_id)
    area_content = areas.get_area_content(message_id)
    area_creation_time = areas.get_area_sent_at(area_content,message_id)
    return render_template("deletion_confirmation.html", area_content=area_content,area_creation_time=area_creation_time)


@app.route("/messages/<string:content>/<string:time>", methods=["GET"])
def get_list_message(content,time):
    user_name = users.get_user_name()
    area_content = content
    area_creation_time = time
    list = messages.get_list_message(area_content, area_creation_time)
    list_ob_info = messages.get_list_ob_info()
    list_images = images.get_list_image()
    return render_template("messages.html", count=len(list)+len(list_images), messages=list, ob_infos = list_ob_info, images=list_images, area_content=area_content, time=time, user_name=user_name)

@app.route("/admin")
def admin():
    user_name = users.get_user_name()
    return render_template("admin.html", user_name=user_name)

@app.route("/reported_areas")
def get_list_reported_areas():
    user_name = users.get_user_name()
    list = areas.get_list_reported_areas()
    return render_template("reported_areas.html", count=len(list), areas=list,user_name=user_name)



@app.route("/new_area")
def new_area():
    user_name = users.get_user_name()
    return render_template("new_area.html", user_name=user_name)

@app.route("/send_area", methods=["POST"])
def send_area():
    check_csrf = users.check_csrf()
    title = request.form["title"]
    if len(title) <= 0:
        return render_template("error.html", message="Alueen nimi ei voi olla tyhjä")
    if len(title) > 100:
        return render_template("error.html", error="Alueen nimi on liian pitkä")
    elif areas.send_area(title):
        return redirect("/")
    else:
        return render_template("error.html", message="Viestin lähetys ei onnistunut")


@app.route("/new_message/<string:area_content>/<string:time>")
def new_message(area_content,time):
    user_name = users.get_user_name()
    return render_template("new_message.html", area_content=area_content, time=time, user_name=user_name)



@app.route("/send_message/<string:area_content>/<string:time>", methods=["POST"])
def send_message(area_content,time):
    check_csrf = users.check_csrf()
    message_content = request.form["content"]
    observation_date = request.form["date"]
    observation_time = request.form["time"]
    location = request.form["name"]
    if len(message_content) <= 0:
        return render_template("error.html", message="Viesti ei voi olla tyhjä")
    if len(message_content) > 5000:
        return render_template("error.html", error="Viesti on liian pitkä")
    if len(str(observation_date)) <= 0:
        return render_template("error.html", message="Lisää vielä päivämäärä, kiitos!")
    if len(str(observation_time)) <= 0:
        return render_template("error.html", message="Lisää vielä kellonaika, kiitos!")
    if len(location) <= 0:
        return render_template("error.html", message="Lisää vielä sijainti, kiitos!")
    
    if messages.send_message(message_content, area_content,time, observation_date=observation_date,observation_time=observation_time,location=location) != False:
        return redirect("/messages/" + str(area_content) + "/" + str(time))
    else:
        return render_template("error.html", message="Viestin lähetys ei onnistunut")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")
    

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")

@app.route("/report_area/<string:area_content>/<string:time>")
def report_area(area_content,time):
    user_name = users.get_user_name()
    return render_template("report_area.html", area_content=area_content,time=time,user_name=user_name)


@app.route("/send_report_area/<string:area_content>/<string:time>", methods=["POST"])
def send_report_area(area_content,time):
    check_csrf = users.check_csrf()
    report_message_content = request.form["content"]
    if len(report_message_content) > 5000:
        return render_template("error.html", error="Perustelut-osio on liian pitkä")
    areas.send_report_area(area_content,report_message_content,time)
    return redirect("/messages/" + str(area_content) + "/" + str(time))

@app.route("/hide_area/<string:content>/<string:time>")
def hide_area(content,time):
    areas.hide_area(content,time)
    return redirect("/reported_areas")


@app.route("/reported_messages")
def get_list_reported_messages():
    user_name = users.get_user_name()
    list = messages.get_list_reported_messages()
    return render_template("reported_messages.html", count=len(list), messages=list, user_name=user_name)


@app.route("/hide_message/<string:content>/<string:area_id>/<string:message_sent_at>")
def hide_message(content,area_id,message_sent_at):
    messages.hide_message(content,area_id,message_sent_at)
    return redirect("/reported_messages")


@app.route("/report_message/<string:message_id>/<string:area_content>/<string:message_sent_time>")
def report_message(message_id,area_content,message_sent_time):
    user_name = users.get_user_name()
    message_content = messages.get_message(message_id)
    return render_template("report_message.html", message_id=message_id, message_content=message_content,area_content=area_content,message_sent_time=message_sent_time,user_name=user_name)

@app.route("/send_report_message/<string:message_id>/<string:area_content>/<string:message_sent_at>", methods=["POST"])
def send_report_message(message_id,area_content,message_sent_at):
    check_csrf = users.check_csrf()
    report_message_content = request.form["content"]
    if len(report_message_content) > 5000:
        return render_template("error.html", error="Perustelut-osio on liian pitkä")
    area_sent_at = areas.get_area_sent_at(area_content,message_id)
    messages.send_report_message(message_id,report_message_content,area_content,message_sent_at,area_sent_at)
    return redirect("/messages/" + str(area_content) + "/" + str(area_sent_at))

@app.route("/remove_area_report/<string:area_report_id>")
def remove_area_report(area_report_id):
    areas.remove_area_report(area_report_id)
    return redirect("/reported_areas")

@app.route("/remove_message_report/<string:message_report_id>")
def remove_message_report(message_report_id):
    messages.remove_message_report(message_report_id)
    return redirect("/reported_messages")

@app.route("/query")
def query():
    return render_template("query.html")

@app.route("/result")
def result():
    query = request.args["query"]
    search_results = messages.search(query)
    if len(search_results) == 0:
        return render_template("error.html", message=f"Hakusanalla '{query}' ei tuloksia.")
    return render_template("result.html", search_results=search_results)

@app.route("/new_image/<string:area_content>/<string:time>")
def new_image(area_content,time):
    user_name = users.get_user_name()
    return render_template("new_image.html", area_content=area_content,time=time,user_name=user_name)


@app.route("/send_image/<string:area_content>/<string:time>", methods=["POST"])
def send_image(area_content,time):
    check_csrf = users.check_csrf()
    file = request.files["file"]
    name = file.filename
    if not name.endswith(".jpg"):
        return "Kuvan loppuosa tulee olla .jpg"
    data = file.read()
    if len(data) > 300*1024:
        return "Kuva on liian iso. Maksimikoko on 307 kilotavua"
    observation_date = request.form["date"]
    observation_time = request.form["time"]
    location = request.form["name"]
    title = request.form["title"]
    if len(title) <= 0:
        return render_template("error.html", message="Alueen nimi ei voi olla tyhjä")
    if len(title) > 100:
        return render_template("error.html", error="Alueen nimi on liian pitkä")
    image_id = images.send_image(name,data)
    message_id = messages.send_message(title,area_content,time,observation_date,observation_time,location)
    messages.add_image_id(image_id,message_id)
    images.add_message_id(message_id,image_id)
    return redirect("/messages/" + str(area_content) + "/" + str(time))


@app.route("/show/<int:id>")
def show_image(id):
    sql = "SELECT data FROM images WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    data = result.fetchone()[0]
    response = make_response(bytes(data))
    response.headers.set("Content-Type", "image/jpeg")
    return response

