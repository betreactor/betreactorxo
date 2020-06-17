import time
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
options = Options()
options.add_argument('--headless')

from bs4 import BeautifulSoup
#pip install bs4
import time
# from database import Database

driver = webdriver.Firefox(options=options)
driver.get("https://www.flashscore.ru/")

time.sleep(1)

elements = driver.find_elements_by_css_selector("div.tabs__tab")
elements[3].click()

def track_matches(container):
    soup = BeautifulSoup(container, "html.parser")
    matches = soup.select(".event__match.event__match--live.event__match--oneLine")
    for match in matches:
        time_match = match.select_one('div.event__stage--block')
        total = match.select_one("div.event__scores.fontBold")
        home = match.select_one("div.event__participant.event__participant--home")
        away = match.select_one("div.event__participant.event__participant--away")
        oddhome = match.select_one("div.odds__odd.icon.icon--arrow.kx.o_1.null.null.odds__odd--betslip")
        odddraw = match.select_one("div.odds__odd.icon.icon--arrow.kx.o_0.null.null.odds__odd--betslip")
        oddaway = match.select_one("div.odds__odd.icon.icon--arrow.kx.o_2.null.null.odds__odd--betslip")
        print(time_match.text, total.text, home.text, '-', away.text, oddhome.text, odddraw.text, oddaway.text)


temp_hash = 0
while True:
    container = driver.find_element_by_css_selector("div[id=live-table]").get_attribute("innerHTML")
    if temp_hash != hash(container):
        track_matches(container)
        temp_hash = hash(container)

time.sleep(2)
driver.close()
# print(elements)

# myLinks= driver.find_elements_by_class_name("mbox0px l-brd")








# elements[0].click()



# def track_matches(container):
#     soup = BeautifulSoup(container, 'html.parser')
#     matches = soup.select('.event__match.event__match--scheduled.event__match--oneLine')
#     for match in matches:
#         time_match = match.select_one('div.event__time')
#         print(time_match)
# temp_hash = 0
# while True:
#     container = driver.find_element_by_css_selector("div[id=live-table]").get_attribute("innerHTML")
#     if temp_hash != hash(container):
#         track_matches(container)
#         temp_hash = hash(container)
#         pass