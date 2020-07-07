# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

from photobagapp.user.decorators import admin_required

blueprint = Blueprint('admin', __name__, url_prefix='/admin')


@blueprint.route('/')
@admin_required
def admin_index():
    title = 'Панель админки'
    return render_template('admin/homepage.html', admin_title=title)
