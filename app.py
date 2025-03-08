from flask import Flask, request, redirect, url_for, send_from_directory, abort
import os
import markdown

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

POSTS = []

HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>Starexx Blogs</title>
    <style>
        body { background: #000; color: white; font-family: Arial, sans-serif; padding: 0; margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh; overflow: hidden; -webkit-tap-highlight-color: transparent; }
        .container { width: 100%%; max-width: 600px; height: 90vh; padding: 10px; overflow-y: auto; }
        h1 { text-align: left; font-size: 28px; margin-left: 8px; margin-bottom: 15px; }
        .post { background: #111; padding: 10px; margin: 10px 0; border-radius: 9px; }
        .post h2, .post p { margin-left: 10px; }
        .post a { color: #007BFF; text-decoration: none; margin-left: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Blogs</h1>
        %s
    </div>
</body>
</html>
"""

OWNER_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PostHub</title>
    <style>
        body { 
            background: #000; 
            color: white; 
            font-family: Arial, sans-serif; 
            padding: 20px;
            -webkit-tap-highlight-color: transparent;
            margin: 0;
        }
        h1, h2 { 
            margin-bottom: 10px; 
        }
        .form { 
            width: 100%%; 
            max-width: 400px; 
        }
        input, textarea { 
            width: 95%%; 
            padding: 12px; 
            background: transparent;
            outline: none;            
            color: white; 
            border: 1px solid #444; 
            border-radius: 9px; 
            font-size: 16px;
            margin-bottom: 10px;
            resize: none;
        }
        input[type="file"] { 
            padding: 8px; 
            background: #000; 
        }
        button { 
            background: #007BFF; 
            border: none; 
            width: 100%%;
            padding: 12px; 
            border-radius: 9px; 
            font-size: 16px;
            color: white;
            cursor: pointer; 
            border: 1px solid #444;
            transition: 0.3s;
        }
        button:hover { 
            background: #0056b3;
        }
        .post { 
            width: 93%%; 
            max-width: 400px; 
            background: #111; 
            padding: 15px; 
            margin-top: 10px; 
            border-radius: 15px; 
            border-left: 5px solid none;
            position: relative;
        }
        .delete-btn { 
            position: absolute; 
            top: 30px; 
            right: 20px; 
            color: #ff4d4d; 
            cursor: pointer; 
            font-size: 20px;
            transition: 0.3s;
        }
        .delete-btn:hover { 
            color: #ff4d4d;
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <h1>Starexx Panel</h1>
    <form class="form" action="/upload" method="post" enctype="multipart/form-data">
        <input type="text" name="title" placeholder="Title" required>
        <textarea name="description" placeholder="Short Description" required></textarea>
        <textarea name="content" placeholder="Full Content (Markdown Supported)" required></textarea>
        <input type="file" name="file">
        <button type="submit">Upload</button>
    </form>
    <h2>Blogs</h2>
    %s
</body>
</html>
"""

POST_VIEW_TEMPLATE = """
<!DOCTYPE html>  
<html lang="en">  
<head>  
    <meta charset="UTF-8">  
    <meta name="viewport" content="width=device-width, initial-scale=1.0">  
    <title>%s - Starexx</title>  
    <style>  
        body {   
            background: #000;   
            color: white;   
            font-family: Arial, sans-serif;   
            padding: 0;   
            margin: 0;   
            display: flex;   
            justify-content: center;   
            align-items: center;   
            height: 100vh;  
            overflow: hidden;  
        }  
        .container {   
            width: 100%%;   
            max-width: 600px;   
            padding: 15px;  
            overflow-y: auto;  
        }  
        h1, p {   
            margin-left: 10px;   
        }  
        .content {   
            background: #121212;   
            padding: 10px;   
            border-radius: 5px;   
            white-space: pre; /* Ensures proper spacing in code */  
            overflow-x: auto; /* Allows horizontal scrolling if needed */  
            font-family: monospace; /* Uses monospace font for better code display */  
            word-wrap: normal;  
            margin-left: 10px;  
        }  
        .download {   
            background: green;   
            color: white;   
            padding: 10px;   
            text-align: center;   
            display: block;   
            margin: 10px auto 0 auto;  
            text-decoration: none;  
            width: fit-content;  
            border-radius: 5px;  
        }  
        a {   
            display: block;   
            text-align: center;   
            margin-top: 10px;   
            color: #007BFF;  
            text-decoration: none;  
        }  
    </style>  
</head>  
<body>  
    <div class="container">  
        <h1>%s</h1>  
        <p>%s</p>  
        <div class="content"><code>%s</code></div>  
        %s  
        <a href="/">Back to Home</a>  
    </div>  
</body>  
</html>
"""

@app.route("/")
def home():
    posts_html = "".join(
        f'<div class="post"><h2>{p["title"]}</h2><p>{p["description"]} <a href="/post/{i}">Read More</a></p></div>'
        for i, p in enumerate(POSTS)
    )
    return HOME_TEMPLATE % posts_html

@app.route("/add")
def owner_panel():
    my_posts = "".join(
        f'<div class="post"><h2>{p["title"]} <span class="delete-btn" onclick="location.href=\'/delete/{i}\'">Delete</span></h2></div>'
        for i, p in enumerate(POSTS)
    )
    return OWNER_TEMPLATE % my_posts

@app.route("/post/<int:post_id>")
def view_post(post_id):
    if 0 <= post_id < len(POSTS):
        post = POSTS[post_id]
        html_content = markdown.markdown(post["content"], extensions=["fenced_code"])
        file_section = f'<a href="/uploads/{post["file"]}" class="download" download>Download File</a>' if post["file"] else ""
        return POST_VIEW_TEMPLATE % (post["title"], post["title"], post["description"], html_content, file_section)
    return abort(404)

@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    if 0 <= post_id < len(POSTS):
        del POSTS[post_id]
    return redirect(url_for("owner_panel"))

@app.route("/upload", methods=["POST"])
def upload():
    title = request.form.get("title")
    description = request.form.get("description")
    content = request.form.get("content")
    file = request.files.get("file")

    file_name = ""
    if file and file.filename:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        file_name = file.filename

    POSTS.append({"title": title, "description": description, "content": content, "file": file_name})
    
    return redirect(url_for("owner_panel"))

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return send_from_directory(UPLOAD_FOLDER, filename)
    return abort(404)

if __name__ == "__main__":
    app.run(debug=True)
