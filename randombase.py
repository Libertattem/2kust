import random
import const
import indicators

dictCreeper = {'creeper': ['creeper', ''], 'creeper_evolved': ['galacticraftcore:evolved_creeper', ''],
               'creeper_spore': ['netherex:spore_creeper', ''],
               'creeper_powered': ['creeper', ',powered:1'],
               'creeper_radioactive': ['creeper', ',Glowing:1,Health:40,Attributes:[{Name:"generic.maxHealth",'
                                                  'Base:40}],Fire:1277951,ExplosionRadius:50,ActiveEffects:[{Id:12,'
                                                  'Amplifier:0,Duration:2147483647}]']}


def chest_pos_generation():
    chestsPos = const.posChests
    chestsArray = list(chestsPos.keys())
    finalChestPos = []
    for i in chestsArray:
        if len(chestsPos[i]) == 1:
            finalChestPos.append(chestsPos[i][0])
        else:
            posSample = random.sample(chestsPos[i], round(len(chestsPos[i]) / 100 * 70))
            finalChestPos = finalChestPos+posSample
    return finalChestPos


def weighted_pick(dic):
    total = sum(dic.values())
    pick = random.randint(0, total - 1)
    tmp = 0
    for key, weight in dic.items():
        tmp += weight
        if pick < tmp:
            if dic == const.weightCreeper:
                key = dictCreeper[key]
            return key


def approx_modif_generator():
    gameRound = indicators.count_round()
    modif1 = round(0.1429 * gameRound ** 2 - 1.3571 * gameRound + 3.2000, 1)
    if modif1 != 0.5:
        modif1 = round(modif1)

    modif2 = round(0.1250 * (gameRound ** 3) - 1.4107 * (gameRound ** 2) + 4.4643 * gameRound - 2.2000, 1)
    if modif2 != 0.5:
        modif2 = round(modif2)

    modif3 = round(-0.4286 * gameRound ** 2 + 2.5714 * gameRound - 1.2000)
    modif4 = round(-0.0833 * gameRound ** 3 + 0.8929 * gameRound ** 2 - 2.0238 * gameRound + 2.2000)
    modif5 = round(-0.0833 * gameRound ** 3 + 1.1071 * gameRound ** 2 - 2.8095 * gameRound + 2.8000)
    return modif1, modif2, modif3, modif4, modif5


def arm_generation_player(forChests: bool = False):
    typeArmor = random.choice(["helmet", "chestplate", "leggings", "boots"])

    armors = {"armor2": const.weightArmor2, "armor3": const.weightArmor3, "armor4": const.weightArmor4,
              "armor5": const.weightArmor5}

    if forChests:
        modif = [1, 1, 1, 1, 1]
    else:
        modif = approx_modif_generator()

    valuesSum2 = sum(armors["armor2"][typeArmor].values()) * modif[1]
    valuesSum3 = sum(armors["armor3"][typeArmor].values()) * modif[2]
    valuesSum4 = sum(armors["armor4"][typeArmor].values()) * modif[3]
    valuesSum5 = sum(armors["armor5"][typeArmor].values()) * modif[4]

    sumWeightsArmor = {"armor2": valuesSum2, "armor3": valuesSum3, "armor4": valuesSum4, "armor5": valuesSum5}

    levelArmor = weighted_pick(sumWeightsArmor)
    pickedArmor = weighted_pick(armors[levelArmor][typeArmor])
    return pickedArmor


def give_generation(forChests: bool = False):
    give = {"give1": const.weightGive1, "give2": const.weightGive2, "give3": const.weightGive3,
            "give4": const.weightGive4, "give5": const.weightGive5}

    if forChests:
        modif = [1, 1, 1, 1, 1]
    else:
        modif = approx_modif_generator()

    valuesSum1 = sum(give["give1"].values()) * modif[0]
    valuesSum2 = sum(give["give2"].values()) * modif[1]
    valuesSum3 = sum(give["give3"].values()) * modif[2]
    valuesSum4 = sum(give["give4"].values()) * modif[3]
    valuesSum5 = sum(give["give5"].values()) * modif[4]

    sumWeightsGive = {"give1": valuesSum1, "give2": valuesSum2, "give3": valuesSum3, "give4": valuesSum4,
                      "give5": valuesSum5}

    levelGive = weighted_pick(sumWeightsGive)
    pickedGive = weighted_pick(give[levelGive])
    return pickedGive


def weapon_generation_player(forChests: bool = False):
    weapons = {"weapon2": const.weightWeapons2, "weapon3": const.weightWeapons3, "weapon4": const.weightWeapons4,
               "weapon5": const.weightWeapons5}

    if forChests:
        modif = [1, 1, 1, 1, 1]
    else:
        modif = approx_modif_generator()

    valuesSum2 = sum(weapons["weapon2"].values()) * modif[1]
    valuesSum3 = sum(weapons["weapon3"].values()) * modif[2]
    valuesSum4 = sum(weapons["weapon4"].values()) * modif[3]
    valuesSum5 = sum(weapons["weapon5"].values()) * modif[4]

    sumWeightsWeapon = {"weapon2": valuesSum2, "weapon3": valuesSum3, "weapon4": valuesSum4, "weapon5": valuesSum5}

    levelWeapon = weighted_pick(sumWeightsWeapon)
    pickedWeapon = weighted_pick(weapons[levelWeapon])
    return pickedWeapon


def arm_generation_npc(weapon=None, helmet=None, chestPlate=None, leggings=None, boots=None):
    param = [weapon, helmet, chestPlate, leggings, boots]
    weights = {"1": [const.weightWeapons1, const.weightArmor1["helmet"], const.weightArmor1["chestplate"],
                     const.weightArmor1["leggings"], const.weightArmor1["boots"]],
               "2": [const.weightWeapons2, const.weightArmor2["helmet"], const.weightArmor2["chestplate"],
                     const.weightArmor2["leggings"], const.weightArmor2["boots"]],
               "3": [const.weightWeapons3, const.weightArmor3["helmet"], const.weightArmor3["chestplate"],
                     const.weightArmor3["leggings"], const.weightArmor3["boots"]],
               "4": [const.weightWeapons4, const.weightArmor4["helmet"], const.weightArmor4["chestplate"],
                     const.weightArmor4["leggings"], const.weightArmor4["boots"]],
               "5": [const.weightWeapons5, const.weightArmor5["helmet"], const.weightArmor5["chestplate"],
                     const.weightArmor5["leggings"], const.weightArmor5["boots"]]}
    gameRound = indicators.count_round()
    r = 0
    for i in param:
        r += 1
        if i is None:
            param[r - 1] = weighted_pick(weights[str(gameRound)][r - 1])

    weapon = param[0]
    helmet = param[1]
    chestPlate = param[2]
    leggings = param[3]
    boots = param[4]
    cmd1 = ',HandItems:[{id:"' + weapon + '",Count:1},{}],ArmorItems:[{id:"' + boots + '",Count:1},{id:"' + \
           leggings + '",Count:1},{id:"' + chestPlate + '",Count:1},{id:"' + helmet + '",Count:1}]'
    return cmd1


def random_radius():
    xrange = random.randint(-const.spawnRadius, const.spawnRadius)
    zrange = random.randint(-const.spawnRadius, const.spawnRadius)
    return xrange, zrange


def random_cmd_for_bot(isBadCMD: bool = False):
    if not isBadCMD:
        badCMD = weighted_pick(const.weightChatCMDGood)
        return badCMD
    else:
        goodCMD = weighted_pick(const.weightChatCMDBad)
        return goodCMD


def bot_answers(type: int):
    """
    (int) -> string

    Возвращает случайную фразу в зависмости от необходимого типа ответа
        1: Ответ при отсутсвии активного ввода команд

        2: Ответ если бот примет решение пойти против сил тьмы

        3: Ответ если бот примет решение пойти против сил добра

        4: Просто случайная фраза возможно шутка
    """
    if type == 1:
        answer = random.choice(["Что-то тухло тут...", "Наверное стоит и мне поучавствовать", "Суету навести охото",
                                "Опять ты стримЁр хренов никому не нужен, дай ка я тебя поразвлекаю",
                                "А что? Зрители твои что ли уснули?? Начинаю мейнстрим",
                                "Ца! Опять мне придеться что-то делать..."])
    elif type == 2:
        answer = random.choice(["Вы че там его дрочите, ну ка...", "Вам его сосвем не жалко?? Ща помогу",
                                "Тэк-с... Надо прекрощать это безобразие...", "Это конечно все прикольно, но..Нет..",
                                "Помощь идет!", "Не дам в обиду стримЁра", "ну что такое опять устроили..",
                                "Лови аптечку!", "Не сдавайся стримЁр", "Опять твою жепу вытаскивать..."])
    elif type == 3:
        answer = random.choice(["Охохохо. Пора творить непотрептсва...", "Тоби конэц... Большой конэц...",
                                "Ну что? Сделаем малнькое недорозумение??",
                                "Я должен был боротся со злом, а не примкнуть к нему)",
                                "Что такое кабздец, давай я щас покажу",
                                "Что-то у тебя все слижком хорошо стримЁр, ненамана это", "Казнить, нельзя помиловать",
                                "Что же вы его все жалеете да жалеете...",
                                "Я хотел написать сюда что-то, а потом дать Osees`у пиз***ей, как видишь в чат я уже "
                                "написал",
                                "маяя хиииии, маяя хуууу, маяяя пи**зда Osees`у",
                                "Вдруг как в сказке скрипнул пердак..", "Ладно, пора бы и мне поделать гадостей"])
    elif type == 4:
        answer = random.choice(
            ["Случайный ответ, мне просто в лом что-то придумывать", "Что же делать то будем??", "", "", "", "", "", "",
             "", "", "", ""])
    return answer
