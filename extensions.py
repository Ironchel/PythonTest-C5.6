import json

import redis

from config import TOKEN_REDIS as _red

cash = redis.Redis(
    host=_red[0],
    port=_red[1],
    password=_red[2])


class ComputationBot:
    """Class for working with the redis database. Processes requests from the user, carries out currency exchange"""

    @staticmethod
    def show_tracking():
        """The function will respond to the “show rate” request by reading data from the redis database"""
        tracking = {
            'EUR': {'USD': 'доллар', 'UAH': 'гривна', 'RUB': 'рубль',
                    'CNY': 'юань', 'PLN': 'злотый', 'BTC': 'биткоин'},
            'USD': {'EUR': 'евро', 'UAH': 'гривна', 'RUB': 'рубль',
                    'CNY': 'юань', 'PLN': 'злотый', 'BTC': 'биткоин'}}
        course_currencies = json.loads(cash.get('course_currencies'))
        result = ''
        for base_currency, currencies in tracking.items():
            result += f'Курс за 1 {base_currency.lower()}\n-----------------\n'
            for currency, name in currencies.items():
                cours = course_currencies['rates'][currency]
                if currency == 'BTC':
                    result += f'{currency} {round(1 / cours)} {base_currency} за биткоин\n'
                else:
                    result += f'{currency} {round(1 / course_currencies["rates"][base_currency] * cours, 2)} {name}\n'
            result += '\n\n*****************\n\n'

        return result

    @staticmethod
    def get_values():
        """The function will respond to the request “List of currencies” by reading data from the redis database"""
        list_currencies = ''
        name_currencies = json.loads(cash.get('name_currencies'))
        for abbreviation, name in name_currencies['symbols'].items():
            list_currencies += abbreviation + '  ' + name + '\n'
        return list_currencies

    @staticmethod
    def check_currencies(curr):
        """The function checks the presence of a currency in the redis database list"""
        course_currencies = json.loads(cash.get('course_currencies'))
        if (curr[0].upper() in course_currencies['rates'].keys() and
                curr[1].upper() in course_currencies['rates'].keys()):
            return True
        else:
            return False

    @staticmethod
    def calculation(calc):
        """The function exchanges currencies at the user's request using data from the redis database"""
        course_currencies = json.loads(cash.get('course_currencies'))
        curr_1 = course_currencies['rates'][f'{calc[0].upper()}']
        curr_2 = course_currencies['rates'][f'{calc[1].upper()}']
        if len(calc) == 3:
            return round((1 / curr_1 * curr_2) * float(calc[2]), 5)
        return round(1 / curr_1 * curr_2, 5)
