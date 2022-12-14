#coding = utf-8
import asyncio
import qq
import time
from config import appid, token
import logging

import readModule
import refreshModule
import otherModule

logging.basicConfig(level=logging.DEBUG)

class MyClient(qq.Client):
    async def on_ready(self):
        print(f'以 {self.user} 身份登录（ID：{self.user.id}）')
        print('------')

    async def on_message(self, message: qq.Message):
        # 我们不希望机器人回复自己
        if message.author.id == self.user.id:
            return

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
            try:
                userInfo = open('./users/' + str(message.author) + '.isregistered', mode = 'x', encoding = 'utf8')
            except IOError:
                await message.reply('注册失败，请不要重复注册', mention_author=message.author)
                return
            #文件初始化
            userInfo.close()
            userInfo = open('./users/' + str(message.author) + '_basicInfo.csv', mode = 'x', encoding = 'utf8')
            #对应 天空之尘,累计签到天数,上一次活跃,大地之烬,连续签到天数
            userInfo.write('0,0,0,0,0')
            userInfo.close()
            userInfo = open('./users/' + str(message.author) + '_weaponList.csv', mode = 'x', encoding = 'utf8')
            userInfo.close()
            userInfo = open('./users/' + str(message.author) + '_itemList.csv', mode = 'x', encoding = 'utf8')
            userInfo.close()
            userInfo = open('./users/' + str(message.author) + '_inGameInfo.csv', mode = 'x', encoding = 'utf8')
            #对应 等级,基础生命值,基础攻击力,总经验值
            userInfo.write('0,2000,50,0')
            userInfo.close()

            await message.reply('注册成功', mention_author = message.author)
            

        """
        个人信息模块
        """


        if '/个人信息' in message.content:
            await message.reply(otherModule.genUserBasicInfoList(str(message.author)), mention_author = message.author)
            

        """
        个人物品模块
        """


        if '/个人物品' in message.content:
            weaponDic = readModule.readUserWeaponList(str(message.author))
            itemDic = readModule.readUserItemList(str(message.author))

            if weaponDic == 'Error' or itemDic == 'Error':
                message.reply('未找到用户，请先注册', mention_author=message.author)
                return

            msg='\n武器名 | 攻击力 | 稀有度\n'
            
            for key in weaponDic:
                weaponInfo = weaponDic[key]
                msg += weaponInfo[0] + ' | ' + weaponInfo[1] + ' | ' +  weaponInfo[3] + '\n'
            msg += '\n物品名 | 数量 | 稀有度\n'

            for key in itemDic:
                itemInfo = itemDic[key]
                msg += itemInfo[0] + ' | ' + itemInfo[1] + ' | ' + itemInfo[3] + '\n'

            await message.reply(msg, mention_author = message.author)


        """
        签到模块
        """


        if '/签到' in message.content:
            #检测签到间隔时间
            currentTime = int(time.time() // 86400)
            infoList = readModule.readUserBasicInfo(str(message.author))

            if(infoList == 'Error'):
                await message.reply('签到失败，请先注册', mention_author = message.author)
                return

            if(currentTime - infoList['lastActivity'] < 1 and infoList['signedDays'] != 0):
                await message.reply('签到失败，请不要在一天之内多次签到', mention_author = message.author)
            else:
                #检测连续签到天数
                if currentTime - infoList['lastActivity'] == 1:
                    continuousSigned = infoList['continuousSigned'] + 1
                    skyDustAmount = infoList['skyDustAmount'] + ((continuousSigned - 3) % 30 * 5)
                else:
                    #重置连续签到
                    continuousSigned = 1
                signedDays = infoList['signedDays'] + 1
                skyDustAmount = infoList['skyDustAmount'] + 10
                refreshModule.refreshBasicInfo(str(message.author), skyDustAmount, signedDays, currentTime, infoList['earthDustAmount'], continuousSigned)

                if continuousSigned > 3:
                    await message.reply('你目前有' + str(skyDustAmount) + '个天空之尘，已累计签到' + str(signedDays) + '天，已连续签到' + str(continuousSigned) + '天，额外获得' + skyDustAmount - 10 + '个天空之尘', mention_author = message.author)
                else:
                    await message.reply('你目前有' + str(skyDustAmount) + '个天空之尘，已累计签到' + str(signedDays) + '天，已连续签到' + str(continuousSigned) + '天', mention_author = message.author)


        """
        活动模块
        """


        if '/活动' in message.content:
            activityInfo = readModule.readActivityInfo()
            activityWeapon = readModule.readActivityWeapon()
            activityItem = readModule.readActivityItem()
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
                user1 = str(message.author)
                user2 = challengeList[1]
                await message.reply('已向' + user2 + '发出请求', mention_author = message.author)
            except IndexError:
                await message.reply('请输入正确的命令格式：/对战||[str:对方的名字]', mention_author = message.author)
                return

            def check(m):
                return m.author == user2

            #超时或拒绝
            try:
                answer = await client.wait_for('message', timeout = 60)
            except asyncio.TimeoutError:
                message.reply('对方超出1分钟未给出回应', mention_author = message.author)
                return
            if str(answer) == '拒绝':
                await message.reply('对方拒绝了你的对战请求', mention_author = message.author)
                return
            elif str(answer) == '接受':
                await message.reply('对方接受了你的对战请求', mention_author = message.author)
            else:
                await message.reply('请不要回答除接受与拒绝之外的其他答案', mention_author = user2)
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