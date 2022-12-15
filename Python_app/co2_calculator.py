import json
import mysql.connector
from geopy.distance import geodesic as GD

import web_start
link = mysql.connector.connect(
        host='127.0.0.1',
        port=3306,
        database='lentopeliprojekti',
        user='root',
        password='Sal41a6sana52S',
        autocommit=True
    )
cursor = link.cursor(buffered=True)

airportList = []


def fetch_data():

    start_point = 'select location from game where id in (select max(id) from game);'
    cursor.execute(start_point)
    start = cursor.fetchone()

    end = "00CN"

    user_fetch = 'select screen_name from game where id in (select max(id) from game);'
    cursor.execute(user_fetch)
    user = cursor.fetchone()

    return start, end, user


def calculate_budget(start,end,user):


    sql = f'select latitude_deg,longitude_deg from airport where ident = "{start}"'
    cursor.execute(sql)
    reply = cursor.fetchone()
    lat = float(reply[0])
    lon = float(reply[1])
    coord1 = (lat, lon)
    airportList.append(coord1)

    sql2 = f'select latitude_deg,longitude_deg from airport where ident = "{end}"'
    cursor.execute(sql2)
    reply2 = cursor.fetchone()
    lat = float(reply2[0])
    lon = float(reply2[1])
    coord2 = (lat, lon)
    airportList.append(coord2)

    dist = GD(airportList[0], airportList[1]).km
    print(f"The distance between A and B is: {dist:.0f} km")

    plane_fetch = 'select planetype from game where id in (select max(id) from game);'
    cursor.execute(plane_fetch)
    plane_co2 = cursor.fetchone()
    plane_cons = float(plane_co2[0])

    print(f"co2_g_km of current aircraft: {plane_cons}")

    dist_calc = GD(airportList[0], airportList[1]).km * plane_cons / 1000
    print(f"co2 consumed during flight: {dist_calc:.0f} co2/kg/km")

    budget_fetch = f'select co2_consumed from game where screen_name  = "{user}"'
    cursor.execute(budget_fetch)
    co2_bud = cursor.fetchone()
    consumption = float(co2_bud[0])
    print(f"co2_consumed at start before adding consumption of current flight: {consumption}")

    budget = f"{(consumption + dist_calc):.0f}"
    print(f"final value of co2_consumed: {(budget)} co2/kg")
    update_sql = f'UPDATE game SET co2_consumed = co2_consumed + {budget} WHERE screen_name = "{user}"'
    cursor.execute(update_sql)
    return


calculate_budget(start,end,user)
print(f"airports visited sorted by coordinates: {airportList}")