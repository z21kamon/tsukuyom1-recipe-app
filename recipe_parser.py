from flask_restful import reqparse
from datetime import datetime

recipe_parser = reqparse.RequestParser()
recipe_parser.add_argument('id', required=True, type=int)
recipe_parser.add_argument('name', required=True, type=str)
recipe_parser.add_argument('author', required=True, type=int)
recipe_parser.add_argument('prep_time', required=True, type=int)
recipe_parser.add_argument('tags', required=True, type=str)
recipe_parser.add_argument('date', required=True, type=datetime)
recipe_parser.add_argument('description', required=True, type=bool)
