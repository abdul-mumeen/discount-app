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
    code = db.Column(db.String(128), unique=True)
    type_id = db.Column(db.String())
    value = db.Column(db.Integer)
    min_apply_value = db.Column(db.Integer, nullable=True)
    category_id = db.Column(db.Integer())
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    # class constructor
    def __init__(self, data):
        """
        Class constructor
        """
        self.code = data.get('code')
        self.type_id = data.get('type_id')
        self.category_id = data.get('category_id')
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

        value = data.get('value')

        if value:
            self.value = data.get('value')

        min_apply_value = data.get('min_apply_value')
        if min_apply_value:
            self.min_apply_value = min_apply_value

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

    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'type_id': self.type_id,
            'value': self.value,
            'min_apply_value': self.min_apply_value,
            'category_id': self.category_id,
            'created_at': self.created_at.strftime("%m/%d/%Y, %H:%M:%S"),
            'modified_at': self.modified_at.strftime("%m/%d/%Y, %H:%M:%S"),
        }
