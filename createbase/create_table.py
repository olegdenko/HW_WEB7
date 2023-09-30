import psycopg2
import configparser
import pathlib

from psycopg2 import Error


file_config = pathlib.Path(__file__).parent.parent.joinpath('config.ini')
config = configparser.ConfigParser()
config.read(file_config)

username = config.get('DB', 'USER')
password = config.get('DB', 'PASSWORD')
database_name = config.get('DB', 'DB_NAME')
domain = config.get('DB', 'DOMAIN')
port = config.get('DB', 'PORT')
url = f'postgresql://{username}:{password}@{domain}:{port}/{database_name}'


def execute_sql_file(filename):
    try:
        connection = psycopg2.connect(
            host=domain,
            database=database_name,
            user=username,
            password=password
        )

        cursor = connection.cursor()

        with open(filename, 'r') as sql_file:
            sql_commands = sql_file.read().split(';')

            for command in sql_commands:
                if command:
                    print(command)
                    cursor.execute(command)

        connection.commit()

    except Error as e:
        print("Помилка при виконанні SQL-запиту:", e)

    finally:
        if connection:
            cursor.close()
            connection.close()


if __name__ == "__main__":
    execute_sql_file("createbase/Create_data_base_postgres_hw_web7.sql")

