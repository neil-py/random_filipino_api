import requests
from bs4 import BeautifulSoup
import sqlite3
import asyncio
import random

def connect():
    """
    Creates a connection to the database and creates required tables if not exist

    """
    con = sqlite3.connect('randomfilipino_db.db')

    # create tables if not exist yet
    create_RAND_ADD_table_query = """
        CREATE TABLE if not exists RAND_ADDRESS (
        STREET VARCHAR (255),
        STATE VARCHAR (255),
        POST_CODE INTEGER
        );
    """
    cursor = con.cursor()
    cursor.execute(create_RAND_ADD_table_query) #execute query
    cursor.close()

    # create tables if not exist yet
    create_FNAME_table_query = """
        CREATE TABLE if not exists FNAME (
        FIRST_NAME VARCHAR (255),
        SEX VARCHAR (100)
        );
    """
    cursor = con.cursor()
    cursor.execute(create_FNAME_table_query) #execute query
    cursor.close()

    create_FNAME_table_query = """
        CREATE TABLE if not exists LNAME (
        LAST_NAME VARCHAR (255)
        );
    """
    cursor = con.cursor()
    cursor.execute(create_FNAME_table_query) #execute query
    cursor.close()

    return con


async def RandomAddressScraper():
    url = "https://www.generatormix.com/random-address-in-philippines?number=20"
    web_request = requests.get(url=url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"})
    url_doc = web_request.text
    soup = BeautifulSoup(url_doc, "html.parser")
    div_data = soup.find_all("div", class_ = "col-6 tile-block-inner marg-top")
    
    SUCCESS_COUNT = 0
    con = connect()
    for address in div_data:
        address_data = {}
        for data in address.find_all("p", class_="text-left"):
            strong_tag = data.find('strong')
            key = strong_tag.text.strip(':')
            value = strong_tag.next_sibling.strip()
            # Check if the key is one of the desired keys
            if key in ["Street", "Suburb/City", "Postcode"]:
                address_data[key] = value
        
        try:
            # add data to database
            insert_db_query = """
                INSERT INTO RAND_ADDRESS values (?,?,?);
            """
            
            cursor = con.cursor()
            cursor.execute(insert_db_query, (address_data['Street'], address_data['Suburb/City'], address_data['Postcode']))
            con.commit()
            SUCCESS_COUNT+=1
            
        except:
            continue

    print(f"SUCCESSFULLY ADDED - {SUCCESS_COUNT}")
    con.close()



def if_fname_exist(con, name):
    cursor = con.cursor()
    cursor.execute("SELECT COUNT(*) FROM FNAME WHERE FIRST_NAME = ?", (name,))
    count = cursor.fetchone()[0]
    return count > 0

def if_lname_exist(con, name):
    cursor = con.cursor()
    cursor.execute("SELECT COUNT(*) FROM lNAME WHERE LAST_NAME = ?", (name,))
    count = cursor.fetchone()[0]
    return count > 0

async def RandomNameScrapper1():
    url = "https://www.random-name-generator.com/philippines?s={seed}&search_terms=&gender=&search_terms=&n=10"
    web_request = requests.get(url=url.format(seed = random.randint(300, 10000)), headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"})
    url_doc = web_request.text
    soup = BeautifulSoup(url_doc, "html.parser")
    card_div_data = soup.find("div", class_ = "card-body")
    name_div = card_div_data.find_all("dd", class_ = "h4 col-12")

    con = connect()
    SUCCESS_COUNT_FIRST = 0
    SUCCESS_COUNT_LAST = 0
    for name in name_div:
        fullname = name.contents[0].strip().split()  # Extract the name
        fname = fullname[0]
        lname = fullname[-1]
        sex = name.small.text.strip('()')  # Extract the sex
        print(fullname, sex)
        if not if_fname_exist(con, fname):
            try:
                insert_db_query_Fname = """
                        INSERT INTO FNAME values (?, ?);
                    """
                cursor = con.cursor()
                cursor.execute(insert_db_query_Fname, (fname, sex))
                con.commit()
                SUCCESS_COUNT_FIRST+=1
            except:
                
                pass
        
        if not if_lname_exist(con, lname):
            try:
                insert_db_query_lname = """
                        INSERT INTO LNAME values (?);
                    """
                cursor.execute(insert_db_query_lname, (lname,))
                con.commit()
                SUCCESS_COUNT_LAST+=1
            except:
                pass
    print("SUCCESS", f" - FNAME: {SUCCESS_COUNT_FIRST} LNAME: {SUCCESS_COUNT_LAST}")
    con.close()

def RandomNameScrapper2():
    pass

async def main():
    await asyncio.gather(*(RandomAddressScraper() for i in range(200)))
        
    

asyncio.run(main())
