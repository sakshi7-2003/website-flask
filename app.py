from flask import Flask
from flask import render_template
from flask import request
from flask import redirect,flash
from flask import session,make_response
from flask_mail import Mail,Message

import mysql.connector
conn=mysql.connector.connect(host="localhost",username="root",password="sakshi#2003**",database="mydata")
curser=conn.cursor()
app=Flask("__name__")

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'jamwalsakshi877@gmail.com'
app.config['MAIL_PASSWORD'] = 'timw cykn lnmm vfvs'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail=Mail(app)

app.secret_key="hello python"
app.secret_key="world"

@app.route("/")
def home():
    return render_template("home.html")
@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/savedata",methods=["post"])
def savedata():
    if request.method=="POST":
        fname=request.form.get("name")
        email=request.form.get("email")
        subject=request.form.get("subject")
        company=request.form.get("company")
        message=request.form.get("message")
        curser.execute(f"insert into hello values('{fname}','{email}','{subject}','{company}','{message}')")
    flash("your data saved successfully....")
    conn.commit()

    msg = Message("Indeed!", sender = "Indeed.alert@indeed.com", recipients = ["rohitanshalanshal@gmail.com"])

    msg.body = f"""UserInfo:::
        Name = {fname}
        Email = {email}
        subject = {subject}
        Message = {message}
        company={company}"""
    mail.send(msg)

    return redirect("/contact")



@app.route("/showdata")
def showdata():
    curser.execute("select*from hello;")
    data=curser.fetchall()
    return render_template("showdata.html",alldata=data)

@app.route("/deletedata/<x>", methods = ["POST"])
def deletethis(x):
    curser.execute(f"delete from hello where Name = '{x}'")
    conn.commit()
    return redirect("/showdata")

@app.route("/updatenow/<x>", methods = ["POST"])
def updatenow(x):
    if request.method == "POST":
       fname=request.form.get("name")
    email=request.form.get("email")
    subject=request.form.get("subject")
    company=request.form.get("company")
    message=request.form.get("message")
    curser.execute(f'update mydata set Name = "{fname}", email = "{email}", subject = "{subject}",company="{company}" message = "{message}" where Name = "{x}";')
    conn.commit()

    flash("Your data updated sucessfully")

    return redirect("/showdata")




if __name__=="__main__":
    app.run(debug=True)