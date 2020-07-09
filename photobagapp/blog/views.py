# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

blueprint = Blueprint('blog', __name__)


@blueprint.route('/blog')
def blog():
    title = 'Блог'
    return render_template('blog/blog.html', page_tittle=title)
