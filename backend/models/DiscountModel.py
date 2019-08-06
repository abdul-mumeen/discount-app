from marshmallow import fields, Schema
import datetime
from ..db import db


class DiscountModel(db.Model):
    """
    Discount Model
    """

    # table name
    __tablename__ = 'discounts'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(128))
    type_id = db.Column(db.String(10))
    value = db.Column(db.Integer)
    min_apply_value = db.Column(db.Integer, nullable=True)
    category_id = db.Column(db.String(10))
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    # class constructor
    def __init__(self, data):
        """
        Class constructor
        """
        self.code = data.get('code')
        self.type_id = data.get('type_id')
        self.value = data.get('value')
        self.min_apply_value = data.get('min_apply_value')
        self.category_id = data.get('category_id')
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_discounts():
        return DiscountModel.query.all()

    @staticmethod
    def get_one_discount(id):
        return DiscountModel.query.get(id)

    def __repr(self):
        return '<id {}>'.format(self.id)
