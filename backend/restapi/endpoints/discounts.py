"""
Discount API /discounts endpoint.
"""
import logging
from flask import request, json
from flask_restplus import Resource, fields, abort
from ..restplus import api
from ...models.DiscountModel import DiscountModel

log = logging.getLogger(__name__)

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
        fields.Integer(required=True,
            description='ID indicating the category the discount belongs to.'),
    })

discount_model = api.model(
    'Discount creation details', {
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
            description='ID indicating the category the discount belongs to.'),
        'code':
        fields.String(required=True,
                      description='Code for the discount generated.'),
        'id':
        fields.Integer(required=True,
                       description='Id of the discount generated.'),
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
        
        return discount, 200

    @ns.marshal_with(discount)
    def delete(self, discount_id):
        """Get discount resource by ID"""
        log.info(f'GET /discounts/{discount_id}')

        discount = DiscountModel.get_one_discount(discount_id)

        if not discount:
            abort(f'Discount with discount_id: {discount_id} not found', 404)
        
        try:
            discount.delete()
        except e:
            log.exception(e)
            abort(f'Unable to delete discount with discount_id: {discount_id}, 500)

        return '', 200


@ns.route('/')
class DiscountsResource(Resource):
    @ns.marshal_with(discounts_get_response_model)
    def get(self):
        """Get all discounts resource"""
        log.info(f'GET /discounts')

        discounts = []
        try:
            discounts = DiscountModel.get_all_discounts()
        except e:
            log.exception(e)
            abort(400, 'Unable to retrieve discounts')

        return {'discounts': discounts}, 200

    @ns.expect(discounts_post_request_model)
    @ns.marshal_with(discount_model)
    def post(self):
        request_payload = request.get_json()

        type_id = request_payload.get('type_id')
        value = request_payload.get('value')
        min_apply_value = request_payload.get('min_apply_value')
        category_id = request_payload.get('category_id')
        code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(12))

        if not value and type_id is not 'free_shipping':
            abort(400, f'Value missing for type_id, {type_id}')

        data = {
            'code': code,
            'type_id': type_id,
            'value': value,
            'min_apply_value': min_apply_value,
            'category_id': category_id,
        }

        try:
            discount = DiscountModel({})
        except e:
            abort(500, 'Error creating discount')

        return discount, 201
