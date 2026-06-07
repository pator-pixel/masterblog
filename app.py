import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


def load_blog_posts():
    with open("blog_posts.json", "r", encoding="utf-8") as file:
        return json.load(file)


def save_blog_posts(posts):
    with open("blog_posts.json", "w", encoding="utf-8") as file:
        json.dump(posts, file, indent=4)


@app.route('/')
def index():
    blog_posts = load_blog_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        blog_posts = load_blog_posts()

        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        new_id = max(post["id"] for post in blog_posts) + 1 if blog_posts else 1

        new_post = {
            "id": new_id,
            "author": author,
            "title": title,
            "content": content
        }

        blog_posts.append(new_post)
        save_blog_posts(blog_posts)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    blog_posts = load_blog_posts()

    updated_posts = [
        post for post in blog_posts if post["id"] != post_id
    ]

    save_blog_posts(updated_posts)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)