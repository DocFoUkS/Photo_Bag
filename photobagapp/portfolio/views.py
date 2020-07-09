# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

blueprint = Blueprint('portfolio', __name__)


@blueprint.route('/portfolio')
def portfolio():
    title = 'Главная'
    return render_template('portfolio/portfolio.html', page_tittle=title)
