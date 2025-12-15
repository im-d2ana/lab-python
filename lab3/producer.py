from kafka import KafkaProducer
import json
import os

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def read_json(filename):
    with open(filename, encoding='utf-8') as file:
        return json.load(file)

def console_input():
    table_name = input("Введите название таблицы: ").strip()
    columns = input("Введите название столбцов (через запятую): ").strip().split(",")
    n = int(input("Сколько строк данных хотите ввести? "))
    data = []

    for i in range(n):
        row = {}
        for col in columns:
            row[col.strip()] = input(f"Введите значение для '{col.strip()}': ")
        data.append(row)

    return table_name, data

def validator(data):
    if not data:
        return False, "Данные пусты"

    keys = set(data[0].keys())
    for row in data:
        if set(row.keys()) != keys:
            return False, "Столбцы данных не совпадают между строками"

    return True, ""

def send_data(topic, data):
    producer.send(topic, value=data)
    producer.flush()

def main():
    while True:
        choice = input("\nВыберите: 'json', 'console', 'exit': ").strip()

        if choice == 'exit':
            break

        elif choice == 'json':
            file = input("Введите название файла: ").strip()
            if not os.path.exists(file):
                print("Файл не найден")
                continue

            table_name = input("Введите название таблицы: ").strip()
            data = read_json(file)

        elif choice == 'console':
            table_name, data = console_input()

        else:
            print("Неверный формат")
            continue

        valid, ans = validator(data)
        if not valid:
            print(f"Ошибка в данных: {ans}")
            continue

        message = {
            "table": table_name,
            "data": data
        }

        send_data("db_topic", message)
        print(f"Данные для таблицы '{table_name}' отправлены")

if __name__ == "__main__":
    main()
