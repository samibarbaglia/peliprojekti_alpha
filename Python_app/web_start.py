import json
from flask import Flask, request, Response, render_template, redirect, render_template_string, jsonify, make_response, url_for
from flask_cors import CORS
from game_start import randomcontingent
import mysql.connector
import airports
from collections import deque


link = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='flight_game',
    user='root',
    password='dB22',
    autocommit=True
    )

cursor = link.cursor(buffered=True)

app = Flask(__name__, template_folder='templates', static_folder='static')
cors = CORS(app)


@app.route('/')
# creates the form to save the username
def index():
    if request.path == '/game':
        return 'game'
    return render_template('front_page.html')

@app.route('/guide')
def guide():
    return render_template('guide.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/game', methods=['GET', 'POST'])
def game_start():
    # Save game data for this round
    nick = request.args.get('name')
    lottery = randomcontingent(link)
    sql = 'insert into game (co2_consumed, co2_budget, location, screen_name) \
    values (0, 10000, %s, %s)'
    val = ('EFHK', nick)
    cursor.execute(sql, val)

    goal = 'update goal set destination = %s'
    val = (lottery[1],)
    cursor.execute(goal, val)

    return redirect('/game/plane')


@app.route('/data')
def data_through():
    data = airports.main()
    cursor.execute('select planetype from game where id in (select max(id) from game);')
    plane_res = cursor.fetchone()
    plane = plane_res[0]
    if plane == 'large':
        limited = deque(data, maxlen=20)
        data = airports_json(limited)
        return data

    elif plane == 'small':
        limited = deque(data, maxlen=10)
        data = airports_json(limited)
        return data


@app.route('/get_coords')
def get_coordinates():
    icaos = data_through()
    targets = {'Helsinki Vantaa Airport': [60.3172,24.963301],}
    for code in icaos:
        cursor.execute('select name, latitude, longitude from airports where ident="' + code + '"')
        row = cursor.fetchone()
        targets[row[0]] = [row[1], row[2]]
    return targets


@app.route('/game/fly/<plane_pick>', methods=['GET', 'POST'])
def fly(plane_pick):
    sql = 'Update game set planetype = %s where id in (select max(id) from game);'
    val = (plane_pick,)
    cursor.execute(sql, val)
    resp = data_through()
    plane = plane_pick
    returning = {'plane': plane, 'data': resp}
    jsonized = json.dumps(returning)
    return render_template('main.html', jsonized=jsonized)


@app.route('/get_plane')
def get_plane():
    cursor.execute('select planetype from game where id in (select max(id) from game)')
    res  = cursor.fetchone()
    plane = res[0]
    return plane


@app.route('/game/plane', methods=['GET'])
def choose_plane():
    return render_template_string('''
    {% extends "base.html" %}
            {% block content %}
            
            <table style=font-family:Rockwell;>
                <tr>
                    <th scope="col" style=font-family:Rockwell;><b>LARGE COMMERCIAL PLANE</b></th>
                </tr>
                <tr>
                    <td style=font-family:Rockwell;>CO2: 62,000 CO2-KG/KM</td>
                </tr>
                <tr>
                    <td style=font-family:Rockwell;>MAX FLIGHT DISTANCE: 5556 KM</td>
                </tr>
                <tr>
                    <td style=border:none><form action="/game/fly/large" method="post"><button type="submit" value="Choose Large">CHOOSE LARGE</button></form></td>
                    </td>
                </tr>
            </table>
            <table>
                <tr>
                    <th scope="col" style=font-family:Rockwell;>SMALL PRIVATE PLANE</th>
                </tr>
                <tr>
                    <td style=font-family:Rockwell;>CO2: 0,583 CO2-KG/KM</td>
                </tr>
                <tr>
                    <td style=font-family:Rockwell;>MAX. FLIGHT DISTANCE: 2778 KM</td>
                </tr>
                <tr>
                    <td style=border:none><form action="/game/fly/small" method="post"><button type="submit" value="Choose Small">CHOOSE SMALL</button>
                    </form></td>
                </tr>
            </table>
        
    {% endblock %}''')


@app.route('/update', methods=['GET'])
def update_data():
    new_data = request.get_json()
    name = ''
    for key in new_data:
        name = key
    cursor.execute('select ident from airport where name = "' + name + '"')
    ident_res = cursor.fetchone()
    icao = ident_res[0]
    cursor.execute('update game set location="' + icao + '" where id in (select max(id) from game)')


@app.route('/get_location')
def get_loc():
    cursor.execute('select location from game where id in (select max(id) from game)')
    get_icao = cursor.fetchone()
    icao = get_icao[0]
    val = (icao,)
    cursor.execute('select name, latitude_deg, longitude_deg from airport where ident = %s', val)
    icao_name = cursor.fetchone()
    location_name = icao_name[0]
    location_coords = [icao_name[1], icao_name[2]]
    location = {location_name: location_coords}
    location_json = json.dumps(location)
    # Returns a json-string
    return location_json

def airports_json(options):
    data = []
    for icao in options:
        req = 'select name, latitude_deg, longitude_deg from airport where ident = %s order by rand();'
        val = (icao,)
        cursor.execute(req, val)

        nextone = cursor.fetchone()
        location = [nextone[1], nextone[2]]
        name = nextone[0]
        item = {name: location}
        data.append(item)
    json_data = json.dumps(data)
    # Returns a json-string
    return json_data


if __name__ == '__main__':
    app.run(use_reloader=True)