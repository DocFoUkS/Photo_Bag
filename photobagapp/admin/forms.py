# -*- coding: utf-8 -*-

from datetime import datetime

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.fields.html5 import DateField, TimeField
from wtforms.validators import ValidationError, InputRequired

from photobagapp.blog.models import Blog
from photobagapp.portfolio.models import Group_photo, Photo


class AdminForm(FlaskForm):
    post_image = FileField('Изображение для поста',
                           render_kw={'class': 'form-control'})
    post_name = StringField('Заголовок поста',
                            render_kw={'class': 'form-control'})
    post_text = TextAreaField('Текст поста',
                              render_kw={'class': 'form-control'},
                              validators=[InputRequired()])
    submit_post = SubmitField('Опубликовать пост',
                              render_kw={'class': 'btn btn-primary'})
    portfolio_image = FileField('Изображение для поста',
                                validators=[FileRequired()],
                                render_kw={'class': 'form-control'})
    portfolio_group = StringField('Тема портфолио',
                                  render_kw={'class': 'form-control'},
                                  validators=[InputRequired()])
    portfolio_text = TextAreaField('Описание',
                                   render_kw={'class': 'form-control'},
                                   validators=[InputRequired()])
    submit_portfolio = SubmitField('Опубликовать портфолио',
                              render_kw={'class': 'btn btn-primary'})
