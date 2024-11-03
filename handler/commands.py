import asyncio
from aiogram import Router, F, types
from aiogram.types import Message, CallbackQuery, LinkPreviewOptions, FSInputFile
from aiogram.filters import CommandStart, Command
from handler.keyboards import *
from database.querysets import *
from datetime import datetime

router = Router()

@router.message(Command("start"))
async def start(message:Message):
    await message.answer("Привет как ваши дела?\nЖелаете прочитать анекдот?",
                         reply_markup= await get_yes_no_kb())
    
@router.message(Command('anekdot30'))
async def anekdot30(message:Message):
    await message.answer('Анекдоты каждые 30 минут:',
                         reply_markup= await get_on_off())

@router.callback_query(F.data.startswith('Да'))
async def yes(callback: CallbackQuery):
    await callback.message.answer(f'Выберите категорию:',reply_markup=await get_categories_kb())
    await callback.answer()
    

@router.callback_query(F.data.startswith('Нет'))
async def no(callback: CallbackQuery):
    await callback.message.answer('Если передумаете, напишите /start')
    await callback.answer()



@router.callback_query(F.data.startswith('Продукт_'))
async def product(callback: CallbackQuery):
    product_id = callback.data.split('_')[1]
    anekdot = await get_product(product_id)
    if anekdot.image.startswith('http') or anekdot.image.startswith('AgAC'):
        image = anekdot.image
    else:
        image = FSInputFile(anekdot.image)
    await callback.message.answer_photo(image, caption=f'{anekdot.name}\n{anekdot.description}')
    await callback.answer()

@router.callback_query(F.data.startswith('start_30min'))
async def on(callback: CallbackQuery):
    
    await callback.message.answer('Анекдоты будут отправляться каждые 30 минут.')
    while True:
        await asyncio.sleep(1)
        anekdot = await get_product(1)
        await callback.message.answer_photo(anekdot.image, caption=f'{anekdot.name}\n{anekdot.description}')
        await callback.answer()
@router.callback_query(F.data.startswith('stop_30min'))
async def off(callback: CallbackQuery):
    await callback.message.answer('Анекдоты каждые 30 минут отключены.')
    await callback.answer()



