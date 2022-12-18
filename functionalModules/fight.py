import qq
import pandas
import asyncio
import random

import toolModules.otherModule as otherModule

async def fight(self: qq.Client, message: qq.Message):
    requestList = message.content.split('||')
    user1 = str(message.author)
    user2 = requestList[1]
    #检测是否自己和自己对战
    if user1 == user2:
        await message.reply('请不要向自己发起对战', mention_author = message.author)
        return
    #检测注册状况
    try:
        checker = open('./users/' + user1 + '.isregistered', mode = 'r', encoding = 'utf8')
    except:
        await message.reply('未找到' + user1 + '，请在确保对方的名字正确且已经注册后再发起挑战', mention_author = message.author)
        return
    else:
        checker.close()
    try:
        checker = open('./users/' + user2 + '.isregistered', mode = 'r', encoding = 'utf8')
    except:
        await message.reply('未找到' + user2 + '，请在确保对方的名字正确且已经注册后再发起挑战', mention_author = message.author)
        return
    else:
        checker.close()
    #检查命令格式
    try:
        user1 = str(message.author)
        user2 = requestList[1]
        await message.reply('正在等待' + user2 + '作出回答.', mention_author = message.author)
    except:
        await message.reply('请输入正确的命令格式：/对战||[对方的名字]', mention_author = message.author)
        return
    #获取回答
    def verify(msg: qq.Message):
        return str(msg.author) == user2
    while True:
        try:
            answer: qq.Message = await self.wait_for(event = 'message', check = verify, timeout = 60)
        #超时
        except asyncio.TimeoutError:
            await message.reply('对方超出1分钟未给出回应', mention_author = message.author)
            return
        if '拒绝' in answer.content:
            await message.reply('对方拒绝了你的对战请求', mention_author = message.author)
            return
        elif '接受' in answer.content:
            await message.reply('对方接受了你的对战请求', mention_author = message.author)
            break
        #乱回答
        else:
            await message.reply('请不要回答除接受与拒绝之外的其他回答', mention_author = answer.author)
    winner, loser = await fightGame(self = self, hostMessage = message, guestMessage = answer, host = user1, guest = user2)
    #读取二人的信息
    winnerBasicInfo = pandas.read_json('./users/' + winner + '_basicInfo.json', typ = 'series')
    winnerInGameInfo = pandas.read_json('./users/' + winner + '_inGameInfo.json', typ = 'series')
    loserBasicInfo = pandas.read_json('./users/' + loser + '_basicInfo.json', typ = 'series')
    loserInGameInfo = pandas.read_json('./users/' + loser + '_inGameInfo.json', typ = 'series')
    #根据等级差计算奖励
    levelDifference = winnerInGameInfo['currentLevel'] - loserInGameInfo['currentLevel']
    if levelDifference >= 10:
        if int(loserBasicInfo['skyDustAmount'] * 0.5) < 5000:
            skyDustAmountMinused = loserBasicInfo['skyDustAmount']  + 10
        else:
            skyDustAmountMinused = int(loserBasicInfo['skyDustAmount'] * 0.5)
        currentExpAdded = random.randint(32767, 65536)
        skyDustAmountAdded = random.randint(2000, 4000)
    elif levelDifference >= 5:
        if int(loserBasicInfo['skyDustAmount'] * 0.3) < 1000:
            skyDustAmountMinused = loserBasicInfo['skyDustAmount'] + 10
        else:
            skyDustAmountMinused = int(loserBasicInfo['skyDustAmount'] * 0.3)
        currentExpAdded = random.randint(8192, 16384)
        skyDustAmountAdded = random.randint(1000, 2000)
    elif levelDifference >= 3:
        if int(loserBasicInfo['skyDustAmount'] * 0.2) < 500:
            skyDustAmountMinused = loserBasicInfo['skyDustAmount'] + 10
        else:
            skyDustAmountMinused = int(loserBasicInfo['skyDustAmount'] * 0.2)
        currentExpAdded = random.randint(1024, 4096)
        skyDustAmountAdded = random.randint(500, 1000)
    else:
        if int(loserBasicInfo['skyDustAmount'] * 0.1) < 250:
            skyDustAmountMinused = loserBasicInfo['skyDustAmount'] + 10
        else:
            skyDustAmountMinused = int(loserBasicInfo['skyDustAmount'] * 0.1)
        currentExpAdded = random.randint(256, 1024)
        skyDustAmountAdded = random.randint(250, 500)
    await message.reply('对战结束：\n' + winner + '获得：天空之尘 +' + str(skyDustAmountAdded) + '  经验值 +' + str(currentExpAdded) + '\n' + loser + '失去：天空之尘 -' + str(skyDustAmountMinused))
    winnerBasicInfo['skyDustAmount'] += skyDustAmountAdded
    winnerInGameInfo['currentExp'] += currentExpAdded
    loserBasicInfo['skyDustAmount'] -= skyDustAmountMinused
    winnerBasicInfo.to_json('./users/' + winner + '_basicInfo.json', indent = 4)
    winnerInGameInfo.to_json('./users/' + winner + '_inGameInfo.json', indent = 4, orient = 'index')
    loserBasicInfo.to_json('./users/' + loser + '_basicInfo.json', indent = 4)
    loserInGameInfo.to_json('./users/' + loser + '_inGameInfo.json', indent = 4, orient = 'index')
    otherModule.updateUserInGameInfo(f_user = winner)


async def fightGame(self: qq.Client, hostMessage: qq.Message, guestMessage: qq.Message, host, guest):
    #读取相关数据
    hostWeaponForm = pandas.read_json('./users/' + host + '_weaponForm.json', orient = 'index')
    hostItemForm = pandas.read_json('./users/' + host + '_itemForm.json', orient = 'index')
    hostInGameInfo = pandas.read_json('./users/' + host + '_inGameInfo.json', typ = 'series')

    guestWeaponForm = pandas.read_json('./users/' + guest + '_weaponForm.json', orient = 'index')
    guestItemForm = pandas.read_json('./users/' + guest + '_itemForm.json', orient = 'index')
    guestInGameInfo = pandas.read_json('./users/' + guest + '_inGameInfo.json', typ = 'series')

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
        case '力量药水':
            return {'basicHP': 200}
        case '恢复药水':
            return {'basicHP': 1000, 'basicAttack': 200}
        case _:
            return 'NoSuchItem'