Telegram bot for exchanging 170 world currencies. The bot can:
1) Show the rate of popular currencies using the "Show rate" button
2) Exchange currency indicating the amount

Launch the bot from the file telegramm_bot.py
File update.py is needed to update the database redis
because requests to API are limited, so a call is made to update.py is made so that the file updates this database
Then the program works directly with database redis.
