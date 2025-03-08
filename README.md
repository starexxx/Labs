# Starexx Blogs

Welcome to **Starexx Blogs**! This is a simple, static blog system where posts are stored as JSON files in the `Posts` folder..

---

## Table of Contents
1. [How to add a new post](#how-to-add-a-new-post)
2. [How to Modify a Post](#how-to-modify-a-post)
3. [How to Change Styles or Layout](#how-to-change-styles-or-layout)
4. [Folder Structure](#folder-structure)
5. [Clone the Repository](#clone-the-repository)

---

## How to add a new post

1. **Create a JSON File**:
   - Go to the Posts folder.
   - Create a new JSON file (e.g., `mypost.json`).

2. **Add Post Content**:
   - Use the following template for your JSON file:
     ```json
     {
       "Post": {
         "Tittle": "Your Post Title",
         "About": "A short description of your post",
         "Content": "The full content of your post. You can use multiple paragraphs.",
         "File": "URL or false"
       }
     }
     ```
   - Replace the placeholders with your actual content.
   - If your post has a file (e.g., an image or document), provide the URL in the `"File"` field. Otherwise, set it to `false`.

3. **Save the File**:
   - Save the JSON file in the Posts folder.

4. **Update the File List**:
   - Open `index.html` and add the new file name to the `files` array in the `<script>` section:
     ```javascript
     const files = [
         'mypost.json'
     ];
     ```

---

## How to Modify a Post

1. **Edit the JSON File**:
   - Go to the Posts folder.
   - Open the JSON file you want to modify (e.g., `post1.json`).

2. **Make Changes**:
   - Update the `"Tittle"`, `"About"`, `"Content"`, or `"File"` fields as needed.

3. **Save the File**:
   - Save your changes.

---

## How to Change Styles or Layout

1. **Edit CSS**:
   - Open `index.html` or `post.html`.
   - Locate the `<style>` tag in the `<head>` section.
   - Modify the CSS to change the appearance of the blog.

2. **Edit HTML**:
   - Open `index.html` or `post.html`.
   - Modify the HTML structure to change the layout.

3. **Save Changes**:
   - Save the file and refresh the browser to see the changes.

---

## Folder Structure

```
project/
│
├── index.html
├── post.html      
├── Posts/             
│   ├── post1.json
│   ├── post2.json
│   └── ...
│
└── README.md
```

---

## Clone the Repository
1. Open your terminal or command prompt.
2. Run the following command to clone the repository:
   ```bash
   git clone https://github.com/starexxx/blogs.git
   ```

## Support

If you encounter any issues or have questions, feel free to reach out!
