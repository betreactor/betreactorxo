import psycopg2
import uuid
from datetime import datetime, timedelta
import requests
import re
import os
from dotenv import load_dotenv
load_dotenv()
import os
from pathlib import Path  # python3 only
env_path = Path('d:') / '.env'
load_dotenv(dotenv_path=env_path)
from blockcypher import get_address_details

token = os.getenv("ps3838")
hostdb = os.getenv("host")
dbtoken = os.getenv("db")
userdb = os.getenv("userdb")
passworddb = os.getenv("passworddb")
tgtoken=os.getenv("tgtoken")



from decimal import Decimal
TWO = Decimal(10) ** -2

# database
def uuider():
    uuidhex64 = uuid.uuid4().hex
    return(uuidhex64)

con = psycopg2.connect(
            host=hostdb,
            database=dbtoken,
            user=userdb,
            password=passworddb)

# FINANCE
def usd_rates():
    r = requests.get('https://api.exchangeratesapi.io/latest?base=USD')

    currencies = r.json()
    usd_rub = round(currencies['rates']['RUB'],2)
    usd_eur = round(currencies['rates']['EUR'],2)
    usd_thb = round(currencies['rates']['THB'],2)
    usd_ils = round(currencies['rates']['ILS'],2)
    usd_nzd = round(currencies['rates']['NZD'],2)

    return usd_rub, usd_eur, usd_thb, usd_ils, usd_nzd
def btc_usd():
    r = requests.get('https://blockchain.info/ticker')

    btcprice = r.json()
    price = float(btcprice['USD']['last'])
    return price
def check_btc_confs():
    # https://www.blockcypher.com/dev/bitcoin/?python#wallet
    btcaddr = input('Please enter BTC wallet to check:')
    r = get_address_details(btcaddr)


    transactions_count = len(r['txrefs'])
    if transactions_count > 3:
        transactions_count = 3

    for i in range (0, transactions_count):

        tr = r['txrefs'][i]
        amount = float(r['txrefs'][i]['value'])
        amount_btc = amount/100000000
        amount_btc_usd = round(amount_btc * btc_usd(),2)
        conf = r['txrefs'][i]['confirmations']

        if conf == 0:
            conf_str = 'Not confirmed'
        if conf == 1:
            conf_str = '1 Confirmation'
        if conf >1:
            conf = str(conf)
            conf_str = conf + ' Confirmations'
        print(amount_btc, " BTC")
        print(amount_btc_usd, '     USD')
        print(conf_str)
        print('================')



# SPORT BETTING
# DB
def create_events():
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS events (uuid UUID, idpin INT, league_id INT, home TEXT, away TEXT, starttime TEXT)')
    con.commit()
def create_odds_pin_soccer():
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS odds_pin_soccer (uuid UUID, home FLOAT(2), draw FLOAT(2), away FLOAT(2))')
    con.commit()
def create_tennis_league():
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS tennis_league (id INT, league TEXT)')
    con.commit()
    print('Success!')
    con.close()
def create_liga_soccer():
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS liga_soccer (id INT, liga TEXT)')
    con.commit()
def fill_soccer_liga():
    r = requests.get('http://api.ps3838.com/v1/leagues?sportId=29 ', headers={"Authorization": token})
    r = r.json()

    num = 0


    for i in range(0, 1623):
        idd = r['leagues'][i]['id']
        lig = str(r['leagues'][i]['name'])
        num += 1

        cur = con.cursor()
        cur.execute("INSERT INTO liga_soccer (id, liga) VALUES ((%(x)s), (%(y)s))", {'x':idd, 'y':lig})
        print(num, idd, lig)
        con.commit()
def fill_tennis_league():
    r = requests.get('http://api.ps3838.com/v1/leagues?sportId=33 ', headers={"Authorization": token})
    r = r.json()

    print(r)
    COUNT = 0
    for x in r:
        if isinstance(r[x], list):
            COUNT += len(r[x])



    for i in range(0, COUNT):
        IDD = r['leagues'][i]['id']
        LEAGUE = str(r['leagues'][i]['name'])

        cur = con.cursor()
        cur.execute("INSERT INTO tennis_league (id, league) VALUES ((%(IDD)s), (%(LEAGUE)s))", {'IDD':IDD, 'LEAGUE':LEAGUE})
        print(IDD, LEAGUE)
        con.commit()


# get line
#         r = requests.get('http://api.ps3838.com/v1/line?sportid=29&oddsformat=decimal&leagueid='
#                          + ligid + '&eventID=' + pinid + '&periodNumber=0&bettype=MONEYLINE&team=DRAW',
#                          headers={"Authorization": token})

def get_sports():
    r = requests.get('http://api.ps3838.com/v1/sports', headers={"Authorization": token})
    sports = r.json()

    count = 0
    for x in sports:
        count = len(sports[x])

    print(count)

    for i in range (0,count):
        print(sports['sports'][i]['id'], sports['sports'][i]['name'])
def check_soccer_tour_by_id(a):

    cur = con.cursor()
    cur.execute("SELECT liga FROM liga_soccer WHERE id=(%(x)s)", {'x':a})
    con.commit()
    data = cur.fetchone()
    print(data[0])
    return data[0]
def get_odds_pin_moneyline_events():

    cur = con.cursor()
    cur.execute("SELECT league_id FROM events")
    con.commit()
    data = [r[0] for r in cur.fetchall()]
    data = str(list(dict.fromkeys(data)))[1:-1]
    league_ids = re.sub('[ ]', '', data)

    r = requests.get('http://api.ps3838.com/v1/odds?sportid=29&oddsformat=decimal&leagueids='+league_ids, headers={"Authorization": token})
    r = r.json()

    cur = con.cursor()
    cur.execute("SELECT idpin FROM events")
    con.commit()
    idpinlist = [r[0] for r in cur.fetchall()]
    idpinlist = list(dict.fromkeys(idpinlist))
    len_pinidlist = len(idpinlist)



    count = len(r['leagues'])
    for i in range(0, count):

        games_in_league = len(r['leagues'][i]['events'])

        for i2 in range(0, games_in_league):
            data = r['leagues'][i]['events'][i2]['id']

            for i3 in range(0, len_pinidlist):
                if (data == idpinlist[i3]):


                    cur.execute("SELECT uuid FROM events WHERE idpin = (%(idpin)s)", {'idpin':idpinlist[i3]})
                    con.commit()

                    gameuid = str([r[0] for r in cur.fetchall()])[2:-2]

                    odds_3way = r['leagues'][i]['events'][i2]['periods'][0]['moneyline']
                    odds_totals = r['leagues'][i]['events'][i2]['periods'][0]['totals'][0]
                    odds_3way_away = float(odds_3way['away'])
                    odds_3way_home = float(odds_3way['home'])
                    odds_3way_draw = float(odds_3way['draw'])

                    cur = con.cursor()
                    cur.execute("UPDATE odds_pin_soccer "
                                "SET home = (%s),"
                                "draw = (%s),"
                                "away = (%s)"
                                "WHERE uuid = (%s)",
                                (odds_3way_home, odds_3way_draw, odds_3way_away, gameuid))
                    con.commit()

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
        for i2 in range(0, count_events_in_league):
            data = r['leagues'][i]['events'][i2]['id']

            odds_3way = r['leagues'][i]['events'][i2]['periods'][0]['moneyline']
            odds_totals = r['leagues'][i]['events'][i2]['periods'][0]['totals'][0]
            odds_3way_away = float(odds_3way['away'])
            odds_3way_home = float(odds_3way['home'])
            odds_3way_draw = float(odds_3way['draw'])

            for i3 in range(0, leneventidlist):
                eventidlist[i3] = int(eventidlist[i3])
                if (data == eventidlist[i3]):
                    cur = con.cursor()
                    cur.execute("UPDATE odds "
                                "SET odd1 = (%s),"
                                "odd2 = (%s),"
                                "odd3 = (%s)"
                                "WHERE uuid = (%s) "
                                "AND game = (%s)"
                                "AND bk = (%s)",
                                (odds_3way_home, odds_3way_draw, odds_3way_away, uuid, 'ML', 'PIN'))
                    print('Pinnacle odds updated successfully')
                    con.commit()
                    con.close()




        # cur = con.cursor()
        # cur.execute('SELECT idpin, league_id FROM events WHERE uuid = %s AND bk = %s', (uuid, 'pin'))
        # con.commit()
        #
        # pindata = (cur.fetchone())
        # idpin = pindata[0]
        # leagueid = pindata[1]


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

# calculation
# surebet
def surebet_2way(odd1, odd2: float = 1.00) -> Decimal:

    position = (1/q1+1/q2)
    if position < 1:
        inversion = 1/position
        inversion = Decimal((inversion - 1) * 100).quantize(TWO)
    else:
        inversion = Decimal((position - 1) * 100 *-1).quantize(TWO)
    return (inversion)
def surebet_3way(odd1, odd2, odd3: float = 1.00) -> Decimal:

    position = (1/q1+1/q2+1/q3)
    if position < 1:
        inversion = 1/position
        inversion = Decimal((inversion - 1) * 100).quantize(TWO)
    else:
        inversion = Decimal((position - 1)*100*-1).quantize(TWO)
    return (inversion)
def place_surebet(odd1, odd2, amount_soft: float = 1.00) -> Decimal:
    surebet = surebet_2way(odd1, odd2)
    amount_pin = round(amount_soft * odd2 / odd1, 2)
    soft_win = round(odd2 * amount_soft - amount_soft - amount_pin,2)
    pin_win = round(odd1 * amount_pin - amount_pin - amount_soft,2)

    print('SUREBET      {}%            '.format(surebet))
    print('')
    print('                          PIN     BET365')
    print('ODDS                      {}    {}'.format(odd1, odd2))
    print('STAKE        EUR          {}      {}'.format(amount_soft, amount_pin))
    print('PROFIT       EUR          {}    {}'.format(pin_win, soft_win))
# place_surebet(2.14, 2.03, 80)


# value
def pro_to_dec(probability: float = 1.00) -> Decimal:
    """
    :param probability:
    :return: dec_odds: Decimal odds
    """
    dec_odds = Decimal(100 / probability).quantize(TWO)
    return dec_odds
def dec_to_pro(odds: int = 100) -> Decimal:
    pro_dec = Decimal(1/q*100).quantize(TWO)
    return pro_dec
def value_bet(odds: float = 1.00, probability: int = 100) -> Decimal:
    # value if > 1
    val = Decimal(q * probability / 100).quantize(TWO)
    return  val
#  odds format http://www.aussportsbetting.com/tools/online-calculators/odds-conversion-calculator/
def us_to_dec(odds: int = 100) -> Decimal:
    """
    :param odds: int value of American odds positive or negative
    :return: dec_odds: Decimal odds
    """
    if odds >= 0:
        dec_odds = Decimal((odds / 100) + 1).quantize(TWO)
    else:
        dec_odds = Decimal((100 / abs(odds)) + 1).quantize(TWO)
    return dec_odds
def mal_to_dec(odds: float = 1) -> Decimal:
    """
    :param odds: float value of Malay odds positive or negative
    :return: dec_odds: Decimal odds
    """
    if odds >= 0:
        dec_odds = Decimal(odds + 1).quantize(TWO)
    else:
        dec_odds = Decimal(1 + (1 / abs(odds))).quantize(TWO)
    return dec_odds
def hk_to_dec(odds: float = 1.00) -> Decimal:
    """
    :param odds: float Hong Kong odds
    :return: dec_odds: Decimal odds
    """
    dec_odds = Decimal(odds + 1).quantize(TWO)
    return dec_odds
def ind_to_dec(odds=1.00):
    """
    :param odds: float value of Indonesian odds positive or negative
    :return: dec_odds: Decimal odds
    """
    if odds >= 0:
        dec_odds = Decimal(odds + 1).quantize(TWO)
    else:
        dec_odds = Decimal(1 + (1 / abs(odds))).quantize(TWO)
    return dec_odds



