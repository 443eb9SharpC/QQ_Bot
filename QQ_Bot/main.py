#coding = utf-8
import math
import random
import qq
import time
from config import appid, token
import logging
import packedCommands

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
            await message.reply('\n菜单：显示菜单\n注册：注册账号\n个人信息：显示拥有的天空之尘数和累计签到天数\n个人物品：显示拥有的所有武器和物品\n签到：每日签到\n活动：显示当前正在进行的活动\n单抽：消耗五十天空之尘抽卡一发\n十连抽：消耗一百天空之尘十连抽', mention_author=message.author)


        """
        注册模块
        """


        if '/注册' in message.content:
            await message.reply('正在注册...', mention_author = message.author)
            print (message.author)
            #尝试增加文件
            try:
                userInfo = open('./users/' + str(message.author) + '.isregistered', mode = 'x', encoding = 'utf8')
            except IOError:
                await message.reply('注册失败，请不要重复注册', mention_author=message.author)
                return
            #文件初始化
            userInfo.close()
            userInfo = open('./users/' + str(message.author) + '_basicInfo.csv', mode = 'x', encoding = 'utf8')
            #对应 天空之尘,累计签到天数,上一次活跃,大地之烬
            userInfo.write('0,0,0,0')
            userInfo.close()
            userInfo = open('./users/' + str(message.author) + '_weaponList.csv', mode = 'x', encoding = 'utf8')
            userInfo.close()
            userInfo = open('./users/' + str(message.author) + '_itemList.csv', mode = 'x', encoding = 'utf8')
            userInfo.close()

            await message.reply('注册成功', mention_author = message.author)
            

        """
        个人信息模块
        """


        if '/个人信息' in message.content:
            infoDic = packedCommands.readUserBasicInfo(str(message.author))
            if infoDic == 'Error':
                await message.reply('查询失败，请先注册')
            else:
                await message.reply('你有' + infoDic['skyDustCount'] + '个天空之尘，已累计签到' + infoDic['signedDays'] + '天', mention_author = message.author)


        """
        个人物品模块
        """


        if '/个人物品' in message.content:
            weaponDic = packedCommands.readUserWeaponList(str(message.author))
            itemDic = packedCommands.readUserItemList(str(message.author))
            msg='\n武器名 | 攻击力 | 稀有度\n'
            
            for key in weaponDic:
                weaponInfo = weaponDic[key]
                msg += weaponInfo[0] + ' | ' + weaponInfo[1] + ' | ' +  weaponInfo[3] + '\n'
            msg += '\n物品名 | 数量 | 稀有度\n'

            for key in itemDic:
                itemInfo = itemDic[key]
                msg += itemInfo[0] + ' | ' + itemInfo[1] + ' | ' + itemInfo[3] + ' | '

            await message.reply(msg, mention_author = message.author)


        """
        签到模块
        """


        if '/签到' in message.content:
            await message.reply('正在签到', mention_author = message.author)
            currentTime = math.floor(time.time() / 86400)
            infoList = packedCommands.readUserBasicInfo(str(message.author))
            if(infoList == 'Error'):
                await message.reply('签到失败，请先注册', mention_author = message.author)
                return
            if(currentTime - int(infoList[2]) < 1 and int(infoList[1]) != 0):
                await message.reply('签到失败，请不要在一天之内多次签到', mention_author = message.author)
            else:
                signedDays = int(infoList[1]) + 1
                skyDust = int(infoList[0]) + 10
                packedCommands.refreshBasicInfo(str(message.author), skyDust, signedDays, currentTime)
                await message.reply('你目前有' + str(skyDust) + '个天空之尘，已累计签到' + str(signedDays) +'天', mention_author = message.author)


        """
        活动模块
        """


        if '/活动' in message.content:
            activityInfo = packedCommands.readActivityInfo()
            activityWeapon = packedCommands.readActivityWeapon()
            activityItem = packedCommands.readActivityItem()
            await message.reply('\n当前活动：' + activityInfo['activityName'] + '\n该活动会在' + str(int(activityInfo['daysRemain']) - math.floor(time.time() / 86400)) + '天后结束\n\n武器 | 攻击力 | 稀有度\n' + activityWeapon['weaponNameString'] + '\n物品 | 数量 | 稀有度\n' + activityItem['itemNameString'], mention_author = message.author)
               
            
        """
        单抽模块
        """


        if '/单抽' in message.content:
            userInfoDic = packedCommands.readUserBasicInfo(str(message.author))

            #天空之尘数量检测
            if int(userInfoDic['skyDustAmount']) < 50:
                await message.reply('抽卡失败，你目前的天空之尘不足50')
                return

            #开始抽卡
            skyDust = int(userInfoDic['skyDustAmount']) - 50
            earthDust = int(userInfoDic['earthDustAmount'])
            await message.reply('咻~')
            elemNameAndType = packedCommands.gacha()

            #读取相关列表
            elemName = elemNameAndType[0]
            elemType = elemNameAndType[1]

            #获取元素的类型以及信息
            if elemType == 'weapon':
                #读取活动所有的武器
                weaponDic = packedCommands.readActivityWeapon()
                #找到抽到的武器的信息列表
                weaponInfoList = weaponDic[elemName]
            else:
                itemDic = packedCommands.readActivityItem()
                itemInfoList = itemDic[elemName]

            #输出
            if elemType == 'weapon':
                userWeaponDic = packedCommands.readUserWeaponList(str(message.author))
                #判断武器是否重复
                if elemName in userWeaponDic:
                    await message.reply('你已获得' + elemName + '，转化为20个大地之烬', mention_author = message.author)
                    earthDust += 20
                else:
                    await message.reply('恭喜你获得了：' + elemName, mention_author = message.author)
                    #保存武器
                    packedCommands.refreshWeaponList(str(message.author), weaponInfoList)
            else:
                packedCommands.refreshItemList(str(message.author), itemInfoList)
                await message.reply('恭喜你获得了' + itemInfoList[1] + '个' + elemName, mention_author = message.author)

            #保存基础数据
            packedCommands.refreshBasicInfo(str(message.author), skyDust, userInfoDic['signedDays'], userInfoDic['lastActivity'], earthDust)


        """
        十连抽模块
        """


        if '/十连抽' in message.content:
            infoList = packedCommands.readUserBasicInfo(str(message.author))
            if int(infoList[0]) < 500:
                await message.reply('抽卡失败，你目前的天空之尘不足500')
                return
            await message.reply('咻咻咻咻咻咻咻咻咻咻~')
            for i in range(0, 10):
                elemList = packedCommands.gacha()
                if elemList[3] == 'item':
                    await message.reply('恭喜你获得了' + elemList[1] + '个' + elemList[0], mention_author = message.author)
                else:
                    await message.reply('恭喜你获得了：' + elemList[0], mention_author = message.author)
                skyDust = int(infoList[0]) - 50
                packedCommands.refreshBasicInfo(str(message.author), skyDust, infoList[1], infoList[2])
                packedCommands.refreshItemList(str(message.author), elemList)


        """
        挑战模块
        """


        if '/挑战' in message.content:
            await message.reply('功能开发中，敬请期待', mention_author = message.author)


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
                        await message.reply(math.floor(time.time() / 86400), mention_author = message.author)
                        return

                    #修改指定用户的天空之尘
                    if commandList[1] == 'modifySkyDustAmount':
                        userInfoDic = packedCommands.readUserBasicInfo(str(commandList[2]))
                        res = packedCommands.refreshBasicInfo(str(commandList[2]), int(commandList[3]), userInfoDic['signedDays'], userInfoDic['lastActivity'], userInfoDic['earthDustAmount'])
                        if res == 'Error':
                            await message.reply('Unknow user: ' + str(commandList[2]))
                        else:
                            await message.reply('Successfully modified' + str(commandList[2]) + '\'s sky dust counts.')
                        return

                    #展示指定用户个人信息
                    if commandList[1] == 'showBasicInfoRaw':
                        infoList = packedCommands.readUserBasicInfo(str(commandList[2]))
                        try:
                            user = infoList[0]
                            skyDust = infoList[1]
                            signedDays = infoList[2]
                            lastActivity = infoList[3]
                        except IndexError:
                            await message.reply('Unknow user: ' + str(commandList[2]))
                            return
                        await message.reply(user + ' ' + skyDust + ' ' + signedDays + ' ' + lastActivity)
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