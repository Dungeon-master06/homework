from aiogram import Router,F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from database.querysets import *
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from handler.keyboards import *

admin_router = Router()

class AddCategory(StatesGroup):
    name = State()

@admin_router.message(Command('add_category'))
async def add_category_admin(message: Message, state: FSMContext):
    await message.answer('Введите название категории')
    await state.set_state(AddCategory.name)


@admin_router.message(AddCategory.name)
async def add_category_name(message: Message, state: FSMContext):
    await add_category(message.text)
    await message.delete()
    await message.answer('Категория добавлена')
    await state.clear()

class AddAnektod(StatesGroup):
    name = State()
    description = State()
    image = State()
    category = State()

@admin_router.message(Command('add_anekdot'))
async def add_anekdot_admin(message: Message, state: FSMContext):
    await message.answer('Введите название анекдота')
    await state.set_state(AddAnektod.name)

@admin_router.message(AddAnektod.name)
async def add_anekdot_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Введите анекдот')
    await state.set_state(AddAnektod.description)

@admin_router.message(AddAnektod.description)
async def add_anekdot_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer('Вберите картинку')
    await state.set_state(AddAnektod.image)

@admin_router.message(AddAnektod.image)
async def add_anekdot_image(message: Message, state: FSMContext):
    await state.update_data(image=message.photo[0].file_id)
    await message.answer('Выберите категорию', reply_markup=await get_categories_kb2())
    await state.set_state(AddAnektod.category)

@admin_router.callback_query(AddAnektod.category)
async def add_anekdot_category(callback: CallbackQuery, state: FSMContext):
    await state.update_data(category=callback.data.split('_')[1])
    data = await state.get_data()
    anekdot = Joke(
        name=data['name'],
        description=data['description'],
        image=data['image'],
        category_id=data['category']
    )
    await add_anekdot_db(anekdot)
    await callback.message.answer('Анекдот добавлен')
    await state.clear()

class AddNoPictureAnecdot(StatesGroup):
    name = State()
    description = State()
    category = State()

@admin_router.message(Command('add_anekdot_no_picture'))
async def add_anekdot_admin(message: Message, state: FSMContext):
    await message.answer('Введите название анекдота')
    await state.set_state(AddNoPictureAnecdot.name)

@admin_router.message(AddNoPictureAnecdot.name)
async def aadd_anekdot_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Введите анекдот')
    await state.set_state(AddNoPictureAnecdot.description)

@admin_router.message(AddNoPictureAnecdot.description)
async def add_anekdot_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer('Выберите категорию', reply_markup=await get_categories_kb2())
    await state.set_state(AddNoPictureAnecdot.category)

@admin_router.callback_query(AddNoPictureAnecdot.category)
async def add_anekdot_category(callback: CallbackQuery, state: FSMContext):
    await state.update_data(category=callback.data.split('_')[1])
    data2 = await state.get_data()
    anekdot_no_picture = Joke(
        name=data2['name'],
        description=data2['description'],
        category_id=data2['category']
    )
    await add_anekdot_db(anekdot_no_picture)
    await callback.message.answer('Анекдот добавлен')
    await state.clear()


@admin_router.message(Command('delete_category'))
async def delete_category(message: Message):
    await message.answer('Выберите категорию для удаления:', reply_markup= await get_categories_kb2())

@admin_router.callback_query(F.data.startswith('Продукт2_'))
async def delete_category_callback(callback: CallbackQuery):
    category_id = callback.data.split('_')[1]
    await callback.message.answer(f'Вы действительно хотите удалить?\nПРЕДУПРЕЖДАЕМ! ЧТО УДАЛЬЯ КАТЕГОРИЮ, ВСЕ АНЕКДОТЫ ТОЖЕ БУДУТ УДАЛЕНЫ', reply_markup= await yes_no_kb2(category_id))

@admin_router.callback_query(F.data.startswith('yes2_'))
async def delete_category_callback(callback: CallbackQuery):
    category_id = callback.data.split('_')[1]
    await delete_category_db(category_id)
    await callback.message.answer('Категория удалена')

@admin_router.callback_query(F.data.startswith('no2'))
async def delete_food_callback(callback: CallbackQuery):
    await callback.message.delete()


@admin_router.message(Command('delete_anekdot'))
async def delete_food(message: Message):
    await message.answer('Выберите анекдот для удаления:', reply_markup= await get_anekdot_kb2())

@admin_router.callback_query(F.data.startswith('anekdot_'))
async def delete_food_callback(callback: CallbackQuery):
    food_id = callback.data.split('_')[1]
    await callback.message.answer(f"Вы действительно хотите удалить это анекдот?", reply_markup= await yes_no_kb(food_id))

@admin_router.callback_query(F.data.startswith('yes_'))
async def delete_food_callback(callback: CallbackQuery):
    food_id = callback.data.split('_')[1]
    await delete_anekdot_db(food_id)
    await callback.message.answer('анекдот удалено')

@admin_router.callback_query(F.data.startswith('no'))
async def delete_food_callback(callback: CallbackQuery):
    await callback.message.delete()