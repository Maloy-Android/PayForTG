import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Твой токен
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
# URL для API Сбербанка
SBERBANK_API_URL = 'https://api.sberbank.ru/v1/payment'  # Замените на нужный эндпоинт

# Учетные данные для API
CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Чтобы пополнить карту, отправь команду /replenish.')

def replenish(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Введите сумму для пополнения:')

def handle_amount(update: Update, context: CallbackContext) -> None:
    amount = update.message.text

    # Проверка, что сумма является числом
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной.")
    except ValueError as e:
        update.message.reply_text(f'Ошибка: {str(e)}')
        return

    # Параметры для API
    payload = {
        'amount': int(amount * 100),  # Сумма в копейках
        'currency': 'RUB',  # Валюта
        'description': 'Пополнение карты',
        # Другие необходимые параметры
    }

    # Заголовки для запроса
    headers = {
        'Content-Type': 'application/json',
        'Client-ID': CLIENT_ID,
        'Client-Secret': CLIENT_SECRET,
    }

    try:
        response = requests.post(SBERBANK_API_URL, json=payload, headers=headers)
        response_data = response.json()

        if response.status_code == 200:
            update.message.reply_text(f'Вы успешно пополнили карту на сумму {amount} рублей.')
        else:
            update.message.reply_text(f'Ошибка: {response_data.get("error_message", "Неизвестная ошибка")}')
    except Exception as e:
        update.message.reply_text(f'Произошла ошибка: {str(e)}')

def main() -> None:
    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('replenish', replenish))
    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_amount))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
