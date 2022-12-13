import json
from flask import Flask, request, jsonify, Response, render_template, redirect
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

app = Flask(__name__)
cors = CORS(app)


@app.route('/')
# creates the form to save the username
def index():
    return '''
    <form action="/game">
        <input name="name" />
        <input type="submit" value="Username"/>
    </form>
    '''


@app.route('/game', methods=['POST', 'GET'])
# Save game data for this round
def game_start():
    nick = request.args.get('name')
    lottery = randomcontingent(link)
    data = {'username': nick, 'goal': lottery[0], 'icao': lottery[1]}
    cursor.execute('insert into game (co2_consumed, co2_budget, location, screen_name) values (0, 10000, "EFHK", ' + nick + ');')
    cursor.execute('update goal set destination = ' + lottery[1] + ';')
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
    return '''<h4>Large passenger airplane</h4><p>Kulutus: 62,000 co2-kg/km<br>Max lentomatka: 5556 km</p>
    <form action="/bg/plane/large" method="post"><button type="submit" value="Choose Large">Choose Large</button></form>
    <br><br>
    <h4>Small airplane</h4><p>Kulutus: 0,583 co2-kg/km<br>Max lentomatka: 2778 km</p>
    <form action="/bg/plane/small" method="post"><button type="submit" value="Choose Small">Choose Small</button>
    </form>'''


def airports_json(options):
    data = []
    for icao in options:
        cursor.execute('select name, ident, iso_country from airport where ident = ' + icao + ';')
        nextone = cursor.fetchone()
        code = nextone[1]
        name = nextone[0]
        country = nextone[2]
        item = {code: (name, country)}
        data.append(item)
    jsonData = json.dumps(data)
    return jsonData


@app.route('/game/fly/<plane_pick>')
def fly(plane_pick):
    cursor.execute('select screen_name from game where id in (select max(id) from game)')
    user_res = cursor.fetchone()
    nick = user_res[0]
    sql = 'Update game set planetype = ' + plane_pick + ' where screen_name =' + nick + ';'
    cursor.execute(sql)
    ports = airports.main()
    if plane_pick == 'large':
        limited = deque(ports, maxlen=20)
        data = airports_json(limited)
        return Response(response=data)

    if plane_pick == 'small':
        limited = deque(ports, maxlen=10)
        data = airports_json(limited)
        return Response(response=data)
    return f'''<p>The plane you chose is: {str(plane_pick)}'''


if __name__ == '__main__':
    app.run(use_reloader=True)
