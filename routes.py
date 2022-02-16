from app import app
from flask import render_template, request, redirect
import users, areas, messages

@app.route("/")
def index():
    list = areas.get_list_area()
    if users.is_admin():
        is_admin = True
        return render_template("index.html", count=len(list), areas=list, is_admin=is_admin)
    else: 
        is_admin = False
    return render_template("index.html", count=len(list), areas=list)

@app.route("/messages/<string:content>/<string:time>", methods=["GET"])
def get_list_message(content,time):
    area_content = content
    area_creation_time = time
    list = messages.get_list_message(area_content, area_creation_time)
    return render_template("messages.html", count=len(list), messages=list, area_content=area_content, time=time)

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/reported_areas")
def get_list_reported_areas():
    list = areas.get_list_reported_areas()
    return render_template("reported_areas.html", count=len(list), areas=list)

@app.route("/reported_messages")
def get_list_reported_messages():
    list = messages.get_list_reported_messages()
    return render_template("reported_messages.html", count=len(list), messages=list)


@app.route("/new_area")
def new_area():
    return render_template("new_area.html")

@app.route("/send_area", methods=["POST"])
def send_area():
    title = request.form["title"]
    if len(title) <= 0:
        return render_template("error.html", message="Alueen nimi ei voi olla tyhjä")
    elif areas.send_area(title):
        return redirect("/")
    else:
        return render_template("error.html", message="Viestin lähetys ei onnistunut")


@app.route("/new_message/<string:area_content>/<string:time>")
def new_message(area_content,time):
    return render_template("new_message.html", area_content=area_content, time=time)



@app.route("/send_message/<string:area_content>/<string:time>", methods=["POST"])
def send_message(area_content,time):
    message_content = request.form["content"]
    if len(message_content) <= 0:
        return render_template("error.html", message="Viesti ei voi olla tyhjä")
    elif messages.send_message(message_content, area_content,time):
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
    return render_template("report_area.html", area_content=area_content,time=time)


@app.route("/send_report_area/<string:area_content>/<string:time>", methods=["POST"])
def send_report_area(area_content,time):
    report_message_content = request.form["content"]
    areas.send_report_area(area_content,report_message_content,time)
    print(f"printtaa{time}")
    return redirect("/messages/" + str(area_content) + "/" + str(time))

@app.route("/hide_area/<string:content>/<string:time>")
def hide_area(content,time):
    areas.hide_area(content,time)
    return redirect("/reported_areas")


@app.route("/hide_message/<string:content>/<string:area>/<string:message_sent_at>")
def hide_message(content,area,message_sent_at):
    print("NÄKYYKÖ")
    messages.hide_message(content,area,message_sent_at)
    return redirect("/reported_messages")


@app.route("/report_message/<string:message_id>/<string:area_content>/<string:message_sent_time>")
def report_message(message_id,area_content,message_sent_time):
    message_content = messages.get_message(message_id)
    return render_template("report_message.html", message_id=message_id, message_content=message_content,area_content=area_content,message_sent_time=message_sent_time)

@app.route("/send_report_message/<string:message_id>/<string:area_content>/<string:message_sent_at>", methods=["POST"])
def send_report_message(message_id,area_content,message_sent_at):
    report_message_content = request.form["content"]
    print("päästäänkö1")
    area_sent_at = areas.get_area_sent_at(area_content,message_id)
    print("päästäänkö2")
    messages.send_report_message(message_id,report_message_content,area_content,message_sent_at,area_sent_at)
    print("päästäänkö3")
    return redirect("/messages/" + str(area_content) + "/" + str(area_sent_at))