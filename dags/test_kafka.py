import uuid
from datetime import datetime
import requests
import json
from kafka import KafkaProducer
import time
import logging

default_args = {
    'owner': 'pactcha',
    'start_date': datetime(2024, 1, 20, 00, 00)
}

def get_data():

    # get data from api 
    res = requests.get("https://randomuser.me/api/")
    # retrive a json like {'results':[<data>]}
    res = res.json()
    # return a dummy personal infomation
    res = res['results'][0]

    return res

def format_data(res):
    data = {}
    location = res['location']
    # Convert a UUID to a string of hex digits in standard form
    data['id'] = str(uuid.uuid4())
    data['first_name'] = res['name']['first']
    data['last_name'] = res['name']['last']
    data['gender'] = res['gender']
    data['address'] = f"{str(location['street']['number'])} {location['street']['name']}, " \
                      f"{location['city']}, {location['state']}, {location['country']}"
    data['post_code'] = location['postcode']
    data['email'] = res['email']
    data['username'] = res['login']['username']
    # date of birth
    data['dob'] = res['dob']['date']
    data['registered_date'] = res['registered']['date']
    data['phone'] = res['phone']
    data['picture'] = res['picture']['medium']

    return data

def jsontostring(res):
    return json.dumps(res).encode('utf-8')

def stream_data():
    # run 2 round for produce data to kafka
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'], max_block_ms=5000) 
    #'localhost:9092' for test
    #'broker:29092' for on docker container
    curr_time = time.time()

    try:
        res = get_data()
        res = format_data(res)
        res = jsontostring(res)
        producer.send('users_information', res)
    except Exception as e:
        logging.error(f'An error occured: {e}')
        
stream_data()