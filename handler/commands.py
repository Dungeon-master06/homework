import asyncio
from aiogram import Router, F, types
from aiogram.types import Message, CallbackQuery, LinkPreviewOptions, FSInputFile
from aiogram.filters import CommandStart, Command
from handler.keyboards import *
from database.querysets import *
from datetime import datetime

import random

router = Router()
anekdot_task = None
stop_event = asyncio.Event()

@router.message(Command("start"))
async def start(message:Message):
    await message.delete()
    await message.answer("Привет как ваши дела?\nЖелаете прочитать анекдот?",
                         reply_markup= await get_yes_no_kb())
    
@router.message(Command('info'))
async def info(message:Message):
    await message.delete()
    link = 'https://www.anekdot.ru/'
    link_preview_options=LinkPreviewOptions(prefer_small_media=True,show_above_text=True)
    await message.answer(f"Тут будет информация о боте
                         \nВсе команды:\n/anekdot30 -(Вкл./Выкл.) Анекдоты каждые 30 минут
                         \n/start - Запуск бота
                         \n/info - Информация о боте
                         \nВсе команды админа:
                         \n/add_anecdot - Добавить новые анекдот
                         \n/add_category - Добавить новую категорию
                         \n/add_anecdot_no_picture - Добавить новый анекдот без картинки
                         \nСсылка на сайт откуда взты анекдоты: {link}",
                         link_preview_options=link_preview_options)
    await message.delete()

@router.message(Command('anekdot30'))
async def anekdot30(message:Message):
    await message.delete()
    await message.answer('Анекдоты каждые 30 минут:',
                         reply_markup= await get_on_off())

@router.callback_query(F.data.startswith('Да'))
async def yes(callback: CallbackQuery):
    await callback.message.answer(f'Выберите категорию:',reply_markup=await get_categories_kb(page=1))
    await callback.answer()
    
@router.callback_query(F.data.startswith('page_'))
async def page(callback: CallbackQuery):
    page = int(callback.data.split('_')[1])
    await callback.message.delete()
    await callback.message.answer(f'Выберите категорию:',reply_markup=await get_categories_kb(page=page))
    await callback.answer()
    
@router.callback_query(F.data.startswith('Нет'))
async def no(callback: CallbackQuery):
    await callback.message.answer('Если передумаете, напишите /start')
    await callback.answer()



@router.callback_query(F.data.startswith('Продукт_'))
async def product(callback: CallbackQuery):
    product_id = callback.data.split('_')[1]
    anekdot = await get_product(product_id)
    if anekdot.image and (anekdot.image.startswith('http') or anekdot.image.startswith('AgAC')):
        image = anekdot.image
    elif anekdot.image:
        image = FSInputFile(anekdot.image)
    else:
        image = None
    if image:
        await callback.message.answer_photo(image, caption=f'Названия:{anekdot.name}\nАнекдот:{anekdot.description}')
    else:
        await callback.message.answer(f'Названия:{anekdot.name}\nАнекдот:{anekdot.description}')
    await callback.answer()

@router.callback_query(F.data.startswith('start_30min'))
async def on(callback: CallbackQuery):
    global anecdote_task
    stop_event.clear()
    await callback.message.answer('Анекдоты будут отправляться каждые 30 минут.')

    async def send_anekdots():
        while not stop_event.is_set():
            await asyncio.sleep(10)
            count = await get_products()
            anekdot = await get_product(random.randint(1, len(count)))
            image = None
            if anekdot.image and (anekdot.image.startswith('http') or anekdot.image.startswith('AgAC')):
                image = anekdot.image
            elif anekdot.image:
                image = FSInputFile(anekdot.image)
            if image:
                await callback.message.answer_photo(image, caption=f'{anekdot.name}\n{anekdot.description}')
            else:
                await callback.message.answer(f'{anekdot.name}\n{anekdot.description}')
    anecdote_task = asyncio.create_task(send_anekdots())
    await callback.answer()

@router.callback_query(F.data.startswith('stop_30min'))
async def off(callback: CallbackQuery):
    global anecdote_task
    stop_event.set()
    if anecdote_task:
        anecdote_task.cancel()
        anecdote_task = None
    await callback.message.answer('Анекдоты каждые 30 минут отключены.')
    await callback.answer()



