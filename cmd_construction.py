import randombase as rand
import const
import random
import indicators

dictPosGood = {"1": const.spawn3, "3": const.spawn2, "6": const.spawn1}
dictPosBad = {"0": const.spawn3, "1": const.spawn2, "3": const.spawn1, "6": const.spawn0}
dictPosTNT = {"0": const.spawn3, "1": const.posTNT3, "3": const.posTNT2, "6": const.posTNT1}


def event_follower():
    followers = indicators.get_followers()
    followersMax = indicators.get_followers_max()
    typeCMD = "followers"
    if followers >= followersMax:
        save_chat_cmd("cmd", typeCMD, "follower")


def create_chest_cmd():
    chestPos = rand.chest_pos_generation()
    typeItem = [[rand.arm_generation_player, "1"], [rand.give_generation, const.weightSize],
                [rand.weapon_generation_player, "1"], [rand.give_generation, const.weightSize]]
    for i in chestPos:
        itemCount = random.randint(1, 8)
        numbers = list(range(0, 26))
        random.shuffle(numbers)
        items = []
        for k in range(itemCount):
            typeItemGeneration = random.choice(typeItem)
            itemId = typeItemGeneration[0]()
            if typeItemGeneration[1] == "1":
                itemSize = typeItemGeneration[1]
            else:
                itemSize = rand.weighted_pick(typeItemGeneration[1])
            items.append('{Slot:' + str(numbers[k]) + 'b,id:"' + itemId + '",Count:' + itemSize + 'b}')

        cmd = '/setblock ' + str(i[0]) + ' ' + str(i[1]) + ' ' + str(i[2]) + ' chest 0 replace {Items:[' + ','.join(
            items) + ']}'
        save_chat_cmd("cmd", "cmd", cmd)


def create_spawn_coordinate(team: str, typeCMD):
    global returnCoordinate
    templates = indicators.game_data()
    if templates['gameData']['castial'] == 0:
        angelWeight = 0
    else:
        angelWeight = templates['gameData']['bartiil'] * 3 + templates['gameData']['habrial'] * 2 \
                      + templates['gameData']['castial']

    if angelWeight == 4:
        angelWeight = 1

    returnCoordinate = []
    if team == "good":
        returnCoordinate.append(random.choice(dictPosGood[str(angelWeight)]))
    elif team == "bad":
        if typeCMD == "custom":
            returnCoordinate.append(random.choice(dictPosBad[str(angelWeight)]))
        elif typeCMD == "cmd" or typeCMD == "tnt":
            abroadPlayers = []
            for i in range(len(templates["playerData"])):
                x = templates["playerData"][i]["posX"]
                y = templates["playerData"][i]["posY"]
                z = templates["playerData"][i]["posZ"]

                if angelWeight == 6:
                    posBase = const.posBase1
                    if (((posBase[0][1] <= z <= posBase[3][1] and posBase[3][0] <= x <= posBase[4][0]) or
                         (posBase[0][1] <= z <= posBase[1][1] and posBase[0][0] <= x <= posBase[5][0])) and
                        posBase[6][0] <= y <= posBase[6][1]) or (const.posSky[0][0] <= x <= const.posSky[1][0] and
                                                                 const.posSky[1][1] <= z <= const.posSky[0][1] and
                                                                 const.posSky[2][0] <= y <= const.posSky[2][1]):
                        continue
                    else:
                        abroadPlayers.append(templates["playerData"][i])

                elif angelWeight == 3:
                    posBase = const.posBase2
                    if ((posBase[0][1] <= z <= posBase[1][1] and posBase[0][0] <= x <= posBase[3][0]) and
                        posBase[4][0] <= y <= posBase[4][1]) or (const.posSky[0][0] <= x <= const.posSky[1][0] and
                                                                 const.posSky[1][1] <= z <= const.posSky[0][1] and
                                                                 const.posSky[2][0] <= y <= const.posSky[2][1]):
                        continue
                    else:
                        abroadPlayers.append(templates["playerData"][i])

                elif angelWeight == 1:
                    posBase = const.posBase3
                    if ((posBase[0][1] <= z <= posBase[1][1] and posBase[0][0] <= x <= posBase[3][0]) and
                        posBase[4][0] <= y <= posBase[4][1]) or (const.posSky[0][0] <= x <= const.posSky[1][0] and
                                                                 const.posSky[1][1] <= z <= const.posSky[0][1] and
                                                                 const.posSky[2][0] <= y <= const.posSky[2][1]):
                        continue
                    else:
                        abroadPlayers.append(templates["playerData"][i])

                elif angelWeight == 0:
                    abroadPlayers.append(templates["playerData"][i])

            if len(abroadPlayers) > 0:
                for k in abroadPlayers:
                    if typeCMD == "tnt":
                        returnCoordinate.append([k["posX"], k["posY"], k["posZ"]])
                    else:
                        XZRad = rand.random_radius()
                        x = XZRad[0]
                        z = XZRad[1]
                        returnCoordinate.append([k["posX"] + x, k["posY"], k["posZ"] + z])

                if typeCMD == "tnt":
                    returnCoordinate.append(random.choice(dictPosTNT[str(angelWeight)]))
                else:
                    returnCoordinate.append(random.choice(dictPosBad[str(angelWeight)]))

            else:
                if typeCMD == "tnt":
                    returnCoordinate.append(random.choice(dictPosTNT[str(angelWeight)]))
                else:
                    returnCoordinate.append(random.choice(dictPosBad[str(angelWeight)]))
    return returnCoordinate


def smn_base_good(nick, cmd, cmd1):
    typeCMD = "cmd"
    spawnPos = create_spawn_coordinate("good", typeCMD)

    for i in spawnPos:
        x = str(i[0])
        y = str(i[1])
        z = str(i[2])
        finalCMD = '/summon ' + cmd + ' ' + x + ' ' + y + ' ' + z + \
                   ' {CustomName:"' + nick + '",CustomNameVisible:1' + cmd1 + '}'
        save_chat_cmd(nick, typeCMD, finalCMD)


def smn_base_bad(nick, cmd, cmd1):
    typeCMD = "cmd"
    spawnPos = create_spawn_coordinate("bad", typeCMD)

    for i in spawnPos:
        x = str(i[0])
        y = str(i[1])
        z = str(i[2])
        finalCMD = '/summon ' + cmd + ' ' + x + ' ' + y + ' ' + z + \
                   ' {CustomName:"' + nick + '",CustomNameVisible:1' + cmd1 + '}'
        save_chat_cmd(nick, typeCMD, finalCMD)


def smn_hard_bad(nick, cmd, cmd1):
    typeCMD = "cmd"
    spawnPos = create_spawn_coordinate("bad", typeCMD)

    for i in spawnPos:
        x = str(i[0])
        y = str(i[1])
        z = str(i[2])
        finalCMD = '/summon ' + cmd + ' ' + x + ' ' + y + ' ' + z
        save_chat_cmd(nick, "cmd", finalCMD)


def smn_bad(nick, cmd, cmd1):
    finalCMD = '/execute @a ~ ~ ~ summon ' + cmd
    save_chat_cmd(nick, "cmd", finalCMD)


def smn_bad_tnt(nick, cmd, cmd1):
    typeCMD = "tnt"
    spawnPos = create_spawn_coordinate("bad", typeCMD)

    for i in spawnPos:
        x = str(i[0])
        y = str(i[1])
        z = str(i[2])
        finalCMD = '/summon ' + cmd + ' ' + x + ' ' + y + ' ' + z + ' {Fuse:30}'
        save_chat_cmd(nick, "cmd", finalCMD)


def effect(nick, cmd, cmd1):
    print(cmd)
    if type(cmd) == list:
        for i in range(len(cmd)):
            print(str(i) + ": " + cmd[i])
            cmdAdd = '/effect @a ' + cmd[i] + ' ' + cmd1
            save_chat_cmd(nick, "cmd", cmdAdd)
    else:
        finalCMD = '/effect @a ' + cmd + ' ' + cmd1
        save_chat_cmd(nick, "cmd", finalCMD)


def give(nick, cmd, cmd1=1):
    finalCMD = cmd + '|' + str(cmd1)
    save_chat_cmd(nick, "give", finalCMD)


def give_all(nick, cmd, cmd1=1):
    finalCMD = "/give @a " + cmd + " " + str(cmd1)
    save_chat_cmd(nick, "cmd", finalCMD)


def wake_up(nick, cmd, cmd1):
    save_chat_cmd(nick, "wakeup", cmd1)


def custom_npc(nick, cmd, cmd1):
    typeCMD = "custom"
    spawnPos = create_spawn_coordinate(cmd1, typeCMD)

    for i in spawnPos:
        x = str(i[0])
        y = str(i[1])
        z = str(i[2])
        finalCMD = cmd + "|" + x + "|" + y + "|" + z
        save_chat_cmd(nick, typeCMD, finalCMD)


def save_chat_cmd(nick: str, typeCmd, cmd):
    with open("command_chat.txt", "a", encoding="UTF-8") as mainCMD:
        mainCMD.write(nick + '|' + typeCmd + '|' + cmd + '\n')


typeCMDConstruction = {"!animal": [smn_base_good, [const.weightAnimal, ""]],
                       "!heal": [effect, ["6", "10"]],
                       "!weapon": [give, [rand.weapon_generation_player, "1"]],
                       "!armor": [give, [rand.arm_generation_player, "1"]],
                       "!cookie": [give_all, ["cookie", "1"]],
                       "!give": [give, [rand.give_generation, const.weightSize]],
                       "!beast": [custom_npc, [const.weightBeast, "good"]],
                       "!human": [custom_npc, [const.weightHuman, "good"]],
                       "!elf": [custom_npc, [const.weightElf, "good"]],
                       "!dwarf": [custom_npc, [const.weightDwarf, "good"]],
                       "!faun": [custom_npc, [const.weightFaun, "good"]],
                       "!centaur": [custom_npc, [const.weightCentaur, "good"]],
                       "!furry": [custom_npc, [const.weightFurry, "good"]],
                       "!naga": [custom_npc, [const.weightNaga, "good"]],
                       "!orc": [custom_npc, [const.weightOrc, "good"]],
                       "!army1": [[custom_npc, [const.weightBeast, "good"]],
                                  [custom_npc, [const.weightHuman, "good"]],
                                  [custom_npc, [const.weightDwarf, "good"]]],
                       "!army2": [[custom_npc, [const.weightElf, "good"]],
                                  [custom_npc, [const.weightFaun, "good"]],
                                  [custom_npc, [const.weightCentaur, "good"]]],
                       "!army3": [[custom_npc, [const.weightFurry, "good"]],
                                  [custom_npc, [const.weightNaga, "good"]],
                                  [custom_npc, [const.weightOrc, "good"]]],
                       "!blessing": [effect, [const.goodEffect, ""]],
                       "!curse": [effect, [const.badEffect, ""]],
                       "!zombie": [smn_base_bad, [const.weightZombie, rand.arm_generation_npc]],
                       "!spider": [smn_base_bad, [const.weightSpiders, ""]],
                       "!skeleton": [smn_base_bad, [const.weightSkeleton,
                                                    [rand.arm_generation_npc, 'bow']]],
                       "!monster": [[smn_base_bad, [const.weightZombie, rand.arm_generation_npc]],
                                    [smn_base_bad, [const.weightSpiders, ""]],
                                    [smn_base_bad, [const.weightSkeleton,
                                                    [rand.arm_generation_npc, 'bow']]]],
                       "!tacticalmonster": [[custom_npc, ["crasher", "bad"]], [custom_npc, ["reaper", "bad"]]],
                       "!creeper": [smn_base_bad, const.weightCreeper],
                       "!hell": [smn_hard_bad, [const.weightHell, ""]],
                       "!thaum": [smn_hard_bad, [const.weightThaumcraft, ""]],
                       "!twil": [smn_hard_bad, [const.weightTwilight, ""]],
                       "!lightning": [smn_bad, ["lightning_bolt", ""]],
                       "!tnt": [smn_bad_tnt, ["tnt", ""]],
                       "!crasher": [custom_npc, ["crasher", "bad"]],
                       "!reaper": [custom_npc, ["reaper", "bad"]],
                       "!icefire": [smn_base_bad, [const.weightIceFire, ",GrowthStage:2, AgeTicks:1956400"]],
                       "!parasite": [smn_hard_bad, [const.weightParasite, ""]],
                       "!lparasite": [smn_hard_bad, [const.weightLParasite, ""]],
                       "!boss": [smn_hard_bad, [const.weightBoss, ""]],
                       "!wakeup": [wake_up, ["wakeup", "wakeup"]]}


def start_cmd(nick, cmd):
    param = typeCMDConstruction.get(cmd)

    if cmd == "!monster":
        param = random.choice(param)
    if cmd == "!tacticalmonster":
        param = random.choice(param)
    if cmd == "!army1":
        param = random.choice(param)
    if cmd == "!army2":
        param = random.choice(param)
    if cmd == "!army3":
        param = random.choice(param)

    construct = param[0]
    paramCMD = param[1]

    if type(paramCMD) == dict:
        paramCMD = rand.weighted_pick(paramCMD)

    paramCMD1 = paramCMD[0]
    paramCMD2 = paramCMD[1]
    # print(construct, paramCMD1, paramCMD2)

    if type(paramCMD1) == dict:
        paramCMD1 = rand.weighted_pick(paramCMD1)

    if callable(paramCMD1):
        paramCMD1 = paramCMD1()

    if type(paramCMD2) == dict:
        paramCMD2 = rand.weighted_pick(paramCMD2)

    if type(paramCMD2) == list:
        paramCMD2 = paramCMD2[0](paramCMD2[1])

    if callable(paramCMD2):
        paramCMD2 = paramCMD2()

    construct(nick, paramCMD1, paramCMD2)
    return paramCMD1
