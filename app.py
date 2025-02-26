from flask import Flask, request, render_template_string, redirect, url_for
import uuid

app = Flask(__name__)

codes = {}

template_home = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>Publisher</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/atom-one-dark.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/highlight.min.js"></script>
    <script>hljs.highlightAll();</script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: "Source Code Pro", monospace;
            outline: none;
            -webkit-tap-highlight-color: transparent;
        }
        
        body {
            background-color: #000;
            color: #fff;
            height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }
        
        textarea {
            width: 100vw;
            height: 100vh;
            padding: 15px;
            border: none;
            background: #000;
            color: white;
            font-size: 10px;
            resize: none;
            border-radius: 0;
        }
        
        .floating-btn {
            position: fixed;
            bottom: 15px;
            right: 15px;
            background: #000;
            border: 1px solid #121212;
            cursor: pointer;
            border-radius: 50px;
            width: 50px;
            height: 50px;
            color: #fff;
            font-size: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background 0.3s;
        }
        
        .floating-btn:hover {
            border: 1px solid #242424;
        }
        
        .floating-select {
            position: fixed;
            bottom: 15px;
            left: 15px;
            background: #000;
            border: 1px solid #121212;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 5px;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <form action="/publish" method="POST">
        <textarea name="code" placeholder="Enter file contents here"></textarea>
        <select name="lang" class="floating-select">
            <option value="python">Python</option>
            <option value="html">HTML</option>
            <option value="css">CSS</option>
            <option value="javascript">JavaScript</option>
            <option value="php">PHP</option>
            <option value="ruby">Ruby</option>
            <option value="perl">Perl</option>
            <option value="bash">Bash</option>
            <option value="java">Java</option>
            <option value="cpp">C++</option>
            <option value="csharp">C#</option>
            <option value="c">C</option>
        </select>
        <button type="submit" class="floating-btn">PUB</button>
    </form>
</body>
</html>
"""

def add_credit(code, lang):
    credits = {
        "html": "<!-- Powered by StarexxLab -->",
        "css": "/* Powered by StarexxLab */",
        "javascript": "// Powered by StarexxLab",
        "php": "// Powered by StarexxLab",
        "python": "# Powered by StarexxLab",
        "ruby": "# Powered by StarexxLab",
        "perl": "# Powered by StarexxLab",
        "bash": "# Powered by StarexxLab",
        "java": "// Powered by StarexxLab",
        "cpp": "// Powered by StarexxLab",
        "csharp": "// Powered by StarexxLab",
        "c": "// Powered by StarexxLab"
    }
    return f"{credits.get(lang, '')}\n{code}"

template_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no, maximum-scale=1.0">
    <title>Script</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/atom-one-dark.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/highlight.min.js"></script>
    <script>hljs.highlightAll();</script>
    <style>
        body { background-color: #000; color: #ffffff; margin: 0; font-family: Arial, sans-serif; overflow: hidden; -webkit-tap-highlight-color: transparent; }
        pre { width: 100vw; height: 100vh; overflow: auto; padding: 20px; background: #000; }
        code { background: #000 !important; display: block; padding: 10px; border-radius: 5px; }
        .copy-btn {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #000;
            border: none;
            cursor: pointer;
            border: 1px solid #121212;
            border-radius: 50%;
            width: 55px;
            height: 55px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background 0.3s, transform 0.2s;
        }
        .copy-btn:hover {
            background: #121212;
            border: 1px solid: #242424;
        }
        .copy-btn svg {
            width: 24px;
            height: 24px;
            fill: #ffffff;
        }
    </style>
</head>
<body>
    <pre><code class="{{ lang }}">{{ code }}</code></pre>
    <button class="copy-btn" onclick="copyCode()">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M16 2H8v2h8V2zm-5 4h2v2h-2V6zM3 10h18v10H3V10zm2 2v6h14v-6H5zm7 1h2v2h-2v-2z"/></svg>
    </button>
    <script>
        function copyCode() {
            const codeElement = document.querySelector('pre code');
            navigator.clipboard.writeText(codeElement.textContent).then(() => {
                alert('Code copied to clipboard!');
            });
        }
    </script>
</body>
</html>

"""

template_invalid = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Invalid Code</title>
    <link href="https://fonts.googleapis.com/css2?family=Source+Code+Pro:wght@400;600&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Source Code Pro', monospace; }
        body {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #000;
            color: rgba(255,255,255,5);
            text-align: center;
            padding: 20px;
        }
        h1 {
            font-size: 24px;
            font-weight: 600;
            color: fff;
            margin-bottom: 10px;
        }
        p {
            font-size: 16px;
            font-weight: 400;
            color: #bbb;
        }
    </style>
</head>
<body>
    <h1>Invalid Code ID!</h1>
    <p>The requested code ID does not exist.</p>
</body>
</html>

"""

template_wrong_route = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>404 Not Found</title>
    <link href="https://fonts.googleapis.com/css2?family=Source+Code+Pro:wght@400;600&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Source Code Pro', monospace; }
        body {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #000;
            color: rgba(255, 255, 255, 0.5);
            text-align: center;
            padding: 20px;
        }
        h1 {
            font-size: 24px;
            font-weight: 600;
            color: #fff;
            margin-bottom: 10px;
        }
        p {
            font-size: 16px;
            font-weight: 400;
            color: #bbb;
        }
    </style>
</head>
<body>
    <h1>404 - Wrong Route</h1>
    <p>The requested page does not exist.</p>
</body>
</html>

"""

@app.route("/")
def home():
    return render_template_string(template_home)

@app.route("/publish", methods=["POST"])
def publish():
    code = request.form.get("code", "")
    lang = request.form.get("lang", "python").lower()
    code = add_credit(code, lang)
    code_id = str(uuid.uuid4())[:8]
    codes[code_id] = {"code": code, "lang": lang}
    return redirect(url_for("view_code", code_id=code_id))

@app.route("/<code_id>")
def view_code(code_id):
    if code_id not in codes:
        return render_template_string(template_invalid)
    return render_template_string(template_code, code=codes[code_id]["code"], lang=codes[code_id]["lang"])

@app.errorhandler(404)
def page_not_found(e):
    return render_template_string(template_wrong_route), 404

if __name__ == "__main__":
    app.run(debug=True)
  
