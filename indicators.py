import json
import random
import math
import configparser
import gifs_base
import strings


def game_data():
    while True:
        try:
            # with open('C:/Users/user123/AppData/Roaming/.minecraft/saves/Новый мир/customnpcs/myjson/player_data.json',
            with open('player_data.json', 'r') as file:
                reading_json = file.read()
                templates = json.loads(reading_json)
                # print(templates)
        except:
            continue
        else:
            return templates


def sec_to_time(sec):
    hours = math.floor(sec / 60 / 60)
    minute = math.floor(sec / 60) - hours * 60
    second = sec - minute * 60 - hours * 60 * 60
    if second < 10:
        second = '0' + str(second)
    else:
        second = str(second)
    if minute < 10:
        minute = '0' + str(minute)
    else:
        minute = str(minute)
    if hours < 1:
        hours = ''
    else:
        hours = str(hours) + ':'
    timer = hours + minute + ':' + second
    return timer


def get_timer():
    while True:
        try:
            timerState = configparser.ConfigParser()
            timerState.read('timer_state.ini')
            timerSec = timerState.getint('Timer', 'int_timenow')
            timerSec = sec_to_time(timerSec)
        except:
            continue
        else:
            return timerSec



def timer_indicator(cmdConstruction):
    while True:
        try:
            timerState = configparser.ConfigParser()
            timerState.read('timer_state.ini')
            timerSec = timerState.getint('Timer', 'int_timenow')
            darknessTime = timerState.getboolean('Timer', 'bool_darknessTime')
            gameRound = timerState.getint('Timer', 'int_roundnow')

            if timerSec == 0 and darknessTime:
                darknessTime = False
                gameRound += 1
                timerSec = 720
                cmdConstruction.save_chat_cmd("cmd", "cmd", "/gamerule doDaylightCycle true")
                print('Обычный режим')

            elif timerSec == 0 and not darknessTime:
                darknessTime = True
                timerSec = 600

                cmdConstruction.save_chat_cmd("cmd", "cmd", "/time set 22500")
                cmdConstruction.save_chat_cmd("cmd", "cmd", "/gamerule doDaylightCycle false")
                print('Режим ада')

            if not darknessTime:
                textToRound = 'Тьма наступит через: '
            else:
                textToRound = 'Конец тьмы через: '

            timerstream = open('timer.txt', 'w', encoding="utf-8")
            timerstream.write(textToRound + sec_to_time(timerSec) + '\nРаунд: ' + str(gameRound))
            timerstream.close()
            timerSec -= 1
            refresh_timer(timerSec, darknessTime, gameRound)
        except:
            continue
        else:
            break


def refresh_timer(timerSec: int = None, darknessTime: bool = None, gameRound: int = None):
    while True:
        try:
            timerState = configparser.ConfigParser()
            timerState.read('timer_state.ini')

            if timerSec is not None:
                timerState.set('Timer', 'int_timenow', str(timerSec))

            if darknessTime is not None:
                timerState.set('Timer', 'bool_darknessTime', str(darknessTime))

            if gameRound is not None:
                timerState.set('Timer', 'int_roundnow', str(gameRound))

            with open('timer_state.ini', 'w', encoding="UTF-8") as configfile:
                timerState.write(configfile)
        except:
            continue
        else:
            break


def count_darkness_time():
    while True:
        try:
            timerState = configparser.ConfigParser()
            timerState.read('timer_state.ini')
            boolDarknessTime = timerState.getboolean('Timer', 'bool_darknessTime')
        except:
            continue
        else:
            return boolDarknessTime


def count_round():
    while True:
        try:
            timerState = configparser.ConfigParser()
            timerState.read('timer_state.ini')
            intRound = timerState.getint('Timer', 'int_roundnow')
        except:
            continue
        else:
            return intRound


def save_followers(followers: str):
    while True:
        try:
            timerState = configparser.ConfigParser()
            timerState.read('timer_state.ini')
            timerState.set('Timer', 'int_followers', followers)
            with open('timer_state.ini', 'w', encoding="UTF-8") as configfile:
                timerState.write(configfile)
        except:
            continue
        else:
            break


def get_followers():
    while True:
        try:
            timerState = configparser.ConfigParser()
            timerState.read('timer_state.ini')
            followers = timerState.getint('Timer', 'int_followers')
        except:
            continue
        else:
            return followers


def get_followers_max():
    while True:
        try:
            timerState = configparser.ConfigParser()
            timerState.read('timer_state.ini')
            followers = timerState.getint('Timer', 'int_followers_max')
        except:
            continue
        else:
            return followers
    # return followers


def get_for_minercaft():
    while True:
        try:
            timerState = configparser.ConfigParser()
            timerState.read('timer_state.ini')
            forMinecraft = timerState.getint('Timer', 'int_for_minecraft')
        except:
            continue
        else:
            return forMinecraft


def get_bot_activity():
    while True:
        try:
            timerState = configparser.ConfigParser()
            timerState.read('timer_state.ini')
            botActivity = timerState.getint('Timer', 'int_bot_activity')
        except:
            continue
        else:
            return botActivity


def create_indicators_config(followersMax, forMinecraft, botActivity):
    timerState = configparser.ConfigParser()
    timerState.add_section('Timer')
    timerState.set('Timer', 'int_timenow', '600')
    timerState.set('Timer', 'bool_darknessTime', 'false')
    timerState.set('Timer', 'int_roundnow', '1')
    timerState.set('Timer', 'int_followers', '0')
    timerState.set('Timer', 'int_followers_max', followersMax)
    timerState.set('Timer', 'int_for_minecraft', forMinecraft)
    timerState.set('Timer', 'int_bot_activity', botActivity)
    with open('timer_state.ini', 'w', encoding="UTF-8") as configfile:
        timerState.write(configfile)


def complete_command(nick, cmd, extraCmd, isBadCMD: bool = False):
    if isBadCMD:
        gifs = random.choice(gifs_base.gif_bad)
        try:
            cmd = strings.cmdTranslate[cmd]
        except:
            cmd = cmd
        try:
            extraCmd = strings.cmdTranslate[extraCmd]
        except:
            extraCmd = extraCmd
        message = '<divbad class="child"><span class="textbad"><span>' + nick + '</span><br><span>' + cmd + ' ' \
                  + extraCmd + '</span></strong></span><img class="gifsbad" src="' + gifs + '"></divbad>'
    else:
        gifs = random.choice(gifs_base.gif_good)
        try:
            cmd = strings.cmdTranslate[cmd]
        except:
            cmd = cmd
        try:
            extraCmd = strings.cmdTranslate[extraCmd]
        except:
            extraCmd = extraCmd
        message = '<divgood class="child"><img  class="gifsgood" src="' + gifs + \
                  '"><span><span class="textgood"><span>' + nick + '</span><br><span>' + cmd + ' ' + extraCmd + \
                  '</span></span></span></divgood>'

    with open("complete_cmd.html", "a", encoding="UTF-8") as addcmd:
        addcmd.write(message + "\n")
