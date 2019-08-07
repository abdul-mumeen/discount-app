"""
Discount API /discounts endpoint.
"""
import logging
import secrets
import string
import json
import os
from flask import request, json
from flask_restplus import Resource, fields, abort
from ..restplus import api
from ...models.DiscountModel import DiscountModel

log = logging.getLogger(__name__)

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../../categories.json')

CATEGORIES_ID = []

with open(filename) as json_file:
    data = json.load(json_file)
    CATEGORIES_ID = [category['id'] for category in data['Categories']]
    print(CATEGORIES_ID)

ns = api.namespace('discounts',
                   description='Adding, retrieving and deleting Discounts')

discounts_post_request_model = api.model(
    'Discount creation details', {
        'type_id':
        fields.String(
            enum=['percentage_value', 'exact_value', 'free_shipping'],
            required=True,
            description='The ID indication the type of discount.'),
        'value':
        fields.Integer(description='Value of the discount.'),
        'min_apply_value':
        fields.Integer(
            description='Minimum purchase before this discount can be applied.'
        ),
        'category_id':
        fields.Integer(
            enum=[*CATEGORIES_ID],
            required=True,
            description='ID indicating the category the discount belongs to.'),
    })

discount_model = api.model(
    'Discount details', {
        'type_id':
        fields.String(
            enum=['percentage_value', 'exact_value', 'free_shipping'],
            required=True,
            description='The ID indication the type of discount.'),
        'value':
        fields.Integer(required=True, description='Value of the discount.'),
        'min_apply_value':
        fields.Integer(
            description='Minimum purchase before this discount can be applied.'
        ),
        'category_id':
        fields.Integer(
            enum=CATEGORIES_ID,
            description='ID indicating the category the discount belongs to.'),
        'code':
        fields.String(required=True,
                      description='Code for the discount generated.'),
        'id':
        fields.Integer(required=True,
                       description='Id of the discount generated.'),
        'created_at':
        fields.String(description='Time the discount was generated.'),
        'modified_at':
        fields.String(description='Time the discount was updated.'),
    })

discounts_get_response_model = api.model(
    'Discounts list',
    {'discounts': fields.List(fields.Nested(discount_model))})


@ns.route('/<string:discount_id>')
class DiscountResource(Resource):
    @ns.marshal_with(discount_model)
    def get(self, discount_id):
        """Get discount resource by ID"""
        log.info(f'GET /discounts/{discount_id}')

        discount = DiscountModel.get_one_discount(discount_id)

        if not discount:
            abort(f'Discount with discount_id: {discount_id} not found', 404)

        return discount.to_dict(), 200

    def delete(self, discount_id):
        """Get discount resource by ID"""
        log.info(f'GET /discounts/{discount_id}')

        discount = DiscountModel.get_one_discount(discount_id)

        if not discount:
            abort(404, f'Discount with discount_id: {discount_id} not found')

        try:
            discount.delete()
        except Exception as e:
            log.exception(e)
            abort(
                500,
                f'Unable to delete discount with discount_id: {discount_id}')

        return f'Discount with id: {discount_id} has been sucessfully deleted', 200


@ns.route('/')
class DiscountsResource(Resource):
    @ns.marshal_with(discounts_get_response_model)
    def get(self):
        """Get all discounts resource"""
        log.info(f'GET /discounts')

        discounts = []
        try:
            discounts = DiscountModel.get_all_discounts()
        except Exception as e:
            log.exception(e)
            abort(400, 'Unable to retrieve discounts')

        discounts_data_list = [discount.to_dict() for discount in discounts]

        return {'discounts': discounts_data_list}, 200

    @ns.expect(discounts_post_request_model, validate=True)
    @ns.marshal_with(discount_model)
    def post(self):
        request_payload = request.get_json()

        type_id = request_payload.get('type_id')
        received_value = request_payload.get('value')
        min_apply_value = request_payload.get('min_apply_value')
        category_id = request_payload.get('category_id')
        code = ''.join(
            secrets.choice(string.ascii_uppercase + string.digits)
            for _ in range(12))

        if type_id != 'free_shipping' and (not received_value
                                           or received_value < 1):
            abort(400, f'Value missing for type_id, {type_id}')

        value = None if type_id == 'free_shipping' else received_value

        data = {
            'code': code,
            'type_id': type_id,
            'value': value,
            'min_apply_value': min_apply_value,
            'category_id': category_id,
        }

        try:
            discount = DiscountModel(data)
            discount.save()
        except Exception as e:
            log.exception(e)
            abort(500, 'Error creating discount')

        return discount.to_dict(), 201
