from .models import *

from sqlalchemy import select,delete,update

async def get_categories():
    async with async_session() as session:
        result = await session.scalars(select(Category))
        return result
    
async def get_anekdots():
    async with async_session() as session:
        result = await session.scalars(select(Joke))
        return result.all()
    
async def get_category(category_id):
    async with async_session() as session:
        result = await session.scalars(select(Joke).where(Joke.category_id == category_id))
        return result
    
async def get_product(product_id):
    async with async_session() as session:
        result =await session.scalar(select(Joke).where(Joke.id == product_id))
        return result
    
async def add_category(text):
    async with async_session() as session:
        category = Category(name = text)
        session.add(category)
        await session.commit()
        await session.refresh(category)
        return category

async def add_anekdot_db(data):
    async with async_session() as session:
        session.add(data)
        await session.commit()
        await session.refresh(data)
        return data
    
async def add_anekdot_db(data2):
    async with async_session() as session:
        session.add(data2)
        await session.commit()
        await session.refresh(data2)
        return data2


async def delete_category_db(category_id):
    async with async_session() as session:
        await session.execute(delete(Category).where(Category.id == category_id))
        await session.commit()

async def delete_anekdot_db(anekdot_id):
    async with async_session() as session:
        await session.execute(delete(Category).where(Category.id == anekdot_id))
        await session.commit()

    
