from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,relationship
from sqlalchemy import ForeignKey,String,Integer,DateTime,Text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncAttrs,async_sessionmaker

from config import MYSQL_URL

engine = create_async_engine(MYSQL_URL, echo=True)
async_session = async_sessionmaker(engine)

class Base(DeclarativeBase,AsyncAttrs):
    pass

class Category(Base):
    __tablename__ = 'categorys'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    joke= relationship('Joke',back_populates="category")

class Joke(Base):
    __tablename__ = 'jokes'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    image: Mapped[str] = mapped_column(String(255), nullable=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('categorys.id'))
    category= relationship('Category',back_populates="joke")


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def add_category():
    async with async_session() as session:
        category = Category(name = 'С картинками')
        
        session.add(category)
        await session.commit()
        await session.refresh(category)
        return category
    
async def add_joke():
    async with async_session() as session:
        joke = Joke(
            name='На собрании разработчиков:',
            description='Если вы считаете свою работу никчёмной, вспомните, что где-то в России есть сотрудник, считающий суммарный долг компании Гугл.',
            image='image/zebra.png',
            category_id=1
        )
        session.add(joke)
        await session.commit()
        await session.refresh(joke)
        return joke
    
