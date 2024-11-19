import sys
sys.stdout.reconfigure(encoding='utf-8')
import sqlalchemy
import json
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Stock, Shop, Sale


def create_connection(sqlsystem, login, password, host, port, db_name):
    try:
        engine = sqlalchemy.create_engine(f'{sqlsystem}://{login}:{password}@{host}:{port}/{db_name}')
        print('Соединение установлено')
        return engine
    except Exception as e:
        print(f'Ошибка подключения: {e}')
        return None


def load_data(session, json_file):
    with open(json_file, 'rt') as f:
        data = json.load(f)

    for line in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[line.get('model')]
        session.add(model(id=line.get('pk'), **line.get('fields')))
    session.commit()
    print("Данные загружены в базу")


def sale_list(session, search):
    if search.isnumeric():
        results = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale) \
            .join(Publisher, Publisher.id == Book.id_publisher) \
            .join(Stock, Stock.id_book == Book.id) \
            .join(Shop, Shop.id == Stock.id_shop) \
            .join(Sale, Sale.id_stock == Stock.id) \
            .filter(Publisher.id == search).all()
    else:
        results = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale) \
            .join(Publisher, Publisher.id == Book.id_publisher) \
            .join(Stock, Stock.id_book == Book.id) \
            .join(Shop, Shop.id == Stock.id_shop) \
            .join(Sale, Sale.id_stock == Stock.id) \
            .filter(Publisher.name == search).all()
    
    if results:
        for book, shop, price, date in results:
            print(f'{book: <40} | {shop: <10} | {price: <10} | {date}')
    else:
        print("Нет данных для заданного запроса.")


if __name__ == '__main__':
    # Подключение к базе данных
    engine = create_connection('postgresql', 'postgres', 'postgres', 'localhost', 5432, 'Homework_last_bd')
    if engine is None:
        exit("Не удалось подключиться к базе данных.")
    
    Session = sessionmaker(bind=engine)
    session = Session()

    # Создание таблиц
    create_tables(engine)

    # Загрузка данных
    load_data(session, 'tests_data.json')

    # Запрос и вывод результатов
    search_input = input('Введите идентификатор или имя автора: ')
    sale_list(session, search_input)

    # Закрытие сессии
    session.close()
