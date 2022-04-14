from twitchio.ext import commands
from datetime import datetime, timedelta
from multiprocessing import Process
import random
import re
import requests
import time
import reg
import cmd_construction
import indicators
import const
import randombase
import ftp
import asyncio

nicks = set()
gallows_start = False
towns_start = False
towns_world_start = False
roulette_start = False

allowBotActivity = True
restartBot = 0
countGoodCMD = 1
countBadCMD = 1
playersToServer = 1
endCMDtime = int(datetime.now().hour) * 60 * 60 + int(datetime.now().minute) * 60 + int(datetime.now().second)
endTimeBotActivity = int(datetime.now().hour) * 60 * 60 + int(datetime.now().minute) * 60 + int(datetime.now().second)

idCMD = 0
# Русская рулетка
lostShots = [1, 2, 3, 4, 5, 6]
shotNumber = 0

# Виселица
answer = ""
word = ""
errors = 0
verbs = set()

# Города
city = ""
cities = list()
last_verb = ""

if reg.nickAdmin == "":
    reg.nickAdmin = reg.nickBot

# Инициализация бота
bot = commands.Bot(
    irc_token="oauth:" + reg.secret,
    token=reg.id_token,
    nick=reg.nickBot,
    prefix="!",  # Префикс комманд (!test)
    initial_channels=[reg.channelName])


def save_message(timeMes, nick, message):
    with open("save_message.txt", "a", encoding="UTF-8") as baseMes:
        baseMes.write('[' + timeMes + '] ' + nick + ': ' + message + '\n')


def timer_round():
    ftp.connect()
    while True:
        print("timer round start")
        ftp.give_server_data(ftp.playerData)
        print("timer round playerData")
        ftp.set_server(ftp.cmdToServer)
        print("timer round cmdToServer")
        ftp.set_server(ftp.messagesToServer)
        print("timer round messagesToServer")
        cmd_construction.event_follower()
        print("timer round event_follower()")
        time.sleep(0.5)

        ftp.give_server_data(ftp.playerData)
        print("2timer round playerData")
        ftp.set_server(ftp.cmdToServer)
        print("2timer round cmdToServer")
        ftp.set_server(ftp.messagesToServer)
        print("2timer round messagesToServer")
        indicators.timer_indicator(cmd_construction)
        print("2timer round timer_indicator(cmd_construction)")
        cmd_construction.event_follower()
        print("2timer round event_follower()")
        time.sleep(0.5)


async def acync_timer_call_back(ctx):
    global restartBot
    global allowBotActivity
    print("acync_timer_call_back")
    await asyncio.sleep(10)
    print(restartBot)
    if restartBot < 20:
        restartBot += 1
        await async_timer(ctx)
    else:
        restartBot = 0
        allowBotActivity = True
        return


async def async_timer(ctx):
    print("async_timer")
    global countBadCMD
    global countGoodCMD
    global playersToServer
    global endCMDtime
    global endTimeBotActivity

    time = int(datetime.now().hour) * 60 * 60 + int(datetime.now().minute) * 60 + int(datetime.now().second)

    amountBadCMD = countGoodCMD - countBadCMD - playersToServer * 5
    amountGoodCMD = countBadCMD - countGoodCMD - playersToServer * 5

    if time - endTimeBotActivity > 600:
        typeActivity = random.randint(1, 6)
        activity = {1: "Не забываейте подписываться на канал!",
                    2: "Рекомендую посетить наш TikTok, ссылка в описании",
                    3: "Заходи на YouTube! Смотри описание данного канала",
                    4: "Хэй, не забывай подписаться на дискорд данного канала (см. описание)",
                    5: "Ты можешь поддерждать автора канала с помощью небольших пожертвований! (см. описание)",
                    6: "На этом канале есть различные развлекухи, введи команду '!help'"}
        endTimeBotActivity = time
        await ctx.send(activity[typeActivity])

    if indicators.get_for_minercaft():
        isRun = random.randint(0, 5)
        if amountBadCMD >= 5 and isRun == 2 and indicators.count_darkness_time():
            await ctx.send(randombase.bot_answers(3))
            await asyncio.sleep(3)

            for i in range(amountBadCMD):
                randCMD = randombase.random_cmd_for_bot(True)
                await ctx.send(randCMD)
                await perform_cmd(ctx, randCMD, True, True)
                await asyncio.sleep(3)

        elif amountGoodCMD >= 5 and isRun == 2:
            await ctx.send(randombase.bot_answers(2))
            await asyncio.sleep(3)

            for i in range(amountGoodCMD):
                randCMD = randombase.random_cmd_for_bot()
                await ctx.send(randCMD)
                await perform_cmd(ctx, randCMD, isBot=True)
                await asyncio.sleep(3)
        else:
            print("Бот ниечего не делает")
            await asyncio.sleep(1)

        if time - endCMDtime > 160:
            await ctx.send(randombase.bot_answers(1))
            await asyncio.sleep(3)
            endCMDtime = time

            if indicators.count_darkness_time():
                for i in range(random.randint(4, 7)):
                    randCMD = randombase.random_cmd_for_bot(True)
                    await ctx.send(randCMD)
                    await perform_cmd(ctx, randCMD, True, True)
                    await asyncio.sleep(3)

            elif not indicators.count_darkness_time():
                for i in range(random.randint(4, 7)):
                    randCMD = randombase.random_cmd_for_bot()
                    await ctx.send(randCMD)
                    await perform_cmd(ctx, randCMD, isBot=True)
                    await asyncio.sleep(3)
    await acync_timer_call_back(ctx)


@bot.event()
async def event_ready():
    print("Бот успешно запущен!")
    if indicators.get_for_minercaft() == 1:
        cmd_construction.create_chest_cmd()  # генерация сундуков в при старте бота
        x = Process(target=timer_round)
        x.start()


@bot.event()
async def event_join(ctx, ctx1):
    global allowBotActivity
    if allowBotActivity:
        if indicators.get_bot_activity():
            allowBotActivity = False
            await async_timer(ctx)


@bot.event()
async def event_usernotice_subscription(metadata):
    print("new follower")


# Основной ивент на получение информации из чата, срабатывает сразу как только приходит сообщение в чат
@bot.event()
async def event_message(ctx):
    global nicks
    # получаем ник зрителя в чате
    try:
        nick_auth = ctx.author.display_name
    except:
        nick_auth = reg.nickBot

    if nick_auth != reg.nickBot:
        print(indicators.count_darkness_time())
        if nick_auth == reg.nickAdmin:
            if ctx.content.lower()[0:9] == '!settimer':
                try:
                    indicators.refresh_timer(timerSec=int(ctx.content.lower()[9:]))
                except:
                    print('Неверное значение времени')
            elif ctx.content.lower()[0:9] == '!setround':
                try:
                    indicators.refresh_timer(gameRound=int(ctx.content.lower()[9:]))
                except:
                    print('Неверное значения раунда')
            elif ctx.content.lower()[0:9] == '!spawnoff':
                # chatcmdtomain('/gamerule doMobSpawning false')
                print('Спавн мобов отключен!')
            elif ctx.content.lower()[0:8] == '!spawnon':
                # chatcmdtomain('/gamerule doMobSpawning true')
                print('Спавн мобов включен!')

        try:
            # получаем теги цветов автора сообщения
            color = ctx.author.tags["color"] if not ctx.author.tags["color"] == "" else "#2d8acc"
        except:
            # если не вышло присваеваем синий
            color = "#2d8acc"
        # время сообщения плюс системная дата, для лога
        time_mess = datetime.strftime(ctx.timestamp + timedelta(hours=5), "%d/%m %H:%M:%S")
        # название канала
        channel_name = ctx.channel.name
        save_message(datetime.strftime(ctx.timestamp, "%H:%M:%S"), nick_auth, ctx.content)  # сохраняем сообщение в TXT
        print("#" + channel_name + "#" + nick_auth + ": " + ctx.content + ";")
        print("")
        # лог в HTML в дальнейшем вип чат
        mess = "<div style=\"background-color: #211d1d\">[" + time_mess + "]#" + channel_name + \
               "# <span style=\"font-weight: bold\">" + "<span style=\"color: " + color + "\">" + nick_auth + \
               "</span>: <span style=\"color: white\">" + ctx.content + ";</span></span></div>"

        # функция записи лога
        with open("log.html", "a") as log:
            log.write(mess + "\n")

        nicks = set()
        list_users = ctx.channel.chatters
        for nickUser in list_users:
            nicks.add(nickUser.name.strip())

        with open("users.txt", "w", encoding="UTF-8") as nick_in_file:
            for nickUser in nicks:
                print(nickUser, file=nick_in_file)

        nickAnswer = "@" + nick_auth

        # Игра Русская рулетка
        global roulette_start
        global shotNumber
        global lostShots

        if "=выстрел" in ctx.content.lower() and roulette_start:
            shot = random.choice(lostShots)
            if shotNumber == shot:
                await ctx.channel.send("/timeout " + nick_auth + " 300")
                answerBot = nickAnswer + ", ты застрелился!"
                # save_message(datetime.strftime(ctx.timestamp, "%H:%M:%S"), reg.nickBot, answerBot)
                await ctx.channel.send(answerBot)
                roulette_start = False
            else:
                lostShots.remove(shot)
                await ctx.channel.send(nickAnswer + ", осечка!")

        # Игра города
        global city
        global last_verb
        global towns_start
        global towns_world_start

        if "=" in ctx.content.lower() and (towns_start or towns_world_start):

            message = ctx.content.lower().split("=")[1]
            if message.strip().lower() in cities:
                await ctx.channel.send(nickAnswer + ", город уже был назван")
            elif message[0].strip() == last_verb:

                townWords = ""
                if towns_world_start:
                    townWords = "words/towns_world.txt"
                elif towns_start:
                    townWords = "words/towns.txt"
                list_city = open(townWords, "r", encoding="UTF-8").readlines()

                if not message.lower() in "".join(list_city).split("\n"):
                    await ctx.channel.send(nickAnswer + ", этого города нету в словаре")
                    print("Нету в словаре: " + message)
                    return

                city = message
                cityAnswer = city.capitalize()

                cities.append(city.lower().strip())

                while city[-1] == "ь" or city[-1] == "ы" or city[-1] == "й" or city[-1] == " ":
                    city = city[:-1]

                last_verb = city[-1]

                await ctx.channel.send(
                    "Город " + cityAnswer + " был назван " + nickAnswer + " следующий город на букву '" + last_verb + "'")
            else:
                await ctx.channel.send(nickAnswer + ", город на букву '" + last_verb + "'")

        # Игра виселица
        global errors
        global gallows_start
        verb = ctx.content.lower()[1]
        nickAnswer = ctx.author.name.lower()

        if "=" in ctx.content.lower() and gallows_start and len(ctx.content) == 2 and re.fullmatch("[а-я]", verb):
            # Проверяем написанную букву
            if verb in verbs:
                # Буква уже была
                await ctx.channel.send("@" + nickAnswer + ", буква уже проверена")
            elif ctx.content.lower()[1] in answer:
                # Буква угадана
                for i in range(0, len(answer)):
                    if answer[i] == verb:
                        word[i] = verb

                verbs.add(verb)

                await ctx.channel.send("@" + nickAnswer + ", буква '" + verb + "' - угадана: " + "".join(word))
            else:
                # Буква не угадана
                verbs.add(verb)

                errors += 1
                await ctx.channel.send(
                    "@" + nickAnswer + ", буква '" + verb + "' - не угадана, осталось попыток " + str(
                        6 - errors) + ": " + "".join(word))

            # Условия поражения и победы
            if answer.strip() == ("".join(word)).strip():
                gallows_start = False
                await ctx.channel.send("Победа! Слово - " + answer)
            elif errors >= 6:
                gallows_start = False
                await ctx.channel.send("Проигрыш! Слово - " + answer)

    # await bot.handle_commands(ctx)


@bot.command(name="help")
async def command_help(ctx):
    print('help')
    if indicators.get_for_minercaft() == 0:
        mess = "Доступные команды: !предсказание !виселица, !города, !городамир, !рулетка, !стоп <игра>(виселица, " \
               "города, рулетка) "
    else:
        mess = "Уточните категорию: '!helpchat', '!helpbad', '!helpgood'"
    await ctx.channel.send(
        "@" + ctx.author.display_name + " . " + mess)


@bot.command(name="helpchat")
async def command_help(ctx):
    print('helpchat')
    await ctx.channel.send(
        "@" + ctx.author.display_name + ". Доступные команды: !предсказание, !виселица, !города, !городамир, "
                                        "!рулетка, !стоп <игра>(виселица, города, рулетка)")


@bot.command(name="helpbad")
async def command_help(ctx):
    print('helpbad')
    if indicators.get_for_minercaft() == 1:
        await ctx.channel.send(
            "@" + ctx.author.display_name + ". Доступные команды: 1 раунд: !random, !zombie, !skeleton, !spider, "
                                            "!lightning, !wakeup, !crasher, !tnt, !boss; 2 раунд: !creeper, !hell, "
                                            "!reaper; 3 раунд: !thaum, !twil, !parasite; 4 раунд: !icefire 4 раунд: "
                                            "!lparasite")


@bot.command(name="helpgood")
async def command_help(ctx):
    print('helpgood')
    if indicators.get_for_minercaft() == 1:
        await ctx.channel.send(
            "@" + ctx.author.display_name + ". Доступные команды: 1 раунд: !random, !animal, !human, !cookie, !heal, "
                                            "!weapon, !armor, !give; 2 раунд: !beast, !dwarf; 3 раунд:  !elf, !faun, "
                                            "!centaur; 4 раунд:  !furry, !naga; 5 раунд: !orc")


@bot.command(name="follow")
async def follow_date(ctx):
    try:
        channel = reg.channelName
        headers = {'Client-ID': reg.id_token, 'Authorization': 'Bearer ' + reg.secret, }

        channel_id_GET = requests.get("https://api.twitch.tv/helix/users?login=" + channel, headers=headers)
        channel_id = str(channel_id_GET.json()["data"][0]["id"])

        response = requests.get('https://api.twitch.tv/helix/users/follows?from_id=' + str(
            ctx.author.tags["user-id"]) + "&to_id=" + channel_id, headers=headers)

        time.sleep(2)

        time_follow = response.json()["data"][0]["followed_at"]
        time_follow = datetime.strptime(time_follow, "%Y-%m-%dT%H:%M:%SZ")

        await ctx.channel.send(
            "@" + ctx.author.name + ", подписался на канал - " + datetime.strftime(time_follow, "%H:%M:%S %d/%m/%Y"))
    except:
        await ctx.channel.send("@" + ctx.author.name + ", это Ваш канал")


@bot.command(name="time")
async def give_time_chatting(ctx):
    nick = ctx.author.name
    target = ctx.content.split(" ")[1] if len(ctx.content.split(" ")) > 1 else nick

    with open("time.txt", "r+", encoding="UTF-8") as file_read:
        file_content = file_read.readlines()
        nicks_file = []
        times = []

        for i in range(0, len(file_content)):
            nicks_file.append(file_content[i].split(":")[0].strip())
            times.append(file_content[i].split(":")[1].strip())

        if nick == target:
            if not nick in nicks_file:
                print(target + ":0", file=file_read)
                times.append("0")

            await ctx.channel.send(
                "@" + nick + ", находится в чате - " + str(int(times[nicks_file.index(nick)]) // 60) + " часов " + str(
                    int(times[nicks_file.index(nick)]) % 60) + " минут")
        else:
            if not target in nicks_file:
                await ctx.channel.send("@" + nick + ", такой пользователь не найден")
                return

            await ctx.channel.send("@" + nick + ", " + target + " находится в чате - " + str(
                int(times[nicks_file.index(target)]) // 60) + " часов " + str(
                int(times[nicks_file.index(target)]) % 60) + " минут")


@bot.command(name="рулетка")
async def game_chat(ctx):
    global roulette_start
    global shotNumber
    global lostShots

    if roulette_start:
        return

    lostShots = [1, 2, 3, 4, 5, 6]
    shotNumber = random.randint(1, 6)

    roulette_start = True
    await ctx.channel.send("Игра 'Русская рулетка' началась(=выстрел)")


@bot.command(name="виселица")
async def game_chat(ctx):
    global gallows_start
    global answer
    global word
    global errors
    global verbs

    if gallows_start:
        return

    words = open("words/gallow.txt", "r", encoding="UTF-8").readlines()

    errors = 0
    verbs = set()
    answer = words[random.randint(0, len(words) - 1)]
    word = list("_" * (len(answer) - 1))

    print("Ответ: " + answer)
    gallows_start = True
    await ctx.channel.send("Игра 'Виселица' началась, написать букву '=а' - Загадано слово " + "".join(word))


@bot.command(name="города")
async def game_chat(ctx):
    global city
    global towns_start
    global towns_world_start
    global cities
    global last_verb

    if towns_start or towns_world_start:
        return

    cities = list()
    list_city = open("words/towns.txt", "r", encoding="UTF-8").readlines()
    city = list_city[random.randint(0, len(list_city) - 1)]
    city = city.strip("\n")
    cityAnswer = city.capitalize()
    cities.append(city.strip().lower())

    while city[-1] == "ь" or city[-1] == "ы" or city[-1] == "й" or city[-1] == " ":
        city = city[:-1]

    last_verb = city[-1]

    towns_start = True
    await ctx.channel.send("Игра 'Города' началась(=Кузнецк), первый город - " + cityAnswer)


@bot.command(name="городамир")
async def game_chat(ctx):
    global city
    global towns_world_start
    global cities
    global last_verb
    global towns_start

    if towns_world_start or towns_start:
        return

    cities = list()
    list_city = open("words/towns_world.txt", "r", encoding="UTF-8").readlines()
    city = list_city[random.randint(0, len(list_city) - 1)]
    city = city.strip("\n")
    cityAnswer = city.capitalize()
    cities.append(city.strip().lower())
    print(city)

    while city[-1] == "ь" or city[-1] == "ы" or city[-1] == "й" or city[-1] == " ":
        city = city[:-1]

    last_verb = city[-1]
    towns_world_start = True
    await ctx.channel.send("Игра 'Города' началась(=Детройт), первый город - " + cityAnswer)


@bot.command(name="предсказание")
async def game_chat(ctx):
    nick = ctx.author.display_name

    firstWords = open("words/ball_first_words.txt", "r", encoding="UTF-8").readlines()
    first = firstWords[random.randint(0, len(firstWords) - 1)]

    if random.randint(1, 4) != 1:
        secondWords = open("words/ball_second_words.txt", "r", encoding="UTF-8").readlines()
        second = secondWords[random.randint(0, len(secondWords) - 1)]
    else:
        second = ''

    thirdWords = open("words/ball_third_words.txt", "r", encoding="UTF-8").readlines()
    third = thirdWords[random.randint(0, len(thirdWords) - 1)]

    fourthWords = open("words/ball_fourth_words.txt", "r", encoding="UTF-8").readlines()
    fourth = fourthWords[random.randint(0, len(fourthWords) - 1)]

    if random.randint(1, 4) != 1:
        fifthWords = open("words/ball_fifth_words.txt", "r", encoding="UTF-8").readlines()
        fifth = fifthWords[random.randint(0, len(fifthWords) - 1)]
    else:
        fifth = ''

    await ctx.channel.send('@' + nick + ', ' + first + ' ' + second + ' ' + third + ' ' + fourth +
                           ' ' + fifth)


@bot.command(name="стоп")
async def stop_game(ctx, game):
    global gallows_start
    global towns_start
    global towns_world_start
    global roulette_start

    if game == "виселица":

        if not gallows_start:
            return

        gallows_start = False
        await ctx.channel.send("Игра 'Виселица' закончилась")
    elif game == "города":

        if not towns_start and not towns_world_start:
            return

        towns_world_start = False
        towns_start = False
        await ctx.channel.send("Игра 'Города' закончилась")
    elif game == "рулетка":

        if not roulette_start:
            return

        roulette_start = False
        await ctx.channel.send("Игра 'Русская рулетка' закончилась")
    else:
        await ctx.channel.send("@" + ctx.author.name + ", игры не существует")


async def perform_cmd(ctx, cmd: str, badCMD: bool = False, gameRound: int = 0, isBot: bool = False):
    global countBadCMD
    global countGoodCMD
    global endCMDtime

    if indicators.get_for_minercaft() == 0:
        # await ctx.channel.send("@" + ctx.author.name + ", эта команда только для Minercaft")
        return

    if not isBot:
        nick = ctx.author.display_name
        channel = ctx.channel
    else:
        nick = reg.nickBot
        channel = ctx

    time = int(datetime.now().hour) * 60 * 60 + int(datetime.now().minute) * 60 + int(datetime.now().second)
    endCMDtime = time

    def dark_condition():
        if badCMD:
            return indicators.count_darkness_time()
        else:
            return True

    def round_condition():
        if gameRound == 0:
            return True
        elif gameRound <= indicators.count_round():
            return True
        else:
            return False

    if not badCMD:
        castialAlive = indicators.game_data()["gameData"]["castial"]
    else:
        castialAlive = 1
    hour = str(int(datetime.now().strftime("%H"))-5) + ":"

    await asyncio.sleep(0.3)
    if (time - const.lastTimeCMD[cmd] >= const.timerCMD[cmd] and dark_condition() and
        round_condition() and castialAlive == 1) or nick == reg.nickBot:

        const.lastTimeCMD[cmd] = time

        if cmd == "!random":
            cmd = randombase.weighted_pick(dict(const.weightChatCMDBad, **const.weightChatCMDGood))

        if cmd == "!wakeup":
            if random.randint(1, 5) == 3:
                returnCMD = cmd_construction.start_cmd(nick, cmd)
            else:
                answerBot = "@" + nick + ", Призвать мертвых не удалось!"
                save_message(hour + datetime.now().strftime("%M:%S"), reg.nickBot, answerBot)
                await ctx.channel.send(answerBot)
        else:
            returnCMD = cmd_construction.start_cmd(nick, cmd)

        if badCMD:
            countBadCMD += 1
        else:
            countGoodCMD += 1

        indicators.complete_command(nick, returnCMD, "", badCMD)
        # await ctx.channel.send("@" + nick + ", команда выполнена!")
    elif not dark_condition():
        answerBot = "@" + nick + ", время 'Тьмы' еще не наступило!"
        save_message(hour + datetime.now().strftime("%M:%S"), reg.nickBot, answerBot)
        await channel.send(answerBot)

    elif not round_condition():
        answerBot = "@" + nick + ", команда будет доступна на " + str(gameRound) + " раунде!"
        save_message(hour + datetime.now().strftime("%M:%S"), reg.nickBot, answerBot)
        await channel.send(answerBot)

    elif castialAlive == 0:
        answerBot = "@" + nick + ", Кастиэль мертв! У сил света нет больше власти!"
        save_message(hour + datetime.now().strftime("%M:%S"), reg.nickBot, answerBot)
        await channel.send(answerBot)
    else:
        answerBot = "@" + nick + ", команда будет доступна через: " + str(
            const.timerCMD[cmd] - time + const.lastTimeCMD[cmd]) + '(сек)'
        save_message(hour + datetime.now().strftime("%M:%S"), reg.nickBot, answerBot)
        await channel.send(answerBot)


@bot.command(name="random")
async def minecraft_cmd(ctx):
    await perform_cmd(ctx, "!random")


@bot.command(name="animal")
async def minecraft_cmd(ctx):
    await perform_cmd(ctx, "!animal")


@bot.command(name="cookie")
async def minecraft_cmd(ctx):
    await perform_cmd(ctx, "!cookie")


@bot.command(name="heal")
async def minecraft_cmd(ctx):
    await perform_cmd(ctx, "!heal")


@bot.command(name="weapon")
async def minecraft_cmd(ctx):
    await perform_cmd(ctx, "!weapon")


@bot.command(name="armor")
async def minecraft_cmd(ctx):
    await perform_cmd(ctx, "!armor")


@bot.command(name="give")
async def minecraft_cmd(ctx):
    await perform_cmd(ctx, "!give")


@bot.command(name="beast")
async def minecraft_cmd(ctx):
    await perform_cmd(ctx, "!beast", gameRound=2)


@bot.command(name="human")
async def minecraft_cmd(ctx):
    await perform_cmd(ctx, "!human")


@bot.command(name="dwarf")
async def minecraft_cmd(ctx):
    await perform_cmd(ctx, "!dwarf", gameRound=2)


@bot.command(name="elf")
async def minecraft_cmd(ctx):
    await perform_cmd(ctx, "!elf", gameRound=3)


@bot.command(name="faun")
async def minecraft_cmd(ctx):
    await perform_cmd(ctx, "!faun", gameRound=3)


@bot.command(name="centaur")
async def minecraft_cmd(ctx):
    await perform_cmd(ctx, "!centaur", gameRound=3)


@bot.command(name="furry")
async def minecraft_cmd(ctx):
    await perform_cmd(ctx, "!furry", gameRound=4)


@bot.command(name="naga")
async def minecraft_cmd(ctx):
    await perform_cmd(ctx, "!naga", gameRound=4)


@bot.command(name="orc")
async def minecraft_cmd(ctx):
    await perform_cmd(ctx, "!orc", gameRound=5)


# bad commands--------------------------------------
@bot.command(name="zombie")
async def minecraft_cmd(ctx):
    await perform_cmd(ctx, "!zombie", True)


@bot.command(name="skeleton")
async def minecraft_cmd(ctx):
    await perform_cmd(ctx, "!skeleton", True)


@bot.command(name="spider")
async def minecraft_cmd(ctx):
    await perform_cmd(ctx, "!spider", True)


@bot.command(name="creeper")
async def minecraft_cmd(ctx):
    await perform_cmd(ctx, "!creeper", True, gameRound=2)


@bot.command(name="hell")
async def minecraft_cmd(ctx):
    await perform_cmd(ctx, "!hell", True, gameRound=2)


@bot.command(name="thaum")
async def minecraft_cmd(ctx):
    await perform_cmd(ctx, "!thaum", True, gameRound=3)


@bot.command(name="twil")
async def minecraft_cmd(ctx):
    await perform_cmd(ctx, "!twil", True, gameRound=3)


@bot.command(name="parasite")
async def minecraft_cmd(ctx):
    await perform_cmd(ctx, "!parasite", True, gameRound=3)


@bot.command(name="icefire")
async def minecraft_cmd(ctx):
    await perform_cmd(ctx, "!icefire", True, gameRound=4)


@bot.command(name="lparasite")
async def minecraft_cmd(ctx):
    await perform_cmd(ctx, "!lparasite", True, gameRound=5)


@bot.command(name="boss")
async def minecraft_cmd(ctx):
    await perform_cmd(ctx, "!boss", True)


@bot.command(name="lightning")
async def minecraft_cmd(ctx):
    await perform_cmd(ctx, "!lightning", True)


@bot.command(name="tnt")
async def minecraft_cmd(ctx):
    await perform_cmd(ctx, "!tnt", True)


@bot.command(name="crasher")
async def minecraft_cmd(ctx):
    await perform_cmd(ctx, "!crasher", True)


@bot.command(name="reaper")
async def minecraft_cmd(ctx):
    await perform_cmd(ctx, "!reaper", True, gameRound=2)


@bot.command(name="wakeup")
async def minecraft_cmd(ctx):
    await perform_cmd(ctx, "!wakeup", True)


# Старт бота

if __name__ == "__main__":
    # ftp.connect()
    bot.run()
