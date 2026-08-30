from flask import Flask,render_template,request
import requests

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

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)