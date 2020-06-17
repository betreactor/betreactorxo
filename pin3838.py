import requests
import datetime
from datetime import datetime, timedelta


def game_time(start):
    format = "%Y-%m-%dT%H:%M:%SZ"
    time_now = datetime.now() + timedelta(hours=-3)
    time_now = time_now.isoformat('T')

    time_now = datetime.strptime(time_now, '%Y-%m-%dT%H:%M:%S.%f')
    time_now = time_now.strftime(format)


    starts = start



    datetime_obj = datetime.strptime(starts, format)
    datetime_obj2 = datetime.strptime(time_now, format)

    remains = datetime_obj - datetime_obj2
    str_remains = str(remains)[:-3]

    gamestart = datetime.strptime(starts, "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=+3)
    date_time_starts = gamestart.strftime("%A, %d %B %H:%M")

    return (date_time_starts, str_remains)
def get_balance_pin3838():

    r = requests.get('http://api.ps3838.com/v1/client/balance', headers={"Authorization": token})
    balance_pin_3838 = r.json()
    balance_pin_3838 = float(balance_pin_3838['availableBalance'])
    return balance_pin_3838


def all_soccer():

    r = requests.get('http://api.ps3838.com/v1/fixtures?sportid=29', headers={"Authorization": token})
    r = r.json()
    count = len(r['league'])
    # print(count, r)

    id = 1

    for i in range(0, count):
        league_name = r['league'][i]['id']
        cur = con.cursor()
        cur.execute("SELECT liga FROM liga_soccer WHERE id=(%(x)s)", {'x':league_name})
        con.commit()
        data = cur.fetchone()
        games_in_league = len(r['league'][i]['events'])
        print(data[0])

        # counts number of games

        game_number = 1

        for i2 in range(0, games_in_league):

            liveStatus = int(r['league'][i]['events'][i2]['liveStatus'])
            if (liveStatus == 0):
                liveStatus = str('not live event')
            if (liveStatus == 1):
                liveStatus = str('LIVE NOW!')
            if (liveStatus == 2):
                liveStatus = str('turns live')


            starts =  r['league'][i]['events'][i2]['starts']
            starts = game_time(starts)

            print(' ', game_number, r['league'][i]['events'][i2]['home'], '-',
                  r['league'][i]['events'][i2]['away'], r['league'][i]['events'][i2]['id'], liveStatus, starts)

            game_number = game_number + 1
        #
        #     league_id = str(input('League id:\n'))
        #     event_id = str(input('Event it:\n'))

    con.close()
def all_soccer_prelive():

    r = requests.get('http://api.ps3838.com/v1/fixtures?sportid=29', headers={"Authorization": token})
    r = r.json()
    count = len(r['league'])

    temp = []
    game_number = 1
    for i in range(0, count):
        league_id = r['league'][i]['id']
        cur = con.cursor()
        cur.execute("SELECT liga FROM liga_soccer WHERE id=(%(x)s)", {'x':league_id})
        con.commit()
        data = cur.fetchone()
        games_in_league = len(r['league'][i]['events'])
        league_name = data[0]

        for i2 in range(0, games_in_league):

            livestatus = int(r['league'][i]['events'][i2]['liveStatus'])

            if (livestatus == 2):


                idpin = r['league'][i]['events'][i2]['id']
                league_id = r['league'][i]['id']
                home = r['league'][i]['events'][i2]['home']
                away = r['league'][i]['events'][i2]['away']
                starttime = r['league'][i]['events'][i2]['starts']

                game_elements = {'idpin': idpin, 'league_id': league_id, 'home': home, 'away': away, 'starttime': starttime}
                temp.append(game_elements)

                start_remain = game_time(starttime)[1]
                start_time_clear = game_time(starttime)[0]
                print(game_number, home, '-', away, league_name, start_remain, start_time_clear, idpin)
                game_number = game_number + 1


    x = int(input()) - 1
    idpin = int(temp[x]['idpin'])
    league_id = int(temp[x]['league_id'])
    home = temp[x]['home']
    away = temp[x]['away']
    starttime = temp[x]['starttime']

    print(home, away, starttime)
    uuid = uuider()

    cur = con.cursor()
    cur.execute('SELECT * FROM gamebase WHERE idpin = (%(idpin)s)', {'idpin': idpin})
    con.commit()
    data = cur.fetchone()

    # check if game already there
    if data == None:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO gamebase (uuid, idpin, league_id, home, away, starttime) VALUES ((%(uuid)s), (%(idpin)s), (%(league_id)s), (%(home)s), (%(away)s), (%(starttime)s))",
            {'uuid': uuid, 'idpin': idpin, 'league_id': league_id, 'home': home, 'away': away, 'starttime': starttime})
        cur.execute(
            "INSERT INTO odds_pin_soccer (uuid) VALUES ((%(uuid)s))", {'uuid': uuid})

        con.commit()
        print(home, '-', away, 'successfully added')
        con.close()
    else:
        print('Already there')
        con.close()





