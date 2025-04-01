from flask import Flask, render_template_string
import os
import re

app = Flask(__name__)

home = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Starexx</title>
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        * {
            -webkit-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            user-select: none;
        }
        
        body {
            font-family: 'Inter', Arial, sans-serif;
            background-color: #000;
            color: white;
            margin: 0;
            padding: 20px;
            -webkit-tap-highlight-color: transparent;
            line-height: 1.5;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        
        h1 {
            color: white;
            padding-bottom: 10px;
            font-weight: 600;
            margin-bottom: 10px;
        }
        
        .post {
            background-color: #000;
            padding: 0 0;
            cursor: pointer;
            border-radius: 4px;
        }
        
        .post-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .post-title {
            font-size: 16px;
            color: white;
            font-weight: 500;
        }
        
        .post-content {
            padding-top: 12px;
            color: #ccc;
            margin-top: 8px;
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease-out;
            font-weight: 400;
        }
        
        .icon {
            color: #666;
            transition: transform 0.3s ease, color 0.2s ease;
        }
        
        .expanded .post-content {
            max-height: 1000px;
            transition: max-height 0.5s ease-in;
        }
        
        .expanded .expand-icon {
            transform: rotate(180deg);
            color: #fff;
        }
        
        code {
            background-color: #000;
            border: 1px solid #121212;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Inter', monospace;
            font-size: 0.9em;
            color: #e0e0e0;
        }
        
        pre {
            position: relative;
            margin: 12px 0;
        }
        
        pre code {
            display: block;
            padding: 12px 16px;
            overflow-x: auto;
            line-height: 1.5;
            font-size: 0.85em;
            -webkit-user-select: text;
            -moz-user-select: text;
            -ms-user-select: text;
            user-select: text;
        }
        
        .copy-icon {
            position: absolute;
            right: 8px;
            top: 25px;
            color: #666;
            cursor: pointer;
            background: #000;
            border-radius: 4px;
            padding: 4px;
            font-size: 16px;
            opacity: 0;
            transition: opacity 0.2s ease, color 0.2s ease;
        }
        
        pre:hover .copy-icon {
            opacity: 1;
        }
        
        .copy-icon:hover {
            color: #fff;
            background: #080808;
        }
        
        a {
            color: #58a6ff;
            text-decoration: none;
        }
        
        a:hover {
            text-decoration: underline;
        }
        
        ::selection {
            background-color: #121212;
            color: #fff; 
        }

        ::-moz-selection {
            background-color: #121212;
            color: #fff;
        }
</style>
</head>
<body>
    <div class="container">
        <h1>Starexx Labs</h1>
        {% for post in posts %}
        <div class="post" onclick="togglePost(this)">
            <div class="post-header">
                <div class="post-title">{{ post.title }}</div>
                <i class="material-icons expand-icon icon">expand_more</i>
            </div>
            <div class="post-content">
                {{ post.content|safe }}
                {% if post.script and post.script != 'null' %}
                <pre>
                    <code id="code{{ loop.index }}">{{ post.script }}</code>
                    <i class="material-icons copy-icon" onclick="copyCode('code{{ loop.index }}', event)">content_copy</i>
                </pre>
                {% endif %}
            </div>
        </div>
        {% endfor %}
    </div>

    <script>
        function togglePost(postElement) {
            const wasExpanded = postElement.classList.contains('expanded');
            const icon = postElement.querySelector('.expand-icon');
            
            document.querySelectorAll('.post.expanded').forEach(expandedPost => {
                if (expandedPost !== postElement) {
                    expandedPost.classList.remove('expanded');
                    expandedPost.querySelector('.expand-icon').textContent = 'expand_more';
                    expandedPost.querySelector('.expand-icon').style.transform = 'rotate(0deg)';
                }
            });
            
            postElement.classList.toggle('expanded');
            icon.textContent = wasExpanded ? 'expand_more' : 'expand_less';
            icon.style.transform = wasExpanded ? 'rotate(0deg)' : 'rotate(180deg)';
        }
        
        function copyCode(id, event) {
            const codeElement = document.getElementById(id);
            const range = document.createRange();
            range.selectNode(codeElement);
            window.getSelection().removeAllRanges();
            window.getSelection().addRange(range);
            
            try {
                const successful = document.execCommand('copy');
                const copyIcon = event.target;
                if (successful) {
                    copyIcon.textContent = 'check';
                    setTimeout(() => copyIcon.textContent = 'content_copy', 2000);
                }
            } catch(err) {
                console.error('Failed to copy text: ', err);
            }
            
            window.getSelection().removeAllRanges();
            event.stopPropagation();
        }
    </script>
</body>
</html>
"""

def parse_post(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    title_match = re.search(r'title\s*=\s*"""(.*?)"""', content, re.DOTALL)
    content_match = re.search(r'content\s*=\s*"""(.*?)"""', content, re.DOTALL)
    script_match = re.search(r'script\s*=\s*"""(.*?)"""', content, re.DOTALL)
    
    return {
        'title': title_match.group(1).strip() if title_match else "Untitled",
        'content': content_match.group(1).strip() if content_match else "",
        'script': script_match.group(1).strip() if script_match else "null"
    }

@app.route('/')
def index():
    posts = []
    posts_dir = os.path.join(os.path.dirname(__file__), 'posts')
    
    if os.path.exists(posts_dir):
        for filename in os.listdir(posts_dir):
            if filename.endswith('.bin'):
                post_path = os.path.join(posts_dir, filename)
                posts.append(parse_post(post_path))
    
    return render_template_string(home, posts=posts)

if __name__ == '__main__':
    app.run(debug=True)
