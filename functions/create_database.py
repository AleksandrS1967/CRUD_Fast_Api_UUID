import os
from dotenv import load_dotenv

import psycopg2
from psycopg2 import sql

load_dotenv()


def create_database():
    # Подключение к существующему серверу PostgreSQL без указания базы данных
    conn = psycopg2.connect(
        dbname='postgres',  # соединяемся с базой по умолчанию
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host='localhost'
    )
    conn.autocommit = True  # необходимо для создания базы данных
    cursor = conn.cursor()

    # Создаем базу данных, если она еще не существует
    try:
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(
            sql.Identifier('task_test_new')
        ))
        print("База данных 'task_test_new' успешно создана.")
    except psycopg2.errors.DuplicateDatabase:
        print("База данных 'task_test_new' уже существует.")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    print("Запуск создания базы...")
    create_database()
    print("Завершено.")
