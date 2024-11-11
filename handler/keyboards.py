from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.querysets import *


async def get_yes_no_kb():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Да", callback_data="Да"
    ))
    builder.add(InlineKeyboardButton(
        text="Нет", callback_data="Нет"
    ))
    return builder.adjust(2).as_markup()

async def get_categories_kb():
    categories = await get_categories()
    builder = InlineKeyboardBuilder()
    for category in categories:
        builder.add(InlineKeyboardButton(
            text= category.name , callback_data=f'Продукт_{category.id}'
        ))
    return builder.adjust(2).as_markup()

async def get_products_kb(category_id):
    products = await get_category(category_id)
    builder = InlineKeyboardBuilder()
    for product in products:    
        builder.add(InlineKeyboardButton(
            text= product.name , callback_data=f'product_{product.id}'
        ))
    return builder.adjust(2).as_markup()

async def get_anekdot_kb2():
    anekdots = await get_anekdots()
    builder = InlineKeyboardBuilder()
    for anekdot in anekdots:
        builder.add(InlineKeyboardButton(
            text= anekdot.name , callback_data=f'anekdot_{anekdot.id}'
        ))
    return builder.adjust(2).as_markup()

async def get_categories_kb2():
    categories = await get_categories()
    builder = InlineKeyboardBuilder()
    for category in categories:
        builder.add(InlineKeyboardButton(
            text= category.name , callback_data=f'Продукт2_{category.id}'
        ))
    return builder.adjust(2).as_markup()

async def get_on_off():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Вкл", callback_data="start_30min"
    ))
    builder.add(InlineKeyboardButton(
        text="Выкл", callback_data="stop_30min"
    ))
    return builder.adjust(2).as_markup()

async def yes_no_kb(anekdot_id):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Да',callback_data=f'yes_{anekdot_id}'))
    builder.add(InlineKeyboardButton(text='Нет',callback_data=f'no'))
    return builder.adjust(2).as_markup()

async def yes_no_kb2(category_id):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Да',callback_data=f'yes2_{category_id}'))
    builder.add(InlineKeyboardButton(text='Нет',callback_data=f'no2'))
    return builder.adjust(2).as_markup()
