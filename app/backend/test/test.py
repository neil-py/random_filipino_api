import requests
import sqlite3
import re
import random
import string
import datetime


request = requests.get("https://neilpy01.pythonanywhere.com/api/random-user")
print(request.json())