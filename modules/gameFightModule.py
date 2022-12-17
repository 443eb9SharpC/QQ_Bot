import asyncio
import qq
import pandas

async def fightGame(self, hostMessage: qq.Message, guestMessage: qq.Message, host, guest):
    #读取相关数据
    hostWeaponForm = pandas.read_json('./users/' + host + '_weaponForm.json', orient = 'index')
    hostItemForm = pandas.read_json('./users/' + host + '_itemForm.json', orient = 'index')
    hostInGameInfo = pandas.read_json('./users/' + host + '_inGameInfo.json', typ = 'series')
    hostWeaponForm.set_index(keys = 'weaponName')
    hostItemForm.set_index(keys = 'itemName')

    guestWeaponForm = pandas.read_json('./users/' + guest + '_weaponForm.json', orient = 'index')
    guestItemForm = pandas.read_json('./users/' + guest + '_itemForm.json', orient = 'index')
    guestInGameInfo = pandas.read_json('./users/' + guest + '_inGameInfo.json', typ = 'series')
    guestWeaponForm.set_index(keys = 'weaponName')
    guestItemForm.set_index(keys = 'itemName')

    #定义检查回复的函数
    def verifyHost(msg: qq.Message):
        return str(msg.author) == host
    def verifyGuest(msg: qq.Message):
        return str(msg.author) == guest

    #开始对战
    round = 1
    currentUserNumber = 0
    endCompetition = False
    while True:
        #根据回合判定
        if currentUserNumber % 2 == 0:
            await hostMessage.reply('回合' + str(round) + '，请' + guest + '行动', mention_author = guestMessage.author)
            currentUserWeaponForm = hostWeaponForm
            currentUserItemForm = hostItemForm
            currentUserMessage = guestMessage
            currentUser = guest
            waitingUserInGameInfo = hostInGameInfo
            waitingUserMessage = hostMessage
            verify = verifyGuest
        elif currentUserNumber % 2 == 1:
            await hostMessage.reply('回合' + str(round) + '，请' + host + '行动', mention_author = guestMessage.author)
            currentUserWeaponForm = guestWeaponForm
            currentUserItemForm = guestItemForm
            currentUserMessage = hostMessage
            currentUser = host
            waitingUserInGameInfo = guestInGameInfo
            waitingUserMessage = guestMessage
            verify = verifyHost

        while True:
            try:
                currenUserActionReply: qq.Message = await self.wait_for(event = 'message', check = verify, timeout = 300)
            except asyncio.TimeoutError:
                await hostMessage.reply(currentUser + '超出时间未操作，默认投降', mention_author = waitingUserMessage.author)
                return
            else:
                if '跳过' in currentUserMessage.content:
                    await waitingUserMessage.reply('对方放弃了本回合', mention_author = waitingUserMessage.author)
                #切分用户消息,获得道具种类和名字
                try:
                    currenUserActionType = currenUserActionReply.content.split(' ')[1].split('||')[0]
                    currentUserActionContent = currenUserActionReply.content.split(' ')[1].split('||')[1]
                except:
                    await currentUserMessage.reply('请输入有效的命令：[武器/物品]||[名字]', mention_author = currentUserMessage.author)

                else:
                    #区分种类
                    if currenUserActionType == '武器':
                        #检测武器是否存在
                        if currentUserActionContent in currentUserWeaponForm.index:
                            #攻击
                            waitingUserInGameInfo['basicHP'] -= guestWeaponForm.at[currentUserActionContent, 'weaponAttack']
                        else:
                            await guestMessage.reply('未找到武器：' + currentUserActionContent, mention_author = guestMessage.author)
                    elif currenUserActionType == '物品':
                        #检测物品是否存在
                        if currentUserActionContent in currentUserItemForm.index:
                            affectedProp: dict = indexItem(f_currentUser = currentUser, f_itemName = currentUserActionContent)
                            #应用物品带来的效果
                            for affectedAttribute, affects in affectedProp.items():
                                waitingUserInGameInfo[affectedAttribute] += affects
                    else:
                        await guestMessage.reply('请输入有效的道具种类：武器或物品', mention_author = currentUserMessage.author)
                        continue
            currentUserNumber += 1
            #判断双方血量
            if hostInGameInfo['basicHP'] <= 0:
                return guest, host
            elif guestInGameInfo['basicHP'] <= 0:
                return host, guest


def indexItem(f_currentUser, f_itemName, f_currentHP):
    userItemForm = pandas.read_json('./users/' + f_currentUser + '_itemForm.json', orient = 'index')
    userItemForm.set_index(keys = 'weaponName')
    match f_itemName:
        case '生命药水':
            return {'basicHP': 1000}