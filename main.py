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
            await message.reply('机器人正在进行大型维护，请耐心等待', mention_author = message.author)


        """
        做作业模块
        """
        if '/作业' in message.content:
            await message.reply('当前没有作业', mention_author = message.author)


        """
        菜单模块
        """

        if '/菜单' in message.content:
            menuFile = open('./assets/menu.txt', mode = 'r', encoding = 'utf8')
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

            userBasicInfo = pandas.DataFrame(columns = ['weaponName', 'weaponAttack', 'weaponRarity', 'weaponRarityRaw'])
            userBasicInfo.to_json('./users/' + user + '_weaponForm.json', indent = 4, orient = 'index')

            userBasicInfo = pandas.DataFrame(columns = ['itemName', 'itemAmount', 'itemRarity', 'itemRarityRaw'])
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
            try:
                userWeaponForm = pandas.read_json('./users/' + user + '_weaponForm.json', orient = 'index')
                userItemForm = pandas.read_json('./users/' + user + '_itemForm.json', orient = 'index')
            except Exception:
                await message.reply('获取失败，请先注册', mention_author = message.author)
            #判断是否为空
            if userWeaponForm.empty == True and userItemForm.empty == True:
                await message.reply('你还没有获得过任何武器或物品', mention_author = message.author)
            else:
                res = ''
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
            activityWeaponForm = pandas.read_json('./activities/activityItemForm.json', orient = 'index')
            activityItemForm = pandas.read_json('./activities/activityItemForm.json', orient = 'index')
            await message.reply('\n当前活动：' + activityInfo['activityName'] + '\n该活动会在' + str(int(activityInfo['daysRemain']) - int(time.time() // 86400)) + '天后结束\n\n武器 | 攻击力 | 稀有度\n' + activityWeapon['weaponNameString'] + '\n物品 | 数量 | 稀有度\n' + activityItem['itemNameString'], mention_author = message.author)
               
            
        """
        单抽模块
        """


        if '/单抽' in message.content:
            userInfoDic = readModule.readUserBasicInfo(str(message.author))

            if userInfoDic == 'Error':
                message.reply('抽卡失败，请先注册', mention_author = message.author)
                return

            #天空之尘数量检测
            if userInfoDic['skyDustAmount'] < 50:
                await message.reply('抽卡失败，你目前的天空之尘不足50')
                return

            #开始抽卡
            skyDust = int(userInfoDic['skyDustAmount']) - 50
            earthDust = int(userInfoDic['earthDustAmount'])
            await message.reply('咻~')
            elemNameAndType = otherModule.gacha()

            #读取相关列表
            elemName = elemNameAndType[0]
            elemType = elemNameAndType[1]

            #获取元素的类型以及信息
            if elemType == 'weapon':
                #读取活动所有的武器
                weaponDic = readModule.readActivityWeapon()
                #找到抽到的武器的信息列表
                weaponInfoList = weaponDic[elemName]
            else:
                itemDic = readModule.readActivityItem()
                itemInfoList = itemDic[elemName]

            #输出
            if elemType == 'weapon':
                userWeaponDic = readModule.readUserWeaponList(str(message.author))
                #判断武器是否重复
                if elemName in userWeaponDic:
                    await message.reply('重复获得' + elemName + '，转化为20个大地之烬', mention_author = message.author)
                    earthDust += 20
                else:
                    await message.reply('恭喜你获得了：' + elemName, mention_author = message.author)
                    #保存武器
                    refreshModule.refreshWeaponList(str(message.author), weaponInfoList)
            elif elemType == 'item':
                #检测是否为天空之尘
                if elemName[:4] == '天空之尘':
                    skyDustAmount += int(elemName[4:len(elemName)])
                    await message.reply('恭喜你获得了' + itemInfoList[1] + '个天空之尘', mention_author = message.author)
                else:
                    await message.reply('恭喜你获得了' + itemInfoList[1] + '个' + elemName, mention_author = message.author)
                    #保存物品
                    refreshModule.refreshItemList(str(message.author), itemInfoList)

            #保存基础数据
            refreshModule.refreshBasicInfo(str(message.author), skyDust, userInfoDic['signedDays'], userInfoDic['lastActivity'], earthDust, userInfoDic['continuousSigned'])


        """
        十连抽模块
        """


        if '/十连抽' in message.content:
            userInfoDic = readModule.readUserBasicInfo(str(message.author))

            if userInfoDic == 'Error':
                message.reply('抽卡失败，请先注册', mention_author = message.author)
                return

            #天空之尘数量检测
            if int(userInfoDic['skyDustAmount']) < 500:
                await message.reply('抽卡失败，你目前的天空之尘不足500')
                return

            #开始抽卡
            skyDustAmount = userInfoDic['skyDustAmount'] - 500
            earthDustAmount = userInfoDic['earthDustAmount']
            await message.reply('咻咻咻咻咻咻咻咻咻咻~')
            for i in range(10):
                elemNameAndType = otherModule.gacha()

                #读取相关列表
                elemName = elemNameAndType[0]
                elemType = elemNameAndType[1]

                #获取元素的类型以及信息
                if elemType == 'weapon':
                    #读取活动所有的武器
                    weaponDic = readModule.readActivityWeapon()
                    #找到抽到的武器的信息列表
                    weaponInfoList = weaponDic[elemName]
                else:
                    itemDic = readModule.readActivityItem()
                    itemInfoList = itemDic[elemName]

                #输出
                if elemType == 'weapon':
                    userWeaponDic = readModule.readUserWeaponList(str(message.author))
                    #判断武器是否重复
                    if elemName in userWeaponDic:
                        await message.reply('重复获得' + elemName + '，转化为20个大地之烬', mention_author = message.author)
                        earthDustAmount += 20
                    else:
                        await message.reply('恭喜你获得了：' + elemName, mention_author = message.author)
                        #保存武器
                        refreshModule.refreshWeaponList(str(message.author), weaponInfoList)
                elif elemType == 'item':
                    #检测是否为天空之尘
                    if elemName[:4] == '天空之尘':
                        skyDustAmount += int(elemName[4:len(elemName)])
                        await message.reply('恭喜你获得了' + itemInfoList[1] + '个天空之尘', mention_author = message.author)
                    else:
                        await message.reply('恭喜你获得了' + itemInfoList[1] + '个' + elemName, mention_author = message.author)
                        #保存物品
                        refreshModule.refreshItemList(str(message.author), itemInfoList)

                #保存基础数据
                refreshModule.refreshBasicInfo(str(message.author), skyDustAmount, userInfoDic['signedDays'], userInfoDic['lastActivity'], earthDustAmount, userInfoDic['continuousSigned'])


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
                        userInfoDic = readModule.readUserBasicInfo(str(commandList[2]))
                        res = refreshModule.refreshBasicInfo(str(commandList[2]), int(commandList[3]), userInfoDic['signedDays'], userInfoDic['lastActivity'], userInfoDic['earthDustAmount'],userInfoDic['continuousSigned'])
                        if res == 'Error':
                            await message.reply('Unknow user: ' + str(commandList[2]))
                        else:
                            await message.reply('Successfully modified ' + str(commandList[2]) + '\'s sky dust amount.')
                        return

                    #展示指定用户个人信息
                    if commandList[1] == 'showBasicInfoRaw':
                        userInfoDic = readModule.readUserBasicInfo(str(commandList[2]))
                        try:
                            user = str(commandList[2])
                            skyDustAmount = userInfoDic['skyDustAmount']
                            signedDays = userInfoDic['signedDays']
                            lastActivity = userInfoDic['lastActivity']
                            earthDustAmount = userInfoDic['earthDustAmount']
                        except IndexError:
                            await message.reply('Unknow user: ' + str(commandList[2]))
                            return
                        await message.reply(user + ' ' + skyDustAmount + ' ' + signedDays + ' ' + lastActivity + ' ' + earthDustAmount)
                        return

                    #显示帮助
                    elif commandList[1] == 'help':
                        await message.reply('\ncurrentTimeStamp：返回当前时间戳对应的天数\modifySkyDustAmount||[str:userName]||[int:skyDustCount]：修改指定用户的天空之尘数', mention_author = message.author)

                    #无效命令判断
                    else:
                        await message.reply('Unknow command. Retype the command or type \"help\" to get help', mention_author = message.author)
                except IndexError:
                    await message.reply('Unknow command. Retype the command or type \"help\" to get help', mention_author = message.author)
            else:
                await message.reply('Authentication Failed')


client = MyClient()
client.run(token=f'{appid}.{token}')