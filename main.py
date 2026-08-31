from flask import Flask,render_template,request
import requests
import smtplib

response=requests.get("https://api.npoint.io/674f5423f73deab1e9a7")
response=response.json()

app=Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html",response=response)

@app.route("/post")
def nextt():
    title = request.args.get("title")
    subtitle = request.args.get("subtitle")
    body = request.args.get("body")
    return render_template("post.html",title=title,subtitle=subtitle,body=body)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact",methods=["POST","Get"])
def contact():
    if request.method == "POST":
        print("function start")
        Name=request.form['name']
        Email=request.form['email']
        Phone=request.form['phone']
        Messages=request.form['message']
        sendmail(Name,Email,Phone,Messages)
        return render_template("contact.html",msg=True)
    return render_template("contact.html",msg=False)

def sendmail(Name,Email,Phone,Messages):
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user="",password="")
        connection.sendmail(
            from_addr="",
            to_addrs="",
            msg=f"Subject:User Message\n\n Name:{Name}\nEmail:{Email}\nPhone:{Phone}\nMessages:{Messages}")

if __name__ == "__main__":
    app.run(debug=True)