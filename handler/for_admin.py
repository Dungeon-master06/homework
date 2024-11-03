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
    await message.answer('Категория добавлена')
    await state.clear()

class AddProduct(StatesGroup):
    name = State()
    description = State()
    image = State()
    category = State()

@admin_router.message(Command('add_product'))
async def add_product_admin(message: Message, state: FSMContext):
    await message.answer('Введите название анекдота')
    await state.set_state(AddProduct.name)

@admin_router.message(AddProduct.name)
async def add_product_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Введите анекдот')
    await state.set_state(AddProduct.description)

@admin_router.message(AddProduct.description)
async def add_product_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer('Вберите картинку')
    await state.set_state(AddProduct.image)

@admin_router.message(AddProduct.image)
async def add_product_image(message: Message, state: FSMContext):
    await state.update_data(image=message.photo[0].file_id)
    await message.answer('Выберите категорию', reply_markup=await get_categories_kb2())
    await state.set_state(AddProduct.category)

@admin_router.callback_query(AddProduct.category)
async def add_product_category(callback: CallbackQuery, state: FSMContext):
    await state.update_data(category=callback.data.split('_')[1])
    data = await state.get_data()
    product = Product(
        name=data['name'],
        description=data['description'],
        image=data['image'],
        category_id=data['category']
    )
    await add_product_db(product)
    await callback.message.answer('Анекдот добавлен')
    await state.clear()
