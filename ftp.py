from ftplib import FTP
import json
import indicators

playerData = 'player_data.json'
cmdToServer = "cmd_to_server.json"
messagesToServer = 'messages_to_server.json'

idCMD = 0
idMessage = 0
ftp = FTP()


def connect():
    global ftp
    HOST = '212.22.93.25'
    PORT = 8821
    ftp.connect(HOST, PORT)
    ftp.login('apvgzxyn', 'gv5Au14yO2')

    ftp.cwd('/212.22.93.25_25580/world/customnpcs/myjson/')


# files = ftp.nlst()
# filename = files[0]  # get first file
# print(filename)
def give_server_data(file_name):
    global ftp
    while True:
        try:
            with open(file_name, 'wb') as file:
                ftp.retrbinary('RETR ' + file_name, file.write)

            with open(file_name, 'r') as file:
                reading_json = file.read()
                templates = json.loads(reading_json)
                # print(templates)
        except:
            continue
        else:
            return templates
    return templates


def give_server_data_local(file_name):
    with open('C:/Users/user123/AppData/Roaming/.minecraft/saves/Новый мир/customnpcs/myjson/' + file_name,
              'r') as file:
        reading_json = file.read()
        templates = json.loads(reading_json)
        # print(templates)
    return templates


def set_server(file_name):
    global idCMD
    global idMessage

    def get_json(getIdCMD=0, getIdMessage=0):
        if getIdCMD != 0 or getIdMessage != 0:
            with open(file_name, 'r') as fileJson:
                readingJson = fileJson.read()
                getData = json.loads(readingJson)
                fileJson.close()
        else:
            getData = None
        return getData

    def give_json_local(newData):
        with open(file_name, "w") as file:
            file.write(json.dumps(newData))

        with open('C:/Users/user123/AppData/Roaming/.minecraft/saves/Новый мир/customnpcs/myjson/' + file_name,
                  "w") as file:
            file.write(json.dumps(newData))

    def give_json(newData):
        with open(file_name, "w") as file:
            file.write(json.dumps(newData))

        with open(file_name, 'rb') as file:
            ftp.storbinary('STOR ' + file_name, file)

    if file_name == cmdToServer:

        timer = indicators.get_timer()
        gameRound = str(indicators.count_round())
        darknessTime = indicators.count_darkness_time()

        data = get_json(getIdCMD=idCMD)
        if data is not None:
            data['timer'] = timer
            data['round'] = gameRound
            data['darkness'] = darknessTime

        with open("command_chat.txt", "r", encoding="UTF-8") as chatCmdMain:
            count = sum(1 for line in chatCmdMain)

            if count > idCMD:
                CMDRun = count - idCMD
                chatCmdMain.seek(0, 0)
                cmdCount = chatCmdMain.readlines()


                for i in range(CMDRun):
                    printChatCMD = cmdCount[idCMD]
                    printChatCMD = printChatCMD[:-1]
                    printChatCMDSplit = printChatCMD.split("|")
                    nameChatters = printChatCMDSplit[0]
                    typeCMD = printChatCMDSplit[1]
                    CMD = printChatCMDSplit[2]
                    if typeCMD == "cmd" or typeCMD == "followers" or typeCMD == "wakeup":
                        param1 = None
                        param2 = None
                        param3 = None
                    elif typeCMD == "custom":
                        param1 = printChatCMDSplit[3]  # x coordinate
                        param2 = printChatCMDSplit[4]  # y coordinate
                        param3 = printChatCMDSplit[5]  # z coordinate
                    elif typeCMD == "give":
                        param1 = printChatCMDSplit[3]  # size stack
                        param2 = None
                        param3 = None

                    if idCMD > 0:
                        to_json = {"id": idCMD, 'nick': nameChatters, 'typeCMD': typeCMD, "cmd": CMD, "param1": param1,
                                   "param2": param2, "param3": param3}
                        data['cmd'].append(to_json)

                    elif idCMD == 0:
                        to_json = {"timer": timer, "round": gameRound, "darkness": darknessTime, "cmd": [
                            {"id": idCMD, 'nick': nameChatters, 'typeCMD': typeCMD, "cmd": CMD, "param1": param1,
                             "param2": param2, "param3": param3}]}
                        data = to_json
                    idCMD += 1
                # give_json_local(data)
            chatCmdMain.close()
        give_json(data)

    elif file_name == messagesToServer:

        with open("save_message.txt", "r", encoding="UTF-8") as savedMessages:
            count = sum(1 for line in savedMessages)

            if count > idMessage:
                MessageRun = count - idMessage
                savedMessages.seek(0, 0)
                messagesCount = savedMessages.readlines()

                data = get_json(getIdMessage=idMessage)

                for i in range(MessageRun):
                    messageCount = messagesCount[idMessage]
                    messageCount = messageCount[:-1]

                    if idMessage > 0:
                        to_json = {"id": idMessage, 'message': messageCount}
                        data['messages'].append(to_json)

                    elif idMessage == 0:
                        to_json = {"messages": [{"id": idMessage, 'message': messageCount}]}
                        data = to_json
                    idMessage += 1
                # give_json_local(data)
                give_json(data)
            savedMessages.close()
# ftp.quit()
