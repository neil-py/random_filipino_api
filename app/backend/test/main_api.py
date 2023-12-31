from flask import Flask, jsonify, render_template
from flask_restful import Resource, Api, reqparse
import sqlite3
import random
import string
import datetime

app = Flask("rand_fil_api", template_folder='app/templates')
app.json.sort_keys = False
app.json.ensure_ascii = False
api = Api(app)

class DatabaseQuery:
    """
    Responsible for handling all database requests
    """
    def __init__(self):
        self.__conn = sqlite3.connect('app/backend/database/randomfilipino_db.db') # **CONNECT TO THE DATABASE

    def close_connection(self):
        self.__conn.close()

    def query_random_address(self):
        """
        Query the Database and return random address records
        """
        cursor = self.__conn.cursor()
        cursor.execute(
            """
            SELECT 
            * 
            FROM 
            RAND_ADDRESS 
            LIMIT 1 
            OFFSET ABS(
                RANDOM()) % 
                    (SELECT COUNT(*) FROM RAND_ADDRESS);
            """
        )
        result = cursor.fetchone() # **FETCHALL RECORDS; RETURNS A SET
        
        
        street = result[0]
        city_suburb = result[1]
        postalcode = result[2]
        return_data = {
                'street': street,
                'city/suburb': city_suburb,
                'postalcode': postalcode
                }
        
        return return_data
    
    def query_random_name(self, gender):
        """
        Query the Database and return random name records based on the 'size' argument
        """
        gender = gender[0].upper() + gender[1:] if gender != None else gender
        cursor = self.__conn.cursor()
        random_first_name_amt = random.randint(1, 2)
        if gender == None:
            cursor.execute(
                """
                SELECT 
                * 
                FROM 
                FNAME
                LIMIT ? 
                OFFSET ABS(
                    RANDOM()) % MAX (
                        (SELECT COUNT(*) FROM LNAME), 1);
                """,
                (random_first_name_amt,)
            )
        else:
            cursor.execute(
                """
                SELECT 
                * 
                FROM 
                FNAME 
                WHERE SEX = ?
                ORDER BY RANDOM() LIMIT ?;
                """,
                 (gender, random_first_name_amt,)
            )

        first_name_result = cursor.fetchall()
        cursor.execute(
            """
            SELECT 
            * 
            FROM 
            LNAME
            LIMIT 1 
            OFFSET ABS(
                RANDOM()) % MAX (
                    (SELECT COUNT(*) FROM LNAME), 1
                    );
            """
        )
        
        last_name_result = cursor.fetchall()

        first_name = first_name_result[0][0] if random_first_name_amt == 1 else f"{first_name_result[0][0]} {first_name_result[1][0]}"
        return_data = {
                    'first_name': first_name,
                    'last_name': last_name_result[0][0],
                    'sex': first_name_result[0][1]
                }
        return return_data
    
class RandomUserInfo:
    """
    Class is responsible for handling random informations
    """
    def __init__(self):
        self._random_numbers = string.digits
    
    def RandomPhoneNumber(self) -> dict:
        philippine_phone_networks = {
            "Globe": ["0905", "0906", "09257", "09258", "0917", "0916", "0915", "0935", "0936", "0937"],
            "DITO": ["0895", "0896", "0897", "0898", "0991", "0992", "0993", "0994"],
            "Smart": ["0908", "0918", "0919", "0920", "0921", "0928", "0897", "0898", "0929", "0939", "0961", "0951", "0998", "0999"],
            "Sun": ["0922", "0923", "0924", "0925", "0931", "0932", "0933", "0934", "0940", "0941"],
            "TNT": ["0930", "0938"]
        }       
        
        network, prefixes = random.choice(list(philippine_phone_networks.items())) # return random pairs for values
        random_prefix = random.choice(prefixes) # select random prefix from the prefixes array of a network

        random_phone_number = f"{random_prefix}{"".join(random.choice(self._random_numbers) for i in range(11-len(random_prefix)))}"

        return_result = {
                'country_code': "+63",
                'phone_number': random_phone_number,
                'network': network
            }
        return return_result


    def RandomEmail(self, first_name, last_name) -> str:
        email_domains = ["gmail.com", "yahoo.com", "outlook.com", "yandex.com", "hotmail.com"]
        string_char = "._"
        rand_num_add = "".join(random.choice(self._random_numbers) for i in range (random.randint(0, 10)))
        base_email_format = f"{first_name.lower()}{random.choice(string_char)}{last_name.lower()}{rand_num_add}@{random.choice(email_domains)}"

        return base_email_format

    def RandomDOB(self):
        today = datetime.date.today()
        current_year = today.year
        random_birth_year = random.randint(current_year-100, current_year)
        random_birth_month = random.choice(["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"])
        random_birth_day = random.randint(1, 31) if random_birth_month == "02" else random.randint(1, 28)

        random_DOB_response = f"{random_birth_year}-{random_birth_month}-{random_birth_day}"

        return random_DOB_response


    def RandomSSN(self) -> str:
        # sample : 123-45-6789
        first_03 = "".join(random.choice(self._random_numbers) for i in range(3))
        second_02 = "".join(random.choice(self._random_numbers) for i in range(2))
        third_04 = "".join(random.choice(self._random_numbers) for i in range(4))
        random_ssn_response = f"{first_03}-{second_02}-{third_04}"

        return random_ssn_response
    

    def RandomNationalID(self) -> str:
        random_number_group = "".join(random.choice(self._random_numbers) for i in range (4))
        random_national_id = f"PSN-{random_number_group}-{random_number_group}-{random_number_group}"

        return random_national_id
    

    def RandomLicense(self) -> dict:
        random_licenses_type  = random.choice(["Student Permit", "Non-Professional", "Professional"])
        random_license_number = "".join(random.choice(self._random_numbers) for i in range(11))

        random_license_response = {
            'type': random_licenses_type,
            'license_number': random_license_number
        }
        
        return random_license_response


    def RandomBankCC(self):
        philippine_banks = [
            "BDO", "Metrobank", "BPI", "Landbank", "PNB",
            "Security Bank", "Chinabank", "UnionBank", "DBP", "RCBC",
            "EastWest Bank", "UCPB", "AUB", "PSBank", "Veterans Bank",
            "Robinsons Bank", "Bank of Commerce", "Maybank", "CTBC Bank", "BDO Private Bank"
        ]
        random_bank_account_number = "".join(random.choice(self._random_numbers) for i in range (random.randint(10, 12)))

        prefix_dict = {'4': "Visa", '5': "Mastercard", '3': "Amex"}
        random_prefix, card_type = random.choice(list(prefix_dict.items()))

        random_bank_account_response = {
            'bank_name': random.choice(philippine_banks),
            'bank_account_number': random_bank_account_number,
            'credit_card_info': {}
        }

        if card_type == "Amex":
            postfix_values = "".join(random.choice(self._random_numbers) for i in range (15))
            random_credit_card = f"{random_prefix}{postfix_values}"
            random_expiry_month = random.choice(["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"])
            random_expiry_year = random.randint(2023, 2050)
            random_security_number = "".join(random.choice(self._random_numbers) for i in range (4))
            random_bank_account_response['credit_card_info']['card_type'] = card_type
            random_bank_account_response['credit_card_info']['card_number'] = random_credit_card
            random_bank_account_response['credit_card_info']['expiry_month'] = random_expiry_month
            random_bank_account_response['credit_card_info']['expiry_year'] = random_expiry_year
            random_bank_account_response['credit_card_info']['security_number'] = random_security_number
        else:
            postfix_values = "".join(random.choice(self._random_numbers) for i in range (15))
            random_credit_card = f"{random_prefix}{postfix_values}"
            random_expiry_month = random.choice(["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"])
            random_expiry_year = random.randint(2023, 2050)
            random_security_number = "".join(random.choice(self._random_numbers) for i in range (3))
            random_bank_account_response['credit_card_info']['card_type'] = card_type
            random_bank_account_response['credit_card_info']['card_number'] = random_credit_card
            random_bank_account_response['credit_card_info']['expiry_month'] = random_expiry_month
            random_bank_account_response['credit_card_info']['expiry_year'] = random_expiry_year
            random_bank_account_response['credit_card_info']['security_number'] = random_security_number

        return random_bank_account_response


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
     

#! DOCUMENTATION ENDPOINT #
@app.route('/')
def index():
    return render_template('index.html')
    
# ! API ENDPOINTS: BE CAREFUL !
api.add_resource(RandomFilipinoUser, '/api/random-user')
api.add_resource(RandomAddress, '/api/random-address')
api.add_resource(RandomName, '/api/random-name')
api.add_resource(RandomPhoneNumber, '/api/random-phone')


if __name__ == '__main__':
    app.run(debug=True)