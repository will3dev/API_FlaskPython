import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from project.models.items import ItemModel

class Items(Resource):
    def get(self):
        return {'item': [
            item.json() for item
            in ItemModel.query.all()
        ]}


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id"
                        )

    test = 'pasta'


    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404



    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred."}

        return item.json(), 201


    def put(self, name):
        # the below is the same as running request.get_json()
        # this will additionally run the json through
        # the reqparse validators
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)


        if not item:
            item = ItemModel(name, data['price'], data['store_id'])

        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"message": "Item deleted"}