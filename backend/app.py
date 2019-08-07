import os
from flask import Flask, Blueprint
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from .db import db
from .models.DiscountModel import DiscountModel
from .restapi.restplus import api
from .restapi.endpoints.healthz import ns as healthz_ns
from .restapi.endpoints.discounts import ns as discounts_ns

MYNAME = 'discount'
app = Flask(MYNAME)
app.config['SECRET_KEY'] = 'secret!'

# user = os.environ['POSTGRES_USER']
# password = os.environ['POSTGRES_PASSWORD']
# db_name = os.environ['POSTGRES_DB']
# host = os.environ['POSTGRES_HOST']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgres://abdulmumeen@localhost:5432/discount_app_db'  # f'postgres://{user}:{password}@{host}:5432/{db_name}'
db.init_app(app)

CORS(app, resources={r"/api/*": {'origins': '*'}})

migrate = Migrate(app=app, db=db, discount=DiscountModel)
manager = Manager(app=app)
manager.add_command('db', MigrateCommand)

blueprint = Blueprint('api', MYNAME, url_prefix='/api')
api.init_app(blueprint)
api.add_namespace(healthz_ns)
api.add_namespace(discounts_ns)
app.register_blueprint(blueprint)

if __name__ == '__main__':
    manager.run()
