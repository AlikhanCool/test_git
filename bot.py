import telebot # библиотека telebot, очень важно
from config import token # импорт токена

bot = telebot.TeleBot(token) 

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я бот для управления чатом.")

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message: # проверка на то, что эта команда была вызвана в ответ на сообщение 
        chat_id = message.chat.id # сохранение id чата
        # сохранение id и статуса пользователя, отправившего сообщение
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status 
        # проверка пользователя
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно забанить администратора.")
        else:
            bot.ban_chat_member(chat_id, user_id) # пользователь с user_id будет забанен в чате с chat_id
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите забанить.")

@bot.message_handler(func=lambda message: True)
def check_for_links_and_ban(message):
    # Проверяем наличие текста и ссылки "https://" в сообщении
    if message.text and "https://" in message.text:
        chat_id = message.chat.id
        user = message.from_user
        
        # Сохраняем информацию о пользователе
        user_id = user.id
        username = user.username or "отсутствует"
        
        try:
            # Проверяем статус пользователя перед баном (чтобы случайно не забанить админа)
            user_status = bot.get_chat_member(chat_id, user_id).status
            if user_status == 'administrator' or user_status == 'creator':
                return # Не баним администраторов за ссылки
            
            # Баним пользователя в чате
            bot.ban_chat_member(chat_id, user_id)
            
            # Удаляем сообщение с ссылкой
            bot.delete_message(chat_id, message.message_id)
            
            # Отправляем уведомление о бане
            bot.send_message(
                chat_id, 
                f"Пользователь @{username} (ID: {user_id}) заблокирован за размещение ссылки."
            )
        except Exception as e:
            # Обработка ошибок
            print(f"Не удалось забанить пользователя {user_id}: {e}")

bot.infinity_polling(none_stop=True)