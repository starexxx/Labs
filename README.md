<div align="center">
<b>Starexx LABS</b><br>
Simple text sharing platform  

</div>

## Quick Start

1. Clone this repository  
2. Install requirements: `pip install flask`  
3. Run: `python app.py`  
4. Access at: `http://localhost:5000`

## Post Creation

Create `.bin` files in `posts/` folder with this format:

<table>
  <tr>
    <th>Section</th>
    <th>Description</th>
    <th>Required</th>
  </tr>
  <tr>
    <td><code>title</code></td>
    <td>Post heading</td>
    <td>Yes</td>
  </tr>
  <tr>
    <td><code>content</code></td>
    <td>Main text content</td>
    <td>Yes</td>
  </tr>
  <tr>
    <td><code>script</code></td>
    <td>Code snippets</td>
    <td>No</td>
  </tr>
</table>

```python
title = """
Your Post Title
"""

content = """
Your main content here.
Supports multiple paragraphs.
"""

script = """
# Optional code block (null for no codes)
print("Hello World")
"""
```

<div align="center">

<br><b><i>DEVELOPED BY STAREXX

</div>
