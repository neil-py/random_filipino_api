from flask import jsonify
from flask_restful import Resource, reqparse
from app.backend.api.data_query import DatabaseQuery, RandomUserInfo
import string
import random
import datetime

class RandomFilipinoUser(Resource):
    # TODO: Handle Random Filipino Information Requests
    
    def __init__(self):
        self.__RandomUser = RandomUserInfo()
        self.__DatabaseQuery = DatabaseQuery()
    
    def CompleteRandomUser(self, gender) -> dict:
        __user_info = self.__DatabaseQuery.query_random_name(gender=gender)
        __first_name = __user_info['first_name']
        __last_name = __user_info['last_name']
        complete_random_user_response = {
            'user_info': __user_info,
            'date_of_birth': self.__RandomUser.RandomDOB(),
            'email_address': self.__RandomUser.RandomEmail(__first_name, __last_name),
            'address': self.__DatabaseQuery.query_random_address(),
            'phone_number': self.__RandomUser.RandomPhoneNumber(),
            'identification': {
                'social_security_number': self.__RandomUser.RandomSSN(),
                'national_id': self.__RandomUser.RandomNationalID(),
                'license': self.__RandomUser.RandomLicense()
            },
            'bank_details': self.__RandomUser.RandomBankCC()

        }

        return complete_random_user_response
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'size',
            type = int,
            help = "Invalid Parameter",
            required = False,
            location = 'args'
        )
        parser.add_argument(
            'gender',
            type = str,
            help = "Invalide Parameter",
            required = False,
            location = 'args'
        )

        args = parser.parse_args()
        size_arg = args['size']
        gender_arg = args['gender']
        complete_random_user_response = {'results': []}

        if gender_arg is not None and str(gender_arg).lower() not in ["male", "female"]:
            return jsonify(message={'gender': 'Invalid Parameter'})
        
        if size_arg == None:
            complete_random_user = self.CompleteRandomUser(gender=None if gender_arg == None else gender_arg)
            complete_random_user_response['results'].append(complete_random_user)
        else:
            count = 0
            while count < size_arg:
                complete_random_user = self.CompleteRandomUser(gender=gender_arg)
                complete_random_user_response['results'].append(complete_random_user)
                count += 1

        self.__DatabaseQuery.close_connection()
        return jsonify(complete_random_user_response)


class RandomAddress(Resource):     
    
    def get(self):
        
        parser = reqparse.RequestParser()
        parser.add_argument('size', 
                            type=int, 
                            help='Invalid Parameter', 
                            required=False,
                            location ='args'
                            )
        args = parser.parse_args()

        size_arg = args['size']
        dbq = DatabaseQuery()
        random_address_dict = {'result': []}
        if size_arg == None:
            random_address_return = dbq.query_random_address()
            random_address_dict['result'].append(random_address_return)
        else:
            count = 0
            while count < size_arg:
                random_address_return = dbq.query_random_address()
                random_address_dict['result'].append(random_address_return)
                count+=1

        dbq.close_connection() #closes database connection after query
        return jsonify(random_address_dict)
  

class RandomName(Resource):
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'size', 
            type = int,
            help = 'Invalid Parameter',
            required=False,
            location='args'
        )
        parser.add_argument(
            'gender',
            type = str,
            help = "Generate name based on gender",
            required = False,
            location = 'args'
        )
        args = parser.parse_args()

        size_arg = args['size']
        gender_arg = args['gender']
        
        dbq = DatabaseQuery()
        random_name_response = {'results': []}
        if gender_arg is not None and str(gender_arg).lower() not in ["male", "female"]:
            return jsonify(message={'gender': 'Invalid Parameter'})
        
        if size_arg == None:
            random_name_return = dbq.query_random_name(gender=None if gender_arg == None else gender_arg)
            random_name_response['results'].append(random_name_return)
        elif size_arg > 30:
            random_name_response['results'].append({
                'error': {
                    'max_limit_reached': {
                        'message': 'requests are limited to 30'
                     }
                    }
                     })
        else:
            count = 0
            while count < size_arg:
                random_name_return = dbq.query_random_name(gender=None if gender_arg == None else gender_arg)
                random_name_response['results'].append(random_name_return)
                count+=1
        dbq.close_connection()
        return jsonify(random_name_response)

class RandomPhoneNumber(Resource):
     
     def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
             'size',
             type = int,
             help = "Size of the result",
             required = False,
             location = 'args'
         )
        args = parser.parse_args()

        size_arg = args['size']
        rnd = RandomUserInfo()
        random_phone_number_return_data = {'result': []}
        if size_arg == None:
            random_phone_number = rnd.RandomPhoneNumber()
            random_phone_number_return_data['result'].append(random_phone_number)
        else:
            count = 0
            while count < size_arg:
                random_phone_number = rnd.RandomPhoneNumber()
                random_phone_number_return_data['result'].append(random_phone_number)
                count+=1

        return jsonify(random_phone_number_return_data)