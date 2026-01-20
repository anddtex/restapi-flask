from flask import Flask
from flask_restful import Resource, reqparse, Api
from flask_mongoengine import MongoEngine
from mongoengine import NotUniqueError
import re

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'users',
    'host': 'mongodb',
    'port': 27017,
    'username': 'admin',
    'password': 'admin',
    'authentication_source': 'admin'
}

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('first_name',
                          type=str,
                          required=True,
                          help="Esse campo não pode ficar em branco"
                          )
_user_parser.add_argument('last_name',
                          type=str,
                          required=True,
                          help="Esse campo não pode ficar em branco"
                          )
_user_parser.add_argument('cpf',
                          type=str,
                          required=True,
                          help="Esse campo não pode ficar em branco"
                          )
_user_parser.add_argument('email',
                          type=str,
                          required=True,
                          help="Esse campo não pode ficar em branco"
                          )
_user_parser.add_argument('birth_date',
                          type=str,
                          required=True,
                          help="Esse campo não pode ficar em branco"
                          )


api = Api(app)
db = MongoEngine(app)


class UserModel(db.Document):
    cpf = db.StringField(required=True, unique=True)
    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=50)
    email = db.EmailField(required=True)
    birth_date = db.DateTimeField(required=True)


class Users(Resource):
    def get(self):
        # return jsonify(UserModel.objects())
        return {'message': 'Usuario 1'}


class User(Resource):

    def validate_cpf(self, cpf):

        # has the correct mask?
        if not re.match(r'\d{3}\.\d{3}\.\d{3}\-\d{2}', cpf):
            return False

        # grab only numbers
        numbers = [int(digit) for digit in cpf if digit.isdigit()]

        # Does it have 11 digits?
        if len(numbers) != 11 or len(set(numbers)) == 1:
            return False

        # Validate first digit after -
        sum_of_products = sum(a*b for a, b in zip(numbers[0:9],
                                                  range(10, 1, -1)))
        excepted_digit = (sum_of_products * 10 % 11) % 10
        if numbers[9] != excepted_digit:
            return False

        # Validate second digit after -
        sum_of_products = sum(a*b for a, b in zip(numbers[0:10],
                                                  range(11, 1, -1)))
        excepted_digit = (sum_of_products * 10 % 11) % 10
        if numbers[10] != excepted_digit:
            return False

        return True

    def post(self):
        data = _user_parser.parse_args()

        if not self.validate_cpf(data["cpf"]):
            return {'message': 'CPF invalido!'}, 400

        try:
            response = UserModel(**data).save()
            return {'message': 'Usuario %s cadastrado com sucesso!' % response.first_name}
        except NotUniqueError:
            return {'message': 'CPF já existe na base de dados!'}, 400

    def get(self, cpf):
        return {'message': 'CPF'}


# determinando os endpoints
api.add_resource(Users, '/users')
api.add_resource(User, '/user', '/user/<string:cpf>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
