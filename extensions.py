import json

import redis

from config import TOKEN_REDIS as _red

cash = redis.Redis(
    host=_red[0],
    port=_red[1],
    password=_red[2])


class ComputationBot:

    @staticmethod
    def show_tracking():
        tracking_eur = {'USD': 'доллар', 'UAH': 'гривна',
                        'RUB': 'рубль', 'CNY': 'юань', 'PLN': 'злотый',
                        'BTC': 'биткоин'}
        tracking_dol = {'EUR': 'евро', 'UAH': 'гривна',
                        'RUB': 'рубль', 'CNY': 'юань', 'PLN': 'злотый',
                        'BTC': 'биткоин'}
        course_currencies = json.loads(cash.get('course_currencies'))
        list_tracking = 'Курс за 1 евро\n-----------------\n'
        for item in tracking_eur.keys():
            cours = course_currencies['rates'][f'{item}']
            if item == 'BTC':
                list_tracking += item + " " + str(
                    round(1 / cours)) + ' € за биткоин'
                continue
            list_tracking += item + " " + str(
                round(1 / course_currencies['rates']['EUR'] * cours,
                      2)) + ' ' + tracking_eur[f'{item}'] + '\n'
        list_tracking += '\n\n*****************\n\nКурс за 1 доллар\n-----------------\n'
        for item_2 in tracking_dol.keys():
            cours = course_currencies['rates'][f'{item_2}']
            if item_2 == 'BTC':
                list_tracking += item_2 + " " + str(round(
                    1 / cours * course_currencies['rates'][
                        'USD'])) + ' $ за биткоин'
                continue
            list_tracking += item_2 + " " + str(
                round(1 / course_currencies['rates']['USD'] * cours,
                      2)) + ' ' + tracking_dol[f'{item_2}'] + '\n'
        return list_tracking

    @staticmethod
    def get_values():
        list_currencies = ''
        name_currencies = json.loads(cash.get('name_currencies'))
        for abbreviation, name in name_currencies['symbols'].items():
            list_currencies += abbreviation + '  ' + name + '\n'
        return list_currencies

    @staticmethod
    def check_currencies(curr):
        course_currencies = json.loads(cash.get('course_currencies'))
        if (curr[0].upper() in course_currencies['rates'].keys() and
                curr[1].upper() in course_currencies['rates'].keys()):
            return True
        else:
            return False

    @staticmethod
    def calculation(calc):
        course_currencies = json.loads(cash.get('course_currencies'))
        curr_1 = course_currencies['rates'][f'{calc[0].upper()}']
        curr_2 = course_currencies['rates'][f'{calc[1].upper()}']
        if len(calc) == 3:
            return round((1 / curr_1 * curr_2) * float(calc[2]), 5)
        return round(1 / curr_1 * curr_2, 5)
