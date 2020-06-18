from functions import *
import sched, time

s = sched.scheduler(time.time, time.sleep)
def do_something(sc):
    print(btc_usd())
    s.enter(5, 1, do_something, (sc,))

s.enter(5, 1, do_something, (s,))
s.run()



# def f100():
#
#     r = requests.get('http://api.ps3838.com/v1/fixtures?sportid=29&islive=2', headers={"Authorization": token})
#     r = r.json()
#     LEAGUE_LEN = len(r['league'])
#
#     temp = []
#     LEAGUE_NAME_LIST_FRESH = []
#     LEAGUE_ID_LIST  = []
#     # LEAGUE_CORNER_LIST_FRESH = []
#     PIN_EVENT_ID_LIST_FRESH = []
#     game_number = 1
#     # for i in range(0, LEAGUE_LEN):
#     for i in range(0, 10):
#         LEAGUE_ID = r['league'][i]['id']
#         cur = con.cursor()
#         cur.execute("SELECT liga FROM liga_soccer WHERE id=(%(id)s)", {'id':LEAGUE_ID})
#         con.commit()
#         data = cur.fetchone()
#
#
#         LEN_EVENTS_IN_LEAGUE = len(r['league'][i]['events'])
#         LEAGUE_NAME = data[0]
#         # if 'Corners' in LEAGUE_NAME:
#         #     LEAGUE_CORNER_LIST_FRESH.append(LEAGUE_NAME)
#         # else:
#         LEAGUE_ID_LIST.append(LEAGUE_ID)
#         LEAGUE_NAME_LIST_FRESH.append(LEAGUE_NAME)
#         EVENTS_IN_LEAGUE_LEN = len(r['league'][i]['events'])
#         #  open game in league
#         for i2 in range(0, EVENTS_IN_LEAGUE_LEN):
#             PIN_EVENT_ID = r['league'][i]['events'][i2]['id']
#             PIN_EVENT_ID = str(PIN_EVENT_ID)
#             PIN_EVENT_ID_LIST_FRESH.append(PIN_EVENT_ID)
#
#
#         LEAGUE_NAME_LIST_FRESH_LEN = len(LEAGUE_NAME_LIST_FRESH)
#         PIN_EVENT_ID_LIST_FRESH_LEN = len(PIN_EVENT_ID_LIST_FRESH)
#
#
#     PIN_EVENT_ID_LIST = []
#     cur = con.cursor()
#     cur.execute('SELECT idpin FROM EVENTS')
#     con.commit()
#     data = cur.fetchall()
#
#
#     xlen = len(data)
#
#     for i3 in range(0, xlen):
#         data1 = str(data[i3])[1:-2]
#         PIN_EVENT_ID_LIST.append(data1)
#
#     PIN_EVENT_ID_LIST_NEW = list(set(PIN_EVENT_ID_LIST) & set(PIN_EVENT_ID_LIST_FRESH))
#     PIN_EVENT_ID_LIST_NEW_LEN = len(PIN_EVENT_ID_LIST_NEW)
#     NEW_EVENTS_STR = str(PIN_EVENT_ID_LIST_FRESH_LEN-PIN_EVENT_ID_LIST_NEW_LEN)
#
#     PIN_EVENT_ID_SET = set(PIN_EVENT_ID_LIST)
#
#     print('')
#     print('Leagues:', LEAGUE_NAME_LIST_FRESH_LEN, 'Events:', PIN_EVENT_ID_LIST_FRESH_LEN)
#     # print('Leagues Corners:', LEAGUE_CORNER_LIST_FRESH_LEN)
#     print('New soccer events found:', NEW_EVENTS_STR)
#
#     for i4 in range(0, LEAGUE_NAME_LIST_FRESH_LEN):
#         events_in_league = len(r['league'][i4]['events'])
#         # if 'Corners' in LEAGUE_NAME:
#         #     continue
#         # else:
#         for i5 in range(0, events_in_league):
#             idpin = str(r['league'][i4]['events'][i5]['id'])
#             if idpin not in PIN_EVENT_ID_SET:
#                 idpin = r['league'][i4]['events'][i5]['id']
#                 uuid = uuider()
#                 league_id = r['league'][i4]['id']
#                 home = r['league'][i4]['events'][i5]['home']
#                 away = r['league'][i4]['events'][i5]['away']
#                 starttime = r['league'][i4]['events'][i5]['starts']
#
#
#
#                 cur = con.cursor()
#                 cur.execute(
#                     "INSERT INTO events (uuid, idpin, league_id, home, away, starttime) "
#                     "VALUES ((%(uuid)s), (%(idpin)s), (%(league_id)s), (%(home)s), (%(away)s), (%(starttime)s))",
#                     {'uuid': uuid, 'idpin': idpin, 'league_id': league_id, 'home': home, 'away': away,
#                      'starttime': starttime})
#                 con.commit()
#             else:
#                 continue
#
#     LEAGUE_ID_LIST_STR = str(list(dict.fromkeys(LEAGUE_ID_LIST)))[1:-1]
#     LEAGUE_ID_LIST_STR = re.sub('[ ]', '', LEAGUE_ID_LIST_STR)
#     LEAGUE_ID_LIST_LEN = len(LEAGUE_ID_LIST)
#
#     xx = 'http://api.ps3838.com/v1/odds?sportid=29&oddsformat=decimal&leagueids='+LEAGUE_ID_LIST_STR
#     print(xx)
#
#     r = requests.get('http://api.ps3838.com/v1/odds?sportid=29&oddsformat=decimal&leagueids='+ LEAGUE_ID_LIST_STR, headers={"Authorization": token})
#     r = r.json()
#     print(r)
#
#     # print(r2, 'hjh')
#
#     # for i6 in range(0, LEAGUE_ID_LIST_LEN):
#     ML_1X2_FT_COUNT = 0
#
#
#     for i6 in range(0, LEAGUE_ID_LIST_LEN):
#         EVENTS_IN_LEAGUE_LEN = len(r['leagues'][i6]['events'])
#
#         for i7 in range(0, EVENTS_IN_LEAGUE_LEN):
#
#
#             try:
#                 MAX_1X2_FT = float(r['leagues'][i6]['events'][i7]['periods'][0]['maxMoneyline'])
#                 LINEID_1X2_FT = int(r['leagues'][i6]['events'][i7]['periods'][0]['lineId'])
#
#                 GAME_TYPE = '1X2FT'
#                 GAMEID = gameid_generator(GAME_TYPE, LINEID_1X2_FT)
#                 print(GAME_TYPE, GAMEID)
#                 HDC_FT_LEN = len(r['leagues'][i6]['events'][i7]['periods'][0]['spreads'])
#                 print(HDC_FT_LEN)
#                 HDC_FT_POINT = r['leagues'][i6]['events'][i7]['periods'][0]['spreads'][0]['hdp']
#                 print('main FT', HDC_FT_POINT)
#                 if HDC_FT_LEN > 1:
#                     for i8 in range(1, HDC_FT_LEN):
#
#                         HDC_FT_ALT_LINEID = r['leagues'][i6]['events'][i7]['periods'][0]['spreads'][i8]['altLineId']
#                         HDC_FT_ALT_POINTS = r['leagues'][i6]['events'][i7]['periods'][0]['spreads'][i8]['hdp']
#                         print(HDC_FT_ALT_POINTS)
#             except KeyError:
#                 print('error')
#                 continue
#
#
#
#
#                 # HDC_1ST_LEN = len(r['leagues'][i6]['events'][i7]['periods'][1]['spreads'])
#                 # print(HDC_1ST_LEN)
#                 # HDC_1ST_POINT = r['leagues'][i6]['events'][i7]['periods'][1]['spreads'][0]['hdp']
#                 # print('main 1st', HDC_1ST_POINT)
#                 #
#                 #
#                 # if HDC_1ST_LEN > 1:
#                 #     for i8 in range(1, HDC_1ST_LEN):
#                 #
#                 #         HDC_1ST_ALT_LINEID = r['leagues'][i6]['events'][i7]['periods'][1]['spreads'][i8]['altLineId']
#                 #         HDC_1ST_ALT_POINTS = r['leagues'][i6]['events'][i7]['periods'][1]['spreads'][i8]['hdp']
#                 #         print(HDC_1ST_ALT_POINTS)
#
#
#
#
#
#
#
#
#                 # LINEID_1ST = float(r['leagues'][i6]['events'][i7]['periods'][1]['lineId'])
#
#
#
#
#             #     LEN_OU_FT = len(ODDS_OU_FT)
#             #     for i3 in range(0, LEN_ODDS_OU_FT):
#             #         LINE_OU_FT = r['leagues'][i]['events'][i2]['periods'][0]['totals'][i3]['points']
#             #         ODD_OVER_OU_FT = r['leagues'][i]['events'][i2]['periods'][0]['totals'][i3]['over']
#             #         ODD_UNDER_OU_FT = r['leagues'][i]['events'][i2]['periods'][0]['totals'][i3]['under']
#             #
#             #     if MAX_1X2_FT >= 20:
#             #
#             #         cur = con.cursor()
#             #         cur.execute("INSERT INTO odds (game, bk, lineid) "
#             #                     "VALUES ('1X2FT', 'PIN', "
#             #                     "(%(LINEID_1X2_FT)s))",
#             #                     {'LINEID_1X2_FT': LINEID_1X2_FT})
#             #         con.commit()
#             #         cur.execute("INSERT INTO odds (game, bk, lineid) "
#             #                     "VALUES ('1X21ST', 'PIN', "
#             #                     "(%(LINEID_1X2_1ST)s))",
#             #                     {'LINEID_1X2_1ST': LINEID_1X2_1ST})
#             #         con.commit()
#             #         ML_1X2_FT_COUNT += 2
#             #     else:
#             #         print('game not found')
#             # except:
#             #     continue
#
#
#     # print('Job done. New games added:', ML_1X2_FT_COUNT)
#
#     # print('Moneyline:', ML_1X2_COUNT, 'Over/Under:', 'Handicap:', 'Team Total:')
#     # print(' First Half:', ML_1X2_COUNT)
#     # print('Moneyline:', ML_1X2_COUNT, 'Over/Under:', 'Handicap:', 'Team Total:')
#
#
# def gameid_generator(gametype, lineid):
#     #
#
#     gameid = str(gametype)+str(lineid)
#     return gameid
#
#
# def tester():
#     r = requests.get('http://api.ps3838.com/v1/odds?sportid=29', headers={"Authorization": token})
#     r = r.json()
#     print(r)
#
#
# f100()