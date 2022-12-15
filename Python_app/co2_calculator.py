import mysql.connector
from geopy.distance import geodesic as GD
import json
link = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='lentopeliprojekti',
    user='root',
    password='Sal41a6sana52S',
    autocommit=True
)

cursor = link.cursor(buffered=True)

airportList = [(60.3172, 24.963301)]


def co2_calculator():
    loc_fetch = 'SELECT a.latitude_deg, a.longitude_deg FROM game g ' \
                'INNER JOIN airport a ON g.location = a.ident WHERE g.id = (SELECT MAX(id) FROM game)'
    cursor.execute(loc_fetch)
    reply = cursor.fetchone()
    lat = float(reply[0])
    lon = float(reply[1])
    coord1 = (lat, lon)
    airportList.append(coord1)

    dist = GD(airportList[-2], airportList[-1]).km
    print(f"The distance between A and B is: {dist:.0f} km")
    plane_fetch = 'SELECT planetype FROM game WHERE id = (SELECT MAX(id) FROM game);'
    cursor.execute(plane_fetch)
    plane_type = cursor.fetchone()[0]

    cons_fetch = f'SELECT co2_g_km FROM planetype WHERE type = "{plane_type}"'
    cursor.execute(cons_fetch)
    plane_cons = float(cursor.fetchone()[0])

    print(f"co2_g_km of current aircraft: {plane_cons}")

    dist_calc = GD(airportList[-2], airportList[-1]).km * plane_cons / 1000
    print(f"co2 consumed during flight: {dist_calc:.0f} co2/kg/km")

    budget_fetch = 'select co2_consumed from game where id in (select max(id) from game);'
    cursor.execute(budget_fetch)
    co2_bud = cursor.fetchone()
    consumption = float(co2_bud[0])
    print(f"co2_consumed at start before adding consumption of current flight: {consumption}")

    budget = f"{(consumption + dist_calc):.0f}"
    print(f"final value of co2_consumed: {budget} co2/kg")
    update_sql = f'UPDATE game SET co2_consumed = co2_consumed + {budget} WHERE id in (select max(id) from game);'
    cursor.execute(update_sql)
    return


co2_calculator()
print(f"airports visited sorted by coordinates: {airportList}")