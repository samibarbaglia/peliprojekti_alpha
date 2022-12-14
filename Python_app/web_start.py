import json
from flask import Flask, request, Response, render_template, redirect, render_template_string, jsonify, url_for
from flask_cors import CORS
from game_start import randomcontingent
import mysql.connector
import airports
from collections import deque


link = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='lentopeliprojekti',
    user='root',
    password='p4r!i3',
    autocommit=True
    )

cursor = link.cursor(buffered=True)

app = Flask(__name__, template_folder='templates')
cors = CORS(app)


@app.route('/')
# creates the form to save the username
def index():
    if request.path == '/game':
        return 'game'
    return render_template('front_page.html')


@app.route('/game', methods=['POST', 'GET'])
# Save game data for this round
def game_start():
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


@app.route('/bg/plane/<plane>', methods=['GET', 'POST'])
# Saves the plane data and redirects to the loop
def plane_choice(plane):
    p_type = plane
    if p_type == 'large':
        # Here there be some sql
        return redirect('/game/fly/large')
    elif p_type == 'small':
        # Here is another sql
        return redirect('/game/fly/small')
    else:
        return '''<h3>Something went wrong</h3>'''


@app.route('/game/plane', methods=['GET'])
def plane():
    return render_template_string('''
    {% extends "base.html" %}
            {% block content %}
            
            <h1>PLANE TYPES </h1>
            <table>
                <tr>
                    <th scope="col">Large</th>
                </tr>
                <tr>
                    <td>Kulutus: 62,000 co2-kg/km</td>
                </tr>
                <tr>
                    <td>Max. lentomatka: 5556 km</td>
                </tr>
                <tr>
                    <td style=border:none><form action="/bg/plane/large" method="post"><button type="submit" value="Choose Large">CHOOSE LARGE</button></form></td>
                    </td>
                </tr>
            </table>
            <table>
                <tr>
                    <th scope="col">Small</th>
                </tr>
                <tr>
                    <td>Kulutus: 0,583 co2-kg/km</td>
                </tr>
                <tr>
                    <td>Max. lentomatka: 2778 km</td>
                </tr>
                <tr>
                    <td style=border:none><form action="/bg/plane/small" method="post"><button type="submit" value="Choose Small">CHOOSE SMALL</button>
                    </form></td>
                </tr>
            </table>
        
    {% endblock %}''')


def airports_json(options):
    data = []
    for icao in options:
        req = 'select name, latitude_deg, longitude_deg from airport where ident = %s'
        val = (icao,)
        cursor.execute(req, val)

        nextone = cursor.fetchone()
        location = [nextone[1], nextone[2]]
        name = nextone[0]
        item = {name: location}
        data.append(item)
    json_data = json.dumps(data)
    return json_data


@app.route('/game/fly/<plane_pick>')
def fly(plane_pick):
    sql = 'Update game set planetype = %s'
    val = (plane_pick,)
    cursor.execute(sql, val)
    ports = airports.main()
    message = plane_pick
    if plane_pick == 'large':
        limited = deque(ports, maxlen=20)
        data = airports_json(limited)
        return render_template('main.html', data=data, message=message)

    elif plane_pick == 'small':
        limited = deque(ports, maxlen=10)
        data = airports_json(limited)
        return render_template('main.html', data=data, message=message)


if __name__ == '__main__':
    app.run(use_reloader=True)
