#coding = utf-8
import asyncio
import qq
import datetime
import pandas
import random
from config import appid, token
import logging
import traceback

import modules.otherModule as otherModule
import modules.gameFightModule as gameFightModule

logging.basicConfig(level = logging.DEBUG)

class MyClient(qq.Client):
    async def on_ready(self):
        print(f'以 {self.user} 身份登录（ID：{self.user.id}）')
        print('------')

    async def on_message(self, message: qq.Message):
        try:
            # 我们不希望机器人回复自己
            if message.author.id == self.user.id:
                return

            if message.channel.id != 13630884 and str(message.author) != '443eb9#C':
                await message.reply('请不要使用开发模式下的命令', mention_author = message.author)
                return
            if message.channel.id == 11672109:
                await message.reply('请不要在制造站使用机器人', mention_author = message.author)
                return


            """
            测试用模块
            """
            if '##测试' in message.content:
                df = pandas.read_excel('./homework/homework.xlsx')
                print(df)
                df.set_index('水果名称')
                print(df)


            """
            菜单模块
            """

            if '##菜单' in message.content:
                menuFile = open('./texts/menu.txt', mode = 'r', encoding = 'utf8')
                menu = menuFile.read()
                menuFile.close()
                await message.reply(menu, mention_author=message.author)


            """
            注册模块
            """


            if '##注册' in message.content:
                #尝试增加文件
                user = str(message.author)
                try:
                    userBasicInfo = open('./users/' + user + '.isregistered', mode = 'x', encoding = 'utf8')
                except:
                    await message.reply('注册失败，请不要重复注册', mention_author=message.author)
                    return
                #文件初始化
                userBasicInfo.close()

                userBasicInfo = pandas.Series(index = ['skyDustAmount', 'signedDays', 'lastActivity', 'earthDustAmount', 'continuousSigned'], data = [0, 0, 0, 0, 0])
                userBasicInfo.to_json('./users/' + user + '_basicInfo.json', indent = 4)

                userBasicInfo = pandas.DataFrame({'weaponName': ['新手剑'], 'weaponAttack': [10], 'weaponRarity': ['Special'], 'weaponRarityRaw': [-1]})
                userBasicInfo.to_json('./users/' + user + '_weaponForm.json', indent = 4, orient = 'index')

                userBasicInfo = pandas.DataFrame({'itemName': ['生命药水'], 'itemAmount': [1], 'itemRarity': ['Common'], 'itemRarityRaw': [5]})
                userBasicInfo.to_json('./users/' + user + '_itemForm.json', indent = 4, orient = 'index')

                userBasicInfo = pandas.Series(index = ['currentLevel', 'basicHP', 'basicAttack', 'currentExp'], data = [0, 2000, 200, 0])
                userBasicInfo.to_json('./users/' + user + '_inGameInfo.json', indent = 4)

                await message.reply('注册成功，如果你不知道如何使用这个机器人，你可以输入 /菜单', mention_author = message.author)


            """
            个人信息模块
            """


            if '##个人信息' in message.content:
                await message.reply(otherModule.genUserBasicInfoList(f_user = str(message.author)), mention_author = message.author)


            """
            个人物品模块
            """


            if '##个人物品' in message.content:
                user = str(message.author)
                try:
                    userWeaponForm = pandas.read_json('./users/' + user + '_weaponForm.json', orient = 'index')
                    userItemForm = pandas.read_json('./users/' + user + '_itemForm.json', orient = 'index')
                except:
                    await message.reply('获取失败，请先注册', mention_author = message.author)
                    return
                res = ''
                #判断是否为空
                if userWeaponForm.empty == True and userItemForm.empty == True:
                    await message.reply('你还没有获得过任何武器或物品', mention_author = message.author)
                else:
                    if userWeaponForm.empty != True:
                        res += otherModule.convertToOutputForm(f_pandasForm = userWeaponForm, f_formType = 'weapon')
                    else:
                        res += '你还没有获得任何武器\n'
                    res += '\n'
                    if userItemForm.empty != True:
                        res += otherModule.convertToOutputForm(f_pandasForm = userItemForm, f_formType = 'item')
                    else:
                        res += '你还没有获得任何物品'
                    await message.reply(res, mention_author = message.author)

            """
            签到模块
            """


            if '##签到' in message.content:
                #检测是否注册
                try:
                    userBasicInfo = pandas.read_json('./users/' + str(message.author) + '_basicInfo.json', typ = 'series')
                except:
                    await message.reply('签到失败，请先注册', mention_author = message.author)
                    return
                #检测签到间隔时间
                currentTime = datetime.date.today().day
                if currentTime - userBasicInfo['lastActivity'] == 0:
                    await message.reply('签到失败，请不要在一天之内多次签到', mention_author = message.author)
                else:
                    #检测连续签到天数
                    if currentTime - userBasicInfo['lastActivity'] == 1:
                        userBasicInfo['continuousSigned'] += 1
                        if userBasicInfo['continuousSigned'] > 3:
                            #连续签到3天后,每天额外获得5个天空之尘
                            userBasicInfo['skyDustAmount'] += (userBasicInfo['continuousSigned'] - 3) % 30 * 5
                    else:
                        #重置连续签到
                        userBasicInfo['continuousSigned'] = 1
                    userBasicInfo['signedDays'] += 1
                    userBasicInfo['skyDustAmount'] += 10
                    userBasicInfo['lastActivity'] = currentTime
                    userBasicInfo.to_json('./users/' + str(message.author) + '_basicInfo.json', indent = 4, orient = 'index')
                    if userBasicInfo['continuousSigned'] > 3:
                        await message.reply('你目前有' + str(userBasicInfo['skyDustAmount']) + '个天空之尘，已累计签到' + str(userBasicInfo['signedDays']) + '天，已连续签到' + str(userBasicInfo['continuousSigned']) + '天，额外获得' + str((userBasicInfo['continuousSigned'] - 3) % 30 * 5) + '个天空之尘', mention_author = message.author)
                    else:
                        await message.reply('你目前有' + str(userBasicInfo['skyDustAmount']) + '个天空之尘，已累计签到' + str(userBasicInfo['signedDays']) + '天，已连续签到' + str(userBasicInfo['continuousSigned']) + '天', mention_author = message.author)


            """
            活动模块
            """


            if '##活动' in message.content:
                activityInfo = pandas.read_json('./activities/activityInfo.json', typ = 'series')
                endTime = datetime.date(activityInfo['endYear'], activityInfo['endMonth'], activityInfo['endDay'])
                daysRemain = endTime.__sub__(datetime.date.today()).days
                if daysRemain <= 0:
                    await message.reply('当前无正在进行的活动', mention_author = message.author)
                    return
                activityWeaponForm = otherModule.convertToOutputForm(f_pandasForm = pandas.read_json('./activities/activityWeaponForm.json', orient = 'index'), f_formType = 'weapon')
                activityItemForm = otherModule.convertToOutputForm(f_pandasForm = pandas.read_json('./activities/activityItemForm.json', orient = 'index'), f_formType = 'item')
                await message.reply('\n当前活动：' + activityInfo['activityName'] + '\n该活动会在' + str(daysRemain) + '天后结束\n' + activityWeaponForm + '\n' + activityItemForm, mention_author = message.author)


            """
            单抽模块
            """


            if '##单抽' in message.content:
                activityInfo = pandas.read_json('./activities/activityInfo.json', typ = 'series')
                endTime = datetime.date(activityInfo['endYear'], activityInfo['endMonth'], activityInfo['endDay'])
                daysRemain = endTime.__sub__(datetime.date.today()).days
                if daysRemain <= 0:
                    await message.reply('当前无正在进行的活动', mention_author = message.author)
                    return
                user = str(message.author)
                try:
                    userBasicInfo = pandas.read_json('./users/' + user + '_basicInfo.json', typ = 'series')
                except:
                    await message.reply('抽卡失败，请先注册', mention_author = message.author)
                    return
                if userBasicInfo['skyDustAmount'] < 100:
                    await message.reply('天空之尘不足', mention_author = message.author)
                userBasicInfo['skyDustAmount'] -= 100
                result = otherModule.gacha()
                #判断抽到的东西的类型
                #武器
                if 'weaponName' in result.columns:
                    #判断是否重复
                    userWeaponForm = pandas.read_json('./users/' + user + '_weaponForm.json', orient = 'index')
                    if result.at[0, 'weaponName'] in userWeaponForm['weaponName'].values:
                        await message.reply('重复获得' + result.at[0, 'weaponName'] + '，已转化为25大地之烬', mention_author = message.author)
                        userBasicInfo['earthDustAmount'] += 25
                    else:
                        await message.reply('获得了' + result.at[0, 'weaponName'], mention_author = message.author)
                        pandas.concat(objs = [userWeaponForm, result], ignore_index = True).to_json('./users/' + user + '_weaponForm.json', indent = 4, orient = 'index')
                #物品
                else:
                    #判断是否是天空之尘
                    if '天空之尘' in result.at[0, 'itemName']:
                        await message.reply('获得了' + str(result.at[0, 'itemAmount']) + '个天空之尘', mention_author = message.author)
                        userBasicInfo['skyDustAmount'] += result.at[0, 'itemAmount']
                    else:
                        userItemForm = pandas.read_json('./users/' + user + '_basicInfo.json', orient = 'index')
                        await message.reply('获得了' + str(result.at[0, 'itemAmount']) + '个' + result['itemName'], mention_author = message.author)
                        #判断是否重复
                        if result.at[0, 'itemName'] in userItemForm['itemName']:
                            userItemForm.at[result.at[0, 'itemName'], 'itemAmount'] += result.at[0, 'itemAmount']
                        else:
                            pandas.concat(objs = [userItemForm, result], ignore_index = True).to_json('./users/' + user + '_itemForm.json', indent = 4, orient = 'index')
                #保存基础数据
                userBasicInfo.to_json('./users/' + user + '_basicInfo.json', indent = 4)


            """
            十连抽模块
            """


            if '##十连抽' in message.content:
                activityInfo = pandas.read_json('./activities/activityInfo.json', typ = 'series')
                endTime = datetime.date(activityInfo['endYear'], activityInfo['endMonth'], activityInfo['endDay'])
                daysRemain = endTime.__sub__(datetime.date.today()).days
                if daysRemain <= 0:
                    await message.reply('当前无正在进行的活动', mention_author = message.author)
                    return
                user = str(message.author)
                try:
                    userBasicInfo = pandas.read_json('./users/' + user + '_basicInfo.json', typ = 'series')
                except:
                    await message.reply('抽卡失败，请先注册', mention_author = message.author)
                    return
                if userBasicInfo['skyDustAmount'] < 1000:
                    await message.reply('天空之尘不足', mention_author = message.author)
                userWeaponForm = pandas.read_json('./users/' + user + '_weaponForm.json', orient = 'index')
                userItemForm = pandas.read_json('./users/' + user + '_basicInfo.json', orient = 'index')
                outputWeaponForm = pandas.DataFrame(columns = ['weaponName', 'weaponAttack', 'weaponRarity', 'weaponRarityRaw'])
                outputItemForm = pandas.DataFrame(columns = ['itemName', 'itemAmount', 'itemRarity', 'itemRarityRaw'])
                outputEarthDustAmount = 0
                outputSkyDustAmount = 0
                finalOutputForm = ''
                userBasicInfo['skyDustAmount'] -= 1000
                for i in range(10): 
                    result = otherModule.gacha()
                    #判断抽到的东西的类型
                    #武器
                    if 'weaponName' in result.columns:
                        #判断是否重复
                        if result.at[0, 'weaponName'] in userWeaponForm['weaponName'].values:
                            result.at[0, 'weaponName'] += '（重复）'
                            outputWeaponForm = pandas.concat(objs = [outputWeaponForm, result], ignore_index = True)
                            outputEarthDustAmount += 25
                            userBasicInfo['earthDustAmount'] += 25
                        else:
                            outputWeaponForm = pandas.concat(objs = [outputWeaponForm, result], ignore_index = True)
                            userWeaponForm = pandas.concat(objs = [userWeaponForm, result], ignore_index = True)
                    #物品
                    else:
                        #判断是否是天空之尘
                        if '天空之尘' in result.at[0, 'itemName']:
                            outputSkyDustAmount += int(result.at[0, 'itemAmount'])
                            userBasicInfo['skyDustAmount'] += result.at[0, 'itemAmount']
                        else:
                            #判断是否重复
                            if result.at[0, 'itemName'] in userItemForm['itemName']:
                                userItemForm.at[result.at[0, 'itemName'], 'itemAmount'] += result.at[0, 'itemAmount']
                            else:
                                userItemForm = pandas.concat(objs = [userItemForm, result], ignore_index = True).to_json('./users/' + user + '_itemForm.json', indent = 4, orient = 'index')
                            #判断是否与最终的输出表格重复
                            if result.at[0, 'itemName'] in outputItemForm['itemName']:
                                outputItemForm.at[result.at[0, 'itemName'], 'itemAmount'] += result.at[0, 'itemAmount']
                            else:
                                outputItemForm = pandas.concat(objs = [outputItemForm, result], ignore_index = True)
                #保存数据
                userBasicInfo.to_json('./users/' + user + '_basicInfo.json', indent = 4)
                userWeaponForm.to_json('./users/' + user + '_weaponForm.json', indent = 4, orient = 'index')
                userItemForm.to_json('./users/' + user + '_itemForm.json', indent = 4, orient = 'index')
                #处理表格数据
                finalOutputForm += otherModule.convertToOutputForm(f_pandasForm = outputWeaponForm, f_formType = 'weapon')
                finalOutputForm += '\n'
                finalOutputForm += otherModule.convertToOutputForm(f_pandasForm = outputItemForm, f_formType = 'item')
                finalOutputForm += '\n\n总计获得' + str(outputSkyDustAmount) + '个天空之尘及' + str(outputEarthDustAmount) + '个大地之烬'
                await message.reply(finalOutputForm, mention_author = message.author)


            """
            商店模块
            """


            """
            对战模块
            """


            if '##对战' in message.content:
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
                    await message.reply('正在等待' + user2 + '作出回答...', mention_author = message.author)
                except:
                    await message.reply('请输入正确的命令格式：/对战||[对方的名字]', mention_author = message.author)
                    return
                #获取回答
                def verify(msg: qq.Message):
                    return str(msg.author) == user2
                while True:
                    try:
                        answer: qq.Message = await client.wait_for(event = 'message', check = verify, timeout = 60)
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
                winner, loser = await gameFightModule.fightGame(self = self, hostMessage = message, guestMessage = answer, host = user1, guest = user2)
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


            """
            帮助模块
            """


            if '##帮助' in message.content:
                command = message.content.split('||')
                try:
                    moduleName = command[1]
                except:
                    await message.reply('请输入正确格式的命令：/帮助||[模块名称]', mention_author = message.author)
                    return
                match moduleName:
                    case '菜单':
                        await message.reply('展示菜单', mention_author = message.author)
                    case '注册':
                        await message.reply('注册账号，除菜单外一切模块的前提是要有账号', mention_author = message.author)
                    case '个人信息':
                        await message.reply('展示你有的天空之尘数量，总计签到天数，大地之烬数量，连续签到天数', mention_author = message.author)
                    case '个人物品':
                        await message.reply('展示你有的所有武器和物品', mention_author = message.author)
                    case '签到':
                        await message.reply('签到操作，每日签到给10天空之尘，连续签到3天后，从第4天开始，每天签到额外给5天空之尘，每30天一个周期', mention_author = message.author)
                    case '活动':
                        await message.reply('展示当前正在进行的活动，即卡池', mention_author = message.author)
                    case '单抽':
                        await message.reply('消耗100天空之尘进行一次单抽，重复获得的每个武器会被转换成25大地之烬，大地之烬可以在商店兑换物品。出货权重：\n0.1 Lengendary, 0.2 Epic, 0.3 Rare, 0.4 Common\n其中1/3概率为武器，2/3概率为物品', mention_author = message.author)
                    case '十连抽':
                        await message.reply('消耗1000天空之尘一次性进行10次单抽', mention_author = message.author)
                    case '对战':
                        await message.reply(open('./texts/help/fight.txt', mode = 'r', encoding = 'utf8').read(), mention_author = message.author)
                    case '帮助':
                        await message.reply('使用方法：\n/帮助||[模块名称]\n显示各模块的详细说明', mention_author = message.author)
                    case _:
                        await message.reply('未找到此模块', mention_author = message.author)


            """
            devtool模块
            """


            if '##devtool' in message.content:
                #判断身份
                if str(message.author) == '443eb9#C':
                    command = message.content.split('||')
                    #判断命令
                    try:
                        #修改指定用户的天空之尘
                        if command[1] == 'modifySkyDustAmount':
                            try:
                                userBasicInfo = pandas.read_json('./users/' + user + '_basicInfo.json', typ = 'series')
                            except:
                                await message.reply('Unknow user: ' + command[2])
                                return
                            userBasicInfo['skyDustAmount'] = int(command[3])
                            userBasicInfo.to_json('./users/' + user + '_basicInfo.json', indent = 4, orient = 'index')
                            await message.reply('Successfully modified ' + str(command[2]) + '\'s sky dust amount.')

                        #展示指定用户个人信息
                        if command[1] == 'showBasicInfoFull':
                            try:
                                userBasicInfo = pandas.read_json('./users/' + user + '_basicInfo.json', typ = 'series')
                            except:
                                await message.reply('Unknow user: ' + str(command[2]))
                                return
                            await message.reply(userBasicInfo)
                            return

                        #显示帮助
                        elif command[1] == 'help':
                            helpFile = open('./texts/commandHelp.txt', mode = 'r' ,encoding = 'utf8')
                            help = helpFile.read()
                            await message.reply(help, mention_author = message.author)

                        #无效命令判断
                        else:
                            await message.reply('Unknow command. Retype the command or type \"help\" to get help', mention_author = message.author)
                    except:
                        await message.reply('Unknow command. Retype the command or type \"help\" to get help', mention_author = message.author)
                else:
                    await message.reply('Authentication Failed')
        except:
            await message.reply('\n发生异常:\n' + traceback.format_exc(), mention_author = message.author)


client = MyClient()
client.run(token = f'{appid}.{token}')