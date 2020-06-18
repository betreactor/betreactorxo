from functions import *
url = tgtoken


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

    r2 = requests.get('http://api.ps3838.com/v1/odds?sportid=33&oddsformat=decimal&leagueids='+LEAGUE_ID_STR, headers={"Authorization": token})
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
    print(name_to_search)

    # r = requests.get('http://api.ps3838.com/v1/fixtures?sportid=33&islive=2', headers={"Authorization": token})
    r = requests.get('http://api.ps3838.com/v1/fixtures?sportid=33&', headers={"Authorization": token})
    r = r.json()
    LEAGUE_LEN = len(r['league'])

    # name_to_search = input('Поиск по имени игрока:')

    COUNT1 = 1
    COUNT2 = 1
    SEARCH_RESULTS_LIST = []

    for i in range(0, LEAGUE_LEN):

            LEAGUE_ID = r['league'][i]['id']
            # LEAGUE_NAME_LIST_FRESH.append(LEAGUE_NAME)
            EVENTS_IN_LEAGUE_LEN = len(r['league'][i]['events'])
            # LEAGUE_NAME_LIST_FRESH.append(LEAGUE_NAME)


            for i2 in range(0, EVENTS_IN_LEAGUE_LEN):
                PIN_EVENT_ID = r['league'][i]['events'][i2]['id']
                # PIN_EVENT_ID_LIST_FRESH.append(PIN_EVENT_ID)
                PLAYER_A =  str(r['league'][i]['events'][i2]['home'])
                PLAYER_B = str(r['league'][i]['events'][i2]['away'])
                # STARTS = r['league'][i]['events'][i2]['starts']
                SEARCH_RESULTS = PLAYER_A, PLAYER_B, PIN_EVENT_ID
                # print(SEARCH_RESULTS)

                if name_to_search in PLAYER_A:
                    SEARCH_RESULTS_LIST.append(SEARCH_RESULTS)
                elif name_to_search in PLAYER_B:
                    SEARCH_RESULTS_LIST.append(SEARCH_RESULTS)
                continue


    # SEARCH_RESULTS_LIST_LEN = len(SEARCH_RESULTS_LIST)
    return SEARCH_RESULTS_LIST
# x = (search_tennis_lines('Lopez'))
# print(x[0])

print(search_tennis_lines('fatic'))

