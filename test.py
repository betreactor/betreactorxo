import requests
import psycopg2
from datetime import datetime, timedelta
import uuid

from functions import token as token, con as con, uuider as uuider, \
        hostdb as hostdb, dbtoken as dbtoken, \
        userdb as userdb, passworddb as passworddb

def uuider():
    uuidhex64 = uuid.uuid4().hex
    return(uuidhex64)


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
con = psycopg2.connect(
            host='localhost',
            database='postgres',
            user='postgres',
            password='a')
from decimal import Decimal
TWO = Decimal(10) ** -2


# def all_soccer_prelive():
#
#     r = requests.get('http://api.ps3838.com/v1/fixtures?sportid=29', headers={"Authorization": token})
#     r = r.json()
#     count = len(r['league'])
#
#     temp = []
#     game_number = 1
#     for i in range(0, count):
#         league_id = r['league'][i]['id']
#         cur = con.cursor()
#         cur.execute("SELECT liga FROM liga_soccer WHERE id=(%(x)s)", {'x':league_id})
#         con.commit()
#         data = cur.fetchone()
#         games_in_league = len(r['league'][i]['events'])
#         league_name = data[0]
#
#         for i2 in range(0, games_in_league):
#
#             livestatus = int(r['league'][i]['events'][i2]['liveStatus'])
#
#             if (livestatus == 2):
#
#
#                 idpin = r['league'][i]['events'][i2]['id']
#                 league_id = r['league'][i]['id']
#                 home = r['league'][i]['events'][i2]['home']
#                 away = r['league'][i]['events'][i2]['away']
#                 starttime = r['league'][i]['events'][i2]['starts']
#
#                 game_elements = {'idpin': idpin, 'league_id': league_id, 'home': home, 'away': away, 'starttime': starttime}
#                 temp.append(game_elements)
#
#                 start_remain = game_time(starttime)[1]
#                 start_time_clear = game_time(starttime)[0]
#                 print(game_number, home, '-', away, league_name, start_remain, start_time_clear, idpin)
#                 game_number = game_number + 1
#
#
#     x = int(input()) - 1
#     idpin = int(temp[x]['idpin'])
#     league_id = int(temp[x]['league_id'])
#     home = temp[x]['home']
#     away = temp[x]['away']
#     starttime = temp[x]['starttime']
#
#     print(home, away, starttime)
#     uuid = uuider()
#
#     cur = con.cursor()
#     cur.execute('SELECT * FROM gamebase WHERE idpin = (%(idpin)s)', {'idpin': idpin})
#     con.commit()
#     data = cur.fetchone()
#
#     # check if game already there
#     if data == None:
#         cur = con.cursor()
#         cur.execute(
#             "INSERT INTO gamebase (uuid, idpin, league_id, home, away, starttime) VALUES ((%(uuid)s), (%(idpin)s), (%(league_id)s), (%(home)s), (%(away)s), (%(starttime)s))",
#             {'uuid': uuid, 'idpin': idpin, 'league_id': league_id, 'home': home, 'away': away, 'starttime': starttime})
#         cur.execute(
#             "INSERT INTO odds_pin_soccer (uuid) VALUES ((%(uuid)s))", {'uuid': uuid})
#
#         con.commit()
#         print(home, '-', away, 'successfully added')
#         con.close()
#     else:
#         print('Already there')
#         con.close()

# bet365_odds_by_eventID()

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
    cur.execute('SELECT * FROM events WHERE idpin = (%(idpin)s)', {'idpin': idpin})
    con.commit()
    data = cur.fetchone()

    # check if game already there
    if data == None:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO events (uuid, idpin, league_id, home, away, starttime) VALUES ((%(uuid)s), (%(idpin)s), (%(league_id)s), (%(home)s), (%(away)s), (%(starttime)s))",
            {'uuid': uuid, 'idpin': idpin, 'league_id': league_id, 'home': home, 'away': away, 'starttime': starttime})
        # cur.execute(
        #     "INSERT INTO table_test (uuid) VALUES ((%(uuid)s))", {'uuid': uuid})

        con.commit()
        print(home, '-', away, 'successfully added')
        con.close()
    else:
        print('Already there')
        con.close()
def list_all_active_games():
    cur = con.cursor()
    cur.execute('SELECT * FROM EVENTS')
    con.commit()
    data = cur.fetchall()

    x = len(data)
    for i in range (0, x):
        print(i+1, data[i][1], data[i][2])
    con.close()
# all_soccer_prelive()
def bet365_soccer_live():
    url = "https://bet365-scoccer-odds.p.rapidapi.com/v1/events/inplay"

    querystring = {"LNG_ID":"1","sport_id":"1"}

    headers = {
        'x-rapidapi-host': "bet365-scoccer-odds.p.rapidapi.com",
        'x-rapidapi-key': "dd2456a101msh79b2e391528e2c7p156cc9jsnc2307836062b"
        }

    r = requests.request("GET", url, headers=headers, params=querystring)

    data = r.json()
    count = int(data['pager']['total'])
    print(data)


    for i in range(0, count):
        id = data['results'][i]['id']
        time = data['results'][i]['time']
        home = data['results'][i]['home']
        away = data['results'][i]['away']
        score = data['results'][i]['ss']
        print(id, home['name'], away['name'], score)
# bet365_soccer_live()
def bet365_soccer_upcomming():
    url = "https://bet365-scoccer-odds.p.rapidapi.com/v2/events/upcoming"

    # querystring = {"LNG_ID": "1", "sport_id": "1"}
    querystring = {"LNG_ID": "1", "page":"2", "day": "20200611", "sport_id": "1"}

    headers = {
        'x-rapidapi-host': "bet365-scoccer-odds.p.rapidapi.com",
        'x-rapidapi-key': "dd2456a101msh79b2e391528e2c7p156cc9jsnc2307836062b"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    r = requests.request("GET", url, headers=headers, params=querystring)

    data = r.json()
    count = int(data['pager']['total'])
    print(data)


    for i in range(0, count):
        id = data['results'][i]['id']
        time = data['results'][i]['time']
        home = data['results'][i]['home']
        away = data['results'][i]['away']
        score = data['results'][i]['ss']
        print(id, home['name'], away['name'], score)
# bet365_soccer_upcomming()
def bet365_odds_by_eventID(event_id):
    url = "https://bet365-scoccer-odds.p.rapidapi.com/v2/event/odds"

    querystring = {"event_id": 2353674}

    headers = {
        'x-rapidapi-host': "bet365-scoccer-odds.p.rapidapi.com",
        'x-rapidapi-key': "dd2456a101msh79b2e391528e2c7p156cc9jsnc2307836062b"
    }

    r = requests.request("GET", url, headers=headers, params=querystring)

    data = r.json()

    # Fulltime 3way
    print(data)
    home_odd_ml = data['results']['odds']['1_1'][0]['home_od']
    draw_odd_ml = data['results']['odds']['1_1'][0]['draw_od']
    away_odd_ml = data['results']['odds']['1_1'][0]['away_od']

    # print('Fulltime', home_odd, draw_odd, away_odd)
    # Asian Handicap 0.0
    # home_odd = data['results']['odds']['1_2'][0]['home_od']
    # away_odd = data['results']['odds']['1_2'][0]['away_od']
    # print('Asian Handicap 0.0', home_odd, away_odd)
    # Goal Line HC 1
    # print(data['results']['odds']['1_3'][0])
    # over_odd = data['results']['odds']['1_3'][0]['over_od']
    # handicap = data['results']['odds']['1_3'][0]['handicap']
    # under_odd = data['results']['odds']['1_3'][0]['under_od']

    # print('Goal Line HC 1:', handicap, over_odd, under_odd)

    # over_odd = data['results']['odds']['1_4'][0]['over_od']
    # handicap = data['results']['odds']['1_4'][0]['handicap']
    # under_odd = data['results']['odds']['1_4'][0]['under_od']
    # print('Asian Corners HC', handicap, over_odd, under_odd)
    # unknow
    # print(data['results']['odds']['1_5'][0])
    # print(data['results']['odds']['1_6'][0])
    # print(data['results']['odds']['1_7'][0])
    # print(data['results']['odds']['1_8'][0])
    return home_odd_ml, draw_odd_ml, away_odd_ml
# bet365_odds_by_eventID()
def bet365_auto_search_from_events():
    cur = con.cursor()
    cur.execute('SELECT * FROM EVENTS')
    con.commit()
    data = cur.fetchall()



    x = len(data)
    for i in range (0, x):
        eventid = data[i][0]
        home = data[i][3]
        away = data[i][4]
        data = str(data[i][5])[:-10].replace('-', '')


        print(i+1, home, away, data)
        print('Enter number to search event at bet365:')
        # input(x)
    url = "https://bet365-scoccer-odds.p.rapidapi.com/v1/events/search"
    querystring = {"time": data, "home": home, "sport_id": "1", "away": away}

    headers = {
        'x-rapidapi-host': "bet365-scoccer-odds.p.rapidapi.com",
        'x-rapidapi-key': "dd2456a101msh79b2e391528e2c7p156cc9jsnc2307836062b"
    }

    r = requests.request("GET", url, headers=headers, params=querystring)

    data = r.json()
    idbet365 = data['results'][0]['id']
    print(data)
    print(idbet365)

    cur = con.cursor()
    cur.execute("UPDATE events SET idbet365 = %s WHERE uuid = %s", (idbet365,eventid,))
    con.commit()

    cur.execute("INSERT INTO odds (uuid, game, bk)"
                "VALUES ((%(eventid)s), 'ML', 'PIN')", {'eventid':eventid})
    cur.execute("INSERT INTO odds (uuid, game, bk)"
                "VALUES ((%(eventid)s), 'ML', 'BET365')", {'eventid':eventid})
    con.commit()
    con.close()
# bet365_auto_search_from_events()
# all_soccer_prelive()
# bet365_auto_search_from_events()
def update_odds_PIN():
    cur = con.cursor()
    cur.execute("SELECT uuid, game FROM odds WHERE BK = 'PIN'")

    con.commit()
    data = cur.fetchall()


    x = len(data)
    ligidlist = []
    eventidlist = []

    for i in range (0, x):
        uuid = data[i][0]
        game = data[i][1]
        cur.execute("SELECT idpin, league_id FROM events WHERE uuid = %s", (uuid,))
        con.commit()
        data = cur.fetchone()
        pinid = str(data[0])
        ligid = str(data[1])
        ligidlist.append(ligid)
        eventidlist.append(pinid)


    eventidlist_count = len(eventidlist)

    if x == 1:
        ligidliststr = str(ligidlist)[2:-2]
    if x > 1:
        ligidliststr = str(ligidlist)[2:-3]

    r = requests.get('http://api.ps3838.com/v1/odds?sportid=29&oddsformat=decimal&leagueids='+ligidliststr, headers={"Authorization": token})
    r = r.json()

    leneventidlist = len(eventidlist)
    count_lig = len(r['leagues'])

    for i in range(0, count_lig):
        count_events_in_league = len(r['leagues'][i]['events'])

        eventinlig = []
        moneyline = []
        # try:
            # for i2 in range(0, count_events_in_league):
        for i2 in range(3, 4):
            data = r['leagues'][i]['events'][i2]['id']
            # print(r['leagues'][i]['events'][i2])

            # MAXIMUMS
            print()
            MAX_1X2_FT = float(r['leagues'][i]['events'][i2]['periods'][0]['maxMoneyline'])
            MAX_1X2_1ST = float(r['leagues'][i]['events'][i2]['periods'][1]['maxMoneyline'])
            MAX_HDC_FT = float(r['leagues'][i]['events'][i2]['periods'][0]['maxSpread'])
            MAX_HDC_1ST = float(r['leagues'][i]['events'][i2]['periods'][1]['maxSpread'])
            MAX_OU_FT = float(r['leagues'][i]['events'][i2]['periods'][0]['maxTotal'])
            MAX_OU_1ST = float(r['leagues'][i]['events'][i2]['periods'][1]['maxTotal'])
            MAX_OU_TEAM_FT = float(r['leagues'][i]['events'][i2]['periods'][0]['maxTeamTotal'])
            MAX_OU_TEAM_1ST = float(r['leagues'][i]['events'][i2]['periods'][1]['maxTeamTotal'])
            # print(MAX_ML_FT, MAX_ML_1ST, MAX_OU_FT, MAX_OU_1ST, MAX_OU_TEAM_FT, MAX_OU_TEAM_1ST, MAX_HDC_FT, MAX_HDC_1ST)

            # FULLTIME MONEYLINE ODDS
            ODD_1X2_HOME_FT = float(r['leagues'][i]['events'][i2]['periods'][0]['moneyline']['home'])
            ODD_1X2_AWAY_FT = float(r['leagues'][i]['events'][i2]['periods'][0]['moneyline']['away'])
            ODD_1X2_DRAW_FT = float(r['leagues'][i]['events'][i2]['periods'][0]['moneyline']['draw'])

            # FULLTIME HANDICAP LINES & ODDS
            ODDS_HDC_FT = r['leagues'][i]['events'][i2]['periods'][0]['spreads']
            ODDS_HDC_FT_LEN = len(ODDS_HDC_FT)
            for i3 in range(0, ODDS_HDC_FT_LEN):
                LINE_HDC_FT = float(r['leagues'][i]['events'][i2]['periods'][0]['spreads'][i3]['hdp'])
                ODD_AWAY_HDC_FT = float(r['leagues'][i]['events'][i2]['periods'][0]['spreads'][i3]['away'])
                ODD_HOME_HDC_FT = float(r['leagues'][i]['events'][i2]['periods'][0]['spreads'][i3]['home'])

            # FULLTIME TOTAL LINE & ODDS
            ODDS_OU_FT = r['leagues'][i]['events'][i2]['periods'][0]['totals']
            LEN_ODDS_OU_FT = len(ODDS_OU_FT)
            for i3 in range(0, LEN_ODDS_OU_FT):
                LINE_OU_FT = r['leagues'][i]['events'][i2]['periods'][0]['totals'][i3]['points']
                ODD_OVER_OU_FT = r['leagues'][i]['events'][i2]['periods'][0]['totals'][i3]['over']
                ODD_UNDER_OU_FT = r['leagues'][i]['events'][i2]['periods'][0]['totals'][i3]['under']

            # FULLTIME TEAMTOTAL LINE & ODDS
            LINE_TOU_AWAY_FT = r['leagues'][i]['events'][i2]['periods'][0]['teamTotal']['away']['points']
            ODD_OVER_TOU_AWAY_FT = r['leagues'][i]['events'][i2]['periods'][0]['teamTotal']['away']['over']
            ODD_UNDER_TOU_AWAY_FT = r['leagues'][i]['events'][i2]['periods'][0]['teamTotal']['away']['under']
            LINE_TOU_HOME_FT = r['leagues'][i]['events'][i2]['periods'][0]['teamTotal']['home']['points']
            ODD_OVER_TOU_HOME_FT = r['leagues'][i]['events'][i2]['periods'][0]['teamTotal']['home']['over']
            ODD_UNDER_TOU_HOME_FT = r['leagues'][i]['events'][i2]['periods'][0]['teamTotal']['home']['under']



            # 1ST HALF MONEYLINE ODDS
            ODD_1X2_HOME_1ST = float(r['leagues'][i]['events'][i2]['periods'][1]['moneyline']['home'])
            ODD_1X2_AWAY_1ST = float(r['leagues'][i]['events'][i2]['periods'][1]['moneyline']['away'])
            ODD_1X2_DRAW_1ST = float(r['leagues'][i]['events'][i2]['periods'][1]['moneyline']['draw'])

            # 1ST HALF HANDICAP LINES & ODDS
            ODDS_HDC_1ST = r['leagues'][i]['events'][i2]['periods'][1]['spreads']
            ODDS_HDC_1ST_LEN = len(ODDS_HDC_1ST)
            for i3 in range(0, ODDS_HDC_1ST_LEN):
                LINE_HDC_1ST = float(r['leagues'][i]['events'][i2]['periods'][1]['spreads'][i3]['hdp'])
                ODD_HDC_AWAY_1ST = float(r['leagues'][i]['events'][i2]['periods'][1]['spreads'][i3]['away'])
                ODD_HDC_HOME_1ST = float(r['leagues'][i]['events'][i2]['periods'][1]['spreads'][i3]['home'])

            # 1ST HALF TOTAL LINES & ODDS
            ODDS_OU_1ST = r['leagues'][i]['events'][i2]['periods'][1]['totals']
            LEN_ODDS_OU_1ST = len(ODDS_OU_1ST)
            for i3 in range(0, LEN_ODDS_OU_1ST):
                LINE_OU_1ST = r['leagues'][i]['events'][i2]['periods'][1]['totals'][i3]['points']
                ODD_OVER_OU_1ST = r['leagues'][i]['events'][i2]['periods'][1]['totals'][i3]['over']
                ODD_UNDER_OU_1ST = r['leagues'][i]['events'][i2]['periods'][1]['totals'][i3]['under']

            # 1ST TEAMTOTAL LINE & ODDS
            LINE_TOU_AWAY_1ST = r['leagues'][i]['events'][i2]['periods'][1]['teamTotal']['away']['points']
            ODD_OVER_TOU_AWAY_1ST = r['leagues'][i]['events'][i2]['periods'][1]['teamTotal']['away']['over']
            ODD_UNDER_TOU_AWAY_1ST = r['leagues'][i]['events'][i2]['periods'][1]['teamTotal']['away']['under']

            LINE_TOU_HOME_1ST = r['leagues'][i]['events'][i2]['periods'][1]['teamTotal']['home']['points']
            ODD_OVER_TOU_HOME_1ST = r['leagues'][i]['events'][i2]['periods'][1]['teamTotal']['home']['over']
            ODD_UNDER_TOU_HOME_1ST = r['leagues'][i]['events'][i2]['periods'][1]['teamTotal']['home']['under']


                # for i3 in range(0, leneventidlist):
                #     eventidlist[i3] = int(eventidlist[i3])
                #     if (data == eventidlist[i3]):
                #         cur = con.cursor()
                #         cur.execute("UPDATE odds "
                #                     "SET odd1 = (%s),"
                #                     "odd2 = (%s),"
                #                     "odd3 = (%s)"
                #                     "WHERE uuid = (%s) "
                #                     "AND game = (%s)"
                #                     "AND bk = (%s)",
                #                     (odds_3way_home, odds_3way_draw, odds_3way_away, uuid, 'ML', 'PIN'))
                #         print('Pinnacle odds updated successfully')
                #         con.commit()
                #         con.close()

        # cur = con.cursor()
        # cur.execute('SELECT idpin, league_id FROM events WHERE uuid = %s AND bk = %s', (uuid, 'pin'))
        # con.commit()
        #
        # pindata = (cur.fetchone())
        # idpin = pindata[0]
        # leagueid = pindata[1]
        # except KeyError:
        #     print('Something not found')
def update_odds_bet365():
    cur = con.cursor()
    cur.execute("SELECT uuid, game FROM odds WHERE BK = 'BET365'")

    con.commit()
    data = cur.fetchall()
    print(data)

    x = len(data)
    ligidlist = []
    eventidlist = []

    for i in range (0, x):
        uuid = data[i][0]
        game = data[i][1]
        cur.execute("SELECT idbet365 FROM events WHERE uuid = %s", (uuid,))
        con.commit()
        data = cur.fetchone()
        ideventbet365 = str(data[0])
        eventidlist.append(ideventbet365)


    eventidlist_count = len(ideventbet365)
    ideventbet365 = int(ideventbet365)

    # return ideventbet365
    # for i in range (0, eventidlist_count):
    data = bet365_odds_by_eventID(ideventbet365)

    home_odd_ml = float(data[0])
    draw_odd_ml = float(data[1])
    away_odd_ml = float(data[2])

    cur = con.cursor()
    cur.execute("UPDATE odds "
                "SET odd1 = (%s),"
                "odd2 = (%s),"
                "odd3 = (%s)"
                "WHERE uuid = (%s) "
                "AND game = (%s)"
                "AND bk = (%s)",
                (home_odd_ml, draw_odd_ml, away_odd_ml, uuid, 'ML', 'BET365'))
    print('BET365 odds updated successfully')
    con.commit()
    con.close()
# update_odds_bet365()
# update_odds_PIN()
def list_all_games_in_event_soccer():

    cur = con.cursor()
    cur.execute("SELECT uuid, game FROM odds WHERE BK = 'PIN'")

    con.commit()
    data = cur.fetchall()


    x = len(data)
    ligidlist = []
    eventidlist = []

    for i in range (0, x):
        uuid = data[i][0]
        game = data[i][1]
        cur.execute("SELECT idpin, league_id FROM events WHERE uuid = %s", (uuid,))
        con.commit()
        data = cur.fetchone()
        pinid = str(data[0])
        ligid = str(data[1])
        ligidlist.append(ligid)
        eventidlist.append(pinid)


    eventidlist_count = len(eventidlist)

    if x == 1:
        ligidliststr = str(ligidlist)[2:-2]
    if x > 1:
        ligidliststr = str(ligidlist)[2:-3]


    r = requests.get('http://api.ps3838.com/v1/odds?sportid=29&oddsformat=decimal&leagueids='+ligidliststr, headers={"Authorization": token})
    print('lllll', type(r))
    r = r.json()

    leneventidlist = len(eventidlist)
    count_lig = len(r['leagues'])

    for i in range(0, count_lig):
        count_events_in_league = len(r['leagues'][i]['events'])

        eventinlig = []
        moneyline = []
        for i2 in range(0, count_events_in_league):
            data = r['leagues'][i]['events'][i2]['id']

            odds_3way = r['leagues'][i]['events'][i2]['periods'][0]['moneyline']
            odds_totals = r['leagues'][i]['events'][i2]['periods'][0]['totals'][0]
            odds_3way_away = float(odds_3way['away'])
            odds_3way_home = float(odds_3way['home'])
            odds_3way_draw = float(odds_3way['draw'])
            print(r['leagues'][i]['events'][i2])

            for i3 in range(0, leneventidlist):
                eventidlist[i3] = int(eventidlist[i3])
                if (data == eventidlist[i3]):
                    cur = con.cursor()
