from flask_restful import Resource, reqparse
from models.store import StoreModel

class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('item',
                        type=str,
                        required=True,
                        help="This ")

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}

    def post(self, name):
        # check to see if the store exists
        if StoreModel.find_by_name(name):
            return {'message': 'A store with teh name "{}" already exists.'.format(name)}, 400

        # if not, create the store
        store = StoreModel(name)
        try:
            # tries to save the store to the database
            store.save_to_db()

        except:
            return {'message': 'Something went wrong trying to save the store.'}, 500

        return store.json()

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'Store deleted'}


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
