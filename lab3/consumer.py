from kafka import KafkaConsumer
import json
import psycopg2
from psycopg2 import sql

consumer = KafkaConsumer(
    "db_topic",
    bootstrap_servers="localhost:9092",
    group_id="db_consumer_v1",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

DB_CONFIG = {
    "dbname": "db_diana",
    "user": "db_user_diana",
    "password": "",
    "host": "",
    "port": 5432
}

conn = psycopg2.connect(**DB_CONFIG)
conn.autocommit = True
cursor = conn.cursor()


def create_table_if_not_exists(table_name, columns):
    columns_sql = ", ".join([f"{col} TEXT" for col in columns])

    query = sql.SQL("""
        CREATE TABLE IF NOT EXISTS {} (
            {}
        );
    """).format(
        sql.Identifier(table_name),
        sql.SQL(columns_sql)
    )

    cursor.execute(query)

def insert_data(table_name, data):
    columns = data[0].keys()

    insert_query = sql.SQL("""
        INSERT INTO {} ({}) VALUES ({})
    """).format(
        sql.Identifier(table_name),
        sql.SQL(", ").join(map(sql.Identifier, columns)),
        sql.SQL(", ").join(sql.Placeholder() * len(columns))
    )

    for row in data:
        cursor.execute(insert_query, list(row.values()))


print("Consumer запущен и ждёт сообщения...")

for message in consumer:
    try:
        payload = message.value

        table = payload["table"]
        data = payload["data"]

        if not data:
            print("Пустые данные — пропуск")
            continue

        columns = data[0].keys()

        create_table_if_not_exists(table, columns)
        insert_data(table, data)

        print(f"Данные успешно записаны в таблицу '{table}'")

    except Exception as e:
        print("Ошибка при обработке сообщения:", e)