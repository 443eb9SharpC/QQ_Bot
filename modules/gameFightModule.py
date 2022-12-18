import asyncio
import qq
import pandas

async def fightGame(self, hostMessage: qq.Message, guestMessage: qq.Message, host, guest):
    #读取相关数据
    hostWeaponForm = pandas.read_json('./users/' + host + '_weaponForm.json', orient = 'index')
    hostItemForm = pandas.read_json('./users/' + host + '_itemForm.json', orient = 'index')
    hostInGameInfo = pandas.read_json('./users/' + host + '_inGameInfo.json', typ = 'series')
    hostWeaponForm.set_index(keys = 'weaponName', inplace = True)
    if hostItemForm.empty != True:
        hostItemForm.set_index(keys = 'itemName', inplace = True)

    guestWeaponForm = pandas.read_json('./users/' + guest + '_weaponForm.json', orient = 'index')
    guestItemForm = pandas.read_json('./users/' + guest + '_itemForm.json', orient = 'index')
    guestInGameInfo = pandas.read_json('./users/' + guest + '_inGameInfo.json', typ = 'series')
    guestWeaponForm.set_index(keys = 'weaponName', inplace = True)
    if hostItemForm.empty != True:
        guestItemForm.set_index(keys = 'itemName', inplace = True)

    #定义检查回复的函数
    def verifyHost(msg: qq.Message):
        return str(msg.author) == host
    def verifyGuest(msg: qq.Message):
        return str(msg.author) == guest

    #开始对战
    round = 1
    currentUserNumber = 0
    while True:
        #根据回合判定
        if currentUserNumber % 2 == 0:
            currentUserInGameInfo = guestInGameInfo
            currentUserWeaponForm = guestWeaponForm
            currentUserItemForm = guestItemForm
            currentUserMessage = guestMessage
            currentUser = guest

            waitingUserInGameInfo = hostInGameInfo
            waitingUserMessage = hostMessage
            waitingUser = host
            verify = verifyGuest
        elif currentUserNumber % 2 == 1:
            currentUserInGameInfo = hostInGameInfo
            currentUserWeaponForm = hostWeaponForm
            currentUserItemForm = hostItemForm
            currentUserMessage = hostMessage
            currentUser = host

            waitingUserInGameInfo = guestInGameInfo
            waitingUserMessage = guestMessage
            waitingUser = guest
            verify = verifyHost

        await hostMessage.reply('当前生命值：\n' + currentUser + '：' + str(currentUserInGameInfo['basicHP']) + '  ' + waitingUser + '：' + str(waitingUserInGameInfo['basicHP']))
        await hostMessage.reply('当前为第' + str(round) + '回合，请' + currentUser + '行动', mention_author = currentUserMessage.author)

        while True:
            try:
                currentUserActionReply: qq.Message = await self.wait_for(event = 'message', check = verify, timeout = 300)
            except asyncio.TimeoutError:
                await hostMessage.reply(currentUser + '超出时间未操作，默认投降', mention_author = waitingUserMessage.author)
                return waitingUser, currentUser
            else:
                if '跳过' in currentUserActionReply.content:
                    await hostMessage.reply('对方放弃了本回合', mention_author = waitingUserMessage.author)
                    currentUserNumber += 1
                    break
                #切分用户消息,获得道具种类和名字
                try:
                    currentUserActionType = currentUserActionReply.content.split()[1].split('||')[0]
                    currentUserActionContent = currentUserActionReply.content.split()[1].split('||')[1]
                except:
                    await hostMessage.reply('请输入有效的命令：[武器/物品]||[名字]', mention_author = currentUserMessage.author)
                    continue
                #区分种类
                if currentUserActionType == '武器':
                    #检测武器是否存在
                    if currentUserActionContent in currentUserWeaponForm.index:
                        #攻击
                        waitingUserInGameInfo['basicHP'] -= currentUserWeaponForm.at[currentUserActionContent, 'weaponAttack'] + currentUserInGameInfo['basicAttack']
                    else:
                        await hostMessage.reply('未找到武器：' + currentUserActionContent, mention_author = currentUserMessage.author)
                        continue
                elif currentUserActionType == '物品':
                    #检测用户的物品是否为空
                    if currentUserItemForm.empty == True:
                        await hostMessage.reply('空物品背包', mention_author = currentUserMessage.author)
                        continue
                    #检测物品是否存在
                    if currentUserActionContent in currentUserItemForm.index:
                        affectedProp: dict = indexItem(f_currentUser = currentUser, f_itemName = currentUserActionContent)
                        #检测是否有此物品
                        if affectedProp == 'NoSuchItem':
                            await hostMessage.reply('未找到物品：' + currentUserActionContent, mention_author = currentUserMessage.author)
                            continue
                        #若物品数量=0,则删除这一个物品
                        currentUserItemForm.at[currentUserActionContent, 'itemAmount'] -= 1
                        if currentUserItemForm.at[currentUserActionContent, 'itemAmount'] == 0:
                            currentUserItemForm.drop(index = currentUserActionContent, inplace = True)
                        currentUserItemForm.to_json('./users/' + currentUser + '_itemForm.json', indent = 4, orient = 'index')
                        #应用物品带来的效果
                        for affectedAttribute, affects in affectedProp.items():
                            currentUserInGameInfo[affectedAttribute] += affects
                else:
                    await guestMessage.reply('请输入有效的道具种类：武器或物品', mention_author = currentUserMessage.author)
                    continue
            currentUserNumber += 1
            round += 1
            #判断双方血量
            if hostInGameInfo['basicHP'] <= 0:
                return guest, host
            elif guestInGameInfo['basicHP'] <= 0:
                return host, guest
            break


def indexItem(f_currentUser, f_itemName):
    userItemForm = pandas.read_json('./users/' + f_currentUser + '_itemForm.json', orient = 'index')
    userItemForm.set_index(keys = 'itemName')
    match f_itemName:
        case '生命药水':
            return {'basicHP': 1000}
        case _:
            return 'NoSuchItem'