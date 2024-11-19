import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Publisher(Base):
    __tablename__ = 'publisher'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True)

class Book(Base):
    __tablename__ = 'book'
    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String)
    id_publisher = sa.Column(sa.Integer, sa.ForeignKey('publisher.id'))
    publisher = relationship("Publisher", back_populates="books")

class Shop(Base):
    __tablename__ = 'shop'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True)

class Stock(Base):
    __tablename__ = 'stock'
    id = sa.Column(sa.Integer, primary_key=True)
    id_book = sa.Column(sa.Integer, sa.ForeignKey('book.id'))
    id_shop = sa.Column(sa.Integer, sa.ForeignKey('shop.id'))
    count = sa.Column(sa.Integer)
    book = relationship("Book")
    shop = relationship("Shop")

class Sale(Base):
    __tablename__ = 'sale'
    id = sa.Column(sa.Integer, primary_key=True)
    price = sa.Column(sa.Float)
    date_sale = sa.Column(sa.Date)
    id_stock = sa.Column(sa.Integer, sa.ForeignKey('stock.id'))
    count = sa.Column(sa.Integer)
    stock = relationship("Stock")

Publisher.books = relationship("Book", order_by=Book.id, back_populates="publisher")

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
