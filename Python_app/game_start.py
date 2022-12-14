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
    sql = 'select name, ident from airport where type like %s or type like %s ' \
          'order by rand() limit 1;'
    val = ("small%", "large%")
    cursor.execute(sql, val)
    result = cursor.fetchall()
    for row in result:
        return row


