import mysql.connector

link = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='flight_game',
    user='root',
    password='dB22',
    autocommit=True
    )

cursor = link.cursor(buffered=True)


def randomcontingent(link):
    sql = 'select name, ident from airport where type like small% or type like large% ' \
          'order by rand() limit 1;'
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        return row


