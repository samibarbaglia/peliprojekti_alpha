import calculate
import mysql.connector

icaos = calculate.airports

link = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='flight_game',
    user='root',
    password='dB22',
    autocommit=True
    )

cursor = link.cursor(buffered=True)


def main():
    icaos.clear()
    cursor.execute('select max(id) from game')
    sql_id = cursor.fetchone()
    id = str(sql_id[0])
    cursor.execute('select screen_name from game where id = ' + id + '')
    name_get = cursor.fetchone()
    nick = name_get[0]
    cursor.execute(f'select location from game where screen_name = "{nick}"')
    location_req = cursor.fetchone()
    location = location_req[0]
    if location == None:
        location = "EFHK"
    calculate.list_it(location, icaos)
    return icaos
