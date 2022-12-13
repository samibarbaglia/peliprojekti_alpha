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
    sql = 'select name, ident from airport where type like "small%" or type like "large%" \
    order by rand() limit 1'
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        return row


def save_data(link):
    print("Hyvät matkustajat, tervetuloa lennolle!\nEnnen lennolle lähtöä anna nimesi: ")
    name = request.args.get('name')

    print("Kiitos, voitte nousta koneeseen.\nNauttikaa lennosta!\n")
    cursor.execute('insert into game (co2_consumed, co2_budget, location, screen_name) \
    values (0, 10000, "EFHK", "' + name +'")')

    contingent = randomcontingent(link)

    print (f"Lähtöpaikka: Helsinki-Vantaa lentokenttä (EFHK)\nPäämäärä: {contingent[0]}, {contingent[1]}\n")
    airport_name = contingent[0]
    cursor.execute('select ident from airport where name = "' + airport_name + '"')
    icao_req = cursor.fetchone()
    icao = icao_req[0]

    cursor.execute('update goal set destination = "' + icao + '"')