from flask import Flask, render_template, redirect, url_for,request,flash,abort
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,relationship
from sqlalchemy import Integer, String, Text
from form import blog,registration,login,comments
from flask_ckeditor import CKEditor
from datetime import date
from functools import wraps
from werkzeug.security import check_password_hash,generate_password_hash
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_gravatar import Gravatar
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

SENDER_MAIL=os.getenv('sender')
RECIVER_MAIL=os.getenv('reciver')
SENDER_PASS=os.getenv('password')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('app_key')
Bootstrap5(app)
checkeditor=CKEditor(app)

loginmanager=LoginManager()
loginmanager.init_app(app)

gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('sql_key')
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    author = relationship("UserPost", back_populates="posts")
    comments=relationship("Comments", back_populates="parent_post")


class UserPost(UserMixin,db.Model):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name:Mapped[str]=mapped_column(String,nullable=True)
    email:Mapped[str]=mapped_column(String,nullable=True,unique=True)
    password:Mapped[str]=mapped_column(String,nullable=True)
    
    posts = relationship("BlogPost", back_populates="author")
    comments= relationship("Comments", back_populates="comment_author")

class Comments(db.Model):
    __tablename__ = "comment"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text:Mapped[str]=mapped_column(String,nullable=True)
    
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    comment_author = relationship("UserPost", back_populates="comments")
    parent_post = relationship("BlogPost", back_populates="comments")
    post_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("blog_posts.id"))
    

@loginmanager.user_loader
def load_user(user_id):
    return db.session.get(UserPost, int(user_id))    

def admin_only(f):
    @wraps(f)
    def decorated_funtion():
        if current_user.id != 1:
            return abort(404)
        return f()
    return decorated_funtion

with app.app_context():
    db.create_all()


@app.route('/')
def get_all_posts():
    data=db.session.execute(db.select(BlogPost))
    posts = data.scalars().all()
    return render_template("index.html", all_posts=posts,loggin=current_user)

@app.route('/<int:post_id>',methods=["POST","GET"])
def show_post(post_id):
    form=comments()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            
            user_comment=Comments(text=form.comment_box.data,
                                  comment_author=current_user,
                                  post_id=post_id)
            db.session.add(user_comment)
            db.session.commit()
            return redirect(url_for('show_post',post_id=post_id))
        else:
            flash("for doing comment you need to login")
            return redirect(url_for('logins'))
    comment_list=db.session.execute(db.select(Comments).where(Comments.post_id == post_id))
    comment_l=comment_list.scalars().all()
    requested_post = db.get_or_404(BlogPost,post_id)
    return render_template("post.html", post=requested_post,loggin=current_user,form=form,coment=comment_l)


@app.route("/new",methods=['POST',"GET"])
@admin_only
def add():
    form=blog()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.check.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template('make-post.html',form=form,loggin=current_user)


@app.route("/edit/<int:id>",methods=["GET","POST"])
@admin_only
def edit(id):
    
    blog_select=db.get_or_404(BlogPost,id)
    form=blog(
    title=blog_select.title,
    subtitle=blog_select.subtitle,
    check=blog_select.body,
    img_url=blog_select.img_url,
    author=blog_select.author)
    
    if form.validate_on_submit():
        blog_select.title = form.title.data
        blog_select.subtitle = form.subtitle.data
        blog_select.img_url = form.img_url.data
        blog_select.author = form.author.data
        blog_select.body = form.check.data    
        db.session.commit()
        return redirect(url_for("show_post", post_id=blog_select.id,))
    
    return render_template('make-post.html',form=form,loggin=current_user)


@app.route("/delte/<int:id>")
@admin_only
def delete(id):
    user=db.get_or_404(BlogPost,id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('get_all_posts'))

# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html",loggin=current_user)


@app.route("/contact",methods=["POST","Get"])
def contact():
    if request.method == "POST":
        print("function start")
        Name=request.form['name']
        Email=request.form['email']
        Phone=request.form['phone']
        Messages=request.form['message']
        sendmail(Name,Email,Phone,Messages)
        return render_template("contact.html",msg=True,loggin=current_user)
    return render_template("contact.html",msg=False,loggin=current_user)

def sendmail(Name,Email,Phone,Messages):
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=SENDER_MAIL,password=SENDER_PASS)
        connection.sendmail(
            from_addr=SENDER_MAIL,
            to_addrs=RECIVER_MAIL,
            msg=f"Subject:User Message\n\n Name:{Name}\nEmail:{Email}\nPhone:{Phone}\nMessages:{Messages}")

@app.route('/register',methods=["GET","POST"])
def register():
    reg=registration()
    if reg.validate_on_submit():
        try:
            user_Data=UserPost(
                name=reg.name.data,
                email=reg.email.data,
                password=generate_password_hash(reg.password.data,method='scrypt', salt_length=8)
                )
            db.session.add(user_Data)
            db.session.commit()
            login_user(user_Data)
            return redirect(url_for('get_all_posts'))
        except:
            flash("You alredy registerd / please login ")
            return redirect(url_for('logins'))
            
    return render_template("register.html",form=reg,loggin=current_user)

@app.route('/login',methods=["GET","POST"])
def logins():
    form=login()
    if form.validate_on_submit():
        user_data=db.session.execute(db.select(UserPost).where(UserPost.email == form.email.data)).scalar()
        if user_data:
            if check_password_hash(user_data.password,form.password.data):
                login_user(user_data)
                return redirect(url_for('get_all_posts'))
            else:
                flash("Your password is incorrect")
        else:
            flash("Your email may be incorrect or you are not register yet")
    return render_template('login.html',form=form,loggin=current_user)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))

if __name__ == "__main__":
    app.run(debug=False)