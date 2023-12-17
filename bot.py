import telebot
from telebot import types
from docx import Document
import tempfile
import os
from datetime import datetime
from Messages_kz import *
from Messages_ru import *

Token = '6916931629:AAG0EB9xsAgJ5RLS_S3BErGwIhGQnr3pWJQ'
bot = telebot.TeleBot(Token)
CHAT_ID = 950968361
previous_messages = {}
messages = []
user_data = {}
question_stack = {}
user_language = {}
questions1 = {
    'Name_student': 'Введите ваше ФИО:',
    'student_gender': 'Вы студент или студентка?',
    'student_group': 'Введите вашу группу:',
    'date_lesson': 'Введите дату занятия:',
    'prichina': 'Введите причину отсутствия на занятие',
}
questions1_kz = {
    'Name_student': 'Аты-жөніңізді енгізіңіз:',
    'student_gender': 'Сіз студент пе, не студентка ма?',
    'student_group': 'Топты енгізіңіз:',
    'date_lesson': 'Сабақ күнін енгізіңіз:',
    'prichina': 'Сабаққа бармау үшін себепті енгізіңіз:',
}
questions2 = {
    'Student_name': 'ВВедите ваше ФИО',
    'Student_group': 'Введите вашу группу',
    'student_gender': 'Вы студент или студентка?',
    'Diplom_ruk': 'Введите имя дипломного руководителя'
}
questions2_kz = {
    'Student_name': 'Аты-жөніңізді енгізіңіз',
    'Student_group': 'Топты енгізіңіз',
    'student_gender': 'Сіз студент пе, не студентка ма?',
    'Diplom_ruk': 'Дипломды басқарушының атын енгізіңіз',
}
questions3 = {
    'Student_name': 'Введите ваше ФИО',
    "nu": 'Введите номер приказа',
    "day": 'Введите день приказа',
    "mont": 'Введите месяц приказа',
    "year": 'Введите год прикаха',
    "course": 'Введите курс',
    "student_group": 'Введите группу студента',
    "prediavlent": 'Введите кому предьявляется'
}
questions3_kz = {
    'Student_name': 'Аты-жөніңізді енгізіңіз',
    "nu": 'Приказ нөмірін енгізіңіз',
    "day": 'Приказ күнін енгізіңіз',
    "mont": 'Приказ айын енгізіңіз',
    "year": 'Приказ жылын енгізіңіз',
    "course": 'Курсты енгізіңіз',
    "student_group": 'Студентті топты енгізіңіз',
    "prediavlent": 'Кімге көз көрсетілгенді енгізіңіз'
}
questions4 = {
    'Student_name' : 'Введите свое ФИО',
    'stay_place':'Введите ваще место проживание',
    'country': 'Введите страну',
    'Addres_life': 'Введите адресс проживания',
    'Addres_registration': 'Введите адресс регистрации',
    'School_end': 'Введите год окончание учебного заведения',
    'Doc_study': 'У вас аттестат или диплом?',
    'altyn_belgi': 'У вас есть алтын белги или вы закончили с отличием?',
    'Language_otdel': 'Введите на какое языковое отделение хотите',
    'inastr_language': 'Какой иностранный язык изучали',
    'level_of_language': 'Уровень иностранного языка',
    'rezhim_uchebi': 'Какой режим учебы хотите? (очное, дистанционное) ',
    'stepen_akadem': 'На какую академическую степень хотите поступить',
    'fakultet': 'Введите на какой факультет',
    'group_obrazovat_programm': 'Введите группу обрзовательных прорамм(4 значный код и название)',
    'obrazovat_programm': 'Введите образовательную программу',
    'type_obrazovaniya': 'Платное или грантное обучение?',
    'financirovanie': 'Введите вид финансирование',
    'Nomer_certificate': 'Номер сертификата ЕНТ или КТ',
    'nomer_granta': 'Введите номер гранта(в случии отсутствия напишите -)',
    'obshezhitiya': 'Вам нужно общежитие?',
    'phone': 'Ваш номер телефона',
    'Father': 'Введите информацию Отца в ввиде ФИО,телефон,адрес регистрации',
    'Mother': 'Введите информацию Матери в ввиде ФИО,телефон,адрес регистрации',
    'Ligot': 'У вас есть льготы?',

}

month_names_ru = {
    'January': 'января',
    'February': 'февраля',
    'March': 'марта',
    'April': 'апреля',
    'May': 'мая',
    'June': 'июня',
    'July': 'июля',
    'August': 'августа',
    'September': 'сентября',
    'October': 'октября',
    'November': 'ноября',
    'December': 'декабря',
}
month_names_kz = {
    'January': 'қаңтар',
    'February': 'ақпан',
    'March': 'наурыз',
    'April': 'сәуір',
    'May': 'мамыр',
    'June': 'маусым',
    'July': 'шілде',
    'August': 'тамыз',
    'September': 'қыркүйек',
    'October': 'қазан',
    'November': 'қараша',
    'December': 'желтоқсан'
}


def social_info(message):
    instagram_link = "https://www.instagram.com/aliakbarisainov/"
    vk_link = "https://vk.com/isain2000"
    social_media_info = f"Инстаграм: {instagram_link}\nВКонтакте: {vk_link}"
    bot.send_message(message.chat.id, social_media_info)


def send_error_message(chat_id, error_text):
    # Замените это на свою функцию отправки сообщений об ошибке
    bot.send_message(chat_id, f" {error_text}")


def fill_document(template_path, data):
    doc = Document(template_path)

    for key, value in data.items():
        for paragraph in doc.paragraphs:
            if f'{{{key}}}' in paragraph.text:
                paragraph.text = paragraph.text.replace(f'{{{key}}}', str(value))
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    if f'{{{key}}}' in cell.text:
                        cell.text = cell.text.replace(f'{{{key}}}', str(value))

    return doc


def send_document(chat_id, doc):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_file:
        temp_file_name = temp_file.name
        doc.save(temp_file_name)
        temp_file.close()
        with open(temp_file_name, 'rb') as file:
            bot.send_document(chat_id, file)
        os.unlink(temp_file_name)


def ask_next_question(message, user_id, template_path, questions):
    if user_id not in user_data:
        user_data[user_id] = {}

    variables = list(questions.keys())
    current_index = len(user_data[user_id])

    if current_index < len(variables):
        next_variable = variables[current_index]
        question_text = questions[next_variable]
        bot.send_message(message.chat.id, question_text)

        user_data[user_id][next_variable] = None
        import functools
        callback = functools.partial(process_answer, user_id=user_id, variable=next_variable,
                                     template_path=template_path, questions=questions)

        bot.register_next_step_handler(message, callback)
    else:
        generate_and_send_document(message, user_id, template_path, questions)


def process_answer(message, user_id, variable, template_path, questions):
    answer = message.text
    if answer.lower() == '/stop':
        if user_language == 'ru':
            bot.send_message(message.chat.id, "Опрос прерван.")
        else:
            bot.send_message(message.chat.id, "Сауалнама үзілді")
        # Очистить данные пользователя, если опрос прерван
        if user_id in user_data:
            del user_data[user_id]
            if user_language == 'kz':
                send_start_message_kz(message)
            else:
                send_start_message(message)
    else:
        if variable == 'date_lesson':
            current_datetime = datetime.now()
            try:
                # Проверка наличия тире в ответе пользователя
                if '-' in answer:
                    start_date_str, end_date_str = answer.split('-')
                    start_date = datetime.strptime(start_date_str.strip(), '%d.%m.%Y')
                    end_date = datetime.strptime(end_date_str.strip(), '%d.%m.%Y')

                    # Проверка ограничений для начальной даты
                    if start_date.year > current_datetime.year or start_date.year < (current_datetime.year - 1):
                        if user_language == 'ru':
                            raise ValueError("Некорректный год")
                        else:
                            raise ValueError("Дұрыс емес жыл")

                    if start_date.month > 12 or start_date.day > 31:
                        if user_language == 'ru':
                            raise ValueError("Некорректный месяц или день")
                        else:
                            raise ValueError("Ай немесе күн жарамсыз")

                    # Проверка ограничений для конечной даты
                    if end_date.year > current_datetime.year or end_date.year < (current_datetime.year - 1):
                        if user_language == 'ru':
                            raise ValueError("Некорректный год")
                        else:
                            raise ValueError("Дұрыс емес жыл")
                    if end_date.month > 12 or end_date.day > 31:
                        if user_language == 'ru':
                            raise ValueError("Некорректный месяц или день")
                        else:
                            raise ValueError("Ай немесе күн жарамсыз")
                    # Сохранение диапазона дат в нужном формате
                    user_data[user_id][
                        variable] = f"от {start_date.strftime('%d.%m.%Y')} по {end_date.strftime('%d.%m.%Y')}"
                else:
                    # Обработка случая с единственной датой
                    date_obj = datetime.strptime(answer, '%d.%m.%Y')
                    if date_obj.year > current_datetime.year or date_obj.year < (current_datetime.year - 1):
                        if user_language == 'ru':
                            raise ValueError("Некорректный год")
                        else:
                            raise ValueError("Дұрыс емес жыл")

                    if date_obj.month > 12 or date_obj.day > 31:
                        if user_language == 'ru':
                            raise ValueError("Некорректный месяц или день")
                        else:
                            raise ValueError("Ай немесе күн жарамсыз")
                    user_data[user_id][variable] = date_obj.strftime('%d.%m.%Y')

                ask_next_question(message, user_id, template_path, questions)
            except ValueError:
                if user_language == 'ru':
                    send_error_message(message.chat.id,
                                       'Некорректные даты. Пожалуйста, введите даты в формате DD.MM.YYYY и убедитесь в правильности значений.')
                else:
                    send_error_message(message.chat.id,
                                       'Дұрыс емес күндер. Күндерді DD.MM.YYYY форматында енгізіп, мәндердің дұрыстығына көз жеткізіңіз.'
                                       '')
                # Запросить дату заново
                bot.send_message(message.chat.id, questions[variable])
                bot.register_next_step_handler(message, process_answer, user_id=user_id, variable=variable,
                                               template_path=template_path, questions=questions)
        elif variable == 'student_gender':
            gender_lower = answer.lower()
            if 'студент' in gender_lower or 'студентка' in gender_lower:
                user_data[user_id][variable] = answer
                ask_next_question(message, user_id, template_path, questions)
            else:
                if user_language == 'ru':
                    send_error_message(message.chat.id,
                                       'Некорректное значение для пола. Введите "студент" или "студентка" в правильной форме.')
                    # Начать опрос заново
                    bot.send_message(message.chat.id, questions[variable])
                    bot.register_next_step_handler(message, process_answer, user_id=user_id, variable=variable,
                                                   template_path=template_path, questions=questions)
                else:
                    send_error_message(message.chat.id,
                                       'Мән жарамсыз. Дұрыс пішінге «студент» немесе «студент» енгізіңіз.')
                    # Начать опрос заново
                    bot.send_message(message.chat.id, questions[variable])
                    bot.register_next_step_handler(message, process_answer, user_id=user_id, variable=variable,
                                                   template_path=template_path, questions=questions)
        else:
            user_data[user_id][variable] = answer
            ask_next_question(message, user_id, template_path, questions)


def generate_and_send_document(message, user_id, template_path, questions):
    if user_id in user_data:
        document_data = user_data[user_id]

        # Автоматическое заполнение 'student_gender_type' на основе ответа пользователя
        if 'student_gender' in document_data and document_data['student_gender']:
            if 'студент' in document_data['student_gender'].lower():
                user_data[user_id]['student_gender_type'] = 'отсутствовал'
                user_data[user_id]['Student_gender_Type'] = 'студента'
            else:
                user_data[user_id]['student_gender_type'] = 'отсутствовала'
                user_data[user_id]['Student_gender_Type'] = 'студентки'

        # Автоматическое заполнение 'Date_create'
        current_datetime = datetime.now()
        document_data['Date_create'] = current_datetime.strftime(
            f'%d {month_names_ru[current_datetime.strftime("%B")]} %Y')

        filled_document = fill_document(template_path, document_data)
        send_document(message.chat.id, filled_document)
        del user_data[user_id]


document_path = 'Docs/Courts/o_priznanii_grazhdanina_nedeesposobnym.docx'
document_path1 = 'Docs/Courts/o_vozmeshchenii_ushcherba_dtp.docx'
document_path2 = 'Docs/Courts/ob_ustanovlenii_fakta_smerti_grazhdanina.docx'


def send_document_asc(chat_id):
    try:
        # Отправка документа с использованием метода send_document
        with open(document_path, 'rb') as document:
            bot.send_document(chat_id, document)
    except Exception as e:
        # Обработка возможных ошибок
        print(f"Ошибка при отправке документа: {e}")


def send_document_acs(chat_id):
    try:
        # Отправка документа с использованием метода send_document
        with open(document_path1, 'rb') as document:
            bot.send_document(chat_id, document)
    except Exception as e:
        # Обработка возможных ошибок
        print(f"Ошибка при отправке документа: {e}")


def send_document_abs(chat_id):
    try:
        # Отправка документа с использованием метода send_document
        with open(document_path2, 'rb') as document:
            bot.send_document(chat_id, document)
    except Exception as e:
        # Обработка возможных ошибок
        print(f"Ошибка при отправке документа: {e}")


def send_start_message(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item2 = types.InlineKeyboardButton("Колледж", callback_data='college')
    item3 = types.InlineKeyboardButton("Правохранительные органы", callback_data='courts')
    markup.add(item2, item3)
    sent_message = bot.send_message(message.chat.id, "Выберите образец который хотите получить", reply_markup=markup)
    # Сохраняем только текущее сообщение пользователя в списке
    previous_messages[message.chat.id] = [sent_message.message_id]


def send_start_message_kz(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item2 = types.InlineKeyboardButton("Колледж", callback_data='college')
    item3 = types.InlineKeyboardButton("Құқықты қауіпсіздік орталықтар", callback_data='courts')
    markup.add(item2, item3)
    sent_message = bot.send_message(message.chat.id, "Образецті таңдау", reply_markup=markup)
    # Сохраняем только текущее сообщение пользователя в списке
    previous_messages[message.chat.id] = [sent_message.message_id]


def language_set(message):
    language_markup = types.InlineKeyboardMarkup(row_width=3)
    item1 = types.InlineKeyboardButton("kz Казахский", callback_data='kz')
    item2 = types.InlineKeyboardButton("ru Русский", callback_data='ru')
    language_markup.add(item1, item2)
    sent_message = bot.send_message(message.chat.id, "Выберите язык", reply_markup=language_markup)


@bot.message_handler(commands=['start'])
def start_message(message):
    language_set(message)


@bot.message_handler(commands=['language'])
def language_pick(message):
    language_set(message)


@bot.message_handler(commands=['info'])
def info(message):
    if user_language == 'kz':
        user_language[message.chat.id] = 'kz'
        bot.send_message(message.chat.id, f"Сіз тілді таңдағаныз:Казахский")
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, start_kz)
        social_info(message)
        bot.send_message(message.chat.id, 'Бастау үшін Құжаттар деп жазыныз')
        bot.send_message(message.chat.id, 'Тіл ауыстыру үшін /language деп жазыныз')


    elif user_language == 'ru':
        user_language[message.chat.id] = 'ru'
        bot.send_message(message.chat.id, f"Вы выбрали язык:Русский")
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, start_ru)
        social_info(message)
        bot.send_message(message.chat.id, 'Для начала напишите Документы')
        bot.send_message(message.chat.id, 'Для смены языка напишите команду /language')
    else:
        bot.send_message(message.chat.id,
                         'Вы не выбрали язык, пожалуйста выберите язык. Для выбора языка напишите /start и выберите ваш язык')
        bot.send_message(message.chat.id,
                         'Сіз тілді таңдауды алмадыңыз, өтініш тілді таңдаңыз. Тілді тандау үшін /start жазып өзініздің тіліңізді танданыз ')


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text.lower() == 'документы' or message.text.upper == 'Документы':
        send_start_message(message)
    elif message.text.lower() == 'құжаттар' or message.text.upper() == 'Құжаттар':
        send_start_message_kz(message)
    elif not user_language:
        bot.send_message(message.chat.id,
                         'Вы не выбрали язык, пожалуйста выберите язык. Для выбора языка напишите /start и выберите ваш язык')
        bot.send_message(message.chat.id,
                         'Сіз тілді таңдауды алмадыңыз, өтініш тілді таңдаңыз. Тілді тандау үшін /start жазып өзініздің тіліңізді танданыз ')
    else:
        bot.send_message(message.chat.id, "Дұрыс емес болмаған команда. Мәлімет алу үшін /info жазыңыз.")
        bot.send_message(message.chat.id, "Неправильная команда. Напишите /info для получения информации.")


@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    user_id = call.from_user.id
    if call.message.chat.id in previous_messages:
        for msg_id in previous_messages[call.message.chat.id]:
            bot.delete_message(call.message.chat.id, msg_id)
        previous_messages[call.message.chat.id] = []

    if call.data == 'kz':
        user_language[call.message.chat.id] = 'kz'
        bot.send_message(call.message.chat.id, f"Сіз тілді таңдағаныз:Казахский")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, start_kz)
        social_info(call.message)
        bot.send_message(call.message.chat.id, 'Бастау үшін Құжаттар деп жазыныз')

    elif call.data == 'ru':
        user_language[call.message.chat.id] = 'ru'
        bot.send_message(call.message.chat.id, f"Вы выбрали язык:Русский")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, start_ru)
        social_info(call.message)
        bot.send_message(call.message.chat.id, 'Для начала напишите Документы')

    if call.data == 'college_button1':
        if user_language == 'ru':
            bot.send_message(call.message.chat.id, "Начнем опрос. Ответьте на следующие вопросы:")
            user_data[user_id] = {}
            ask_next_question(call.message, user_id, template_path='PHOTOS/College/Обьяснительная.docx',
                              questions=questions1)
        else:
            bot.send_message(call.message.chat.id, "Сауалнаманы бастау. Алдағы сұрауларға жауап беріңіз")
            user_data[user_id] = {}
            ask_next_question(call.message, user_id, template_path='PHOTOS/College/Обьяснительная.docx',
                              questions=questions1_kz)
    elif call.data == 'college_button2':
        if user_language == 'ru':
            bot.send_message(call.message.chat.id, "Начнем опрос. Ответьте на следующие вопросы:")
            user_data[user_id] = {}
            ask_next_question(call.message, user_id, template_path='PHOTOS/College/Заявление.docx',
                              questions=questions2)
        else:
            bot.send_message(call.message.chat.id, "Сауалнаманы бастау. Алдағы сұрауларға жауап беріңіз")
            user_data[user_id] = {}
            ask_next_question(call.message, user_id, template_path='PHOTOS/College/Заявление.docx',
                              questions=questions2_kz)
    elif call.data == 'college_button3':
        if user_language == 'ru':
            bot.send_message(call.message.chat.id, "Начнем опрос. Ответьте на следующие вопросы:")
            user_data[user_id] = {}
            ask_next_question(call.message, user_id, template_path='PHOTOS/College/СПРАВКА.docx', questions=questions3)
        else:
            bot.send_message(call.message.chat.id, "Сауалнаманы бастау. Алдағы сұрауларға жауап беріңіз")
            user_data[user_id] = {}
            ask_next_question(call.message, user_id, template_path='PHOTOS/College/СПРАВКА.docx',
                              questions=questions3_kz)
    if call.data == 'college':
        if user_language == 'ru':
            markup1 = types.InlineKeyboardMarkup(row_width=2)
            item2_1 = types.InlineKeyboardButton("Объяснительная", callback_data='college_button1')
            item2_2 = types.InlineKeyboardButton("Заявления на дипломного руководителя ",
                                                 callback_data='college_button2')
            item2_3 = types.InlineKeyboardButton("Справка", callback_data='college_button3')
            item2_4 = types.InlineKeyboardButton("Назад", callback_data='college_back_button')
            markup1.add(item2_1, item2_2, item2_3, item2_4)
            sent_message = bot.send_message(chat_id=call.message.chat.id, text="Выберите документ",
                                            reply_markup=markup1)
            previous_messages[call.message.chat.id] = [sent_message.message_id]
        else:
            markup1 = types.InlineKeyboardMarkup(row_width=2)
            item2_1 = types.InlineKeyboardButton("Түсіндіруші хат", callback_data='college_button1')
            item2_2 = types.InlineKeyboardButton("Дипломды басқарушыға өтініштер ",
                                                 callback_data='college_button2')
            item2_3 = types.InlineKeyboardButton("Сұрау", callback_data='college_button3')
            item2_4 = types.InlineKeyboardButton("Кері қайту", callback_data='college_back_button')
            markup1.add(item2_1, item2_2, item2_3, item2_4)
            sent_message = bot.send_message(chat_id=call.message.chat.id, text="Құжатты таңдау",
                                            reply_markup=markup1)
            previous_messages[call.message.chat.id] = [sent_message.message_id]
    elif call.data == 'college_back_button':
        if user_language == 'kz':
            send_start_message_kz(call.message)
        else:
            send_start_message(call.message)
    if call.data == 'courts':
        if user_language == 'ru':
            markup1 = types.InlineKeyboardMarkup(row_width=2)
            item3_1 = types.InlineKeyboardButton("Признание гражданина недееспособным", callback_data='courts_button1')
            item3_2 = types.InlineKeyboardButton("О возмещение ущерба дтп", callback_data='courts_button2')
            item3_3 = types.InlineKeyboardButton("Об установление факта смерти", callback_data='courts_button3')
            item3_4 = types.InlineKeyboardButton("Назад", callback_data='courts_back_button')
            markup1.add(item3_1, item3_2, item3_3, item3_4)
            sent_message = bot.send_message(chat_id=call.message.chat.id, text="Выберите документ",
                                            reply_markup=markup1)
            # Сохраняем только текущее сообщение пользователя в списке
            previous_messages[call.message.chat.id] = [sent_message.message_id]
        else:
            markup1 = types.InlineKeyboardMarkup(row_width=2)
            item3_1 = types.InlineKeyboardButton("Гражданын елестік емес деп тану", callback_data='courts_button1')
            item3_2 = types.InlineKeyboardButton("Автошаға туынды дамуды компенсациялау",
                                                 callback_data='courts_button2')
            item3_3 = types.InlineKeyboardButton("Құжатты таңдау", callback_data='courts_button3')
            item3_4 = types.InlineKeyboardButton("Кері қайту", callback_data='courts_back_button')
            markup1.add(item3_1, item3_2, item3_3, item3_4)
            sent_message = bot.send_message(chat_id=call.message.chat.id, text="Құжатты таңдау",
                                            reply_markup=markup1)
            # Сохраняем только текущее сообщение пользователя в списке
            previous_messages[call.message.chat.id] = [sent_message.message_id]
    elif call.data == 'courts_back_button':
        if user_language == 'kz':
            send_start_message_kz(call.message)
        else:
            send_start_message(call.message)
    if call.data == 'courts_button1':
        send_document_asc(user_id)
    if call.data == 'courts_button2':
        send_document_acs(user_id)
    if call.data == 'courts_button3':
        send_document_abs(user_id)
    # Эта строка запускает бота и начинает прослушивание сообщений


bot.polling(none_stop=True, timeout=123)
