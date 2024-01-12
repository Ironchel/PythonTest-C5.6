import telebot
from telebot import types

from config import TOKEN_TELEGR as _tel
from exception import ApiException
from exception import ServerException
from extensions import ComputationBot

megiron_bot = telebot.TeleBot(_tel)
commands = ['Показать курс', 'Обмен валют', 'Список валют', '👍']


@megiron_bot.message_handler(commands=['start'])
def main_menu(message):
    """Command function /start in telegram bot. Displays the main window with buttons"""
    markur = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = types.KeyboardButton('Показать курс')
    button_2 = types.KeyboardButton('Обмен валют')
    button_3 = types.KeyboardButton('Список валют')
    markur.add(button_1, button_2, button_3)
    megiron_bot.send_message(message.chat.id,
                             text='Что бы вы хотели сделать?\n\n'
                                  'Для показа инструкций выберите /help',
                             reply_markup=markur)


@megiron_bot.message_handler(commands=['help'])
def help_menu(message):
    """Command function /help in telegram bot. Shows instructions for using the bot"""
    megiron_bot.send_message(message.chat.id,
                             text="Валюта указывается тремя латинскими буквами!\n"
                                  "Нельзя обменивать одну и туже валют!\n\n"
                                  "1) Если вы хотите посмотреть курс валюты,\n"
                                  "бот покажет какой сейчас курс в $ и €\n\n"
                                  "2) Если вы хотите обменять валюту определённой суммы\n"
                                  "вы должны выбрать 'Обмен валют'\n"
                                  "затем выбрать валюту, которую хотите обменять\n"
                                  "затем выбрать в какую валюту обменять\n"
                                  "затем указать сумму первой валюты\n"
                                  "Пример: 'usd eur 10' или 'USD EUR 94'\n\n"
                                  "3) Если вы хотите посмотреть список валют\n"
                                  "вы должны выбрать 'Список валют'\n"
                                  "или же написать каманду '/values'")


@megiron_bot.message_handler(commands=['values'])
def values_list(message):
    """Command function /values in telegram bot. Displays a list of available currencies"""
    try:
        check_values = ServerException.check_values()
        megiron_bot.send_message(message.chat.id,
                                 text=f'{check_values}  \n\n'
                                      f'Нужна помощь? Нажмите /help')
    except ServerException as e:
        megiron_bot.reply_to(message, f'Ошибка связи с базой данных: \n{e}')


@megiron_bot.message_handler(content_types=['text'])
def antwort(message):
    """Function for text in telegram bot. Interacts with the user and responds to user requests"""
    if message.text == 'Список валют':
        try:
            check_values = ServerException.check_values()
            megiron_bot.send_message(message.chat.id,
                                     text=f'{check_values}  \n\n'
                                          f'Нужна помощь? Нажмите /help')
        except ServerException as e:
            megiron_bot.reply_to(message,
                                 f'Ошибка связи с базой данных: \n{e}')

    elif message.text == 'Показать курс':
        try:
            check_tracking = ServerException.check_tracking()
            megiron_bot.send_message(message.chat.id,
                                     text=f'{check_tracking}\n'
                                          f'Нужна помощь? Нажмите /help')
        except ServerException as e:
            megiron_bot.reply_to(message,
                                 f'Ошибка связи с базой данных: \n{e}')

    elif message.text == 'Обмен валют':
        megiron_bot.send_message(message.chat.id,
                                 text='Напишите валюту, которую хотите обменять.\n'
                                      'Затем в какую валюту обменять\n'
                                      'Затем укажите сумму первой валюты\n'
                                      '(Напимер так: "usd eur 50" или "USD EUR 250"\n')
    try:
        check = message.text.split(' ')
        check_calc = ComputationBot.check_currencies(check)
        if not check_calc and message.text not in commands:
            raise ApiException('Таких валют нет =(\n'
                               'Попробуйте ещё раз\n'
                               'Список валют здесь /values')
        elif check_calc and len(check) != 3:
            raise ApiException('Слишком много данных\n'
                               'Или не хватает данных\n'
                               'Введите две валюты и сумму\n'
                               'Помощь тут /help')
        elif check_calc and check[0] == check[1]:
            raise ApiException('Нельзя обменивать одну и туже валюту\n'
                               'Список валют тут /values')
        elif check_calc and len(check) == 3:
            ApiException.check_number(check[2])
            megiron_bot.send_message(message.chat.id, text='Сейчас посчитаю')
            megiron_bot.send_message(message.chat.id,
                                     text=f'За {check[2]} {check[0].upper()} вы получите {ComputationBot.calculation(check)} {check[1].upper()}')
        elif message.text == '👍':
            raise ApiException('Спасибо большое! Рад что понравилось)')

    except ApiException as e:
        megiron_bot.reply_to(message, f'Ошибка ввода: \n{e}')
    except IndexError as e:
        megiron_bot.reply_to(message, f'Ошибка ввода: \n{e}\n'
                                      f'Вы ввели только одну правильную валюту')
    except Exception as e:
        megiron_bot.reply_to(message, f'Все пропало!!!\n{e}')


megiron_bot.polling(none_stop=True, interval=0)
