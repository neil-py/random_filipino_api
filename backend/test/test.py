import requests
import sqlite3
import re
import random
import string
import datetime


random_number_group = "".join(random.choice("0123456789") for i in range (4))
random_national_id = f"PSN-{random_number_group}-{random_number_group}-{random_number_group}"

print(random_national_id)