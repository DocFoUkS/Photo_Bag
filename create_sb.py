# -*- coding: utf-8 -*-
from photobagapp import db, create_app

db.create_all(app=create_app())