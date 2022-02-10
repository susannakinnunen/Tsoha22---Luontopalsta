from app import app
from flask import render_template, request, redirect
import users, areas, messages

@app.route("/")
def index():
    list = areas.get_list_area()
    return render_template("index.html", count=len(list), areas=list)

@app.route("/messages/<string:content>")
def get_list_message(content):
    area_content = content
    list = messages.get_list_message(area_content)
    print(list)
    return render_template("messages.html", count=len(list), messages=list, area_content=area_content)


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


@app.route("/new_message/<string:area_content>")
def new_message(area_content):
    return render_template("new_message.html", area_content=area_content)



@app.route("/send_message/<string:area_content>", methods=["POST"])
def send_message(area_content):
    message_content = request.form["content"]
    if len(message_content) <= 0:
        return render_template("error.html", message="Viesti ei voi olla tyhjä")
    elif messages.send_message(message_content, area_content):
        return redirect("/messages/" + str(area_content))
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

@app.route("/report_area/<string:area_content>/<string:area_creator_user>",  methods=["POST"])
def report_area(area_content, area_creator_user):
    reporter = users.user_id()
    return render_template("report_area.html", area_content=area_content, reporter=reporter, area_creator_user=area_creator_user)




@app.route("/send_report_area/<string:area_content>/string:<area_creator_user>", methods=["POST"])
def send_report_area(area_content, area_creator_user,reporter):
    message_content = request.form["content"]
    areas.send_report_area(area_content,area_creator_user,reporter,message_content)
    return redirect("/messages/" + str(area_content))
