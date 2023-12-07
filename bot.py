import telebot
from telebot import types

BOT_TOKEN = '6955520296:AAF6jQdg71O5pOic3vd5Dbja2syQ5lXPWq0'
bot = telebot.TeleBot(BOT_TOKEN)

library = {
    1: {
        'id': 1,
        'title': 'Сияние',
        'genre': 'Ужасы',
        'year': 1977,
        'author': 'Стивен Кинг',
        'preface': '…Проходят годы, десятилетия, но потрясающая история писателя Джека Торранса, его сынишки Дэнни, наделенного необычным даром, и поединка с темными силами, обитающими в роскошном отеле «Оверлук», по-прежнему завораживает и держит в неослабевающем напряжении читателей самого разного возраста…',
        'download_link': 'https://limbook.net/download/b8701ef8-3ae8-4cf3-85e2-1b50db7cdccf/fb2',
    },
    2: {
        'id': 2,
        'title': 'Грозовой перевал',
        'genre': 'Исторические романы',
        'year': 1847,
        'author': 'Эмили Бронте',
        'preface': 'Англия 18 века. Маленький Хитклифф – никому не нужный ребенок, да к тому же еще сильно больной. Владелец поместья под названием «Грозовой перевал» решает взять мальчика к себе и воспитать как своего родного ребенка, несмотря на то, что у него уже есть двое родных детей – дочь Кэтрин и сын Хиндли. Хитклифф вместе с Кэтрин становятся неразлучны. Дети привязаны друг к другу. Спустя годы хозяин дома умирает. Поместье переходит по наследству Хиндли, а Кэтрин отправляют в семью, владеющую Мызой Скворцов, для воспитания и обучения подобающим молодой леди манерам. Судьба Хитклиффа складывается хуже – его отправляют работать, как обычного батрака',
        'download_link': 'https://limbook.net/download/3330c90c-cd28-4fd5-8f77-5957dc009ef8/fb2',
    },
    3:{'id': 3,
        'title': 'ТРИУМФАЛЬНАЯ АРКА',
        'genre': 'Исторические романы',
        'year': 1945,
        'author': 'Эрих Мария Ремарк',
        'preface': 'В произведении "Триумфальная арка" мы увидим немного непривычную нашим представлениям Францию: полуосвещённые, тусклые улицы Парижа, тяжёлое небо со сгустившимися тучами, из которых пробивается вниз косой, непрерывный дождь. Погода будто отображает душевное состояние проживающего тут населения: отчаяние, разбившиеся мечты, неблагополучие, голод и ожидание неизбежной трагедии. Это томление, конец европейского мира, вскоре здесь будут править фашисты и распоряжаться этими местами по своему личному усмотрению, не обращая внимания на потребности других людей.',
        'download_link': 'https://limbook.net/download/fa5dfd8b-5702-423b-b8ed-2d10b80b9a97/fb2',
    },

}


@bot.message_handler(commands=['start'])
def start(message):
    user = message.from_user
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id, f"Привет, {user.first_name}! Я бот библиотеки книг. Напиши /help для получения инструкций.", reply_markup=markup)

@bot.message_handler(commands=['help'])
def help_command(message):
    user = message.from_user
    bot.send_message(message.chat.id, 'Список доступных команд:\n'
                                      '/start - Начать бота\n'
                                      '/genres - Выбрать по жанрам\n'
                                      '/authors - Выбрать по авторам\n'
                                      '/book +id книги" - вывести всю иформацию о книге\n'
                                      '/addbook - Добавить новую книгу (для администраторов)', reply_markup=types.ReplyKeyboardRemove(selective=False))


@bot.message_handler(commands=['genres'])
def genres(message):
    genres_set = set(book['genre'] for book in library.values())
    genres_list = list(genres_set)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    
    markup.add('Назад')
    
    for genre in genres_list:
        markup.add(genre)
    bot.send_message(message.chat.id, 'Выберите жанр книги:', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text != 'Назад' and message.text in [book['genre'] for book in library.values()])
def handle_genre_choice(message):
    genre_choice = message.text
    books_with_genre = [book for book in library.values() if book['genre'] == genre_choice]
    if books_with_genre:
        bot.send_message(message.chat.id, f'Книги в жанре "{genre_choice}":')
        for book in books_with_genre:
            bot.send_message(message.chat.id, f'{book["title"]}\n/id {book["id"]}')
    else:
        bot.send_message(message.chat.id, f'Нет книг в жанре "{genre_choice}".')



@bot.message_handler(commands=['book'])
def book(message):
    user_id = message.from_user.id
    context = message.text.split(' ')[1] if len(message.text.split(' ')) > 1 else None

    if context is not None:
        try:
            book_id = int(context)
            book = library.get(book_id)

            if book:
                book_info = f'Название: {book["title"]}\n'
                book_info += f'Жанр: {book["genre"]}\n'
                book_info += f'Год издания: {book["year"]}\n'
                book_info += f'Автор: {book["author"]}\n'
                book_info += f'Предисловие: {book["preface"]}\n'
                book_info += f'Ссылка на скачивание: {book["download_link"]}\n'

                bot.send_message(message.chat.id, book_info)
            else:
                bot.send_message(message.chat.id, 'Книга с указанным id не найдена.')
        except ValueError:
            bot.send_message(message.chat.id, 'Укажите корректный id книги.')
    else:
        bot.send_message(message.chat.id, 'Укажите id книги.')


@bot.message_handler(commands=['authors'])
def authors(message):
    authors_set = set(book['author'] for book in library.values())
    authors_list = list(authors_set)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

    markup.add('Назад')
    
    for author in authors_list:
        markup.add(author)
    
    bot.send_message(message.chat.id, 'Выберите автора книги:', reply_markup=markup)
    bot.register_next_step_handler(message, handle_author_choice)


def handle_author_choice(message):
    author_choice = message.text
    if author_choice == 'Назад':
        start(message)
        return

    books_by_author = [book for book in library.values() if book['author'] == author_choice]
    
    if books_by_author:
        bot.send_message(message.chat.id, f'Книги, заавторством "{author_choice}":')
        for book in books_by_author:
            bot.send_message(message.chat.id, f'{book["title"]}\n/id {book["id"]}')
    else:
        bot.send_message(message.chat.id, f'Нет книг, заавторством "{author_choice}".')

admin_password = "Qwerty123!"
ADD_BOOK_TITLE, ADD_BOOK_GENRE, ADD_BOOK_YEAR, ADD_BOOK_AUTHOR, ADD_BOOK_PREFACE, ADD_BOOK_LINK = range(6)
@bot.message_handler(commands=['addbook'])
def add_book(message):
    bot.send_message(message.chat.id, 'Введите пароль для добавления книги:')
    bot.register_next_step_handler(message, check_admin_password)

def check_admin_password(message):
    user_id = message.from_user.id
    context = message.text
    
    if context == admin_password:
        bot.send_message(message.chat.id, 'Пароль верный. Введите название книги:')
        bot.register_next_step_handler(message, add_book_title)
    else:
        bot.send_message(message.chat.id, 'Неверный пароль. Добавление книги запрещено.')



# def add_book_title(message):
#     user_id = message.chat.id
#     context = message.text
    




@bot.message_handler(func=lambda message: True)
def unknown(message):
    bot.send_message(message.chat.id, 'Не знаю такой команды. Воспользуйтесь /help для получения инструкций.')


if __name__ == '__main__':
    bot.polling(none_stop=True)