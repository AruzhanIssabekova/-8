import psycopg2
from datetime import datetime
while True:
    user_id = input("Введите ваш id: ")
    if not user_id or not user_id.isnumeric():
        print("Не верные данные")
        continue
    
    with psycopg2.connect(
        dbname = "my_vahta",
        user = "postgres",
        password = "admin",
        host = "localhost",
        port ="5432"
    ) as connect:
        with connect.cursor() as cur:
            cur.execute(f"SELECT * FROM users WHERE user_id = {user_id};")
            user = cur.fetchone()
            if not user:
                print("Пользователь с таким id не существует: ")
                continue
            action = input("Введите 'пришел' или 'ушел': ").strip().lower()
        

        with connect.cursor() as cur:
            if action == 'пришел':
                corrent_time = datetime.now()
                cur.execute(f"""INSERT INTO work_time (user_id, status, time_into) 
                VALUES ({user_id}, true, '{corrent_time}')""")
                print("Время прихода записано")
            elif action == 'ушел':
                corrent_time = datetime.now()
                cur.execute("""SELECT * FROM work_time WHERE user_id = %s AND status = %s ORDER BY time_into DESC LIMIT 1""", (user_id, True))
                s = cur.fetchone()
                if s:
                    cur.execute("""UPDATE work_time SET status = %s, time_out = %s WHERE id = %s""", (False, corrent_time, s[0]))
                    print("Время ухода записано")
                else:
                    print("Нет открытой записи для этого пользователя")
            else:
                print("Неизвестное действие. Введите 'пришел' или 'ушел'")
