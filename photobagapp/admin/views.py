# -*- coding: utf-8 -*-

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user

from photobagapp.admin.forms import AdminForm
from photobagapp.db import db
from photobagapp.user.decorators import admin_required
from photobagapp.blog.models import Blog
from photobagapp.portfolio.models import Photo, Group_photo

blueprint = Blueprint('admin', __name__, url_prefix='/admin')


@blueprint.route('/')
@admin_required
def admin_index():
    title = 'Панель админки'
    admin_form = AdminForm()
    return render_template('admin/homepage.html',
                           page_title=title,
                           form=admin_form)


@blueprint.route('/process_post', methods=['POST'])
def process_post():
    form = AdminForm()

    if form.validate_on_submit():
        if form.post_image.data:
            post_img = Photo(data=form.post_image.data)
            db.session.add(post_img)
            db.session.commit()
        new_post = Blog(caption=form.post_name.data,
                        text=form.post_text.data)
        db.session.add(new_post)
        db.session.commit()
        flash(u'Успешная публикация поста')
        return redirect(url_for('main.index'))
    else:
        for field, errors in form.errors.items():
            for err in errors:
                flash('Ошибка в поле {}: {}'.format(getattr(form, field).label.text, err))

        return redirect(url_for('admin.admin_index'))


@blueprint.route('/process_portfolio', methods=['POST'])
def process_portfolio():
    form = AdminForm()

    if form.validate_on_submit():
        if form.portfolio_image.data:
            portfolio_img = Photo(data=form.portfolio_image.data)
            db.session.add(portfolio_img)
            db.session.commit()
        new_group = Group_photo(caption=form.portfolio_group.data,
                                text=form.portfolio_text.data)
        db.session.add(new_group)
        db.session.commit()
        flash(u'Успешная публикация портфолио')
        return redirect(url_for('main.index'))
    else:
        for field, errors in form.errors.items():
            for err in errors:
                flash('Ошибка в поле {}: {}'.format(getattr(form, field).label.text, err))

        return redirect(url_for('admin.admin_index'))
