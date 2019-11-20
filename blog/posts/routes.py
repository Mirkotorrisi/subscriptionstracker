from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from blog import db
from blog.models import Post, Comment
from blog.posts.forms import PostForm, CommentForm

posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post pubblicato con successo!', 'success')
        return redirect(url_for('main.index'))

    return render_template('new_post.html', title='Nuovo Post', form=form, legend="Nuovo Post")


@posts.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content = form.body.data, author=current_user.username, post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        flash('Commento pubblicato con successo!', 'success')
        return redirect(url_for('posts.post', post_id=post.id, comments=post.comments)) 
    return render_template('post.html', title=post.title, post=post, form=form, comments=post.comments, legend="Commenti")


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.body.data
        db.session.commit()
        flash("Post modificato", 'info')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.body.data = post.content
    return render_template('new_post.html', title='Modifica Post', form=form, legend="Modifica Post")


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post eliminato', 'info')
    return redirect(url_for('main.index'))
