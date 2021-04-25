from flask_restful import abort, Resource
from flask import jsonify
from recipe_parser import recipe_parser
from data import db_session
from data.recipes import Recipe


def abort_if_recipe_not_found(recipe_id):
    session = db_session.create_session()
    recipe = session.query(Recipe).get(recipe_id)
    if not recipe:
        abort(404, message=f"Recipe {recipe_id} not found")


class RecipesResource(Resource):
    def get(self, recipe_id):
        abort_if_recipe_not_found(recipe_id)
        session = db_session.create_session()
        recipe = session.query(Recipe).get(recipe_id)
        return jsonify({'recipe': recipe.to_dict()})

    def delete(self, recipe_id):
        abort_if_recipe_not_found(recipe_id)
        session = db_session.create_session()
        recipe = session.query(Recipe).get(recipe_id)
        session.delete(recipe)
        session.commit()
        return jsonify({'success': 'OK'})


class RecipesListResource(Resource):
    def get(self):
        session = db_session.create_session()
        recipes = session.query(Recipe).all()
        return jsonify({'recipes': [item.to_dict() for item in recipes]})

    def post(self):
        args = recipe_parser.parse_args()
        session = db_session.create_session()
        recipe = Recipe(
            id=args['id'],
            name=args['name'],
            author=args['author'],
            prep_time=args['prep_time'],
            tags=args['tags'],
            date=date['date'],
            description=args['description'],
            ingredients=args['ingredients'],
            image_url=args['imgae_url'],
            cropped_image_url=args['cropped_image_url'],
            cotw=args['cotw'],
            views_count=args['views_count']
        )
        session.add(recipe)
        session.commit()
        return jsonify({'success': 'OK'})
