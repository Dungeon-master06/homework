from .models import *

from sqlalchemy import select,delete,update

async def get_categories():
    async with async_session() as session:
        result = await session.scalars(select(Category))
        return result
    
async def get_products():
    async with async_session() as session:
        result = await session.scalars(select(Product))
        return result
    
async def get_category(category_id):
    async with async_session() as session:
        result = await session.scalars(select(Product).where(Product.category_id == category_id))
        return result
    

async def get_product(product_id):
    async with async_session() as session:
        result =await session.scalar(select(Product).where(Product.id == product_id))
        return result
async def add_category(text):
    async with async_session() as session:
        category = Category(name = text)
        session.add(category)
        await session.commit()
        await session.refresh(category)
        return category

async def add_product_db(data):
    async with async_session() as session:
        session.add(data)
        await session.commit()
        await session.refresh(data)
        return data
    


    
