from flask import render_template, request, Blueprint
from blog.models import Post
from sqlalchemy import desc


main = Blueprint('main', __name__)

@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('index.html', title="Home", posts=posts)

@main.route('/about')
def about():
    return render_template('about.html', title="About")

@main.route('/top')
def top_posts():
    posts = Post.query.all()
    top_posts = []
    for i in range(3):
        top = max(post.likes.count() for post in posts)
        for post in posts:
            if post.likes.count() >= top:
                top_posts.append(post)
                posts.remove(post)
    
    return render_template('top.html', title="Top", posts=top_posts)

@main.route('/most_commented')
def most_commented():
    posts = Post.query.all()
    
    top_posts = []
    for i in range(3):
        top = max(post.comments.count() for post in posts)
        for post in posts:
            print(post)
            if post.comments.count() >= top:
                top_posts.append(post)
                posts.remove(post)
    
    return render_template('top.html', title="Top", posts=top_posts)
