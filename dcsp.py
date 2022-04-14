import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options
from logzero import logger, logfile
import indicators
import subprocess
import cmd_construction
import const

options = Options()
options.add_argument("--headless")
ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)

logfile('my_logfile.log')

driver = webdriver.Chrome(executable_path='C:/chromedriver/chromedriver.exe', options=options)
# driver = webdriver.Chrome(executable_path='C:\chromedriver\chromedriver.exe')
driver.get('https://www.donationalerts.com/widget/alerts?group_id=1&token=F8wSQ9uevmrKgLHklKfg')
driver.execute_script(
    "window.open('https://www.donationalerts.com/widget/instream-stats?id=1385623&token=F8wSQ9uevmrKgLHklKfg')")
driver.switch_to.window(driver.window_handles[0])

donationConstant = ('', '', '')

finalText = ('', '', '')
finalTextSecurity = ('', '', '')

print('Ведите количество подписчиков необходимое для запуска события')
followersMax = input()

print('Взаимодействие с Minecraft? 1 - да, 0 - нет')
forMinecraft = input()

print('Разрешить участвовать боту? 1 - да, 0 - нет')
botActivity = input()

indicators.create_indicators_config(followersMax, forMinecraft, botActivity)

print('Нажмите ввод для начала работы программы и старта отсчета')
input()

if __name__ == "__main__":
    processBot = subprocess.Popen(["python", "bottwich.py"])

# цикл для поиска сообщения о донате ---------------------------------------------------------------------------------
while True:
    if indicators.get_for_minercaft() == 0:
        continue

    # indicators.timer_indicator()
    try:
        findClass = WebDriverWait(driver, 0, ignored_exceptions=ignored_exceptions).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, ".image_top__text_bottom")))
        findtext = findClass.text
    except:
        findtext = ''

    # Выделяем три основных показателя и собираим их в список
    name = findtext[:findtext.find("-") - 1]
    sumWithoutSpace = findtext[findtext.find("-") + 2:findtext.find("/") - 5]
    sumDonation = sumWithoutSpace.split()
    sumDonation = ''.join(sumDonation)
    sumDonation = sumDonation.replace(',', '.')
    message = findtext[findtext.find("/") + 2:]

    donationConstant = [name, sumDonation, message]
    # Основное условие проверяющее донат на повторы и его отсутствие
    if donationConstant == finalTextSecurity:
        print('нет изменений в донатах(повтор)')
    elif findtext == '':
        print('нет изменений в донатах')
    else:
        finalTextSecurity = donationConstant
        finalText = donationConstant
        # Проверка на значение суммы, десятичные или целые
        try:
            finalTextSum = int(finalText[1])
        except:
            finalTextSum = float(finalText[1])

        # Ищем необходимую сумму в таблице с защитой от неверных сумм
        sumCount = False
        sumError = False
        sumSmall = False
        commandCount = []

        while not sumCount:
            if str(finalTextSum) in const.donationSum:
                commandCount = const.donationSum[str(finalTextSum)]
                sumCount = True
            elif finalTextSum < 25:
                sumSmall = True
                sumCount = True
            else:
                sumError = True
                finalTextSum = round(finalTextSum - 0.1, 1)
                # print(finalTextSum)
                if finalTextSum < 0:
                    finalTextSum = 25

        if sumCount and not sumSmall:
            for i in range(commandCount[1]):

                if commandCount[0][:1] == "!":
                    cmd_construction.start_cmd(finalText[0], commandCount[0])
                elif commandCount == "iceandfire:firedragon" or commandCount == 'iceandfire:icedragon':
                    cmd_construction.smn_base_bad(finalText[0], commandCount[0], ",AgeTicks:1956400")
                else:
                    cmd_construction.smn_hard_bad(finalText[0], commandCount[0], "")

        elif sumCount and sumSmall:
            print("Сумма меньше минимальной")

    # ______________________________________________________

    driver.switch_to.window(driver.window_handles[1])

    findFollowers = WebDriverWait(driver, 0, ignored_exceptions=ignored_exceptions).until(
        ec.presence_of_all_elements_located((By.CSS_SELECTOR, ".word-container")))
    followers = findFollowers[0].text
    indicators.save_followers(followers)
    driver.switch_to.window(driver.window_handles[0])


    time.sleep(1)
