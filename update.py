import json

import redis
import requests

from config import TOKEN_APIKEY as _api
from config import TOKEN_REDIS as _red


class Course:
    """This class updates the redis database via an API request"""
    @staticmethod
    def add_pars(endpoints):
        """This function sends a request to the API"""
        header = {'apikey': _api}
        pars = requests.get(f'https://api.apilayer.com/fixer/{endpoints}',
                            params=header).content
        return json.loads(pars)

    @staticmethod
    def add_cash():
        """This function sends the response from the API to the redis database"""
        cash = redis.Redis(
            host=_red[0],
            port=_red[1],
            password=_red[2])

        cash.set('name_currencies', json.dumps(Course.add_pars('symbols')))
        cash.set('course_currencies', json.dumps(Course.add_pars('latest')))
        if cash.get('name_currencies') and cash.get('course_currencies'):
            print('Super')
        else:
            print("No super")


Course.add_cash()
