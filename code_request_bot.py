from telebot import TeleBot, types
import sqlite3
from datetime import datetime
now = datetime.now()



token='6709615504:AAHXlUquuFDxZ2RkX5m4CTQN0rru_jM_I60'#6507239473:AAHV3QVbhJmagkAu54pbC5BcSXuydKNGmHc
bot = TeleBot(token)

db = sqlite3.connect('data.db', check_same_thread=False)
sql = db.cursor()

company_name = ''
work_type = ''
workers = ''
work_date = ''
worker_id = ''
id=''
operation_type=1
cars = ''
delivery_or_work = 1
people_or_car = 1
delivery_name = ''
list_of_materials = ''
date_of_work = ''
place_of_work = ''
type_of_work = ''
curator_contact = ''
which_type_of_work=''
delivery_date=''
list_of_materials=''
head_of_workers=''
guest_name = ''
guest_date = ''
guest_phone = ''
guest_car = ''

guard_id='-4064013770'


@bot.message_handler(commands=['start'])
def start(message):
    start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
    sm1 = types.KeyboardButton('Заявка на Работы')
    sm2 = types.KeyboardButton('Заявка на Доставку')
    sm3 = types.KeyboardButton('Пропуск для гостя')
    start_markup.add(sm1, sm2, sm3)
    bot.send_message(message.chat.id, 'Какой тип заявки хотите подать? (выберите на клавиатуре)', reply_markup=start_markup)
    
@bot.message_handler(content_types=['text'])
def main(message):
    global worker_id, people_or_car
    print(f"[{now.strftime("%d/%m/%Y %H:%M:%S")}][{message.chat.id}] {message.text}")
    if message.text == "Заявка на Работы":
        works(message)
    elif message.text == 'Пропуск для гостя':
        bot.send_message(message.chat.id, "Отпрвьте ФИО гостя")
        bot.register_next_step_handler(message, get_guest_name)
    elif message.text == "Подать заявку на Работы":
        people_or_car = 1
        bot.send_message(message.chat.id, 'Введите название вашей компании')
        bot.register_next_step_handler(message, get_company_name)
    elif message.text == "Зарегистрировать технику":
        people_or_car = 2
        bot.send_message(message.chat.id, 'Введите название вашей компании')
        bot.register_next_step_handler(message, get_company_name)
    elif message.text == "Заявка на Доставку":
        bot.send_message(message.chat.id, 'Введите название вашей компании')
        bot.register_next_step_handler(message, get_company_delivery_name)
    elif message.text == 'Подтвердить' and operation_type == 1:
        bot.send_message(message.chat.id, 'Заявка отправлена')
        write_to_db(message)
    elif message.text == 'Подтвердить' and operation_type == 2:
        worker_id = message.chat.id
        bot.send_message(message.chat.id, 'Заявка отправлена')
        write_to_db(message)
    elif message.text == 'Подтвердить' and operation_type == 3:
        worker_id = message.chat.id
        sql.execute(f"SELECT * FROM requests_for_work_from_{worker_id}")
        data = sql.fetchall()
        message_to_send = f"Компания: {data[id][1]}\nДата проведения работ: {work_date}\nМесто проведения работ: {data[id][3]}\nВид работ: {data[id][4]}\nРаботники: {data[id][5]}\nОтветственный: {data[id][6]} \nМашины: {data[id][7]}\nКуратор codevelopment: {data[id][8]}"
        bot.send_message(guard_id, f'''<b>Новая заявка на работы 🏗️</b>
<b>Компания:</b> {data[id][1]}
<b>Дата проведения работ:</b> {work_date}
<b>Локация:</b> {data[id][3]}
<b>Вид работ:</b> {data[id][4]}
<b>Работники:</b> {data[id][5]}
<b>Ответственный за карту:</b> {data[id][6]}
<b>Техника:</b> {data[id][7]}
<b>Куратор от CODE:</b> {data[id][8]}''', parse_mode='html')
        bot.send_message(message.chat.id, "Заявка отправлена")
    elif message.text == 'Подтвердить' and operation_type == 4:
        bot.send_message(guard_id, f'''<b>Новая заявка на гостя🟠</b>
<b>ФИО:</b> {guest_name}
<b>Дата прихода:</b> {guest_date}
<b>Номер телефона:</b> {guest_phone}
<b>Данные авто:</b> {guest_car}''', parse_mode='html')
        bot.send_message(message.chat.id, "Заявка отправлена")
    elif message.text == 'Перезаполнить зявку' and operation_type == 1:
        bot.send_message(message.chat.id, 'Введите название вашей компании')
        bot.register_next_step_handler(message, get_company_delivery_name)
    elif message.text == 'Перезаполнить зявку' and operation_type == 2:
        bot.send_message(message.chat.id, 'Введите название вашей компании')
        bot.register_next_step_handler(message, get_company_name)
    elif message.text == 'Перезаполнить зявку' and operation_type == 3:
        old_request(message)
    elif message.text == 'Перезаполнить зявку' and operation_type == 4:
        bot.send_message(message.chat.id, "Отпрвьте ФИО гостя")
        bot.register_next_step_handler(message, get_guest_name)
    elif message.text == 'Отправить старую заявку с новой датой':
        old_request(message)
    elif message.text == 'Назад':
        start(message)

def get_guest_name(message):
    global guest_name
    guest_name = message.text
    bot.send_message(message.chat.id, "Отправьте дату прихода гостя")
    bot.register_next_step_handler(message, get_guest_date)

def get_guest_date(message):
    global guest_date
    guest_date = message.text
    bot.send_message(message.chat.id, "Отправьте номер телефона гостя")
    bot.register_next_step_handler(message, get_guest_phone)
    
def get_guest_phone(message):
    global guest_phone
    guest_phone = message.text
    bot.send_message(message.chat.id, "Отправьте данные авто гостя (Ford Focus A153AAA197)")
    bot.register_next_step_handler(message, get_guest_car)
    
def get_guest_car(message):
    global guest_car, operation_type
    guest_car = message.text
    operation_type = 4
    bot.send_message(message.chat.id, f'''<b>Новая заявка на гостя🟠</b>
<b>ФИО:</b> {guest_name}
<b>Дата прихода:</b> {guest_date}
<b>Номер телефона:</b> {guest_phone}
<b>Данные авто:</b> {guest_car}''', parse_mode='html')
    conf_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    cm1 = types.KeyboardButton('Подтвердить')
    cm2 = types.KeyboardButton('Перезаполнить зявку')
    cm3 = types.KeyboardButton("Назад")
    conf_markup.add(cm1, cm2, cm3)
    bot.send_message(message.chat.id, 'Проверьте правильность введенных данных и подтвердите отправку заявки', reply_markup=conf_markup)

def old_request(message):
    
    worker_id = message.chat.id
    print(worker_id)
    sql.execute(f"SELECT * FROM requests_for_work_from_{worker_id}")
    data = sql.fetchall()
    k=1
    for i in range(len(data)):

        print(len(data))
        message_to_send = f"{str(k)}.\nКомпания: {data[i][1]}\nМесто проведения работ: {data[i][3]}\nВид работ: {data[i][4]}\nРаботники: {data[i][5]}\nОтветственный: {data[i][6]} \nМашины: {data[i][7]}\nКуратор codevelopment: {data[i][8]}"
        bot.send_message(guard_id, f'''<b>Новая заявка на работы 🏗️</b>
<b>Компания:</b> {data[i][1]}
<b>Локация:</b> {data[i][3]}
<b>Вид работ:</b> {data[i][4]}
<b>Работники:</b> {data[i][5]}
<b>Ответственный за карту:</b> {data[i][6]}
<b>Техника:</b> {data[i][7]}
<b>Куратор от CODE:</b> {data[i][8]}''', parse_mode='html')
        k+=1
    bot.register_next_step_handler(message, request_resend_id)
    bot.send_message(message.chat.id, 'Напишите номер заявки из списка (например: 1)')

def works(message):
    global delivery_or_work
    delivery_or_work = 2
    works_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    wm1 = types.KeyboardButton('Подать заявку на Работы')
    wm2 = types.KeyboardButton('Отправить старую заявку с новой датой')
    wm3 =  types.KeyboardButton('Назад')
    works_markup.add(wm1, wm2, wm3)
    bot.send_message(message.chat.id, 'Что вы хотите сделать?', reply_markup=works_markup)


def request_resend_id(message):
    global id
    id=message.text
    bot.send_message(message.chat.id, 'Отправте новую дату в формате 01.01.2021')
    bot.register_next_step_handler(message, request_resend_date)

def request_resend_date(message):
    global operation_type, id, work_date
    worker_id = message.chat.id
    sql.execute(f"SELECT * FROM requests_for_work_from_{worker_id}")
    data = sql.fetchall()
    print(data)
    try:
        id = int(id)-1
        work_date = message.text
        message_to_send = f"Компания: {data[id][1]}\nДата проведения работ: {work_date}\nМесто проведения работ: {data[id][3]}\nВид работ: {data[id][4]}\nРаботники: {data[id][5]}\nОтветственный: {data[id][6]} \nМашины: {data[id][7]}\nКуратор codevelopment: {data[id][8]}"
    except:
        bot.send_message(message.chat.id, 'Неверный номер заявки, попробуйте еще раз')
        bot.register_next_step_handler(message, request_resend_id)
        old_request(message)
        exit()
    work_date = message.text
    message_to_send = f"Компания: {data[id][1]}\nДата проведения работ: {work_date}\nМесто проведения работ: {data[id][3]}\nВид работ: {data[id][4]}\nРаботники: {data[id][5]}\nОтветственный: {data[id][6]} \nМашины: {data[id][7]}\nКуратор codevelopment: {data[id][8]}"
    bot.send_message(message.chat.id, f'''<b>Новая заявка на работы 🏗️</b>
<b>Компания:</b> {data[id][1]}
<b>Дата проведения работ:</b> {work_date}
<b>Локация:</b> {data[id][3]}
<b>Вид работ:</b> {data[id][4]}
<b>Работники:</b> {data[id][5]}
<b>Ответственный за карту:</b> {data[id][6]}
<b>Техника:</b> {data[id][7]}
<b>Куратор от CODE:</b> {data[id][8]}''', parse_mode='html')
    operation_type=3
    conf_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    cm1 = types.KeyboardButton('Подтвердить')
    cm2 = types.KeyboardButton('Перезаполнить зявку')
    cm3 = types.KeyboardButton("Назад")
    conf_markup.add(cm1, cm2, cm3)
    bot.send_message(message.chat.id, 'Проверьте правильность введенных данных и подтвердите отправку заявки', reply_markup=conf_markup)
    

def get_company_name(message):
    global company_name
    company_name = message.text
    bot.send_message(message.chat.id, 'Введите дату проведения работ (например: 01.01.2021)')
    bot.register_next_step_handler(message, get_date_of_work)
    
def get_date_of_work(message):
    global date_of_work
    date_of_work = message.text
    bot.send_message(message.chat.id, 'Введите локацию проведения работ')
    bot.register_next_step_handler(message, get_place_of_work)
    
def get_place_of_work(message):
    global place_of_work
    place_of_work = message.text
    bot.send_message(message.chat.id, 'Введите вид работ')
    bot.register_next_step_handler(message, get_type_of_work)
    
def get_type_of_work(message):
    global type_of_work
    type_of_work = message.text
    bot.send_message(message.chat.id, 'Введите имена и иницалы работников через запятую (например: Иванов И.И., Петров П.П.)')
    bot.register_next_step_handler(message, get_workers)
    
def get_workers(message):
    global workers
    workers = message.text
    bot.send_message(message.chat.id, 'Введите ФИО ответственного за карту')
    bot.register_next_step_handler(message, get_head_of_workers)

def get_head_of_workers(message):
    global head_of_workers
    head_of_workers = message.text
    bot.send_message(message.chat.id, 'Введите модели и номера техники (например: Ford Focus А123АА999, Toyota Camry В123ВВ998)')
    bot.register_next_step_handler(message, get_cars)

def get_cars(message):
    global cars
    cars = message.text
    bot.send_message(message.chat.id, 'Введите контакты менеджера от codevelopment с которым вы согласовывали работу (например: Сафар, Гарегин, Андрей и т.д.)')
    bot.register_next_step_handler(message, get_curator_contact)
    
def get_curator_contact(message):
    global curator_contact, operation_type, worker_id
    worker_id = message.chat.id
    operation_type = 2
    curator_contact = message.text
    bot.send_message(guard_id, f'''<b>Новая заявка на работы 🏗️</b>
<b>Компания:</b> {company_name}
<b>Дата проведения работ:</b> {date_of_work}
<b>Локация:</b> {place_of_work}
<b>Вид работ:</b> {type_of_work}
<b>Работники:</b> {workers}
<b>Ответственный за карту:</b> {head_of_workers}
<b>Техника:</b> {cars}
<b>Куратор от CODE:</b> {curator_contact}''', parse_mode='html')
    conf_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    cm1 = types.KeyboardButton('Подтвердить')
    cm2 = types.KeyboardButton('Перезаполнить зявку')
    cm3 = types.KeyboardButton("Назад")
    conf_markup.add(cm1, cm2, cm3)
    bot.send_message(message.chat.id, 'Проверьте правильность введенных данных и подтвердите отправку заявки', reply_markup=conf_markup)

def get_company_delivery_name(message):
    global company_name
    company_name = message.text
    bot.send_message(message.chat.id, 'Введите дату доставки (например: 01.01.2021)')
    bot.register_next_step_handler(message, get_delivery_date)

def get_delivery_date(message):
    global delivery_date
    delivery_date = message.text
    bot.send_message(message.chat.id, 'Введите краткий список материалов')
    bot.register_next_step_handler(message, get_list_of_materials)
    
def get_list_of_materials(message):
    global list_of_materials
    list_of_materials = message.text
    bot.send_message(message.chat.id, 'Введите для какого вида работ нужны материалы')
    bot.register_next_step_handler(message, get_which_type_of_work)
    
def get_which_type_of_work(message):
    global which_type_of_work
    which_type_of_work = message.text
    bot.send_message(message.chat.id, 'Введите ФИО ответственного за получении материалов')
    bot.register_next_step_handler(message, get_head_of_workers_del)

def get_head_of_workers_del(message):
    global head_of_workers
    head_of_workers = message.text
    bot.send_message(message.chat.id, 'Введите модели и номера техники (например: Ford Focus А123АА999, Toyota Camry В123ВВ999)')
    bot.register_next_step_handler(message, get_del_cars)
    
def get_del_cars(message):
    global cars, operation_type, delivery_or_work, worker_id
    worker_id = message.chat.id
    cars = message.text
    operation_type = 1
    delivery_or_work = 1
    conf_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    cm1 = types.KeyboardButton('Подтвердить')
    cm2 = types.KeyboardButton('Перезаполнить зявку')
    cm3 = types.KeyboardButton("Назад")
    conf_markup.add(cm1, cm2, cm3)
    bot.send_message(message.chat.id, 'Проверьте правильность введенных данных и подтвердите отправку заявки', reply_markup=conf_markup)
    bot.send_message(message.chat.id, f'''<b>Новая заявка на доставку 📦</b>
<b>Компания:</b> {company_name}
<b>Дата доставки:</b> {delivery_date}
<b>Краткий список материалов:</b> {list_of_materials}
<b>Для какого вида работ нужны материалы:</b> {which_type_of_work}
<b>Ответственный за получение материалов:</b> {head_of_workers}
<b>Техника:</b> {cars}''', parse_mode='html')
    

def write_to_db(message):
    global delivery_or_work, worker_id

    if delivery_or_work == 1:
        delivery_or_work = 'Доставка'
        bot.send_message(guard_id, f'''<b>Новая заявка на доставку 📦</b>
<b>Компания:</b> {company_name}
<b>Дата доставки:</b> {delivery_date}
<b>Краткий список материалов:</b> {list_of_materials}
<b>Для какого вида работ нужны материалы:</b> {which_type_of_work}
<b>Ответственный за получение материалов:</b> {head_of_workers}
<b>Техника:</b> {cars}''', parse_mode='html')
    elif delivery_or_work == 2:
        delivery_or_work = 'Работы'
        sql.execute(f"""CREATE TABLE IF NOT EXISTS requests_for_work_from_{worker_id} (
        request_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        company_name TEXT NOT NULL,
        work_date TEXT NOT NULL,
        place_of_work TEXT NOT NULL,
        type_of_work TEXT NOT NULL,
        workers TEXT NOT NULL,
        head_of_workers TEXT NOT NULL,
        cars TEXT NOT NULL,
        contacts TEXT NOT NULL
        )""")
        db.commit()
        sql.execute(f"INSERT INTO requests_for_work_from_{worker_id} VALUES (?,?,?,?,?,?,?,?,?)", (None, company_name, work_date, place_of_work, type_of_work, workers, head_of_workers, cars, curator_contact))
        db.commit()
        bot.send_message(guard_id, f'''<b>Новая заявка на работы 🏗️</b>
<b>Компания:</b> {company_name}
<b>Дата проведения работ:</b> {date_of_work}
<b>Локация:</b> {place_of_work}
<b>Вид работ:</b> {type_of_work}
<b>Работники:</b> {workers}
<b>Ответственный за карту:</b> {head_of_workers}
<b>Техника:</b> {cars}
<b>Куратор от CODE:</b> {curator_contact}''', parse_mode='html')
    else:
        delivery_or_work = 'Гости'

bot.polling(non_stop=True)