# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

blueprint = Blueprint('main', __name__)


@blueprint.route('/')
def index():
    title = 'Главная'
    return render_template('main/index.html', page_tittle=title)
