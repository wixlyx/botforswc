from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, Message
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database import Db
from visit_make import visitmake

TOKEN = ''

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
db = Db('database.db')


class Send(StatesGroup):
    nexta = State()


class Codewords(StatesGroup):
    words = State()


class Newadmin(StatesGroup):
    admin = State()


class Deleteadmin(StatesGroup):
    username = State()


class Dialog(StatesGroup):
    spam = State()


class Profile(StatesGroup):
    name = State()
    surname = State()
    city = State()
    role = State()
    year = State()
    description = State()
    superpower = State()
    photo = State()


@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message):
    if db.profile_exists(message.from_user.username):
        admin = db.is_admin(message.from_user.username)[0]
        if admin == 1:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(types.InlineKeyboardButton(text="Рассылка"),
                         types.InlineKeyboardButton(text="Задать кодовые слова"),
                         types.InlineKeyboardButton(text="Вывести таблицу лидеров"),
                         types.InlineKeyboardButton(text="Обнулить баллы"),
                         types.InlineKeyboardButton(text="Добавить админа"),
                         types.InlineKeyboardButton(text="Удалить админа"), )
            await message.answer('Добро пожаловать в Админ-Панель! Выберите действие на клавиатуре',
                                 reply_markup=keyboard)
        else:
            menu5 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn_new = KeyboardButton('Заполнить заново')
            menu5.add(btn_new)
            await message.answer('У тебя уже есть визитка', reply_markup=menu5)
    else:
        btn_ru = KeyboardButton('Русский')
        btn_en = KeyboardButton('English')
        menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        menu.add(btn_ru, btn_en)
        await message.answer('Select language', reply_markup=menu)


@dp.message_handler(lambda message: message.text == 'Заполнить заново')
async def redo(message: types.Message):
    db.delete(message.from_user.username)
    await bot_start(message)


@dp.message_handler(lambda message: message.text == 'Русский', state='*')
async def bot_start(message: types.Message):
    await message.answer('👋🏻 Привет, друг Sky World Community. Давай познакомимся?')
    await message.answer('Я Помощник SWC и сейчас я сделаю для тебя визитку партнера.')
    await message.answer('✏️ Напиши свое Имя👇🏻')
    await Profile.name.set()


@dp.message_handler(state=Profile.name)
async def insert_name(message: types.Message, state: FSMContext):
    await state.update_data(profile_name=message.text)
    await message.reply(f'👌🏻 Отлично')
    await message.answer("✏️ Напиши свою фамилию 👇🏻")
    await Profile.next()


@dp.message_handler(state=Profile.surname)
async def insert_surname(message: types.Message, state: FSMContext):
    await state.update_data(profile_surname=message.text)
    await message.reply(f'Отлично')
    await message.answer("✏️ Напиши свою страну и город 👇🏻")
    await Profile.next()


@dp.message_handler(state=Profile.city)
async def insert_city(message: types.Message, state: FSMContext):
    await state.update_data(profile_city=message.text)
    await Profile.next()
    await message.answer('👌🏻 Отлично')
    await message.answer('✏️ Напиши свою роль в сообществе 👇🏻')


@dp.message_handler(state=Profile.role)
async def insert_role(message: types.Message, state: FSMContext):
    if len(message.text) < 121:
        await state.update_data(profile_role=message.text)
        await Profile.next()
    else:
        await message.answer(f'В вашем тексте {len(message.text)} символов! '
                             f'Сократите и напишите ответ текстом (до 120 символов)👇🏻 🧡')
        return
    menu1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_2015 = KeyboardButton('2015')
    btn_2016 = KeyboardButton('2016')
    btn_2017 = KeyboardButton('2017')
    btn_2018 = KeyboardButton('2018')
    btn_2019 = KeyboardButton('2019')
    btn_2020 = KeyboardButton('2020')
    btn_2021 = KeyboardButton('2021')
    btn_2022 = KeyboardButton('2022')
    menu1.add(btn_2015, btn_2016, btn_2017, btn_2018, btn_2019, btn_2020, btn_2021, btn_2022)
    await message.answer('✏️ Выбери, с какого года ты состоишь в сообществе SWC?', reply_markup=menu1)


@dp.message_handler(state=Profile.year)
async def insert_year(message: types.Message, state: FSMContext):
    await state.update_data(profile_year=message.text)
    await Profile.next()
    await message.answer('🔥 Супер!')
    await message.answer('✏️ Расскажи о себе в 3 предложениях')
    await message.answer('(!!️ максимум 120 знаков)👇🏻')


@dp.message_handler(state=Profile.description)
async def insert_description(message: types.Message, state: FSMContext):
    if len(message.text) < 121:
        await state.update_data(profile_description=message.text)
        await Profile.next()
    else:
        await message.answer(f'В вашем тексте {len(message.text)} символов! '
                             f'Сократите и напишите ответ текстом (до 120 символов)👇🏻 🧡')
        return
    await message.answer("✏️ Чем можешь помочь партнёрам по сообществу? Какая твоя суперсила?")
    await message.answer('(!!️ максимум 120 знаков)👇🏻')


@dp.message_handler(state=Profile.superpower)
async def insert_superpower(message: types.Message, state: FSMContext):
    if len(message.text) < 121:
        await state.update_data(profile_superpower=message.text)
        await Profile.next()
    else:
        await message.answer(f'В вашем тексте {len(message.text)} символов! '
                             f'Сократите и напишите ответ текстом (до 120 символов)👇🏻 🧡')
        return
    await message.answer("Пришли свою фотографию 📸")


@dp.message_handler(state=Profile.photo, content_types=['photo'])
async def insert_photo(message: types.Message, state: FSMContext):
    await message.photo[-1].download('photo_user/' + str(message.from_user.id) + '.jpg')
    await Profile.next()
    user_data = await state.get_data()
    db.create_profile(message.from_user.username, str(user_data['profile_name']), str(user_data['profile_surname']),
                      str(user_data['profile_city']), user_data['profile_role'], user_data['profile_year'],
                      str(user_data['profile_description']), str(user_data['profile_superpower']),
                      'photo/' + str(message.from_user.id) + '.jpg', message.from_user.id)
    await message.answer("⏳ Пару секунд, рисую картинку 👨🏻‍🎨")
    await state.finish()
    visitmake(str(message.from_user.id), message.from_user.username, str(user_data['profile_name']),
              str(user_data['profile_surname']),
              str(user_data['profile_city']), user_data['profile_role'], str(user_data['profile_superpower']),
              user_data['profile_year'])
    photo = open('visits/' + str(message.from_user.id) + '_visit' + '.png', 'rb')
    await message.answer('👀 Посмотри, что получилось, все ли верно?')
    await message.answer_photo(photo)
    btn_yes = KeyboardButton('Да, все верно')
    btn_no = KeyboardButton('Нет, заполнить заново')
    menu2 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    menu2.add(btn_yes, btn_no)
    await message.answer('✅ Если тебе нравится картинка, нажми «ДА»👇🏻', reply_markup=menu2)


@dp.message_handler(lambda message: message.text == 'Да, все верно')
async def bot_yes(message: types.Message, state: FSMContext):
    await Send.nexta.set()
    image = open('visits/' + str(message.from_user.id) + '_visit' + '.png', 'rb')
    text = '@' + message.from_user.username + ', Добро пожаловать в SWC 🧡'
    await bot.send_photo(chat_id=-1001168982861, photo=image, caption=text)
    btn_n = KeyboardButton('ДА')
    menu6 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    menu6.add(btn_n)
    await message.answer('Точно?', reply_markup=menu6)


@dp.message_handler(state=Send.nexta)
async def send(message: Message, state: FSMContext):
    image = open('visits/' + str(message.from_user.id) + '_visit' + '.png', 'rb')
    text2 = f'О себе: {(db.get_info(message.from_user.username)[0])[5]}'
    await bot.send_photo(chat_id=-1001597876985, photo=image, caption=text2)
    menu7 = InlineKeyboardMarkup(resize_keyboard=True)
    btn_1 = InlineKeyboardButton('Посмотреть всех партнеров', url='https://t.me/+6ZEqjLuN-000ZTky')
    btn_2 = InlineKeyboardButton('Присоединиться в чат партнеров', url='https://t.me/+to9nZqTJTKhkNWMy')
    menu7.add(btn_1, btn_2)
    await message.answer('😘 Спасибо, теперь мы знакомы! Если захочешь поделиться визиткой в соцсетях, отмечай SWC 🧡', reply_markup=menu7)
    await state.finish()


@dp.message_handler(lambda message: message.text == 'Нет, заполнить заново')
async def bot_no(message: types.Message):
    db.delete(message.from_user.id)
    await bot_start(message)


@dp.message_handler(content_types=['text'], text='Рассылка')
async def spam(message: Message):
    admin = db.is_admin(message.from_user.username)[0]
    if admin == 1:
        await Dialog.spam.set()
        await message.answer('Напиши текст рассылки')
    else:
        await message.answer('Вы не являетесь админом')


@dp.message_handler(state=Dialog.spam)
async def start_spam(message: Message, state: FSMContext):
    spam_base = db.spam()
    for z in range(len(spam_base)):
        await bot.send_message(spam_base[z][0], message.text)
    await message.answer('Рассылка завершена')
    await state.finish()


@dp.message_handler(content_types=['text'], text='Задать кодовые слова')
async def codewords(message: Message):
    admin = db.is_admin(message.from_user.username)[0]
    if admin == 1:
        await Codewords.words.set()
        await message.answer('Напиши слова через запятую, чтобы добавить \n напиши /clear чтобы очистить')
    else:
        await message.answer('Вы не являетесь админом')


@dp.message_handler(commands=['clear'])
async def clear_words(message: types.Message):
    file = open('resources/words.txt', 'r+')
    file.truncate(0)
    file.close()


@dp.message_handler(state=Codewords.words)
async def push_words(message: Message, state: FSMContext):
    file = open('resources/words.txt', 'w', encoding='utf-8')
    file.write(message.text)
    file.close()
    await message.answer('Слова заданы')
    await state.finish()
    await start(message)


@dp.message_handler(lambda message: message.text == 'Вывести таблицу лидеров')
async def bot_lead(message: types.Message):
    admin = db.is_admin(message.from_user.username)[0]
    if admin == 1:
        final = ''
        for i in db.leaders()[::-1]:
            text = f'@{i[0]} набрал(а) {i[1]} баллов \n'
            final += text
        await message.answer('Список Лидеров')
        await message.answer(final)
        btn_t = KeyboardButton('Отправить в канал')
        menu4 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        menu4.add(btn_t)
        await message.answer('Устраивает?', reply_markup=menu4)
    else:
        await message.answer('Вы не админ')
        await start(message)


@dp.message_handler(lambda message: message.text == 'Отправить в канал')
async def bot_lead(message: types.Message):
    final = ''
    for i in db.leaders()[::-1]:
        text = f'@{i[0]} набрал(а) {i[1]} баллов \n'
        final += text
    await bot.send_message(chat_id=-1001685968921, text=final)
    await start(message)


@dp.message_handler(lambda message: message.text == 'Обнулить баллы')
async def bot_null(message: types.Message):
    admin = db.is_admin(message.from_user.username)[0]
    if admin == 1:
        db.null()
        await message.answer('Баллы успешно обнулены')
        await start(message)
    else:
        await message.answer('Вы не админ')
    await start(message)


@dp.message_handler(lambda message: message.text == 'Добавить админа')
async def add_admin(message: types.Message):
    admin = db.is_admin(message.from_user.username)[0]
    if admin == 1:
        await message.answer('Пришли мне ник (без знака @)')
        await Newadmin.admin.set()
    else:
        await message.answer('Вы не админ')


@dp.message_handler(state=Newadmin.admin)
async def add_admin_2(message: Message, state: FSMContext):
    db.add_admin(message.text)
    await message.answer('Админ добавлен')
    await state.finish()
    await start(message)


@dp.message_handler(lambda message: message.text == 'Удалить админа')
async def del_admin(message: types.Message):
    admin = db.is_admin(message.from_user.username)[0]
    if admin == 1:
        await message.answer('Пришли мне ник (без знака @)')
        await Deleteadmin.username.set()
    else:
        await message.answer('Вы не админ')


@dp.message_handler(state=Deleteadmin.username)
async def del_admin_2(message: Message, state: FSMContext):
    db.delete_admin(message.text)
    await message.answer('Админ удален')
    await state.finish()
    await start(message)


@dp.message_handler()
async def word_finder(message: types.Message):
    if db.profile_exists(message.from_user.username) is True:
        file = open('resources/words.txt', 'r', encoding='utf-8')
        word_list = file.read().split(', ')
        mes_words = message.text.split()
        for mes_word in mes_words:
            if mes_word in word_list:
                db.add_point(1, message.from_user.id)
                await message.answer('+1 бал')

        file.close()


executor.start_polling(dp, skip_updates=True)
