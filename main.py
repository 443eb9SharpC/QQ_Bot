#coding = utf-8
import asyncio
import qq
import time
import pandas
from config import appid, token
import logging

import modules.readModule as readModule
import modules.refreshModule as refreshModule
import modules.otherModule as otherModule

logging.basicConfig(level = logging.DEBUG)

class MyClient(qq.Client):
    async def on_ready(self):
        print(f'以 {self.user} 身份登录（ID：{self.user.id}）')
        print('------')

    async def on_message(self, message: qq.Message):
        # 我们不希望机器人回复自己
        if message.author.id == self.user.id:
            return

        if str(message.author) != '443eb9#C':
            await message.reply('机器人正在进行维护，请耐心等待', mention_author = message.author)
            return


        """
        做作业模块
        """
        if '/作业' in message.content:
            df = pandas.read_excel('./homework/homework.xlsx')
            df.to_json('./homework/hw.json', indent = 4, orient = 'index')


        """
        菜单模块
        """

        if '/菜单' in message.content:
            menuFile = open('./texts/menu.txt', mode = 'r', encoding = 'utf8')
            menu = menuFile.read()
            menuFile.close()
            await message.reply(menu, mention_author=message.author)


        """
        注册模块
        """


        if '/注册' in message.content:
            #尝试增加文件
            user = str(message.author)
            try:
                userBasicInfo = open('./users/' + user + '.isregistered', mode = 'x', encoding = 'utf8')
            except IOError:
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

            userBasicInfo = pandas.Series(index = ['currentLevel', 'basicHP', 'basicAttack', 'totalExp'], data = [0, 2000, 50, 0])
            userBasicInfo.to_json('./users/' + user + '_inGameInfo.json', indent = 4)

            await message.reply('注册成功', mention_author = message.author)
            

        """
        个人信息模块
        """


        if '/个人信息' in message.content:
            await message.reply(otherModule.genUserBasicInfoList(f_user = str(message.author)), mention_author = message.author)
            

        """
        个人物品模块
        """


        if '/个人物品' in message.content:
            user = str(message.author)
            res = ''
            try:
                userWeaponForm = pandas.read_json('./users/' + user + '_weaponForm.json', orient = 'index')
                userItemForm = pandas.read_json('./users/' + user + '_itemForm.json', orient = 'index')
            except Exception:
                await message.reply('获取失败，请先注册', mention_author = message.author)
                return
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


        if '/签到' in message.content:
            #检测是否注册
            try:
                userBasicInfo = pandas.read_json('./users/' + str(message.author) + '_basicInfo.json', typ = 'series')
            except Exception:
                await message.reply('签到失败，请先注册', mention_author = message.author)
                return
            #检测签到间隔时间
            currentTime = int(time.time() // 86400)
            if(currentTime - userBasicInfo['lastActivity'] < 1 and userBasicInfo['signedDays'] != 0):
                await message.reply('签到失败，请不要在一天之内多次签到', mention_author = message.author)
            else:
                #检测连续签到天数
                if currentTime - userBasicInfo['lastActivity'] == 1:
                    continuousSigned = userBasicInfo['continuousSigned'] + 1
                    skyDustAmount = userBasicInfo['skyDustAmount'] + ((continuousSigned - 3) % 30 * 5)
                else:
                    #重置连续签到
                    continuousSigned = 1
                signedDays = userBasicInfo['signedDays'] + 1
                skyDustAmount = userBasicInfo['skyDustAmount'] + 10
                refreshModule.refreshBasicInfo(f_user = str(message.author), f_skyDustAmount = skyDustAmount, f_signedDays = signedDays, f_lastActivity = currentTime, f_continuousSigned = continuousSigned) 

                if continuousSigned > 3:
                    await message.reply('你目前有' + str(skyDustAmount) + '个天空之尘，已累计签到' + str(signedDays) + '天，已连续签到' + str(continuousSigned) + '天，额外获得' + skyDustAmount - 10 + '个天空之尘', mention_author = message.author)
                else:
                    await message.reply('你目前有' + str(skyDustAmount) + '个天空之尘，已累计签到' + str(signedDays) + '天，已连续签到' + str(continuousSigned) + '天', mention_author = message.author)


        """
        活动模块
        """


        if '/活动' in message.content:
            activityInfo = pandas.read_json('./activities/activityInfo.json', typ = 'series')
            activityWeaponForm = otherModule.convertToOutputForm(f_pandasForm = pandas.read_json('./activities/activityItemForm.json', orient = 'index'), f_formType = 'weapon')
            activityItemForm = otherModule.convertToOutputForm(f_pandasForm = pandas.read_json('./activities/activityItemForm.json', orient = 'index'), f_formType = 'item')
            daysRemain = int(activityInfo['endDay'] - int(time.time() // 86400))
            await message.reply('\n当前活动：' + activityInfo['activityName'] + '\n该活动会在' + daysRemain + '天后结束\n\n' + activityWeaponForm + '\n\n' + activityItemForm, mention_author = message.author)
               
            
        """
        单抽模块
        """


        if '/单抽' in message.content:
            user = str(message.author)
            userBasicInfo = pandas.read_json('./users/' + user + '_basicInfo.json', typ = 'series')
            userBasicInfo['skyDustAmount'] -= 100
            result = otherModule.gacha()
            #判断抽到的东西的类型
            #武器
            if 'weaponName' in result.index:
                #判断是否重复
                userWeaponForm = pandas.read_json('./users/' + user + '_weaponForm.json', orient = 'index')
                if result['weaponName'] in userWeaponForm['weaponName']:
                    await message.reply('重复获得' + result['weaponName'] + '，已转化为25大地之烬', mention_author = message.author)
                    userBasicInfo['earthDustAmount'] += 25
                else:
                    await message.reply('获得了' + result['weaponName'], mention_author = message.author)
                    pandas.concat(objs = [userWeaponForm, result], ignore_index = True).to_json('./users/' + user + '_weaponForm.json', indent = 4, orient = 'index')
            #物品
            else:
                #判断是否是天空之尘
                if '天空之尘' in result['itemName']:
                    await message.reply('获得了' + str(result['itemAmount']) + '个天空之尘', mention_author = message.author)
                    userBasicInfo['skyDustAmount'] += result['itemAmount']
                else:
                    userItemForm = pandas.read_json('./users/' + user + '_basicInfo.json', orient = 'index')
                    await message.reply('获得了' + str(result['itemAmount']) + '个' + result['itemName'], mention_author = message.author)
                    #判断是否重复
                    if result['itemName'] in userItemForm['itemName']:
                        userItemForm.at[result['itemName'], 'itemAmount'] += result['itemAmount']
                    else:
                        pandas.concat(objs = [userItemForm, result], ignore_index = True).to_json('./users/' + user + '_itemForm.json', indent = 4, orient = 'index')
            #保存基础数据
            userBasicInfo.to_json('./users/' + user + '_basicInfo.json', indent = 4)


        """
        十连抽模块
        """


        if '/十连抽' in message.content:
            user = str(message.author)
            userBasicInfo = pandas.read_json('./users/' + user + '_basicInfo.json', typ = 'series')
            outputWeaponForm = pandas.DataFrame(columns = ['weaponName', 'weaponAttack', 'weaponRarity', 'weaponRarityRaw'])
            outputItemForm = pandas.DataFrame(columns = ['itemName', 'itemAmount', 'itemRarity', 'itemRarityRaw'])
            outputEarthDustAmount = 0
            outputSkyDustAmount = 0
            finalOutputForm = ''
            for i in range(10): 
                result = otherModule.gacha()
                #判断抽到的东西的类型
                #武器
                if 'weaponName' in result.index:
                    #判断是否重复
                    userWeaponForm = pandas.read_json('./users/' + user + '_weaponForm.json', orient = 'index')
                    if result['weaponName'] in userWeaponForm['weaponName']:
                        result['weaponName'] += '（重复）'
                        pandas.concat(onjs = [outputWeaponForm, result], ignore_index = True)
                        userBasicInfo['earthDustAmount'] += 25
                        outputEarthDustAmount += 25
                    else:
                        pandas.concat(objs = [outputWeaponForm, result], ignore_index = True)
                        userWeaponForm = pandas.concat(objs = [userWeaponForm, result], ignore_index = True)
                #物品
                else:
                    #判断是否是天空之尘
                    if '天空之尘' in result['itemName']:
                        outputSkyDustAmount += result['itemAmount']
                        userBasicInfo['skyDustAmount'] += result['itemAmount']
                    else:
                        userItemForm = pandas.read_json('./users/' + user + '_basicInfo.json', orient = 'index')
                        #判断是否重复
                        if result['itemName'] in userItemForm['itemName']:
                            userItemForm.at[result['itemName'], 'itemAmount'] += result['itemAmount']
                        else:
                            userItemForm = pandas.concat(objs = [userItemForm, result], ignore_index = True)
                        #判断输出列表是否重复
                        if result['itemName'] in outputItemForm['itemName']:
                            outputItemForm.at[result['itemName'], 'itemAmount'] += result['itemAmount']
                        else:
                            pandas.concat(objs = [outputItemForm, result], ignore_index = True)
            #保存数据
            userBasicInfo.to_json('./users/' + user + '_basicInfo.json', indent = 4)
            userWeaponForm.to_json('./users/' + user + '_weaponForm.json', indent = 4, orient = 'index')
            userItemForm.to_json('./users/' + user + '_itemForm.json', indent = 4, orient = 'index')
            #处理表格数据
            finalOutputForm += otherModule.convertToOutputForm(f_pandasForm = outputWeaponForm, f_formType = 'weapon')
            finalOutputForm += '\n\n'
            finalOutputForm += otherModule.convertToOutputForm(f_pandasForm = outputItemForm, f_formType = 'item')
            finalOutputForm += '总计获得' + outputSkyDustAmount + '个天空之尘及' + outputEarthDustAmount + '个大地之烬'
            await message.reply(finalOutputForm, mention_author = message.author)


        """
        对战模块
        """


        if '/对战' in message.content:
            challenge = message.content
            challengeList = challenge.split('||')
            #检查命令格式
            try:
                user2 = challengeList[1]
                await message.reply('正在等待' + user2 + '作出回答...', mention_author = message.author)
            except IndexError:
                await message.reply('请输入正确的命令格式：/对战||[str:对方的名字]', mention_author = message.author)
                return

            def verify(msg):
                return str(msg.author) == user2

            #超时或拒绝
            try:
                answer = await client.wait_for(event = 'message', check = verify, timeout = 60)
            except asyncio.TimeoutError:
                await message.reply('对方超出1分钟未给出回应', mention_author = message.author)
                return

            if '拒绝' in answer.content:
                await message.reply('对方拒绝了你的对战请求', mention_author = message.author)
                return
            elif '接受' in answer.content:
                await message.reply('对方接受了你的对战请求', mention_author = message.author)
            else:
                await message.reply('请不要回答除接受与拒绝之外的其他答案', mention_author = answer.author)
            #开始对战


        """
        反馈模块
        """


        """
        devtool模块
        """


        if 'devtool' in message.content:
            #判断身份
            if str(message.author) == '443eb9#C':
                command = message.content
                commandList = command.split('||')
                #判断命令
                try:
                    #展示当前时间戳对应的天数
                    if commandList[1] == 'currentTimeStamp':
                        await message.reply(int(time.time() / 86400), mention_author = message.author)
                        return

                    #修改指定用户的天空之尘
                    if commandList[1] == 'modifySkyDustAmount':
                        try:
                            userBasicInfo = pandas.read_json('./users/' + user + '_basicInfo.json', typ = 'series')
                        except Exception:
                            await message.reply('Unknow user: ' + commandList[2])
                            return
                        userBasicInfo['skyDustAmount'] = int(commandList[3])
                        userBasicInfo.to_json('./users/' + user + '_basicInfo.json', indent = 4, orient = 'index')
                        await message.reply('Successfully modified ' + str(commandList[2]) + '\'s sky dust amount.')

                    #展示指定用户个人信息
                    if commandList[1] == 'showBasicInfoFull':
                        try:
                            userBasicInfo = pandas.read_json('./users/' + user + '_basicInfo.json', typ = 'series')
                        except Exception:
                            await message.reply('Unknow user: ' + str(commandList[2]))
                            return
                        await message.reply(userBasicInfo)
                        return

                    #显示帮助
                    elif commandList[1] == 'help':
                        helpFile = open('./texts/commandHelp.txt', mode = 'r' ,encoding = 'utf8')
                        help = helpFile.read()
                        await message.reply(help, mention_author = message.author)

                    #无效命令判断
                    else:
                        await message.reply('Unknow command. Retype the command or type \"help\" to get help', mention_author = message.author)
                except Exception:
                    await message.reply('Unknow command. Retype the command or type \"help\" to get help', mention_author = message.author)
            else:
                await message.reply('Authentication Failed')


client = MyClient()
client.run(token=f'{appid}.{token}')