# Blog Website

A simple and dynamic blog website built as a learning project using **Flask, Bootstrap, Jinja2, HTML, and CSS**.

The main purpose of this project is to learn how a Python Flask backend can work with an external API and dynamically display data on web pages using Jinja2 templates.

## 🚀 Features

* Dynamic blog posts fetched from an external API
* Flask backend for routing and page rendering
* Jinja2 templating for displaying dynamic content
* Bootstrap for responsive and modern UI
* Individual blog post pages
* About page
* Contact page
* Navigation between different pages
* Query parameters used to send post data to the blog post page

## 🛠️ Technologies Used

* **Python**
* **Flask**
* **Jinja2**
* **Bootstrap**
* **HTML5**
* **CSS3**
* **Requests**
* **REST API**

## 📡 API Integration

The blog posts are fetched from an external API using Python's `requests` library.

```python
response = requests.get("https://api.npoint.io/674f5423f73deab1e9a7")
response = response.json()
```

The API response contains the blog post data, which is passed to the Jinja2 template:

```python
return render_template("index.html", response=response)
```

Jinja2 is then used to display the posts dynamically in the HTML page.

## 🔄 How It Works

The application follows this basic flow:

```text
External API
     ↓
Python Requests
     ↓
Flask
     ↓
Jinja2 Template
     ↓
Bootstrap + HTML
     ↓
Web Browser
```

When the home page is opened, Flask fetches the blog data from the API and sends it to `index.html`.

Each blog post can then be opened on the `/post` route with its title, subtitle, and body passed through URL query parameters.

Example:

```text
/post?title=The+Life+of+Cactus&subtitle=Interesting+Life&body=...
```

Flask retrieves these values using:

```python
title = request.args.get("title")
subtitle = request.args.get("subtitle")
body = request.args.get("body")
```

and sends them to `post.html`.

## 📁 Project Structure

```text
blog-project/
│
├── main.py
│
├── templates/
│   ├── index.html
│   ├── post.html
│   ├── about.html
│   └── contact.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── assets/
│
└── README.md
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
```

### 2. Open the project folder

```bash
cd blog-project
```

### 3. Install dependencies

```bash
pip install flask requests
```

### 4. Run the application

```bash
python main.py
```

### 5. Open in browser

```text
http://127.0.0.1:5000/
```

## 📄 Available Pages

| Page      | Route      |
| --------- | ---------- |
| Home      | `/`        |
| About     | `/about`   |
| Contact   | `/contact` |
| Blog Post | `/post`    |

## 🎯 Learning Objectives

This project was created to practice:

* Flask application structure
* Flask routing
* Rendering HTML templates
* Jinja2 template syntax
* Passing data from Python to HTML
* Handling URL query parameters with `request.args.get()`
* Fetching data from an external API
* Using the Python `requests` library
* Using Bootstrap components and responsive layouts
* Connecting frontend templates with a Python backend

## 👨‍💻 Purpose

This is a **learning-based project** created to understand the fundamentals of building a dynamic website with **Flask and Bootstrap** and to learn how an external API can be integrated into a web application.
