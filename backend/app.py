import os
from flask import Flask, render_template, request, json, abort
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from .db import db
from .models.DiscountModel import DiscountModel

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgres://abdulmumeen@localhost:5432/discount_app_db'
db.init_app(app)

migrate = Migrate(app=app, db=db, discount=DiscountModel)

manager = Manager(app=app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
