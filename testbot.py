from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db import helldb
from pyqiwip2p import QiwiP2P
import random

fdshfdshfshdf = "https://socweb.net/api/v2?action=services&key=GH6FF9tTDThb5GgbThTQmnJXVRA6XfU3xOWvQS4GGIVVKVnqjU7aFguvnHiq"
BotDB = helldb('hellshopdb.db')
storage = MemoryStorage()
bot = Bot(token="5935502269:AAGXliqwbr4eOKlhHTzjxHQ2VPtkC4MIkck")
dp = Dispatcher(bot, storage=storage)
p2p = QiwiP2P(auth_key='eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6ImxoOGdhbC0wMCIsInVzZXJfaWQiOiI3OTg0MTI3NDc3NSIsInNlY3JldCI6IjEzYjcyMGNhOGFlZDNiZTkxMGFjOWIzYWViMjQ3NzBlM2ZkM2E1Y2NkNTNmYjBjYTE4YzZlN2VmZmZlMjIzOTIifX0=')
# ======================================Админ Часть======================================


@dp.message_handler(commands=['sendall'], state='*')
async def mailing(message: types.Message):
    if message.from_user.id == 934479352:
        text = message.text[9:]
        users = BotDB.get_user()
        for row in users:
            try:
                await bot.send_message(row[0], text)
                if int(row[1]) != 1:
                    BotDB.set_active(row[0], 1)
            except:
                BotDB.set_active(row[0], 0)
    await bot.send_message(message.from_user.id, 'Рассылка успешно отправлена!')


# ======================================Клиентская Часть======================================


@dp.message_handler(commands=['start'], state='*')
async def command_start(message: types.Message, state: FSMContext):
    if not BotDB.user_exists(message.from_user.id):
        BotDB.add_user(message.from_user.id)
    await bot.send_message(message.from_user.id, """👋 <b>Приветствую в Hell Shop.
🛒 Приятных покупок.</b>""", reply_markup=kb_client, parse_mode='html')
    await state.finish()


# Products
@dp.message_handler(Text(equals='🛒 Товары', ignore_case=True), state='*')
async def command_products(message: types.Message, state: FSMContext):
    await message.answer('🛍 <b>Выберите категорию:</b>', reply_markup=om, parse_mode='html')
    await state.finish()


# Telegram
@dp.callback_query_handler(lambda c: c.data == 'tg_premiumkb', state='*')
async def tg_inline_item_menu(callback_query: types.CallbackQuery):
    chat_id = callback_query.from_user.id
    balance = BotDB.user_balance(chat_id)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, text=f"""💳 <b>Баланс:</b> {balance}₽
🏷 <b>Выберите нужный вам товар:</b>""", reply_markup=inline_item_tg(), parse_mode='html')


@dp.callback_query_handler(text='cancel', state='*')
async def cancel_products(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text('🛍 <b>Выберите категорию:</b>', parse_mode='html')
    await callback_query.message.edit_reply_markup(reply_markup=om)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('tg'), state='*')
async def process_callback_tg(callback_query: types.CallbackQuery):
    code = callback_query.data
    res_str = code.replace('tg_', '')
    x = res_str
    products = BotDB.get_item_tg(x)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, text=f"""<b>Покупка товара:</b>
➖➖➖➖➖➖➖➖➖➖➖➖➖
<b>🏷 Название: </b>{products[1]}
<b>🗃 Категория: </b>🌟 {products[2]}
<b>📜 Описание: </b>{products[3]}
<b>💰 Стоимость: </b>{products[4]}₽
<b>📦 Количество: </b>{products[5]} шт""", reply_markup=buy_item_tg(products[0]), parse_mode='html')


@dp.callback_query_handler(text='canceltg', state='*')
async def cancel_products_tg(callback_query: types.CallbackQuery):
    chat_id = callback_query.from_user.id
    balance = BotDB.user_balance(chat_id)
    await callback_query.message.edit_text(f"""💳 <b>Баланс:</b> {balance}₽
🏷 <b>Выберите нужный вам товар:</b>""", parse_mode='html')
    await callback_query.message.edit_reply_markup(reply_markup=inline_item_tg())


# Vpn
@dp.callback_query_handler(lambda c: c.data == 'vpnkb', state='*')
async def vpn_inline_item_menu(callback_query: types.CallbackQuery):
    chat_id = callback_query.from_user.id
    balance = BotDB.user_balance(chat_id)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, text=f"""💳 <b>Баланс:</b> {balance}₽
🏷 <b>Выберите нужный вам товар:</b>""", reply_markup=inline_item_vpn(), parse_mode='html')


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('vpn'), state='*')
async def process_callback_vpn(callback_query: types.CallbackQuery, state: FSMContext):
    code = callback_query.data
    res_str = code.replace('vpn_', '')
    x = res_str
    products = BotDB.get_item_vpn(x)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, text=f"""<b>Покупка товара:</b>
➖➖➖➖➖➖➖➖➖➖➖➖➖
<b>🏷 Название: </b>{products[1]}
<b>🗃 Категория: </b>🩸 {products[2]}
<b>📜 Описание: </b>{products[3]}
<b>💰 Стоимость: </b>{products[4]}₽
<b>📦 Количество: </b>{products[5]} шт""", reply_markup=buy_item_vpn(products[0]), parse_mode='html')
    async with state.proxy() as data:
        data['productsvpn'] = products


@dp.callback_query_handler(text='cancelvpn', state='*')
async def cancel_products_vpn(callback_query: types.CallbackQuery):
    chat_id = callback_query.from_user.id
    balance = BotDB.user_balance(chat_id)
    await callback_query.message.edit_text(f"""💳 <b>Баланс:</b> {balance}₽
🏷 <b>Выберите нужный вам товар:</b>""", parse_mode='html')
    await callback_query.message.edit_reply_markup(reply_markup=inline_item_vpn())


class purchase(StatesGroup):
    input_amount = State()


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('buy_item_vpn'), state='*')
async def purchase_vpn(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        products = data['productsvpn']
    chat_id = callback_query.from_user.id
    balance = BotDB.user_balance(chat_id)
    await bot.send_message(callback_query.from_user.id, f"""<b>Введите количество товаров для покупки.</b>
▶️ От 1 до {products[5]}
➖➖➖➖➖➖➖➖➖➖➖➖➖
🏷 Товар: {products[1]}
💰 Ваш баланс: {balance}₽""", parse_mode='html')
    await state.set_state(purchase.input_amount)


def number(_str):
    try:
        int(_str)
        return True
    except ValueError:
        return False


@dp.message_handler(state=purchase.input_amount)
async def check_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        products = data['productsvpn']
    chat_id = message.from_user.id
    balance = BotDB.user_balance(chat_id)
    productsid = products[0]
    cheque = random.randint(1000000000, 9999999999)
    if number(message.text):
        mes = int(message.text)
        if mes <= products[5]:
            if mes > 0:
                if balance >= mes * products[4]:
                    await bot.send_message(chat_id, f"""✅ <b>Вы успешно купили товар(ы).</b>
➖➖➖➖➖➖➖➖➖➖➖➖➖
📃 Чек: #{cheque}
🏷 Название товара: {products[1]}
📦 Куплено товаров: {mes}
💵 Сумма покупки: {products[4] * mes}₽
👤 Покупатель: @{message.from_user.full_name} ({chat_id})""", parse_mode='html')
                    BotDB.set_item_vpn(productsid, products[5]-mes)
                    BotDB.set_balance(chat_id, balance-(products[4]*mes))
                    await state.finish()
                else:
                    await bot.send_message(chat_id, f"""❌ <b>Недостаточно средств на счете.</b>
➖➖➖➖➖➖➖➖➖➖➖➖➖
🏷 Введите количество товаров для покупки
▶️ От 1 до {products[5]}
➖➖➖➖➖➖➖➖➖➖➖➖➖
🏷 Товар: {products[1]}
💰 Ваш баланс: {balance}₽""", parse_mode='html')
            else:
                await bot.send_message(chat_id, f"""❌ <b>Неверное количество товаров.</b>
➖➖➖➖➖➖➖➖➖➖➖➖➖
🏷 Введите количество товаров для покупки
▶️ От 1 до {products[5]}
➖➖➖➖➖➖➖➖➖➖➖➖➖
🏷 Товар: {products[1]}
💰 Ваш баланс: {balance}₽""", parse_mode='html')
        else:
            await bot.send_message(chat_id, f"""❌ <b>Неверное количество товаров.</b>
➖➖➖➖➖➖➖➖➖➖➖➖➖
🏷 Введите количество товаров для покупки
▶️ От 1 до {products[5]}
➖➖➖➖➖➖➖➖➖➖➖➖➖
🏷 Товар: {products[1]}
💰 Ваш баланс: {balance}₽""", parse_mode='html')
    else:
        await bot.send_message(chat_id, f"""❌ <b>Данные были введены неверно.</b>
➖➖➖➖➖➖➖➖➖➖➖➖➖
🏷 Введите количество товаров для покупки
▶️ От 1 до {products[5]}
➖➖➖➖➖➖➖➖➖➖➖➖➖
🏷 Товар: {products[1]}
💰 Ваш баланс: {balance}₽""", parse_mode='html')


# Profile
@dp.message_handler(Text(equals='👤 Профиль', ignore_case=True), state='*')
async def command_profile(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    balance = BotDB.user_balance(chat_id)
    await message.answer(f"""🔑 <b>ID:</b> {message.from_user.id}
💳 <b>Баланс:</b> {balance}₽""", reply_markup=profile_menu(), parse_mode='html')
    await state.finish()


# Replenishment
class replenishment(StatesGroup):
    entering_amount = State()
    check_payment = State()


@dp.callback_query_handler(text='balance_menu')
async def imput_amount(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, "💰 <b>Введите сумму пополнения</b>", reply_markup=rt_cancel(), parse_mode='html')
    await state.set_state(replenishment.entering_amount)


@dp.callback_query_handler(text='cancelrt', state='*')
async def replenishment_cancel(callback_query: types.CallbackQuery, state: FSMContext):
    chat_id = callback_query.from_user.id
    balance = BotDB.user_balance(chat_id)
    await callback_query.message.edit_text(f"""🔑 <b>ID:</b> {callback_query.from_user.id}
💳 <b>Баланс:</b> {balance}₽""", parse_mode='html')
    await callback_query.message.edit_reply_markup(reply_markup=profile_menu())
    await state.finish()


def is_number(_str):
    try:
        float(_str)
        return True
    except ValueError:
        return False


@dp.message_handler(state=replenishment.entering_amount)
async def replenishment_message(message: types.Message):
    if message.chat.type == "private":
        if is_number(message.text):
            message_balance = float(message.text)
            if message_balance >= 10:
                comment = str(message.from_user.id) + "_" + str(random.randint(1000, 9999))
                bill = p2p.bill(amount=message_balance, lifetime=15, comment=comment)
                BotDB.add_check(message.from_user.id, message_balance, bill.bill_id)
                await bot.send_message(message.from_user.id, f"""<b>Для пополнения баланса перейдите по кнопке и оплатите счет.</b>
                
🔄 После оплаты, нажмите на проверить оплату.""", reply_markup=rt_check(url=bill.pay_url, bill=bill.bill_id), parse_mode='html')
                await replenishment.next()
            else:
                await bot.send_message(message.from_user.id, """❌ <b>Неверная сумма пополнения.</b>
▶️ Cумма не должна быть меньше 10₽.
💰 Введите сумму для пополнения средств.""", parse_mode='html')
        else:
            await bot.send_message(message.from_user.id, """❌ <b>Данные были введены неверно.</b>
💰 Введите сумму для пополнения средств""", parse_mode='html')


@dp.callback_query_handler(text_contains="check_", state=replenishment.check_payment)
async def replenishment_check(callback: types.CallbackQuery, state: FSMContext):
    bill = str(callback.data[6:])
    info = BotDB.get_check(bill)
    if info != False:
        if str(p2p.check(bill_id=bill).status) == "PAID":
            user_balance = BotDB.user_balance(callback.from_user.id)
            bal = float(info[1])
            BotDB.set_balance(callback.from_user.id, user_balance+bal)
            await bot.send_message(callback.from_user.id, "✅ <b>Ваш баланс пополнен!</b>", parse_mode='html')
        else:
            await callback.answer("❌ Счет не оплачен!", show_alert=True)
    else:
        await callback.answer("🚫 Счет не найден!", show_alert=True)
    await state.finish()


# Other
@dp.message_handler(Text(equals='💭 Инфо', ignore_case=True), state='*')
async def command_info(message: types.Message, state: FSMContext):
    await message.answer('❗ <b>Выберите действие:</b>', reply_markup=urlkb, parse_mode='html')
    await state.finish()


@dp.message_handler(Text(equals='📜 Правила', ignore_case=True), state='*')
async def command_rules(message: types.Message, state: FSMContext):
    await message.answer("""<b>1.Правила замены невалидного материала</b>

1.1 Замена возможна в том случае, если:
💔 Отсутствует или неверный пароль к купленному вами аккаунту.
💔 Бот выдал пустую ссылку.
В остальных случаях замены нет!

1.2 Что необходимо для получения услуги замены невалидного материала:
💔 Видеозапись ДО момента покупки и до попытки захода в аккаунт.
💔 Настоятельно рекомендуется проверять материал сразу после покупки.
💔 Гарантийный срок для замены - 20 минут с момента покупки материала в нашем сервисе.

2. <b>Правила и условия работы нашего сервиса.</b>

2.1 Правила работы:
💔 Бесплатно аккаунты не раздаём.
💔 Вернуть, обменять аккаунт, если он вам как-то не подошел, не зашел и прочее - невозможно.
💔 В случае обмана с вашей стороны по невалиду - отказ в возврате средств, сотрудничестве, замене. Итог - блокировка в нашем сервисе.
💔 Администрация сервиса вправе отказать в обслуживании и поддержке клиенту без объяснения причин.
💔 Также сервис не несет ответственность за ваши действия. За баланс и проходимость ваших работ.
💔 Совершая покупку вы автоматически соглашаетесь со ВСЕМИ правилами сервиса.

2.2 Условия работы:

💔 Время обработки одной заявки может составлять весь гарантийный срок аккаунта.
💔 Мы всегда идём на компромисс и помогаем решить возникшие проблемы.
💔 Правила по отдельным товарам написаны в описании категорий.


❗️<b>Незнание правил не освобождает от ответственности❗</b>""", parse_mode="html")
    await state.finish()


@dp.message_handler()
async def invalid_command(message: types.Message):
    await bot.send_message(message.from_user.id, """♦ Неизвестная команда.
▶️Введите /start""")


# ======================================Кнопки======================================

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton('🛒 Товары')
b2 = KeyboardButton('👤 Профиль')
b3 = KeyboardButton('📜 Правила')
b4 = KeyboardButton('💭 Инфо')
kb_client.add(b1).insert(b2).add(b3).insert(b4)

urlkb = InlineKeyboardMarkup(row_width=2)
urlb1 = InlineKeyboardButton(text='⚙ Админ/Реклама', url='https://t.me/smurf00')
urlb2 = InlineKeyboardButton(text='🆘 Тех.поддержка', url='https://t.me/smurf00')
urlb3 = InlineKeyboardButton(text='❤ Все проекты', url='https://t.me/testchathell')
urlkb.add(urlb1).insert(urlb2).add(urlb3)

om = InlineKeyboardMarkup(row_width=2)
om1 = InlineKeyboardButton(text='🌟 Tg Premium', callback_data='tg_premiumkb')
om2 = InlineKeyboardButton(text='🩸 VPN', callback_data='vpnkb')
om3 = InlineKeyboardButton(text='📕 Схемы', callback_data='sxem')
om4 = InlineKeyboardButton(text='✉ Почты', callback_data='mail')
om.add(om1).insert(om2).add(om3).insert(om4)


# Telegram
def inline_item_tg():
    tg = InlineKeyboardMarkup(row_width=1)
    tgitem = BotDB.get_inline_item_tg()
    for products in tgitem:
        btn_text = f'{products[1]} | {products[2]}₽ | {products[3]} шт'
        tg1 = InlineKeyboardButton(text=btn_text, callback_data=f'tg_{products[0]}')
        tg.add(tg1)
    cn = InlineKeyboardButton(text='⬅️ Вернуться ↩', callback_data='cancel')
    tg.add(cn)
    return tg


def buy_item_tg(products):
    buy = InlineKeyboardMarkup(row_width=1)
    buy1 = InlineKeyboardButton(text='💰 Купить', callback_data=f'buy_item_tg{products}')
    cn1 = InlineKeyboardButton(text='⬅️ Вернуться ↩', callback_data='canceltg')
    buy.add(buy1).add(cn1)
    return buy


# Vpn
def inline_item_vpn():
    vpn = InlineKeyboardMarkup(row_width=1)
    vpnitem = BotDB.get_inline_item_vpn()
    for products in vpnitem:
        btn_text = f'{products[1]} | {products[2]}₽ | {products[3]} шт'
        vpn1 = InlineKeyboardButton(text=btn_text, callback_data=f'vpn_{products[0]}')
        vpn.add(vpn1)
    cn = InlineKeyboardButton(text='⬅️ Вернуться ↩', callback_data='cancel')
    vpn.add(cn)
    return vpn


def buy_item_vpn(products):
    buy = InlineKeyboardMarkup(row_width=1)
    buy1 = InlineKeyboardButton(text='💰 Купить', callback_data=f'buy_item_vpn_{products}')
    buy.add(buy1)
    cn1 = InlineKeyboardButton(text='⬅️ Вернуться ↩', callback_data='cancelvpn')
    buy.add(cn1)
    return buy


# Profile
def profile_menu():
    tm = InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
    tm1 = InlineKeyboardButton(text='💰 Пополнить', callback_data='balance_menu')
    tm2 = InlineKeyboardButton(text='🛒 История покупок', callback_data='history')
    tm.add(tm1).insert(tm2)
    return tm


def rt_cancel():
    rt = InlineKeyboardMarkup(row_width=1)
    rt1 = InlineKeyboardButton(text='⬅️ Вернуться ↩', callback_data='cancelrt')
    rt.add(rt1)
    return rt


def rt_check(isUrl=True, url="", bill=""):
    qiwiMenu = InlineKeyboardMarkup(row_width=1)
    if isUrl:
        btnUrlQIWI = InlineKeyboardButton(text="🔷 Перейти к оплате", url=url)
        qiwiMenu.insert(btnUrlQIWI)
    btnCheckQIWI = InlineKeyboardButton(text="🌀 Проверить оплату", callback_data="check_"+bill)
    qiwiMenu.insert(btnCheckQIWI)
    return qiwiMenu


# ======================================Другое======================================


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)