from flask import jsonify
from flask_restful import Resource, reqparse
from mongoengine import NotUniqueError
from .model import UserModel
import re

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


class Users(Resource):
    def get(self):
        return jsonify(UserModel.objects())
        # return {'message': 'Usuario 1'}


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
        response = UserModel.objects(cpf=cpf)

        if response:
            return jsonify(response)
        # return jsonify(UserModel.objects(cpf=cpf))
        return {'message': 'Usuario inexistente na base de dados!'}, 400
