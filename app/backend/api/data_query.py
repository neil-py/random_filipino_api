import sqlite3
import random
import string
import datetime



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
                    'gender': first_name_result[0][1]
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