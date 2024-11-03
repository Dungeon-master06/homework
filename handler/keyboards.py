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

