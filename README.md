# 📝 Blog Website

A dynamic blog website built as a learning project using **Python, Flask, Bootstrap 5, Jinja2, SQLite, SQLAlchemy, Flask-Login, CKEditor, and Gravatar**.

The project started as a simple Flask blog that fetched posts from an external API. It was later upgraded to use a **SQLite database** for storing users, blog posts, and comments.

The main purpose of this project is to understand how a Flask application can handle **user authentication, database relationships, CRUD operations, forms, comments, and admin-only access**.

---

## 🚀 Features

* User registration
* User login and logout
* Password hashing
* User authentication using Flask-Login
* Login session management
* Admin-only access for managing blog posts
* Create new blog posts
* Edit existing blog posts
* Delete blog posts
* Blog posts stored in SQLite database
* Registered users stored in SQLite database
* Comments stored in SQLite database
* Logged-in users can comment on blog posts
* Each blog post is connected to its author
* Each comment is connected to its author and blog post
* Gravatar profile images
* CKEditor for rich text blog content
* Bootstrap 5 responsive design
* Flash messages
* About page
* Contact page
* Contact form
* Send contact messages through email
* Environment variables for sensitive information

---

## 🛠️ Technologies Used

* **Python**
* **Flask**
* **Flask-SQLAlchemy**
* **SQLAlchemy**
* **SQLite**
* **Flask-Login**
* **Flask-Bootstrap5**
* **Flask-CKEditor**
* **Flask-Gravatar**
* **Flask-WTF**
* **Jinja2**
* **Bootstrap 5**
* **HTML5**
* **CSS3**
* **Werkzeug**
* **python-dotenv**
* **smtplib**

---

# 🗄️ Database

This project uses **SQLite** as the database.

Flask-SQLAlchemy is used to connect the Flask application with the SQLite database.

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'

db = SQLAlchemy(model_class=Base)
db.init_app(app)
```

The application creates the database tables using:

```python
with app.app_context():
    db.create_all()
```

The project mainly uses three tables:

```text
users
   │
   ├───────────────┐
   │               │
   ↓               ↓
blog_posts      comments
   │               │
   └───────┬───────┘
           │
           ↓
        comments
```

---

# 👤 User Model

The `users` table stores registered users.

```python
class UserPost(UserMixin, db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    name: Mapped[str] = mapped_column(
        String,
        nullable=True
    )

    email: Mapped[str] = mapped_column(
        String,
        nullable=True,
        unique=True
    )

    password: Mapped[str] = mapped_column(
        String,
        nullable=True
    )

    posts = relationship(
        "BlogPost",
        back_populates="author"
    )

    comments = relationship(
        "Comments",
        back_populates="comment_author"
    )
```

Each user has:

* ID
* Name
* Email
* Password

The password is stored as a **hashed password**, not as plain text.

---

# 📝 Blog Post Model

Blog posts are stored in the `blog_posts` table.

```python
class BlogPost(db.Model):
    __tablename__ = "blog_posts"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    title: Mapped[str] = mapped_column(
        String(250),
        unique=True,
        nullable=False
    )

    subtitle: Mapped[str] = mapped_column(
        String(250),
        nullable=False
    )

    date: Mapped[str] = mapped_column(
        String(250),
        nullable=False
    )

    body: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    img_url: Mapped[str] = mapped_column(
        String(250),
        nullable=False
    )

    author_id: Mapped[int] = mapped_column(
        Integer,
        db.ForeignKey("users.id")
    )

    author = relationship(
        "UserPost",
        back_populates="posts"
    )

    comments = relationship(
        "Comments",
        back_populates="parent_post"
    )
```

Each blog post contains:

* ID
* Title
* Subtitle
* Date
* Body
* Image URL
* Author ID

The `author_id` is a **foreign key** that connects the blog post to a user.

---

# 💬 Comments Model

Users can comment on blog posts after logging in.

Comments are stored in the `comment` table.

```python
class Comments(db.Model):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    text: Mapped[str] = mapped_column(
        String,
        nullable=True
    )

    author_id: Mapped[int] = mapped_column(
        Integer,
        db.ForeignKey("users.id")
    )

    comment_author = relationship(
        "UserPost",
        back_populates="comments"
    )

    parent_post = relationship(
        "BlogPost",
        back_populates="comments"
    )

    post_id: Mapped[int] = mapped_column(
        Integer,
        db.ForeignKey("blog_posts.id")
    )
```

Each comment contains:

* Comment ID
* Comment text
* Author ID
* Blog post ID

This allows the application to know:

```text
Who wrote the comment?
        ↓
      User

Which post was commented on?
        ↓
    Blog Post
```

---

# 🔗 Database Relationships

The project uses SQLAlchemy relationships to connect the tables.

## User → Blog Posts

```python
posts = relationship(
    "BlogPost",
    back_populates="author"
)
```

This allows:

```python
user.posts
```

to access the posts created by that user.

---

## Blog Post → User

```python
author = relationship(
    "UserPost",
    back_populates="posts"
)
```

This allows:

```python
post.author
```

to access the user who created the post.

---

## User → Comments

```python
comments = relationship(
    "Comments",
    back_populates="comment_author"
)
```

This allows:

```python
user.comments
```

to access the comments written by that user.

---

## Comment → User

```python
comment_author = relationship(
    "UserPost",
    back_populates="comments"
)
```

This allows:

```python
comment.comment_author
```

to access the user who wrote the comment.

---

## Blog Post → Comments

```python
comments = relationship(
    "Comments",
    back_populates="parent_post"
)
```

This allows:

```python
post.comments
```

to access all comments belonging to that post.

---

## Comment → Blog Post

```python
parent_post = relationship(
    "BlogPost",
    back_populates="comments"
)
```

This allows:

```python
comment.parent_post
```

to access the blog post on which the comment was made.

---

# 🔐 User Authentication

The project uses **Flask-Login** for authentication.

Flask-Login is initialized with:

```python
loginmanager = LoginManager()
loginmanager.init_app(app)
```

The application uses:

```python
UserMixin
```

to provide the required login-related functionality for the user model.

Users can:

* Register
* Login
* Logout
* Stay logged in through a session
* Access features depending on their login status

---

# 🔑 User Loader

Flask-Login needs to know how to find the current user from the stored user ID.

This is done using:

```python
@loginmanager.user_loader
def load_user(user_id):
    return db.session.get(UserPost, int(user_id))
```

When Flask-Login needs the current user, it gets the user's ID and uses this function to find that user in the database.

---

# 📝 Registration

Users can create an account from the registration page.

The password is hashed before being stored in the database.

```python
password = generate_password_hash(
    reg.password.data,
    method='scrypt',
    salt_length=8
)
```

The new user is then added to the database:

```python
user_Data = UserPost(
    name=reg.name.data,
    email=reg.email.data,
    password=generate_password_hash(
        reg.password.data,
        method='scrypt',
        salt_length=8
    )
)

db.session.add(user_Data)
db.session.commit()
```

After successful registration, the user is automatically logged in:

```python
login_user(user_Data)
```

---

# 🔓 Login

During login, the application searches for the user using their email:

```python
user_data = db.session.execute(
    db.select(UserPost).where(
        UserPost.email == form.email.data
    )
).scalar()
```

If the user exists, the submitted password is checked against the stored password hash:

```python
check_password_hash(
    user_data.password,
    form.password.data
)
```

If the password is correct:

```python
login_user(user_data)
```

The user is logged in and redirected to the home page.

---

# 🚪 Logout

Users can logout using:

```python
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))
```

The `logout_user()` function logs the current user out.

---

# 👑 Admin Access

The project has a custom `admin_only` decorator.

```python
def admin_only(f):
    @wraps(f)
    def decorated_funtion():
        if current_user.id != 1:
            return abort(404)

        return f()

    return decorated_funtion
```

In the current project, **User ID 1 is treated as the admin**.

The admin can:

* Create blog posts
* Edit blog posts
* Delete blog posts

The protected routes are:

```text
/new
/edit/<id>
/delte/<id>
```

---

# ➕ Creating a Blog Post

The admin can create a new blog post from the `/new` route.

The post is connected to the currently logged-in user:

```python
new_post = BlogPost(
    title=form.title.data,
    subtitle=form.subtitle.data,
    body=form.check.data,
    img_url=form.img_url.data,
    author=current_user,
    date=date.today().strftime("%B %d, %Y")
)
```

Here:

```python
author=current_user
```

connects the new blog post with the logged-in user.

The post is then saved:

```python
db.session.add(new_post)
db.session.commit()
```

---

# ✏️ Editing a Blog Post

The admin can edit an existing blog post.

The post is first retrieved from the database:

```python
blog_select = db.get_or_404(BlogPost, id)
```

The existing data is used to fill the form:

```python
form = blog(
    title=blog_select.title,
    subtitle=blog_select.subtitle,
    check=blog_select.body,
    img_url=blog_select.img_url,
    author=blog_select.author
)
```

After submitting the form, the post is updated:

```python
blog_select.title = form.title.data
blog_select.subtitle = form.subtitle.data
blog_select.img_url = form.img_url.data
blog_select.author = form.author.data
blog_select.body = form.check.data

db.session.commit()
```

---

# 🗑️ Deleting a Blog Post

The admin can delete a blog post.

The post is first found:

```python
user = db.get_or_404(BlogPost, id)
```

Then it is deleted:

```python
db.session.delete(user)
db.session.commit()
```

After deletion, the user is redirected to the home page.

---

# 💬 Adding Comments

Only logged-in users can add comments.

The comment form is first validated:

```python
if form.validate_on_submit():
```

The application then checks whether the user is logged in:

```python
if current_user.is_authenticated:
```

A comment is created using the current user:

```python
user_comment = Comments(
    text=form.comment_box.data,
    comment_author=current_user,
    post_id=post_id
)
```

The comment is saved:

```python
db.session.add(user_comment)
db.session.commit()
```

If the user is not logged in, a flash message is displayed:

```python
flash("for doing comment you need to login")
```

---

# 🖊️ CKEditor

The project uses **Flask-CKEditor** for rich text editing.

CKEditor is initialized using:

```python
checkeditor = CKEditor(app)
```

It is used for writing blog post content and provides a rich text editor instead of a normal text field.

This makes it possible to format blog content with things such as:

* Bold text
* Italic text
* Lists
* Paragraphs
* Links
* Other rich text formatting

---

# 👤 Gravatar

The project uses **Flask-Gravatar** to display profile images for users.

```python
gravatar = Gravatar(
    app,
    size=100,
    rating='g',
    default='retro',
    force_default=False,
    force_lower=False,
    use_ssl=False
)
```

Gravatar generates a profile image based on the user's email address.

---

# 📧 Contact Form

The website contains a Contact page where users can send messages.

The form collects:

* Name
* Email
* Phone number
* Message

The form sends the data to Flask using a `POST` request:

```python
Name = request.form['name']
Email = request.form['email']
Phone = request.form['phone']
Messages = request.form['message']
```

The message is then sent through email using Python's built-in `smtplib` library.

```python
with smtplib.SMTP("smtp.gmail.com") as connection:
    connection.starttls()

    connection.login(
        user=SENDER_MAIL,
        password=SENDER_PASS
    )

    connection.sendmail(
        from_addr=SENDER_MAIL,
        to_addrs=RECIVER_MAIL,
        msg=f"Subject:User Message\n\n"
            f"Name:{Name}\n"
            f"Email:{Email}\n"
            f"Phone:{Phone}\n"
            f"Messages:{Messages}"
    )
```

---

# 🔒 Environment Variables

Sensitive information is stored in a `.env` file instead of directly inside the Python code.

The project uses environment variables for:

* Flask secret key
* Sender email
* Receiver email
* Email password

Example `.env` file:

```env
app_key=your_secret_key
sender=your_email@gmail.com
reciver=receiver@gmail.com
password=your_app_password
```

The values are loaded using:

```python
from dotenv import load_dotenv
import os

load_dotenv()

SENDER_MAIL = os.getenv('sender')
RECIVER_MAIL = os.getenv('reciver')
SENDER_PASS = os.getenv('password')

app.config['SECRET_KEY'] = os.getenv('app_key')
```

The `.env` file should **never be uploaded to GitHub**.

Add it to `.gitignore`:

```text
.env
```

---

# 🔄 Application Flow

## Home Page

```text
Browser
   ↓
Flask
   ↓
SQLite Database
   ↓
Blog Posts
   ↓
Jinja2
   ↓
HTML + Bootstrap
   ↓
Browser
```

---

## Registration

```text
Registration Form
       ↓
   POST Request
       ↓
      Flask
       ↓
  Validate Form
       ↓
  Hash Password
       ↓
  SQLite Database
       ↓
   Login User
       ↓
    Home Page
```

---

## Login

```text
Login Form
    ↓
POST Request
    ↓
Flask
    ↓
Find User by Email
    ↓
Check Password
    ↓
login_user()
    ↓
User Session
```

---

## Blog Post Creation

```text
Admin
  ↓
New Post Form
  ↓
POST Request
  ↓
Flask
  ↓
Create BlogPost
  ↓
Connect Post with current_user
  ↓
SQLite Database
```

---

## Comment

```text
Logged-in User
      ↓
 Comment Form
      ↓
 POST Request
      ↓
    Flask
      ↓
Create Comment
      ↓
SQLite Database
      ↓
Display Comment
```

---

# 📁 Project Structure

```text
blog-project/
│
├── main.py
├── form.py
├── .env
├── .gitignore
├── README.md
│
├── instance/
│   └── posts.db
│
├── static/
│   ├── css/
│   └── assets/
│
└── templates/
    ├── about.html
    ├── contact.html
    ├── footer.html
    ├── header.html
    ├── index.html
    ├── login.html
    ├── make-post.html
    ├── post.html
    └── register.html
```

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone <your-repository-url>
```

## 2. Open the Project Folder

```bash
cd blog-project
```

## 3. Install Dependencies

Install the required packages:

```bash
pip install flask
pip install flask-bootstrap
pip install flask-sqlalchemy
pip install flask-ckeditor
pip install flask-login
pip install flask-gravatar
pip install flask-wtf
pip install python-dotenv
```

Or install all dependencies using:

```bash
pip install -r requirements.txt
```

## 4. Create `.env`

Create a `.env` file in the main project folder:

```env
app_key=your_secret_key
sender=your_email@gmail.com
reciver=receiver@gmail.com
password=your_app_password
```

## 5. Run the Application

```bash
python main.py
```

The application runs on:

```text
http://127.0.0.1:5003/
```

---

# 📄 Available Pages

| Page        | Route         |
| ----------- | ------------- |
| Home        | `/`           |
| Blog Post   | `/<post_id>`  |
| New Post    | `/new`        |
| Edit Post   | `/edit/<id>`  |
| Delete Post | `/delte/<id>` |
| About       | `/about`      |
| Contact     | `/contact`    |
| Register    | `/register`   |
| Login       | `/login`      |
| Logout      | `/logout`     |

---

# 🎯 Learning Objectives

This project was created to practice:

* Flask application structure
* Flask routing
* GET and POST requests
* Jinja2 templates
* Bootstrap 5
* Flask-WTF forms
* SQLite database
* Flask-SQLAlchemy
* SQLAlchemy models
* Primary keys
* Foreign keys
* SQLAlchemy relationships
* `back_populates`
* One-to-many relationships
* Database CRUD operations
* `db.get_or_404()`
* User registration
* User login and logout
* Flask-Login
* `current_user`
* User sessions
* Password hashing
* Password verification
* Admin-only routes
* Custom decorators
* Flask flash messages
* CKEditor
* Gravatar
* Environment variables
* Sending emails using `smtplib`
* Handling form data
* Connecting users with blog posts
* Connecting users with comments
* Connecting comments with blog posts

---

# 🔐 Security

The project uses some basic security practices:

* Passwords are stored as hashes instead of plain text.
* Flask secret key is stored in an environment variable.
* Email credentials are stored in environment variables.
* `.env` is excluded from Git using `.gitignore`.
* Admin routes are protected using a custom decorator.
* User authentication is handled using Flask-Login.
* Passwords are checked using Werkzeug's password hashing functions.

---

# 🎓 Purpose

This is a **learning-based Flask project** created to understand how a dynamic blog website can work with a database.

The project was initially created using an external API for blog posts. It was later upgraded to use a **SQLite database**.

The upgraded version allows the application to:

* Register and store users
* Login and logout users
* Store hashed passwords
* Store blog posts in a database
* Connect blog posts with their authors
* Allow logged-in users to add comments
* Connect comments with users
* Connect comments with blog posts
* Create, edit, and delete blog posts
* Restrict blog management to the admin
* Use CKEditor for rich text content
* Display user avatars using Gravatar
* Send contact messages through email

The main goal of this project is to practice building a complete Flask application with **authentication, database relationships, CRUD operations, forms, comments, and user-generated content**.


