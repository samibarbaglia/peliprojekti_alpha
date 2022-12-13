from geopy import distance
import mysql.connector

airports = []

link = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='flight_game',
    user='root',
    password='dB22',
    autocommit=True
    )

cursor = link.cursor(buffered=True)


def list_it(locale, listit):
    cursor.execute('select screen_name, planetype from game where id in (select max(id) from game)')
    response = cursor.fetchone()
    nick = response[0]
    plane = response[1]

    get1 = 'select latitude_deg, longitude_deg from airport where ident ="' + locale + '"'
    cursor.execute(get1)

    reply = cursor.fetchall()
    loc1 = ''

    cursor.execute('select max_distance from planetype where type = "' + plane + '"')
    get2 = cursor.fetchall()
    dist = get2[0]

    for line in reply:
        loc1 = line

    cursor.execute('select ident, latitude_deg, longitude_deg from airport, planetype where airport.type like "' + plane + '%" \
              and planetype.type = "' + plane + '" ORDER BY latitude_deg DESC, longitude_deg')

    reply2 = cursor.fetchall()

    for nextone in reply2:
        loc2 = (nextone[1], nextone[2])
        gap = distance.distance(loc1, loc2)

        if gap <= dist[0]:
            listit.append(nextone[0])