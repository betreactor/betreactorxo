from functions import *
# url = tgtoken


def get_tennis_lines():
    r = requests.get('http://api.ps3838.com/v1/fixtures?sportid=33&islive=2', headers={"Authorization": token})
    r = r.json()
    LEAGUE_LEN = len(r['league'])

    print(r)


    blist = []
    LEAGUE_NAME_LIST_FRESH = []
    EVENT_TITLE_LIST = []
    LEAGUE_ID_LIST = []
    PIN_EVENT_ID_LIST_FRESH = []
    EVENT_SELECTID = 1
    for i in range(0, LEAGUE_LEN):
        try:
            LEAGUE_ID = r['league'][i]['id']
            cur = con.cursor()
            cur.execute("SELECT league FROM tennis_league WHERE id=(%(id)s)", {'id':LEAGUE_ID})
            con.commit()
            data = cur.fetchone()


            LEN_EVENTS_IN_LEAGUE = len(r['league'][i]['events'])
            LEAGUE_NAME = str(data[0])
            print(LEAGUE_NAME)

            # LEAGUE_ID_LIST.append(LEAGUE_ID)
            LEAGUE_NAME_LIST_FRESH.append(LEAGUE_NAME)
            EVENTS_IN_LEAGUE_LEN = len(r['league'][i]['events'])

            for i2 in range(0, EVENTS_IN_LEAGUE_LEN):
                PIN_EVENT_ID = r['league'][i]['events'][i2]['id']
                # print(r['league'][i])
                # # PIN_EVENT_ID = str(PIN_EVENT_ID)
                PIN_EVENT_ID_LIST_FRESH.append(PIN_EVENT_ID)
                PLAYER_A =  str(r['league'][i]['events'][i2]['home'])
                PLAYER_B = str(r['league'][i]['events'][i2]['away'])
                # STARTS = r['league'][i]['events'][i2]['starts']
                STATUS = str(r['league'][i]['events'][i2]['status'])

                if STATUS == 'H':
                    STATUS_INT = 0
                    STATUS_STR = '          N/A'

                elif STATUS == 'I':
                    STATUS_INT = 1
                    STATUS_STR = '          Low'

                elif STATUS == 'O':
                    STATUS_INT = 2
                    STATUS_STR = '          Available'

                print(' ', EVENT_SELECTID, PLAYER_A, ' - ', PLAYER_B, STATUS_STR)
                # print(' (%d)' % EVENT_SELECTID + PLAYER_A + ' - ' + PLAYER_B, STATUS_STR)
                EVENT_SELECTID += 1
                EVENT_TITLE =  (PLAYER_A) +' - '+ str(PLAYER_B)+STATUS_STR
                # LEAGUE_ID_LIST.append(r['league'][i])
                LEAGUE_ID_LIST.append(LEAGUE_ID)
                EVENT_TITLE_LIST.append(EVENT_TITLE)



        except:
            continue
    print('')
    print(LEAGUE_ID_LIST)


    SELECT_ID = int(input('Выбери номер события:'))-1


    LEAGUE_ID_STR = str(LEAGUE_ID_LIST[SELECT_ID])
    EVENT_TITLE = (EVENT_TITLE_LIST[SELECT_ID])
    PIN_LINEID = (PIN_EVENT_ID_LIST_FRESH[SELECT_ID])

    r2 = requests.get('http://api.ps3838.com/v1/odds?sportid=33&islive=2&oddsformat=decimal&leagueids='+LEAGUE_ID_STR, headers={"Authorization": token})
    r2 = r2.json()

    # print(r2)

    EVENTS_IN_LEAGUE_LEN = len(r2['leagues'][0]['events'])

    for i3 in range(0, EVENTS_IN_LEAGUE_LEN):
        idpintemp = r2['leagues'][0]['events'][i3]['id']

        if idpintemp == PIN_LINEID:
            print('huhu')
            print(r2['leagues'][0]['events'][i3]['periods'][0]['lineId'])
            print(r2['leagues'][0]['events'][i3]['periods'][0]['moneyline'])
        else:
            continue
# get_tennis_lines_today()

def search_tennis_lines(name_to_search):
    name_to_search = name_to_search.capitalize()
    r = requests.get('http://api.ps3838.com/v1/fixtures?sportid=33&islive=2', headers={"Authorization": token})
    r = r.json()
    LEAGUE_LEN = len(r['league'])

    # print(r)
    # name_to_search = input('Поиск по имени игрока:')

    COUNT = 0
    SEARCH_RESULTS_LIST = []

    for i in range(0, LEAGUE_LEN):

            LEAGUE_ID = r['league'][i]['id']
            EVENTS_IN_LEAGUE_LEN = len(r['league'][i]['events'])



            for i2 in range(0, EVENTS_IN_LEAGUE_LEN):
                PIN_EVENT_ID = r['league'][i]['events'][i2]['id']
                PLAYER_A = str(r['league'][i]['events'][i2]['home'])
                PLAYER_B =  str(r['league'][i]['events'][i2]['away'])
                STARTS_ISO8601 = r['league'][i]['events'][i2]['starts']
                LEAGUE_ID_FOR_FOUND_EVENT = r['league'][i]['id']

                SEARCH_RESULTS = PIN_EVENT_ID, PLAYER_A, PLAYER_B, STARTS_ISO8601, LEAGUE_ID_FOR_FOUND_EVENT

                if name_to_search in PLAYER_A:
                    SEARCH_RESULTS_LIST.append(SEARCH_RESULTS)
                    COUNT += 1
                    continue
                elif name_to_search in PLAYER_B:
                    SEARCH_RESULTS_LIST.append(SEARCH_RESULTS)
                    COUNT += 1
                    continue
                continue

    # return SEARCH_RESULTS_LIST
    SEARCH_RESULTS_LIST_LEN = len(SEARCH_RESULTS_LIST)
    if SEARCH_RESULTS_LIST_LEN == 0:
        print('По данным %s ничего не найдено' % name_to_search)
    else:

        LEAGUE_NAME  = check_tennis_tour_by_id(int(LEAGUE_ID_FOR_FOUND_EVENT))
        print('Найдено событий: ', SEARCH_RESULTS_LIST_LEN)
        count3 = 1

        for i3 in range (0, SEARCH_RESULTS_LIST_LEN):
            PIN_EVENT_ID = int(SEARCH_RESULTS_LIST[i3][0])
            PLAYER_A = SEARCH_RESULTS_LIST[i3][1]
            PLAYER_B = SEARCH_RESULTS_LIST[i3][2]
            STARTS_ISO8601 = SEARCH_RESULTS_LIST[i3][3]
            STARTS = EVENT_START(SEARCH_RESULTS_LIST[i3][3])

            if count3 == 1:
                print(STARTS[0] + STARTS[1])
                print(SEARCH_RESULTS_LIST[i3][1] + ' - ' + SEARCH_RESULTS_LIST[i3][2] + ' * ' + LEAGUE_NAME)

            else:
                print(STARTS[0] + STARTS[1])
                print(count3, SEARCH_RESULTS_LIST[i3][1] + ' - ' + SEARCH_RESULTS_LIST[i3][2] + ' * ' + LEAGUE_NAME)
            print('*****************************************************')
            count3 += 1

        if count3 == 2:
            SELECT_N = 0
        else:
            SELECT_N = int(input('Enter game ID:')) - 1

        PIN_EVENT_ID = SEARCH_RESULTS_LIST[SELECT_N][0]
        LEAGUE_ID_STR = str(SEARCH_RESULTS_LIST[SELECT_N][4])

        PIN_TENNIS_GAMES_FROM_EVENT(PIN_EVENT_ID, LEAGUE_ID_STR, PLAYER_A, PLAYER_B, STARTS_ISO8601)
        INSERT_TO_EVENTS(PIN_EVENT_ID, LEAGUE_ID_STR, PLAYER_A, PLAYER_B, STARTS_ISO8601)

    #     SELECT_INSERT_TO_EVENTS = str(input('Добавить в базу? 1) да 2) вернуться к поиску'))
    #
    # if SELECT_INSERT_TO_EVENTS == str(1):



x = (search_tennis_lines('kirkin'))


# def PIN_UPDATE_GAMES_AND_ODDS_FROM_EVENTS():
#     EVENT_UUID_LIST = []
#     PIN_EVENTID_LIST = []
#     LEAGUE_LIST = []
#
#
#     cur = con.cursor()
#     cur.execute("SELECT uuid, pinid, pinleagueid FROM events")
#     con.commit()
#     EVENTS_DATA = cur.fetchall()
#     print(EVENTS_DATA[0])
#     EVENTS_DATA_LEN = len(EVENTS_DATA)
#
#     for i in range(0, EVENTS_DATA_LEN):
#         EVENT_UUID_LIST.append(EVENTS_DATA[i][0])
#         PIN_EVENTID_LIST.append(EVENTS_DATA[i][1])
#         LEAGUE_LIST.append(EVENTS_DATA[i][2])
#     con.close()
#
#     LEAGUE_LIST = league_list_to_str(LEAGUE_LIST)
#
#
#     r = requests.get(URL, headers={"Authorization": token})
#     r = r.json()
#     #
#     # print(r)







# PIN_UPDATE_GAMES_AND_ODDS_FROM_EVENTS()