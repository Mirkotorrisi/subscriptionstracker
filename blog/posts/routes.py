from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from blog import db
from blog.models import Abbonati
from blog.posts.forms import NuovoAbbonato
import datetime

posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = NuovoAbbonato()
    if form.validate_on_submit():
        post = Abbonati(nome=form.nome.data, cell=form.cell.data, scadenza=form.scadenza.data, quota=form.quota.data, versato=form.versato.data, note=form.note.data)
        db.session.add(post)
        db.session.commit()
        flash('Socio pubblicato con successo!', 'success')
        return redirect(url_for('main.index'))

    return render_template('new_post.html', title='Nuovo abbonato', form=form, legend="Nuovo Abbonato")


@posts.route('/post/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_post(id):
    post = Abbonati.query.get_or_404(id)
    form = NuovoAbbonato()
    if form.validate_on_submit():
        post.nome = form.nome.data
        post.cell = form.cell.data
        post.scadenza = form.scadenza.data
        post.quota = form.quota.data
        post.versato += int(form.versato.data)
        post.note = form.note.data
        db.session.commit()
        flash("Socio modificato", 'info')
        return redirect(url_for('main.index'))
    elif request.method == "GET":
        form.nome.data = post.nome
        form.cell.data = post.cell
        form.scadenza.data = post.scadenza
        form.quota.data = post.quota
        form.note.data = post.note
    return render_template('new_post.html', title='Modifica Socio', form=form, legend="Modifica Socio")


@posts.route('/post/<int:id>/delete', methods=['POST'])
@login_required
def delete_post(id):
    post = Abbonati.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash('Socio eliminato', 'info')
    return redirect(url_for('main.index'))